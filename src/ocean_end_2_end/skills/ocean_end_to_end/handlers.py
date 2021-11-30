# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2019 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This package contains a scaffold of a handler."""

from typing import Optional, cast

from aea.configurations.base import PublicId
from aea.protocols.base import Message
from aea.skills.base import Handler

from packages.eightballer.skills.ocean_end_to_end.strategy import OceanStrategy

from packages.eightballer.protocols.ocean.message import OceanMessage


class OceanHandler(Handler):
    """This class scaffolds a handler."""

    SUPPORTED_PROTOCOL = OceanMessage.protocol_id  # type: Optional[PublicId]

    def setup(self) -> None:
        """Implement the setup."""
        self.log = self.context.logger

    def handle(self, message: Message) -> None:
        """
        Implement the reaction to an envelope.

        :param message: the message
        """
        self.log.debug(f"Handling message {message}")
        strategy = cast(OceanStrategy, self.context.strategy)
        if message.performative == OceanMessage.Performative.DEPLOYMENT_RECIEPT:
            if message.type == "d2c":
                self.log.info(f"Recieved deployment reciept for data token!")
                strategy.data_to_compute_address = {"did": message.did,
                                                    "datatoken_contract_address": message.datatoken_contract_address}
                strategy.is_data_to_compute_deployed = True
                strategy.is_in_flight = False
            elif message.type == "algorithm":
                self.log.info(f"Recieved deployment reciept for algorithm!")
                strategy.algorithm_address = {"did": message.did,
                                                    "datatoken_contract_address": message.datatoken_contract_address}
                strategy.is_algorithm_deployed = True
                strategy.is_in_flight = False
            elif message.type == "permissions":
                self.log.info(f"updated permissions!")
                strategy.is_data_permissioned = True
                strategy.is_in_flight = False

            elif message.type == "data_download":
                self.log.info(f"created data asset for download!")
                strategy.is_data_download_deployed = True
                strategy.is_in_flight = False
                strategy.download_params["datatoken_address"] = message.datatoken_contract_address
                strategy.download_params["asset_did"] = message.did
                strategy.datapool_params["datatoken_address"] = message.datatoken_contract_address
            else:
                raise ValueError(f"Performative not valid: {message.performative}, {message.type}")
                
        elif message.performative == OceanMessage.Performative.RESULTS:
            self.log.info(f"{message.content}")
            if strategy.is_d2c_active: 
                self.log.info(f"results for d2c job!")
                strategy.has_completed_d2c_job = True 

            if strategy.is_download_active:
                self.log.info(f"Recieved results down job!")
                strategy.has_completed_download_job = True 

            strategy.is_in_flight = False
        elif message.performative == OceanMessage.Performative.POOL_DEPLOYMENT_RECIEPT:
            self.log.info(f"Sucecssfully deployed pool for asset!")
            strategy.is_in_flight = False
            strategy.is_pool_deployed = True
            strategy.download_params["pool_address"] = message.pool_address
            
        else:
            raise ValueError("Unhandled Message!!!")
            

        

    def teardown(self) -> None:
        """Implement the handler teardown."""
        self.log.info(f"tearing down handler ")
