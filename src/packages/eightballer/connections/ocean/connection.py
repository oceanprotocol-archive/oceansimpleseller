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
import hashlib
import os
import time
from datetime import datetime
from typing import Any, Dict, Optional, Union

import requests
from aea.configurations.base import PublicId
from aea.connections.base import BaseSyncConnection, Connection
from aea.mail.base import Envelope
from ocean_lib.structures.file_objects import UrlFile
from packages.eightballer.protocols.ocean.message import OceanMessage

"""
Choose one of the possible implementations:

Sync (inherited from BaseSyncConnection) or Async (inherited from Connection) connection and remove unused one.
"""

CONNECTION_ID = PublicId.from_str("eightballer/ocean:0.1.0")

import json
import os

import ocean_lib
import web3
from eth_account import Account
from ocean_lib.agreements.service_types import ServiceTypes
from ocean_lib.data_provider.data_service_provider import DataServiceProvider
from ocean_lib.example_config import ExampleConfig
from ocean_lib.models.compute_input import ComputeInput
from ocean_lib.ocean.ocean import Ocean
from ocean_lib.services.service import Service
from ocean_lib.web3_internal.constants import ZERO_ADDRESS
from ocean_lib.web3_internal.currency import to_wei
from ocean_lib.web3_internal.wallet import Wallet
from web3._utils.threads import Timeout

Account.enable_unaudited_hdwallet_features()

from string import Template

D2C_TEMPLATE = Template(
    """{
    "main": {
        "type": "dataset",
        "files": [
     {
       "url": "$url",
     "index": 0,
       "contentType": "text/text"
     }
    ],
    "name": "$name", "author": "$author", "license": "$license",
    "dateCreated": "$date_created"
    }
}
"""
)


DATA_SERVICES_TEMPLATE = Template(
    """{
    "main": {
        "name": "DATA_dataAssetAccessServiceAgreement",
        "creator": "$creator_address",
        "timeout": 86400,
        "datePublished": "$date_published",
        "cost": 1.0
        }
    }
"""
)


# Specify metadata and service attributes, for "GPR" algorithm script.
# In same location as Branin test dataset. GPR = Gaussian Process Regression.
ALGO_TEMPLATE = Template(
    """{
    "main": {
        "type": "algorithm",
        "algorithm": {
           "language": "$language",
            "format": "$format",
            "version": "$version",
            "container": {
              "entrypoint": "$entrypoint",
              "image": "$image",
              "tag": "$tag"
            }
        },
        "files": [
	  {
	    "url": "$files_url",
	    "index": 0,
	    "contentType": "text/text"
	  }
	],
	"name": "$name",
    "author": "$author",
    "license": "$license",
	"dateCreated": "$date_created"
    }
}
"""
)

