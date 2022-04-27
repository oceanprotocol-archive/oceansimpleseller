#
# Copyright 2021 Ocean Protocol Foundation
# SPDX-License-Identifier: Apache-2.0
#
# import time

# import pytest

from aea.mail.base import Envelope
from aea.configurations.base import ComponentType, ConnectionConfig, PublicId

from packages.eightballer.connections.ocean.connection import OceanConnection
from packages.eightballer.protocols.ocean.message import OceanMessage

def test_datatoken_creation():
    """Tests that a compute job with a raw algorithm starts properly."""

    # ocean = OceanConnection(ConnectionConfig("test","test", "1.0.0"), "None")

    # ocean_message = OceanMessage()

    # envelope = Envelope(to="test", sender="msg.sender", message="msg")
    
    # OceanMessage._deploy_datatoken(envelope)
