#
# Copyright 2021 Ocean Protocol Foundation
# SPDX-License-Identifier: Apache-2.0
#
import asyncio
import os
from aea.mail.base import Envelope
from aea.configurations.base import ConnectionConfig

from packages.eightballer.connections.ocean.connection import OceanConnection
from packages.eightballer.protocols.ocean.message import OceanMessage
from mock import patch, Mock


@patch.object(OceanConnection, "put_envelope")
def test_datatoken_creation(put_envelope):
    """Tests that _deploy_datatoken function works as expected."""

    def side_effect(envelope):
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
            ocean_network_url=os.environ["OCEAN_NETWORK_URL"],
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
            "dataset_url": "https://raw.githubusercontent.com/trentmc/branin/main/branin.arff",
            "name": "example",
            "description": "example",
            "author": "Trent",
            "license": "CCO",
        },
    )

    envelope = Envelope(to="test", sender="msg.sender", message=ocean_message)

    ocean.on_send(envelope)


@patch.object(OceanConnection, "put_envelope")
def test_deploy_algorithm(put_envelope):
    """Tests that _deploy_algorithm function works as expected."""

    def side_effect(envelope):
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
            ocean_network_url=os.environ["OCEAN_NETWORK_URL"],
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
            "checksum": "44e10daa6637893f4276bb8d7301eb35306ece50f61ca34dcab550",
            "tag": "python-branin",
            "files_url": "https://raw.githubusercontent.com/trentmc/branin/main/gpr.py",
            "name": "gpr",
            "description": "gpr",
            "author": "Trent",
            "license": "CCO",
            "date_created": "2019-12-28T10:55:11Z",
        },
    )

    envelope = Envelope(to="test", sender="msg.sender", message=ocean_message)

    ocean.on_send(envelope)


@patch.object(OceanConnection, "put_envelope")
def test_permission_dataset(put_envelope):
    """Tests that _permission_dataset function works as expected."""
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
            ocean_network_url=os.environ["OCEAN_NETWORK_URL"],
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
            "dataset_url": "https://raw.githubusercontent.com/trentmc/branin/main/branin.arff",
            "name": "example",
            "description": "example",
            "author": "Trent",
            "license": "CCO",
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
            ocean_network_url=os.environ["OCEAN_NETWORK_URL"],
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
            "checksum": "44e10daa6637893f4276bb8d7301eb35306ece50f61ca34dcab550",
            "tag": "python-branin",
            "files_url": "https://raw.githubusercontent.com/trentmc/branin/main/gpr.py",
            "name": "gpr",
            "description": "gpr",
            "author": "Trent",
            "license": "CCO",
            "date_created": "2019-12-28T10:55:11Z",
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
        assert envelope.message.type == "permissions"
        assert (
            envelope.message.performative
            == OceanMessage.Performative.DEPLOYMENT_RECIEPT
        )

    put_envelope.side_effect = side_effect

    ocean.on_send(envelope)


@patch.object(OceanConnection, "put_envelope")
def test_create_fixed_rate(put_envelope):
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
            ocean_network_url=os.environ["OCEAN_NETWORK_URL"],
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
            "dataset_url": "https://raw.githubusercontent.com/trentmc/branin/main/branin.arff",
            "name": "example",
            "description": "example",
            "author": "Trent",
            "license": "CCO",
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
            ocean_network_url=os.environ["OCEAN_NETWORK_URL"],
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
            "checksum": "44e10daa6637893f4276bb8d7301eb35306ece50f61ca34dcab550",
            "tag": "python-branin",
            "files_url": "https://raw.githubusercontent.com/trentmc/branin/main/gpr.py",
            "name": "gpr",
            "description": "gpr",
            "author": "Trent",
            "license": "CCO",
            "date_created": "2019-12-28T10:55:11Z",
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
        OceanMessage.Performative.CREATE_POOL,
        _body={
            "datatoken_address": datatoken_address,
            "rate": 1,
            "ocean_amt": 10,
        },
    )

    def side_effect(envelope):
        assert (
            envelope.message.performative
            == OceanMessage.Performative.POOL_DEPLOYMENT_RECIEPT
        )

    put_envelope.side_effect = side_effect

    envelope = Envelope(to="test", sender="msg.sender", message=ocean_message)

    ocean.on_send(envelope)