ALGO_SERVICE_TEMPLATE = Template(
    """{
        "main": {
            "name": "ALG_dataAssetAccessServiceAgreement",
            "creator": "$address",
            "timeout": 3600,
            "datePublished": "$date_published",
            "cost": 1.0
        }
    }"""
)


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
        if envelope.message.performative == OceanMessage.Performative.CREATE_POOL:
            self._create_pool(envelope)
        if envelope.message.performative == OceanMessage.Performative.DOWNLOAD_JOB:
            self._purchase_datatoken(envelope)

    def _purchase_datatoken(self, envelope: Envelope):
        try:
            self.ocean.pool.buy_data_tokens(
                pool_address=envelope.message.pool_address,
                amount=to_wei(envelope.message.datatoken_amt),
                max_OCEAN_amount=to_wei(envelope.message.max_cost_ocean),
                from_wallet=self.wallet,
            )

            msg = OceanMessage(
                performative=OceanMessage.Performative.DOWNLOAD_JOB,
                **{
                    "datatoken_address": "unused",
                    "datatoken_amt": -1,
                    "max_cost_ocean": -1,
                    "asset_did": "unused",
                    "pool_address": "unused",
                },
            )
            msg.sender = envelope.to
            msg.to = envelope.sender

            envelope = Envelope(to=msg.to, sender=msg.sender, message=msg)
            self.put_envelope(envelope)
            self.logger.info(f"Purchased 1 datatoken")

        except Exception as e:
            self.logger.error("Couldn't purchase datatokens")
            self.logger.error(e)

    def _download_asset(self, envelope: Envelope):
        did = envelope.message.asset_did
        token_address = envelope.message.datatoken_address
        data_token = self.ocean.get_data_token(token_address)
        if data_token.balanceOf(self.wallet.address) < envelope.message.datatoken_amt:
            self.logger.info(
                f"insufficient data tokens.. Purchasing from the open market."
            )
            self.ocean.pool.buy_data_tokens(
                envelope.message.pool_address,
                amount=to_wei(envelope.message.datatoken_amt),
                max_OCEAN_amount=to_wei(envelope.message.max_cost_ocean),
                from_wallet=self.wallet,
            )
        else:
            self.logger.info(f"Already has sufficient Datatokens.")

        asset = self.ocean.assets.resolve(did)
        service = asset.get_service(ServiceTypes.ASSET_ACCESS)

        # Bob sends his datatoken to the service
        quote = self.ocean.assets.order(
            asset.did, self.wallet.address, service_index=service.index
        )
        order_tx_id = self.ocean.assets.pay_for_service(
            self.ocean.web3,
            quote.amount,
            quote.data_token_address,
            asset.did,
            service.index,
            ZERO_ADDRESS,
            self.wallet,
            service.get_c2d_address(),
        )
        print(f"order_tx_id = '{order_tx_id}'")

        # Bob downloads. If the connection breaks, Bob can request again by showing order_tx_id.
        file_path = self.ocean.assets.download(
            asset.did,
            service.index,
            self.wallet,
            order_tx_id,
            destination="./downloads/",
        )
        print(f"file_path = '{file_path}'")  # e.g. datafile.0xAf07...
        data = open(file_path, "rb").read()

        msg = OceanMessage(performative=OceanMessage.Performative.RESULTS, content=data)
        msg.sender = envelope.to
        msg.to = envelope.sender
        envelope = Envelope(to=msg.to, sender=msg.sender, message=msg)
        self.put_envelope(envelope)
        self.logger.info(f"completed download! Sending result to handler!")

    def _create_pool(self, envelope: Envelope, retries=2):
        if retries == 0:
            raise ValueError("Failed to deploy pool...")
        try:
            pool = self.ocean.pool.create(
                envelope.message.datatoken_address,
                data_token_amount=to_wei(envelope.message.datatoken_amt),
                OCEAN_amount=to_wei(envelope.message.ocean_amt),
                from_wallet=self.wallet,
            )
            pool_address = pool.address
            print(f"Deployed pool_address = '{pool_address}'")
        except (web3.exceptions.TransactionNotFound, ValueError) as e:
            self.logger.error(f"Failed to deploy pool!")
            self._create_pool(envelope, retries - 1)

        msg = OceanMessage(
            performative=OceanMessage.Performative.POOL_DEPLOYMENT_RECIEPT,
            pool_address=pool_address,
        )
        msg.sender = envelope.to
        msg.to = envelope.sender
        envelope = Envelope(to=msg.to, sender=msg.sender, message=msg)
        self.put_envelope(envelope)
        self.logger.info(f"Data pool created! Sending result to handler!")

    def _create_d2c_job(self, envelope):
        DATA_did = envelope.message.data_did  # for convenience
        ALG_did = envelope.message.algo_did
        DATA_DDO = self.ocean.assets.resolve(
            DATA_did
        )  # make sure we operate on the updated and indexed metadata_cache_uri versions
        ALG_DDO = self.ocean.assets.resolve(ALG_did)

        compute_service = DATA_DDO.get_service("compute")
        algo_service = ALG_DDO.get_service("access")

        self.logger.info(f"ordering dataset {DATA_did}")
        dataset_order_requirements = self.ocean.assets.order(
            DATA_did, self.wallet.address, service_type=compute_service.type
        )
        self.logger.info(f"paying for dataset {DATA_did}")
        DATA_order_tx_id = self.ocean.assets.pay_for_service(
            self.ocean.web3,
            dataset_order_requirements.amount,
            dataset_order_requirements.data_token_address,
            DATA_did,
            compute_service.index,
            ZERO_ADDRESS,
            self.wallet,
            dataset_order_requirements.computeAddress,
        )
        self.logger.info(f"paid for dataset {DATA_did} receipt: {DATA_order_tx_id}")

        self.logger.info(f"ordering algorithm {ALG_did}")
        algo_order_requirements = self.ocean.assets.order(
            ALG_did, self.wallet.address, service_type=algo_service.type
        )
        self.logger.info(f"paying for algorithm {ALG_did}")
        ALG_order_tx_id = self.ocean.assets.pay_for_service(
            self.ocean.web3,
            algo_order_requirements.amount,
            algo_order_requirements.data_token_address,
            ALG_did,
            algo_service.index,
            ZERO_ADDRESS,
            self.wallet,
            algo_order_requirements.computeAddress,
        )
        self.logger.info(f"paid for algo {ALG_did} receipt: {ALG_order_tx_id}")
        self.logger.info(f"starting compute job....")
        compute_inputs = [
            ComputeInput(DATA_did, DATA_order_tx_id, compute_service.index)
        ]
        job_id = self.ocean.compute.start(
            compute_inputs,
            self.wallet,
            algorithm_did=ALG_did,
            algorithm_tx_id=ALG_order_tx_id,
            algorithm_data_token=ALG_DDO.data_token_address,
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

        result_file = self.ocean.compute.result_file(DATA_did, job_id, 0, self.wallet)

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
        trusted_algos = self.add_publisher_trusted_algorithm(
            data_ddo.did, algo_ddo.did, self.ocean_config.metadata_cache_uri
        )
        data_ddo.update_compute_privacy(
            trusted_algorithms=trusted_algos,
            trusted_algo_publishers=[],
            allow_all=True,
            allow_raw_algorithm=True,
        )
        self.ocean.assets.update(data_ddo, publisher_wallet=self.wallet)
        msg = OceanMessage(
            performative=OceanMessage.Performative.DEPLOYMENT_RECIEPT,
            type="permissions",
            did="",
            datatoken_contract_address="",
        )
        msg.sender = envelope.to
        msg.to = envelope.sender
        envelope = Envelope(to=msg.to, sender=msg.sender, message=msg)
        self.put_envelope(envelope)
        self.logger.info(f"Permissioned datasets. ")

    def _deploy_data_to_download(self, envelope: Envelope):
        datatoken = self._deploy_datatoken(envelope)

        provider_url = DataServiceProvider.get_url(self.ocean.config)

        # Calc DATA service compute descriptor
        service_attributes = json.loads(
            DATA_SERVICES_TEMPLATE.substitute(
                creator_address=self.wallet.address,
                date_published=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            )
        )

        DATA_service = Service(
            service_endpoint=provider_url,
            service_type=ServiceTypes.ASSET_ACCESS,
            attributes=service_attributes,
        )

        data_metadata = json.loads(
            D2C_TEMPLATE.substitute(
                url=envelope.message.dataset_url,
                name=envelope.message.name,
                author=envelope.message.author,
                license=envelope.message.license,
                date_created=envelope.message.date_created,
            )
        )

        try:
            DATA_ddo = self.ocean.assets.create(
                metadata=data_metadata,
                publisher_wallet=self.wallet,
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

        # Encrypt file(s) using provider
        DATA_encrypted_files = self.ocean.assets.encrypt_files([DATA_url_file])

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
            files=DATA_encrypted_files,
            timeout=3600,
            compute_values=DATA_compute_values,
        )

        # Publish asset with compute service on-chain.
        DATA_asset = self.ocean.assets.create(
            metadata=DATA_metadata,
            publisher_wallet=self.wallet,
            encrypted_files=DATA_encrypted_files,
            services=[DATA_compute_service],
            erc721_address=erc721_nft.address,
            deployed_erc20_tokens=[erc20_token],
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

        from ocean_lib.structures.file_objects import UrlFile

        ALGO_url_file = UrlFile(
            url=envelope.message.files_url
        )

        # Encrypt file(s) using provider
        ALGO_encrypted_files = self.ocean.assets.encrypt_files([ALGO_url_file])

        # Publish asset with compute service on-chain.
        # The download (access service) is automatically created, but you can explore other options as well
        ALGO_asset = self.ocean.assets.create(
            metadata=ALGO_metadata,
            publisher_wallet=self.wallet,
            encrypted_files=ALGO_encrypted_files,
            erc721_address=ALGO_nft_token.address,
            deployed_erc20_tokens=[ALGO_datatoken],
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

        erc721_nft = self.ocean.create_erc721_nft(
            envelope.message.data_nft_name, envelope.message.datatoken_name, self.wallet
        )

        cap = self.ocean.to_wei(100)

        # nft_factory = self.ocean.get_nft_factory()

        erc20_token = erc721_nft.create_datatoken(
            template_index=1,  # default value
            name=envelope.message.datatoken_name,  # name for ERC20 token
            symbol=envelope.message.datatoken_name,  # symbol for ERC20 token
            minter=self.wallet.address,  # minter address
            fee_manager=self.wallet.address,  # fee manager for this ERC20 token
            publish_market_order_fee_address=self.wallet.address,  # publishing Market Address
            publish_market_order_fee_token=ZERO_ADDRESS,  # publishing Market Fee Token
            cap=cap,
            publish_market_order_fee_amount=0,
            bytess=[b""],
            from_wallet=self.wallet,
        )

        self.logger.info(f"created the data token.")

        self.logger.info(
            f"DATA_datatoken.address = '{erc20_token.address}'\n publishing"
        )
        return erc721_nft, erc20_token

    def add_publisher_trusted_algorithm(
        self, asset_or_did: str, algo_did: str, metadata_cache_uri: str
    ) -> list:
        """
        :return: List of trusted algos
        """
        asset = self.ocean.assets.resolve(asset_or_did)

        compute_service = asset.get_service(ServiceTypes.CLOUD_COMPUTE)
        assert (
            compute_service
        ), "Cannot add trusted algorithm to this asset because it has no compute service."
        privacy_values = compute_service.attributes["main"].get("privacy")
        if not privacy_values:
            privacy_values = {}
            compute_service.attributes["main"]["privacy"] = privacy_values

        assert isinstance(privacy_values, dict), "Privacy key is not a dictionary."
        trusted_algos = privacy_values.get("publisherTrustedAlgorithms", [])
        # remove algo_did if already in the list
        trusted_algos = [ta for ta in trusted_algos if ta["did"] != algo_did]

        # now add this algo_did as trusted algo
        algo_ddo = self.ocean.assets.resolve(algo_did)
        trusted_algos.append(self.generate_trusted_algo_dict(asset_or_did=algo_ddo.did))

        # update with the new list
        privacy_values["publisherTrustedAlgorithms"] = trusted_algos
        assert (
            compute_service.attributes["main"]["privacy"] == privacy_values
        ), "New trusted algorithm was not added. Failed when updating the privacy key. "
        return trusted_algos

    def generate_trusted_algo_dict(
        self, asset_or_did: str = None, metadata_cache_uri: Optional[str] = None
    ) -> dict:
        """
        :return: Object as follows:
        ```
        {
            "did": <did>,
            "filesChecksum": <str>,
            "containerSectionChecksum": <str>
        }
        ```
        """
        ddo = self.ocean.assets.resolve(asset_or_did)

        algo_metadata = ddo.metadata
        return {
            "did": ddo.did,
            "filesChecksum": self.create_checksum(
                algo_metadata.get("encryptedFiles", "")
                + json.dumps(algo_metadata["main"]["files"], separators=(",", ":"))
            ),
            "containerSectionChecksum": self.create_checksum(
                json.dumps(
                    algo_metadata["main"]["algorithm"]["container"],
                    separators=(",", ":"),
                )
            ),
        }

    def create_checksum(self, text: str) -> str:
        """
        :return: str
        """
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

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
