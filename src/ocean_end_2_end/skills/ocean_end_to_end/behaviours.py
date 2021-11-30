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

"""This package contains a scaffold of a behaviour."""

from typing import cast

from aea.skills.base import Behaviour, Envelope
from packages.eightballer.skills.ocean_end_to_end import PUBLIC_ID as SENDER_ID
from packages.eightballer.skills.ocean_end_to_end.strategy import OceanStrategy

from packages.eightballer.protocols.ocean.message import OceanMessage
from packages.eightballer.protocols.ocean.dialogues import (
    OceanDialogue,
    OceanDialogues
)



class OceanBehaviourBase(Behaviour):
    """This class scaffolds a behaviour."""

    def setup(self) -> None:
        """Implement the setup."""
        self.log = self.context.logger

    def teardown(self) -> None:
        """Implement the task teardown."""
        self.log.debug(f"Tearing down the behaviour")


        
class OceanD2CBehaviour(OceanBehaviourBase):
    
    def act(self) -> None:
        """Implement the act."""
        strategy = cast(OceanStrategy, self.context.strategy)
    
        if strategy.is_in_flight or not strategy.is_d2c_active:
            return 
    
        if not strategy.is_data_to_compute_deployed and \
            strategy.data_to_compute_address == {}:
            self.log.info(f"Initialising deploying the data_to_compute!!")
            self.__create_envelope(OceanMessage.Performative.DEPLOY_D2C, 
                               **strategy.data_to_compute_params)
            return
                               
        if not strategy.is_algorithm_deployed and \
            strategy.algorithm_address == {}:
            self.log.info(f"Initialising deploying the algorithm!")
            self.__create_envelope(OceanMessage.Performative.DEPLOY_ALGORITHM, 
                               **strategy.algorithm_params)
            return

        if not strategy.is_data_permissioned and \
            strategy.is_algorithm_deployed and \
            strategy.is_data_to_compute_deployed:
            self.log.info(f"permissioning the dataset to allow d 2 c !")
            self.__create_envelope(OceanMessage.Performative.PERMISSION_DATASET, 
                               **strategy.get_permission_request())
            return 

        if strategy.is_data_permissioned and \
            strategy.is_algorithm_deployed and \
            strategy.is_data_to_compute_deployed and \
            not strategy.has_completed_d2c_job:
            self.log.info(f"submitting the data 2 compute job!")
            self.__create_envelope(OceanMessage.Performative.D2C_JOB, 
                               **strategy.get_permission_request())
                
        if strategy.has_completed_d2c_job:
            self.log.info(f"Completed the d2c demonstration... Setting strategy to download behaviour")
            strategy.is_d2c_active = False
            strategy.is_processing = False
            

        
    def __create_envelope(self, performative: OceanMessage.Performative, **kwargs) -> None:
        strategy = cast(OceanStrategy, self.context.strategy)
        receiver_id = "eightballer/ocean:0.1.0"
        msg = OceanMessage(
            performative=performative,
            **kwargs
        )
        msg.sender = str(SENDER_ID)
        msg.to = receiver_id
        file_upload_envolope = Envelope(
            to=receiver_id, sender=str(SENDER_ID), message=msg
        )
        self.context.outbox.put(file_upload_envolope)
        strategy.is_in_flight = True

        
class OceanDataAccessBehaviour(OceanBehaviourBase):
    
    def act(self) -> None:
        """Implement the act."""
        strategy = cast(OceanStrategy, self.context.strategy)
    
        if strategy.is_in_flight or not strategy.is_download_active:
            return 

            
        if not strategy.is_data_download_deployed and \
            strategy.data_download_address == {}:
            self.log.info(f"Initialising deploying the data_to_download!!")
            self.__create_envelope(OceanMessage.Performative.DEPLOY_DATA_DOWNLOAD, 
                               **strategy.data_to_compute_params)
            return
        
        if not strategy.is_pool_deployed and \
            strategy.download_params['pool_address']== "":
            self.log.info(f"Initialising creating the data pool!")
            self.__create_envelope(OceanMessage.Performative.CREATE_POOL, 
                               **strategy.datapool_params)
            return
            
        if strategy.is_data_download_deployed and \
            strategy.is_pool_deployed:
            self.log.info(f"creating the data download!")
            self.__create_envelope(OceanMessage.Performative.DOWNLOAD_JOB, 
                               **strategy.download_params)
            return
            
        if strategy.is_data_download_ and \
            strategy.is_pool_deployed and \
            strategy.download_job_completed:
            self.log.info(f"completed the data download!")
            strategy.is_download_active = False
            strategy.is_processing = False

        
    def __create_envelope(self, performative: OceanMessage.Performative, **kwargs) -> None:
        strategy = cast(OceanStrategy, self.context.strategy)
        receiver_id = "eightballer/ocean:0.1.0"
        msg = OceanMessage(
            performative=performative,
            **kwargs
        )
        msg.sender = str(SENDER_ID)
        msg.to = receiver_id
        file_upload_envolope = Envelope(
            to=receiver_id, sender=str(SENDER_ID), message=msg
        )
        self.context.outbox.put(file_upload_envolope)
        strategy.is_in_flight = True


class OceanDemoBehaviour(Behaviour):
    def act(self):
        strategy = cast(OceanStrategy, self.context.strategy)

        if strategy.is_processing:
            return
        if strategy.demo_d2c and not strategy.has_completed_d2c_job:
            self.context.logger.info(f"Setting D2C Behaviour to active")
            strategy.is_processing = True
            strategy.is_d2c_active = True
            return 
        elif strategy.demo_download and not strategy.has_completed_download_job:
            strategy.is_download_active = True
            strategy.is_processing = True
            self.context.logger.info(f"Setting Download Behaviour to active")
        

        
    def teardown(self):
        pass

    def setup(self):
        pass
        