import os
from eth_account import Account
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
