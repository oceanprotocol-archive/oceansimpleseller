import os
from eth_account import Account


def _seller_wallet():
    with open(os.environ["SELLER_AEA_KEY_ETHEREUM_PATH"], "r") as f:
        key = f.read()
    acct = Account.from_key(key)

    return acct


def _buyer_wallet():
    with open(os.environ["BUYER_AEA_KEY_ETHEREUM_PATH"], "r") as f:
        key = f.read()
    acct = Account.from_key(key)

    return acct
