#!/usr/bin/env python3

import os
from typing import List
from ocean_lib.example_config import ExampleConfig
from ocean_lib.models.datatoken import Datatoken
from ocean_lib.ocean.ocean import Ocean
from ocean_lib.web3_internal.wallet import Wallet


def distribute_ocean_tokens(
    ocean: Ocean,
    amount: int,
    recipients: List[str],
    ocean_deployer_wallet: Wallet,
) -> None:
    """
    Mint OCEAN tokens to seller and buyer
    """
    OCEAN_token = Datatoken(ocean.web3, address=ocean.OCEAN_address)

    for recipient in recipients:
        if OCEAN_token.balanceOf(recipient) < amount:
            OCEAN_token.transfer(recipient, amount, from_wallet=ocean_deployer_wallet)


if __name__ == "__main__":
    config = ExampleConfig.get_config()
    ocean = Ocean(config)
    amount = ocean.web3.toWei(10000, "ether")
    ocean_deployer_wallet = Wallet(
        ocean.web3,
        private_key=os.getenv("FACTORY_DEPLOYER_PRIVATE_KEY"),
        block_confirmations=config.block_confirmations,
        transaction_timeout=config.transaction_timeout,
    )

    recipients = []
    for private_key_envvar in ["SELLER_AEA_KEY_ETHEREUM", "BUYER_AEA_KEY_ETHEREUM"]:
        private_key = os.environ.get(private_key_envvar)
        if not private_key:
            continue

        w = Wallet(
            ocean.web3,
            private_key=private_key,
            block_confirmations=config.block_confirmations,
            transaction_timeout=config.transaction_timeout,
        )

        recipients.append(w.address)

    distribute_ocean_tokens(ocean, amount, recipients, ocean_deployer_wallet)
