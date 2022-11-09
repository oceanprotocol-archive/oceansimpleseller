#!/usr/bin/env python3

import os
from typing import List
from brownie.network import accounts
from ocean_lib.example_config import ExampleConfig
from ocean_lib.models.datatoken import Datatoken
from ocean_lib.ocean.ocean import Ocean


def distribute_ocean_tokens(
    ocean: Ocean,
    amount: int,
    recipients: List[str],
    ocean_deployer_wallet,
) -> None:
    """
    Mint OCEAN tokens to seller and buyer
    """
    OCEAN_token = Datatoken(ocean.web3, address=ocean.OCEAN_address)

    for recipient in recipients:
        if OCEAN_token.balanceOf(recipient) < amount:
            OCEAN_token.mint(recipient, amount, {"from": ocean_deployer_wallet})


if __name__ == "__main__":
    config = ExampleConfig.get_config(os.getenv("OCEAN_NETWORK_NAME"))
    ocean = Ocean(config)
    amount = ocean.web3.toWei(10000, "ether")
    ocean_deployer_wallet = accounts.add(os.getenv("FACTORY_DEPLOYER_PRIVATE_KEY"))

    recipients = []
    for private_key_envvar in ["SELLER_AEA_KEY_ETHEREUM", "BUYER_AEA_KEY_ETHEREUM"]:
        private_key = os.environ.get(private_key_envvar)
        if not private_key:
            continue

        w = accounts.add(private_key)
        recipients.append(w.address)

    distribute_ocean_tokens(ocean, amount, recipients, ocean_deployer_wallet)
