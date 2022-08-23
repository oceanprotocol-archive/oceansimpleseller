#
# Copyright 2021 Ocean Protocol Foundation
# SPDX-License-Identifier: Apache-2.0
#
from src.tests.utils import convert_to_bytes_format


def test_convert_to_bytes_format():
    """Tests convert_to_bytes_format function."""
    data = str(b"0x//&652898")
    assert isinstance(data, str)
    new_data = convert_to_bytes_format(data=data)
    assert isinstance(new_data, bytes)
    assert new_data == b"0x//&652898"
