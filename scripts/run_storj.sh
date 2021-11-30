#! /bin/bash
cd ./src/ocean_publisher
# set Storj configurations
aea -s config set connections.storj_file_transfer.config.storj_creds.endpoint_url "$STORJ_ENDPOINT"
aea -s config set connections.storj_file_transfer.config.storj_creds.aws_secret_access_key "$STORJ_ACCESS_KEY"
aea -s config set connections.storj_file_transfer.config.storj_creds.aws_access_key_id "$STORJ_ACCESS_KEY_ID"
aea -s config set connections.storj_file_transfer.config.target_skill_id $TARGET_SKILL

aea -s run

