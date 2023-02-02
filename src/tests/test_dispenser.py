#
# Copyright 2021 Ocean Protocol Foundation
# SPDX-License-Identifier: Apache-2.0
#
import asyncio
import os

from mock import patch, Mock

from aea.mail.base import Envelope
from aea.configurations.base import ConnectionConfig

from packages.eightballer.connections.ocean.connection import OceanConnection
from packages.eightballer.protocols.ocean.message import OceanMessage
from web3.main import Web3
from brownie.network import accounts, chain


@patch.object(OceanConnection, "put_envelope")
def test_create_dispenser(put_envelope):
    """Tests that _deploy_algorithm & _create_fixed_rate functions work as expected."""
    global data_ddo
    global algo_ddo

    def side_effect(envelope):
        global data_ddo
        data_ddo = envelope.message.did
        assert (
            envelope.message.performative
            == OceanMessage.Performative.DEPLOYMENT_RECIEPT
        )

    put_envelope.side_effect = side_effect

    ocean = OceanConnection(
        ConnectionConfig(
            "ocean",
            "eightballer",
            "0.1.0",
            ocean_network_name=os.environ["OCEAN_NETWORK_NAME"],
            key_path=os.environ["SELLER_AEA_KEY_ETHEREUM_PATH"],
        ),
        "None",
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(ocean.connect())

    ocean_message = OceanMessage(
        OceanMessage.Performative.DEPLOY_D2C,
        _body={
            "data_nft_name": "data_nft_c2d",
            "datatoken_name": "datatoken_c2d",
            "amount_to_mint": 100,
            "dataset_url": "https://raw.githubusercontent.com/oceanprotocol/c2d-examples/main/branin_and_gpr/branin.arff",
            "name": "example",
            "description": "example",
            "author": "Trent",
            "license": "CCO",
            "has_pricing_schema": False,
        },
    )

    envelope = Envelope(to="test", sender="msg.sender", message=ocean_message)

    ocean.on_send(envelope)

    def side_effect(envelope):
        global algo_ddo
        algo_ddo = envelope.message.did
        assert (
            envelope.message.performative
            == OceanMessage.Performative.DEPLOYMENT_RECIEPT
        )

    put_envelope.side_effect = side_effect

    ocean = OceanConnection(
        ConnectionConfig(
            "ocean",
            "eightballer",
            "0.1.0",
            ocean_network_name=os.environ["OCEAN_NETWORK_NAME"],
            key_path=os.environ["SELLER_AEA_KEY_ETHEREUM_PATH"],
        ),
        "None",
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(ocean.connect())

    ocean_message = OceanMessage(
        OceanMessage.Performative.DEPLOY_ALGORITHM,
        _body={
            "data_nft_name": "algo_nft_c2d",
            "datatoken_name": "algo_token",
            "amount_to_mint": 100,
            "language": "python",
            "format": "docker-image",
            "version": "0.1",
            "entrypoint": "python $ALGO",
            "image": "oceanprotocol/algo_dockers",
            "checksum": "sha256:8221d20c1c16491d7d56b9657ea09082c0ee4a8ab1a6621fa720da58b09580e4",
            "tag": "python-branin",
            "files_url": "https://raw.githubusercontent.com/oceanprotocol/c2d-examples/main/branin_and_gpr/gpr.py",
            "name": "gpr",
            "description": "gpr",
            "author": "Trent",
            "license": "CCO",
            "date_created": "2019-12-28T10:55:11Z",
            "has_pricing_schema": False,
        },
    )

    envelope = Envelope(to="test", sender="msg.sender", message=ocean_message)

    ocean.on_send(envelope)

    ocean_message = OceanMessage(
        OceanMessage.Performative.PERMISSION_DATASET,
        _body={"algo_did": algo_ddo, "data_did": data_ddo},
    )

    envelope = Envelope(to="test", sender="msg.sender", message=ocean_message)

    def side_effect(envelope):
        global datatoken_address
        datatoken_address = envelope.message.datatoken_contract_address
        assert envelope.message.type == "permissions"
        assert (
            envelope.message.performative
            == OceanMessage.Performative.DEPLOYMENT_RECIEPT
        )

    put_envelope.side_effect = side_effect

    ocean.on_send(envelope)

    ocean_message = OceanMessage(
        OceanMessage.Performative.CREATE_DISPENSER,
        _body={
            "datatoken_address": datatoken_address,
        },
    )

    def side_effect(envelope):
        assert (
            envelope.message.performative
            == OceanMessage.Performative.DISPENSER_DEPLOYMENT_RECIEPT
        )

    put_envelope.side_effect = side_effect

    envelope = Envelope(to="test", sender="msg.sender", message=ocean_message)

    ocean.on_send(envelope)


@patch.object(OceanConnection, "put_envelope")
def test_purchase_datatoken(put_envelope):
    """Tests that _purchase_datatoken function works as expected as buyer role."""
    global data_ddo
    global algo_ddo
    global exchange_id

    def side_effect(envelope):
        global data_ddo
        data_ddo = envelope.message.did
        assert (
            envelope.message.performative
            == OceanMessage.Performative.DEPLOYMENT_RECIEPT
        )

    put_envelope.side_effect = side_effect

    ocean = OceanConnection(
        ConnectionConfig(
            "ocean",
            "eightballer",
            "0.1.0",
            ocean_network_name=os.environ["OCEAN_NETWORK_NAME"],
            key_path=os.environ["SELLER_AEA_KEY_ETHEREUM_PATH"],
        ),
        "None",
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(ocean.connect())

    ocean_message = OceanMessage(
        OceanMessage.Performative.DEPLOY_D2C,
        _body={
            "data_nft_name": "data_nft_c2d",
            "datatoken_name": "datatoken_c2d",
            "amount_to_mint": 100,
            "dataset_url": "https://raw.githubusercontent.com/oceanprotocol/c2d-examples/main/branin_and_gpr/branin.arff",
            "name": "example",
            "description": "example",
            "author": "Trent",
            "license": "CCO",
            "has_pricing_schema": False,
        },
    )

    envelope = Envelope(to="test", sender="msg.sender", message=ocean_message)

    ocean.on_send(envelope)

    def side_effect(envelope):
        global algo_ddo
        algo_ddo = envelope.message.did
        assert (
            envelope.message.performative
            == OceanMessage.Performative.DEPLOYMENT_RECIEPT
        )

    put_envelope.side_effect = side_effect

    ocean = OceanConnection(
        ConnectionConfig(
            "ocean",
            "eightballer",
            "0.1.0",
            ocean_network_name=os.environ["OCEAN_NETWORK_NAME"],
            key_path=os.environ["SELLER_AEA_KEY_ETHEREUM_PATH"],
        ),
        "None",
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(ocean.connect())

    ocean_message = OceanMessage(
        OceanMessage.Performative.DEPLOY_ALGORITHM,
        _body={
            "data_nft_name": "algo_nft_c2d",
            "datatoken_name": "algo_token",
            "amount_to_mint": 100,
            "language": "python",
            "format": "docker-image",
            "version": "0.1",
            "entrypoint": "python $ALGO",
            "image": "oceanprotocol/algo_dockers",
            "checksum": "sha256:8221d20c1c16491d7d56b9657ea09082c0ee4a8ab1a6621fa720da58b09580e4",
            "tag": "python-branin",
            "files_url": "https://raw.githubusercontent.com/oceanprotocol/c2d-examples/main/branin_and_gpr/gpr.py",
            "name": "gpr",
            "description": "gpr",
            "author": "Trent",
            "license": "CCO",
            "date_created": "2019-12-28T10:55:11Z",
            "has_pricing_schema": False,
        },
    )

    envelope = Envelope(to="test", sender="msg.sender", message=ocean_message)

    ocean.on_send(envelope)

    ocean_message = OceanMessage(
        OceanMessage.Performative.PERMISSION_DATASET,
        _body={"algo_did": algo_ddo, "data_did": data_ddo},
    )

    envelope = Envelope(to="test", sender="msg.sender", message=ocean_message)

    def side_effect(envelope):
        global datatoken_address
        datatoken_address = envelope.message.datatoken_contract_address
        assert envelope.message.type == "permissions"
        assert (
            envelope.message.performative
            == OceanMessage.Performative.DEPLOYMENT_RECIEPT
        )

    put_envelope.side_effect = side_effect

    ocean.on_send(envelope)

    ocean_message = OceanMessage(
        OceanMessage.Performative.CREATE_DISPENSER,
        _body={
            "datatoken_address": datatoken_address,
            "rate": 1,
            "ocean_amt": 10,
        },
    )

    def side_effect(envelope):
        global datatoken_address
        global dispenser_status
        datatoken_address = envelope.message.datatoken_address
        dispenser_status = envelope.message.dispenser_status
        assert dispenser_status is True
        assert (
            envelope.message.performative
            == OceanMessage.Performative.DISPENSER_DEPLOYMENT_RECIEPT
        )

    put_envelope.side_effect = side_effect

    envelope = Envelope(to="test", sender="msg.sender", message=ocean_message)

    ocean.on_send(envelope)

    ocean2 = OceanConnection(
        ConnectionConfig(
            "ocean",
            "eightballer",
            "0.1.0",
            ocean_network_name=os.environ["OCEAN_NETWORK_NAME"],
            key_path=os.environ["BUYER_AEA_KEY_ETHEREUM_PATH"],
        ),
        "None",
    )

    loop2 = asyncio.get_event_loop()
    loop2.run_until_complete(ocean2.connect())

    def side_effect(envelope):
        assert envelope.message.performative == OceanMessage.Performative.DOWNLOAD_JOB

    put_envelope.side_effect = side_effect

    ocean2.on_connect()

    # seller_wallet = accounts.add(os.environ["SELLER_AEA_KEY_ETHEREUM"])
    buyer_wallet = accounts.add(os.environ["BUYER_AEA_KEY_ETHEREUM"])

    datatoken = ocean2.ocean.get_datatoken(datatoken_address)
    tx = datatoken.dispense(
        amount=Web3.toWei(envelope.message.datatoken_amt, "ether"),
        tx_dict={"from": buyer_wallet},
    )

    ocean_message = OceanMessage(
        OceanMessage.Performative.DOWNLOAD_JOB,
        _body={
            "datatoken_address": datatoken_address,
            "datatoken_amt": 2,
            "asset_did": data_ddo,
            "order_tx_id": tx.txid,
        },
    )

    envelope = Envelope(to="test", sender="msg.sender", message=ocean_message)

    ocean2.on_send(envelope)
