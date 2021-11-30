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

"""This package contains a scaffold of a model."""

from aea.skills.base import Model


class OceanStrategy(Model):
    """This class scaffolds a model."""
    _is_data_to_compute_deployed = False
    _is_data_to_compute_minted = False
    _is_data_to_compute_published = False

    
    _deployments = {}

    _is_pool_deployed = False


    _is_algorithm_deployed = False
    _is_algorithm_minted = False
    _is_algorithm_published = False

    _is_data_download_deployed = False
    _is_data_download_minted = False
    _is_data_download_published = False

    _is_data_permissioned = False

    _is_in_flight = False
    _has_completed_d2c_job = False
    _has_completed_download_job = False

    _data_to_compute_params = {}
    _algorithm_params = {}
    _download_params = {}
    _datapool_params = {}

    _is_d2c_active = False
    _is_download_active = False

    @property
    def is_d2c_active(self):
        return self._is_d2c_active

    @is_d2c_active.setter
    def is_d2c_active(self, value):
        self._is_d2c_active = value
    @property
    def is_download_active(self):
        return self._is_download_active

    @is_download_active.setter
    def is_download_active(self, value):
        self._is_download_active = value
    
    @property
    def has_completed_download_job(self):
        return self._has_completed_download_job

    @has_completed_download_job.setter
    def has_completed_download_job(self, value):
        self._has_completed_download_job = value
    
    @property
    def has_completed_d2c_job(self):
        return self._has_completed_d2c_job

    @has_completed_d2c_job.setter
    def has_completed_d2c_job(self, value):
        self._has_completed_d2c_job = value
    
    @property
    def is_data_permissioned(self):
        return self._is_data_permissioned

    @is_data_permissioned.setter
    def is_data_permissioned(self, value):
        self._is_data_permissioned = value
    
    @property
    def is_data_download_deployed(self):
        return self._is_data_download_deployed
    
    @is_data_download_deployed.setter
    def is_data_download_deployed(self, value):
        self._is_data_download_deployed = value

    @property
    def is_data_to_compute_deployed(self):
        return self._is_data_to_compute_deployed
    
    @is_data_to_compute_deployed.setter
    def is_data_to_compute_deployed(self, value):
        self._is_data_to_compute_deployed = value

    @property
    def is_data_to_compute_minted(self):
        return self._is_data_to_compute_minted

    @is_data_to_compute_minted.setter
    def is_data_to_compute_minted(self, value: bool):
        self._is_data_to_compute_minted = value
    
    @property
    def is_data_to_compute_published(self):
        return self._is_data_to_compute_published

    @is_data_to_compute_published.setter
    def is_data_to_compute_published(self, value: bool):
        self._is_data_to_compute_published = value
    
    @property
    def is_in_flight(self):
        return self._is_in_flight
    
    @is_in_flight.setter
    def is_in_flight(self, value: bool):
        self._is_in_flight = value
        

    @property
    def algorithm_address(self):
        return self._deployments['algorithm']
    
    @algorithm_address.setter
    def algorithm_address(self, value):
        self._deployments['algorithm'] = value

    @property
    def data_to_compute_address(self):
        return self._deployments['data_to_compute']
    
    @data_to_compute_address.setter
    def data_to_compute_address(self, value):
        self._deployments['data_to_compute'] = value

    @property
    def data_download_address(self):
        return self._deployments['data_download']
    
    @data_download_address.setter
    def data_download_address(self, value):
        self._deployments['data_download'] = value

    @property
    def is_pool_deployed(self):
        return self._is_pool_deployed
    
    @is_pool_deployed.setter
    def is_pool_deployed(self, value):
        self._is_pool_deployed = value

    @property
    def is_algorithm_deployed(self):
        return self._is_algorithm_deployed
    
    @is_algorithm_deployed.setter
    def is_algorithm_deployed(self, value):
        self._is_algorithm_deployed = value

    @property
    def algorithm_params(self):
        return self._algorithm_params

    @property
    def data_to_compute_params(self):
        return self._data_to_compute_params

    @property
    def datapool_params(self):
        return self._datapool_params

    @datapool_params.setter
    def datapool_params(self, value):
        self._datapool_params = value
        
    @property
    def download_params(self):
        return self._download_params

    @download_params.setter
    def download_params(self, value):
        self._download_params = value
        
    def get_permission_request(self):
        algo_did = self.algorithm_address.get("did", None)
        if algo_did is None:
            raise ValueError("Agent does not have algo did! make sure it has been deployed.")
        data_did = self.data_to_compute_address.get("did", None)
        if data_did is None:
            raise ValueError("Agent does not have data did! make sure it has been deployed.")
        return {
            "algo_did": algo_did,
            "data_did": data_did
        }


    def __init__(self,**kwargs):
        self._data_to_compute_params = kwargs.pop('data_to_compute_params')
        self._algorithm_params = kwargs.pop('algorithm_params')
        self._download_params = kwargs.pop('download_params')
        self._datapool_params = kwargs.pop('datapool_params')
        self._deployments = kwargs.pop('deployments')
        super().__init__(**kwargs)

    def setup(self):
        self.log = self.context.logger
        self.log.info(f"Initialised the strategy.")
        if self.data_to_compute_address != {}:
            self.is_data_to_compute_deployed = True
        if self.algorithm_address != {}:
            self.is_algorithm_deployed =True
        
        self.is_d2c_active = False
        self.is_download_active = False

        self.is_processing = False

        self.demo_d2c = False
        self.demo_download = True
        