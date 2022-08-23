import os
from eth_account import Account
from ocean_lib.utils.utilities import convert_to_bytes
from ocean_lib.web3_internal.wallet import Wallet


def _seller_wallet(ocean_connection):
    with open(os.environ["SELLER_AEA_KEY_ETHEREUM_PATH"], "r") as f:
        key = f.read()
    acct = Account.from_key(key)

    return Wallet(
        ocean_connection.ocean.web3,
        acct.privateKey.hex(),
        ocean_connection.ocean_config.block_confirmations,
        ocean_connection.ocean_config.transaction_timeout,
    )


def _buyer_wallet(ocean_connection):
    with open(os.environ["BUYER_AEA_KEY_ETHEREUM_PATH"], "r") as f:
        key = f.read()
    acct = Account.from_key(key)

    return Wallet(
        ocean_connection.ocean.web3,
        acct.privateKey.hex(),
        ocean_connection.ocean_config.block_confirmations,
        ocean_connection.ocean_config.transaction_timeout,
    )


def convert_to_bytes_format(data: str) -> bytes:
    """Converts a bytes string into bytes."""
    assert data[0:2] == "b'"
    indexes = slice(2, len(data) - 1)
    data = data[indexes]

    return convert_to_bytes(data=data)
