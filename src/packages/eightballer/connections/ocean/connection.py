# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2019 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------
"""Scaffold connection and channel."""
import time
from typing import Any

from datetime import datetime, timedelta
from aea.configurations.base import PublicId
from aea.connections.base import BaseSyncConnection
from aea.mail.base import Envelope
from packages.eightballer.protocols.ocean.message import OceanMessage

"""
Choose one of the possible implementations:

Sync (inherited from BaseSyncConnection) or Async (inherited from Connection) connection and remove unused one.
"""

CONNECTION_ID = PublicId.from_str("eightballer/ocean:0.1.0")

import os

import ocean_lib
from eth_account import Account
from ocean_lib.data_provider.data_service_provider import DataServiceProvider
from ocean_lib.example_config import ExampleConfig
from ocean_lib.models.compute_input import ComputeInput
from ocean_lib.ocean.ocean import Ocean
from ocean_lib.structures.file_objects import UrlFile
from ocean_lib.services.service import Service
from ocean_lib.web3_internal.constants import ZERO_ADDRESS
from ocean_lib.web3_internal.wallet import Wallet
from web3._utils.threads import Timeout

Account.enable_unaudited_hdwallet_features()


class OceanConnection(BaseSyncConnection):
    """Proxy to the functionality of the SDK or API."""

    MAX_WORKER_THREADS = 5

    connection_id = CONNECTION_ID

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pragma: no cover
        """
        Initialize the connection.

        The configuration must be specified if and only if the following
        parameters are None: connection_id, excluded_protocols or restricted_to_protocols.

        Possible arguments:
        - configuration: the connection configuration.
        - data_dir: directory where to put local files.
        - identity: the identity object held by the agent.
        - crypto_store: the crypto store for encrypted communication.
        - restricted_to_protocols: the set of protocols ids of the only supported protocols for this connection.
        - excluded_protocols: the set of protocols ids that we want to exclude for this connection.

        :param args: arguments passed to component base
        :param kwargs: keyword arguments passed to component base
        """
        super().__init__(*args, **kwargs)

    def main(self) -> None:
        """
        Run synchronous code in background.

        SyncConnection `main()` usage:
        The idea of the `main` method in the sync connection
        is to provide for a way to actively generate messages by the connection via the `put_envelope` method.

        A simple example is the generation of a message every second:
        ```
        while self.is_connected:
            envelope = make_envelope_for_current_time()
            self.put_enevelope(envelope)
            time.sleep(1)
        ```
        In this case, the connection will generate a message every second
        regardless of envelopes sent to the connection by the agent.
        For instance, this way one can implement periodically polling some internet resources
        and generate envelopes for the agent if some updates are available.
        Another example is the case where there is some framework that runs blocking
        code and provides a callback on some internal event.
        This blocking code can be executed in the main function and new envelops
        can be created in the event callback.
        """

    def on_send(self, envelope: Envelope) -> None:
        """
        Send an envelope.

        :param envelope: the envelope to send.
        """
        self.logger.debug(f"Receieved {envelope} in connection")

        if envelope.message.performative == OceanMessage.Performative.DEPLOY_D2C:
            self._deploy_data_for_d2c(envelope)
        if envelope.message.performative == OceanMessage.Performative.DEPLOY_ALGORITHM:
            self._deploy_algorithm(envelope)
        if (
            envelope.message.performative
            == OceanMessage.Performative.PERMISSION_DATASET
        ):
            self._permission_dataset(envelope)
        if envelope.message.performative == OceanMessage.Performative.D2C_JOB:
            self._create_d2c_job(envelope)
        if (
            envelope.message.performative
            == OceanMessage.Performative.DEPLOY_DATA_DOWNLOAD
        ):
            self._deploy_data_to_download(envelope)

    def _download_asset(self, envelope: Envelope):
        did = envelope.message.asset_did
        asset = self.ocean.assets.resolve(did)
        service = asset.get_service_by_id("0")

        order_tx_id = self.ocean.assets.pay_for_access_service(
            asset,
            service,
            consume_market_order_fee_address=self.wallet.address,
            consume_market_order_fee_token=service.datatoken.address,
            consume_market_order_fee_amount=0,
            wallet=self.wallet,
        )

        print(f"order_tx_id = '{order_tx_id}'")

        # Bob downloads. If the connection breaks, Bob can request again by showing order_tx_id.
        file_path = self.ocean.assets.download(
            asset=asset,
            service=service,
            consumer_wallet=self.wallet,
            destination="./downloads/",
            order_tx_id=order_tx_id,
        )
        print(f"file_path = '{file_path}'")  # e.g. datafile.0xAf07...
        data = open(file_path, "rb").read()

        msg = OceanMessage(performative=OceanMessage.Performative.RESULTS, content=data)
        msg.sender = envelope.to
        msg.to = envelope.sender
        envelope = Envelope(to=msg.to, sender=msg.sender, message=msg)
        self.put_envelope(envelope)
        self.logger.info(f"completed download! Sending result to handler!")

    def _create_d2c_job(self, envelope):
        DATA_did = envelope.message.data_did  # for convenience
        ALG_did = envelope.message.algo_did
        DATA_DDO = self.ocean.assets.resolve(
            DATA_did
        )  # make sure we operate on the updated and indexed metadata_cache_uri versions
        ALG_DDO = self.ocean.assets.resolve(ALG_did)

        compute_service = DATA_DDO.get_service("compute")
        algo_service = ALG_DDO.get_service("access")

        # allows the algorithm for C2D for that data asset
        compute_service.add_publisher_trusted_algorithm(ALG_DDO)
        DATA_DDO = self.ocean.assets.update(DATA_DDO, self.wallet)

        free_c2d_env = self.ocean.compute.get_free_c2d_environment(
            compute_service.service_endpoint
        )

        DATA_compute_input = ComputeInput(DATA_DDO, compute_service)
        ALGO_compute_input = ComputeInput(ALG_DDO, algo_service)

        # Pay for dataset and algo for 1 day

        self.logger.info(f"paying for dataset {DATA_did}")
        datasets, algorithm = self.ocean.assets.pay_for_compute_service(
            datasets=[DATA_compute_input],
            algorithm_data=ALGO_compute_input,
            consume_market_order_fee_address=self.wallet.address,
            wallet=self.wallet,
            compute_environment=free_c2d_env["id"],
            valid_until=int((datetime.utcnow() + timedelta(days=1)).timestamp()),
            consumer_address=free_c2d_env["consumerAddress"],
        )

        self.logger.info(
            f"paid for dataset {DATA_did} receipt: {datasets} with algorithm {algorithm}"
        )
        self.logger.info(f"starting compute job....")
        job_id = self.ocean.compute.start(
            consumer_wallet=self.wallet,
            dataset=datasets[0],
            compute_environment=free_c2d_env["id"],
            algorithm=algorithm,
        )

        self.logger.info(f"Started compute job with id: {job_id}")
        res = self.ocean.compute.status(DATA_did, job_id, self.wallet)
        while True:
            res_1 = self.ocean.compute.status(DATA_did, job_id, self.wallet)
            if res_1 != res:
                res = res_1
                self.logger.info(f"compute job with id: {job_id} @ {res_1}")
                if (code := res_1["status"]) in [20, 30, 40, 50, 60]:
                    continue
                elif code == 70:
                    break
            time.sleep(2)

        result_file = self.ocean.compute.compute_job_result_logs(
            DATA_DDO, compute_service, job_id, self.wallet
        )[0]

        msg = OceanMessage(
            performative=OceanMessage.Performative.RESULTS, content=result_file
        )
        msg.sender = envelope.to
        msg.to = envelope.sender
        envelope = Envelope(to=msg.to, sender=msg.sender, message=msg)
        self.put_envelope(envelope)
        self.logger.info(f"completed D2C! Sending result to handler!")

    def _permission_dataset(self, envelope: Envelope):
        data_ddo = self.ocean.assets.resolve(envelope.message.data_did)
        algo_ddo = self.ocean.assets.resolve(envelope.message.algo_did)

        if data_ddo is None or algo_ddo is None:
            raise ValueError(
                f"Unable to loaded the assets from their dids. Please confirm correct deployemnt on ocean!"
            )

        compute_service = data_ddo.services[0]
        compute_service.add_publisher_trusted_algorithm(algo_ddo)

        data_ddo = self.ocean.assets.update(data_ddo, self.wallet)

        msg = OceanMessage(
            performative=OceanMessage.Performative.DEPLOYMENT_RECIEPT,
            type="permissions",
            did=data_ddo.did,
            datatoken_contract_address=data_ddo.datatokens[0].get("address"),
        )
        msg.sender = envelope.to
        msg.to = envelope.sender
        envelope = Envelope(to=msg.to, sender=msg.sender, message=msg)
        self.put_envelope(envelope)
        self.logger.info(f"Permissioned datasets. ")

    def _deploy_data_to_download(self, envelope: Envelope):
        data_nft, datatoken = self._deploy_datatoken(envelope)

        provider_url = DataServiceProvider.get_url(self.ocean.config)
        DATA_files = [envelope.message.data_url_file]

        DATA_service = Service(
            service_id="0",
            service_type="access",
            service_endpoint=provider_url,
            datatoken=datatoken.address,
            files=DATA_files,
            timeout=0,
        )

        DATA_metadata = {
            "created": envelope.message.date_created,
            "updated": envelope.message.date_created,
            "description": "envelope.message.description",
            "name": envelope.message.name,
            "type": "dataset",
            "author": envelope.message.author,
            "license": envelope.message.license,
        }

        try:
            DATA_ddo = self.ocean.assets.create(
                metadata=DATA_metadata,
                publisher_wallet=self.wallet,
                data_nft_address=data_nft.address,
                services=[DATA_service],
                data_token_address=datatoken.address,
                encrypt=True,
            )
            self.logger.info(f"DATA did = '{DATA_ddo.did}'")
        except ocean_lib.exceptions.AquariusError as error:  # and how exactly is the did generated???
            self.logger.error(f"Error with creating asset. {error}")
            msg = error.args[0]
            if "is already registered to another asset." in msg:
                self.logger.error(f"Trying to resolve pre-existing did..")
                DATA_ddo = self.ocean.assets.resolve(msg.split(" ")[2])

        self.logger.info(f"Ensure asset is cached in aquarius")
        self._ensure_asset_cached_in_aquarius(DATA_ddo.did)

        msg = OceanMessage(
            performative=OceanMessage.Performative.DEPLOYMENT_RECIEPT,
            type="data_download",
            did=DATA_ddo.did,
            datatoken_contract_address=datatoken.address,
        )
        msg.sender = envelope.to
        msg.to = envelope.sender
        deployment_envelope = Envelope(to=msg.to, sender=msg.sender, message=msg)
        self.put_envelope(deployment_envelope)

    def _deploy_data_for_d2c(self, envelope: Envelope):
        erc721_nft, erc20_token = self._deploy_datatoken(envelope)

        DATA_metadata = {
            "created": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "updated": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "description": "envelope.message.description",  # TODO replace description field
            "name": envelope.message.name,
            "type": "dataset",
            "author": envelope.message.author,
            "license": envelope.message.license,
        }

        DATA_url_file = UrlFile(url=envelope.message.dataset_url)

        # Set the compute values for compute service
        DATA_compute_values = {
            "allowRawAlgorithm": False,
            "allowNetworkAccess": True,
            "publisherTrustedAlgorithms": [],
            "publisherTrustedAlgorithmPublishers": [],
        }

        # Create the Service
        from ocean_lib.services.service import Service

        DATA_compute_service = Service(
            service_id="2",
            service_type="compute",
            service_endpoint=self.ocean.config.provider_url,
            datatoken=erc20_token.address,
            files=[DATA_url_file],
            timeout=3600,
            compute_values=DATA_compute_values,
        )

        # Publish asset with compute service on-chain.
        DATA_asset = self.ocean.assets.create(
            metadata=DATA_metadata,
            publisher_wallet=self.wallet,
            files=[DATA_url_file],
            services=[DATA_compute_service],
            data_nft_address=erc721_nft.address,
            deployed_datatokens=[erc20_token],
        )
        self.logger.info(f"DATA did = '{DATA_asset.did}'")

        msg = OceanMessage(
            performative=OceanMessage.Performative.DEPLOYMENT_RECIEPT,
            type="d2c",
            did=DATA_asset.did,
            datatoken_contract_address=erc20_token.address,
        )
        msg.sender = envelope.to
        msg.to = envelope.sender
        deployment_envelope = Envelope(to=msg.to, sender=msg.sender, message=msg)
        self.put_envelope(deployment_envelope)

    def _deploy_algorithm(self, envelope: Envelope):
        """ """
        ALGO_nft_token, ALGO_datatoken = self._deploy_datatoken(envelope)

        ALGO_date_created = envelope.message.date_created
        ALGO_metadata = {
            "created": ALGO_date_created,
            "updated": ALGO_date_created,
            "description": envelope.message.description,
            "name": envelope.message.author,
            "type": "algorithm",
            "author": envelope.message.author,
            "license": envelope.message.license,
            "algorithm": {
                "language": envelope.message.language,
                "format": envelope.message.format,
                "version": envelope.message.version,
                "container": {
                    "entrypoint": envelope.message.entrypoint,
                    "image": envelope.message.image,
                    "tag": envelope.message.tag,
                    "checksum": envelope.message.checksum,
                },
            },
        }

        ALGO_url_file = UrlFile(url=envelope.message.files_url)

        # Publish asset with compute service on-chain.
        # The download (access service) is automatically created, but you can explore other options as well
        ALGO_asset = self.ocean.assets.create(
            metadata=ALGO_metadata,
            publisher_wallet=self.wallet,
            files=[ALGO_url_file],
            data_nft_address=ALGO_nft_token.address,
            deployed_datatokens=[ALGO_datatoken],
        )

        self.logger.info(f"ALG did = '{ALGO_asset.did}'")

        msg = OceanMessage(
            performative=OceanMessage.Performative.DEPLOYMENT_RECIEPT,
            type="algorithm",
            did=ALGO_asset.did,
            datatoken_contract_address=ALGO_datatoken.address,
        )
        msg.sender = envelope.to
        msg.to = envelope.sender
        deployment_envelope = Envelope(to=msg.to, sender=msg.sender, message=msg)
        self.put_envelope(deployment_envelope)

    def _ensure_asset_cached_in_aquarius(
        self, did: str, timeout: float = 600, poll_latency: float = 1
    ):
        """Ensure asset is cached in Aquarius
        Default timeout = 10 mins
        Default poll_latency = 1 second
        """
        with Timeout(timeout) as _timeout:
            while True:
                asset = self.ocean.assets.resolve(did)
                if asset is not None:
                    break
                _timeout.sleep(poll_latency)

    def _deploy_datatoken(self, envelope: Envelope):
        self.logger.info(f"interacting with ocean to deploy data token ...")

        print("Create ERC721 data NFT: begin.")

        erc721_nft = self.ocean.create_data_nft(
            name=envelope.message.data_nft_name,
            symbol=envelope.message.datatoken_name,
            from_wallet=self.wallet,
        )

        erc20_token = erc721_nft.create_datatoken(
            template_index=1,  # default value
            name=envelope.message.datatoken_name,  # name for ERC20 token
            symbol=envelope.message.datatoken_name,  # symbol for ERC20 token
            minter=self.wallet.address,  # minter address
            fee_manager=self.wallet.address,  # fee manager for this ERC20 token
            publish_market_order_fee_address=self.wallet.address,  # publishing Market Address
            publish_market_order_fee_token=ZERO_ADDRESS,  # publishing Market Fee Token
            publish_market_order_fee_amount=0,
            bytess=[b""],
            from_wallet=self.wallet,
        )

        self.logger.info(f"created the data token.")

        self.logger.info(
            f"DATA_datatoken.address = '{erc20_token.address}'\n publishing"
        )
        return erc721_nft, erc20_token

    def on_connect(self) -> None:
        """
        Tear down the connection.

        Connection status set automatically.
        """
        os.environ["OCEAN_NETWORK_URL"] = self.configuration.config.get(
            "ocean_network_url"
        )
        self.ocean_config = ExampleConfig.get_config()
        self.ocean = Ocean(self.ocean_config)

        with open(self.configuration.config.get("key_path"), "r") as f:
            key = f.read()
        acct = Account.from_key(key)

        # Create wallet
        self.wallet = Wallet(
            self.ocean.web3,
            acct.privateKey.hex(),
            self.ocean_config.block_confirmations,
            self.ocean_config.transaction_timeout,
        )

        self.logger.info(
            f"connected to Ocean with config.network_url = '{self.ocean_config.network_url}'"
        )
        self.logger.info(
            f"connected to Ocean with config.block_confirmations = {self.ocean_config.block_confirmations.value}"
        )
        self.logger.info(
            f"connected to Ocean with config.metadata_cache_uri = '{self.ocean_config.metadata_cache_uri}'"
        )
        self.logger.info(
            f"connected to Ocean with config.provider_url = '{self.ocean_config.provider_url}'"
        )
        self.logger.info(f"Address used: {acct.address}")

    def on_disconnect(self) -> None:
        """
        Tear down the connection.

        Connection status set automatically.
        """
