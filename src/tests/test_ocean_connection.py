#
# Copyright 2021 Ocean Protocol Foundation
# SPDX-License-Identifier: Apache-2.0
#
import asyncio
import os
from aea.mail.base import Envelope
from aea.configurations.base import ComponentType, ConnectionConfig, PublicId

from packages.eightballer.connections.ocean.connection import OceanConnection
from packages.eightballer.protocols.ocean.message import OceanMessage


def test_datatoken_creation():
    """Tests that _deploy_datatoken function works as expected."""

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
            "token0_name": "DATA1",
            "token1_name": "DATA1",
            "amount_to_mint": 100,
            "dataset_url": "https://raw.githubusercontent.com/trentmc/branin/main/branin.arff",
            "name": "example", # TODO add description field
            "author": "Trent",
            "license": "CCO",
        },
    )

    envelope = Envelope(to="test", sender="msg.sender", message=ocean_message)

    ocean.on_send(envelope)
