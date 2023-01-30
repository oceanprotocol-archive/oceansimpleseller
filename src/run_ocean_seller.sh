#! /bin/bash

NAME="ocean_seller"

# distribute_ocean_tokens if using barge and ganache
if [ $OCEAN_NETWORK_NAME == development ]; then
  python distribute_ocean_tokens.py
fi

aea create $NAME
cd $NAME

# setup the private key
echo -n $SELLER_AEA_KEY_ETHEREUM > ethereum_private_key.txt
echo -n $SELLER_AEA_KEY_FETCHAI > fetchai_private_key.txt

aea add-key fetchai
aea add-key fetchai fetchai_private_key.txt --connection

# fetchd config chain-id capricorn-1
# fetchd config node https://rpc-capricorn.fetch.ai:443

# setup fetch libraries
# generic protocols
aea add protocol fetchai/acn:1.1.7
aea add protocol fetchai/contract_api:1.1.7
aea add protocol fetchai/fipa:1.1.7
aea add protocol fetchai/ledger_api:1.1.7
aea add protocol fetchai/oef_search:1.1.7

#generic connections
aea add connection fetchai/ledger:0.21.5
aea add connection fetchai/p2p_libp2p:0.27.5
aea add connection fetchai/soef:0.27.6

# routing
aea config set --type dict agent.default_routing \
'{
  "fetchai/ledger_api:1.1.7": "fetchai/ledger:0.21.5",
  "fetchai/oef_search:1.1.7": "fetchai/soef:0.27.6"
}'
aea config set agent.default_connection fetchai/p2p_libp2p:0.27.5
# soef setup and configuration for p2p nodes

aea config set --type dict vendor.fetchai.connections.p2p_libp2p.config \
'{
  "delegate_uri": null,
  "entry_peers": ["/dns4/acn.fetch.ai/tcp/9000/p2p/16Uiu2HAkw1ypeQYQbRFV5hKUxGRHocwU5ohmVmCnyJNg36tnPFdx","/dns4/acn.fetch.ai/tcp/9001/p2p/16Uiu2HAmVWnopQAqq4pniYLw44VRvYxBUoRHqjz1Hh2SoCyjbyRW"],
  "public_uri": null,
  "local_uri": "127.0.0.1:9001"
}'


# custom connections
aea add connection eightballer/ocean:0.1.0
aea add connection eightballer/storj_file_transfer:0.1.0

# custom protocols
aea add protocol eightballer/file_storage:0.1.0
aea add protocol eightballer/ocean:0.1.0

# custom skills
aea add skill eightballer/ocean_seller:0.1.0

# setup connections
aea config set vendor.fetchai.connections.ledger.config.ledger_apis.fetchai.address $FETCH_URL
aea config set vendor.fetchai.connections.ledger.config.ledger_apis.fetchai.denom $FETCH_DENOM
aea config set vendor.fetchai.connections.ledger.config.ledger_apis.fetchai.chain_id $FETCH_CHAIN_ID
aea config set vendor.eightballer.connections.ocean.config.ocean_network_name $OCEAN_NETWORK_NAME
aea config set vendor.fetchai.connections.ledger.config.ledger_apis.ethereum.address $RPC_URL
aea config set vendor.eightballer.connections.ocean.config.key_path ethereum_private_key.txt
aea config set --type dict vendor.eightballer.connections.storj_file_transfer.config.storj_creds \
'{
  "aws_access_key_id": "jx7bgg74ceog3eznrovaiqcy23sa",
  "aws_secret_access_key": "j2wulv3drlgrt5apjr2csc5lmkzyqpqakgzuoc63fn6wedxmnu2ng",
  "endpoint_url": "https://gateway.eu1.storjshare.io"
}'

aea config set --type dict vendor.eightballer.skills.ocean_seller.strategy.args \
'
{
    "deployments":{
        "data_to_compute": {},
        "data_download": {},
        "algorithm": {}
        },
    "algorithm_params": {
        "data_nft_name": "algo_nft_c2d",
        "datatoken_name": "algo_token",
        "amount_to_mint": 100,
        "language": "python",
        "format": "docker-image",
        "version": "0.1",
        "entrypoint": "python $ALGO",
        "image": "oceanprotocol/algo_dockers",
        "checksum": "sha256:8221d20c1c16491d7d56b9657ea09082c0ee4a8ab1a6621fa720da58b09580e4",
        "tag": "python-branin",
        "files_url": "https://raw.githubusercontent.com/oceanprotocol/c2d-examples/main/branin_and_gpr/gpr.py",
        "name": "gpr",
        "description": "gpr",
        "author": "Trent",
        "license": "CCO",
        "date_created": "2019-12-28T10:55:11Z"
        },
    "data_to_compute_params":{
        "data_nft_name": "data_nft_c2d",
        "datatoken_name": "datatoken_c2d",
        "amount_to_mint": 100,
        "dataset_url": "https://raw.githubusercontent.com/oceanprotocol/c2d-examples/main/branin_and_gpr/branin.arff",
        "name": "example",
        "description": "Compute service to run GPR algorithm.",
        "author": "Trent",
        "license": "CCO",
        "date_created": "2019-12-28T10:55:11Z"
        },
    "data_exchange_params":{
        "datatoken_address": "",
        "datatoken_amt": 50,
        "ocean_amt": 1,
        "rate": 1
    },
}'




aea install
aea build
aea issue-certificates
aea run