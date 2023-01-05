#! /bin/bash

NAME="ocean_buyer"

# distribute_ocean_tokens if using barge and ganache
if [ $OCEAN_NETWORK_NAME == developement ]; then
  python distribute_ocean_tokens.py
fi

aea create $NAME
cd $NAME

# setup the private key
echo -n $BUYER_AEA_KEY_ETHEREUM > ethereum_private_key.txt
echo -n $BUYER_AEA_KEY_FETCHAI > fetchai_private_key.txt

aea add-key fetchai
aea add-key fetchai fetchai_private_key.txt --connection

# fetchd config chain-id capricorn-1
# fetchd config node https://rpc-capricorn.fetch.ai:443

# setup fetch libraries
# generic protocols
aea add protocol fetchai/acn:1.1.6
aea add protocol fetchai/contract_api:1.1.6
aea add protocol fetchai/fipa:1.1.6
aea add protocol fetchai/ledger_api:1.1.6
aea add protocol fetchai/oef_search:1.1.6

#generic connections
aea add connection fetchai/ledger:0.21.4
aea add connection fetchai/p2p_libp2p:0.27.4
aea add connection fetchai/soef:0.27.5

# routing
aea config set --type dict agent.default_routing \
'{
  "fetchai/ledger_api:1.1.6": "fetchai/ledger:0.21.4",
  "fetchai/oef_search:1.1.6": "fetchai/soef:0.27.5"
}'
aea config set agent.default_connection fetchai/p2p_libp2p:0.27.4
# soef setup and configuration for p2p nodes

aea config set --type dict vendor.fetchai.connections.p2p_libp2p.config \
'{
  "delegate_uri": null,
  "entry_peers": ["/dns4/acn.fetch.ai/tcp/9000/p2p/16Uiu2HAkw1ypeQYQbRFV5hKUxGRHocwU5ohmVmCnyJNg36tnPFdx","/dns4/acn.fetch.ai/tcp/9001/p2p/16Uiu2HAmVWnopQAqq4pniYLw44VRvYxBUoRHqjz1Hh2SoCyjbyRW"],
  "public_uri": null,
  "local_uri": "127.0.0.1:9000"
}'


# custom connections
aea add connection eightballer/ocean:0.1.0

# custom protocols
aea add protocol eightballer/ocean:0.1.0

# custom skills
aea add skill eightballer/ocean_buyer:0.1.0


# setup connections
aea config set vendor.fetchai.connections.ledger.config.ledger_apis.fetchai.address $FETCH_URL
aea config set vendor.fetchai.connections.ledger.config.ledger_apis.fetchai.denom $FETCH_DENOM
aea config set vendor.fetchai.connections.ledger.config.ledger_apis.fetchai.chain_id $FETCH_CHAIN_ID
aea config set vendor.eightballer.connections.ocean.config.ocean_network_name  $OCEAN_NETWORK_NAME
aea config set vendor.fetchai.connections.ledger.config.ledger_apis.ethereum.address $RPC_URL
aea config set vendor.eightballer.connections.ocean.config.key_path ethereum_private_key.txt


aea install
aea build
aea issue-certificates
aea run