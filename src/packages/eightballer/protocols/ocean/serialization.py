# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2021 eightballer
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

"""Serialization module for ocean protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
from typing import Any, Dict, cast

from aea.mail.base_pb2 import DialogueMessage
from aea.mail.base_pb2 import Message as ProtobufMessage
from aea.protocols.base import Message, Serializer

from packages.eightballer.protocols.ocean import ocean_pb2
from packages.eightballer.protocols.ocean.custom_types import ErrorCode
from packages.eightballer.protocols.ocean.message import OceanMessage


class OceanSerializer(Serializer):
    """Serialization for the 'ocean' protocol."""

    @staticmethod
    def encode(msg: Message) -> bytes:
        """
        Encode a 'Ocean' message into bytes.

        :param msg: the message object.
        :return: the bytes.
        """
        msg = cast(OceanMessage, msg)
        message_pb = ProtobufMessage()
        dialogue_message_pb = DialogueMessage()
        ocean_msg = ocean_pb2.OceanMessage()

        dialogue_message_pb.message_id = msg.message_id
        dialogue_reference = msg.dialogue_reference
        dialogue_message_pb.dialogue_starter_reference = dialogue_reference[0]
        dialogue_message_pb.dialogue_responder_reference = dialogue_reference[1]
        dialogue_message_pb.target = msg.target

        performative_id = msg.performative
        if performative_id == OceanMessage.Performative.DEPLOY_DATA_DOWNLOAD:
            performative = ocean_pb2.OceanMessage.Deploy_Data_Download_Performative()  # type: ignore
            token0_name = msg.token0_name
            performative.token0_name = token0_name
            token1_name = msg.token1_name
            performative.token1_name = token1_name
            dataset_url = msg.dataset_url
            performative.dataset_url = dataset_url
            name = msg.name
            performative.name = name
            author = msg.author
            performative.author = author
            date_created = msg.date_created
            performative.date_created = date_created
            license = msg.license
            performative.license = license
            amount_to_mint = msg.amount_to_mint
            performative.amount_to_mint = amount_to_mint
            ocean_msg.deploy_data_download.CopyFrom(performative)
        elif performative_id == OceanMessage.Performative.DEPLOY_C2D:
            performative = ocean_pb2.OceanMessage.Deploy_C2D_Performative()  # type: ignore
            token0_name = msg.token0_name
            performative.token0_name = token0_name
            token1_name = msg.token1_name
            performative.token1_name = token1_name
            dataset_url = msg.dataset_url
            performative.dataset_url = dataset_url
            name = msg.name
            performative.name = name
            author = msg.author
            performative.author = author
            date_created = msg.date_created
            performative.date_created = date_created
            license = msg.license
            performative.license = license
            amount_to_mint = msg.amount_to_mint
            performative.amount_to_mint = amount_to_mint
            ocean_msg.deploy_c2d.CopyFrom(performative)
        elif performative_id == OceanMessage.Performative.DEPLOY_ALGORITHM:
            performative = ocean_pb2.OceanMessage.Deploy_Algorithm_Performative()  # type: ignore
            token0_name = msg.token0_name
            performative.token0_name = token0_name
            token1_name = msg.token1_name
            performative.token1_name = token1_name
            amount_to_mint = msg.amount_to_mint
            performative.amount_to_mint = amount_to_mint
            language = msg.language
            performative.language = language
            format = msg.format
            performative.format = format
            version = msg.version
            performative.version = version
            entrypoint = msg.entrypoint
            performative.entrypoint = entrypoint
            image = msg.image
            performative.image = image
            tag = msg.tag
            performative.tag = tag
            files_url = msg.files_url
            performative.files_url = files_url
            name = msg.name
            performative.name = name
            author = msg.author
            performative.author = author
            date_created = msg.date_created
            performative.date_created = date_created
            license = msg.license
            performative.license = license
            ocean_msg.deploy_algorithm.CopyFrom(performative)
        elif performative_id == OceanMessage.Performative.POOL_DEPLOYMENT_RECIEPT:
            performative = ocean_pb2.OceanMessage.Pool_Deployment_Reciept_Performative()  # type: ignore
            pool_address = msg.pool_address
            performative.pool_address = pool_address
            ocean_msg.pool_deployment_reciept.CopyFrom(performative)
        elif performative_id == OceanMessage.Performative.DEPLOYMENT_RECIEPT:
            performative = ocean_pb2.OceanMessage.Deployment_Reciept_Performative()  # type: ignore
            type = msg.type
            performative.type = type
            did = msg.did
            performative.did = did
            datatoken_contract_address = msg.datatoken_contract_address
            performative.datatoken_contract_address = datatoken_contract_address
            ocean_msg.deployment_reciept.CopyFrom(performative)
        elif performative_id == OceanMessage.Performative.CREATE_POOL:
            performative = ocean_pb2.OceanMessage.Create_Pool_Performative()  # type: ignore
            datatoken_address = msg.datatoken_address
            performative.datatoken_address = datatoken_address
            datatoken_amt = msg.datatoken_amt
            performative.datatoken_amt = datatoken_amt
            ocean_amt = msg.ocean_amt
            performative.ocean_amt = ocean_amt
            ocean_msg.create_pool.CopyFrom(performative)
        elif performative_id == OceanMessage.Performative.DOWNLOAD_JOB:
            performative = ocean_pb2.OceanMessage.Download_Job_Performative()  # type: ignore
            datatoken_address = msg.datatoken_address
            performative.datatoken_address = datatoken_address
            datatoken_amt = msg.datatoken_amt
            performative.datatoken_amt = datatoken_amt
            max_cost_ocean = msg.max_cost_ocean
            performative.max_cost_ocean = max_cost_ocean
            asset_did = msg.asset_did
            performative.asset_did = asset_did
            pool_address = msg.pool_address
            performative.pool_address = pool_address
            ocean_msg.download_job.CopyFrom(performative)
        elif performative_id == OceanMessage.Performative.PERMISSION_DATASET:
            performative = ocean_pb2.OceanMessage.Permission_Dataset_Performative()  # type: ignore
            algo_did = msg.algo_did
            performative.algo_did = algo_did
            data_did = msg.data_did
            performative.data_did = data_did
            ocean_msg.permission_dataset.CopyFrom(performative)
        elif performative_id == OceanMessage.Performative.C2D_JOB:
            performative = ocean_pb2.OceanMessage.C2D_Job_Performative()  # type: ignore
            data_did = msg.data_did
            performative.data_did = data_did
            algo_did = msg.algo_did
            performative.algo_did = algo_did
            ocean_msg.c2d_job.CopyFrom(performative)
        elif performative_id == OceanMessage.Performative.RESULTS:
            performative = ocean_pb2.OceanMessage.Results_Performative()  # type: ignore
            content = msg.content
            performative.content = content
            ocean_msg.results.CopyFrom(performative)
        elif performative_id == OceanMessage.Performative.ERROR:
            performative = ocean_pb2.OceanMessage.Error_Performative()  # type: ignore
            error_code = msg.error_code
            ErrorCode.encode(performative.error_code, error_code)
            error_msg = msg.error_msg
            performative.error_msg = error_msg
            error_data = msg.error_data
            performative.error_data.update(error_data)
            ocean_msg.error.CopyFrom(performative)
        elif performative_id == OceanMessage.Performative.END:
            performative = ocean_pb2.OceanMessage.End_Performative()  # type: ignore
            ocean_msg.end.CopyFrom(performative)
        else:
            raise ValueError("Performative not valid: {}".format(performative_id))

        dialogue_message_pb.content = ocean_msg.SerializeToString()

        message_pb.dialogue_message.CopyFrom(dialogue_message_pb)
        message_bytes = message_pb.SerializeToString()
        return message_bytes

    @staticmethod
    def decode(obj: bytes) -> Message:
        """
        Decode bytes into a 'Ocean' message.

        :param obj: the bytes object.
        :return: the 'Ocean' message.
        """
        message_pb = ProtobufMessage()
        ocean_pb = ocean_pb2.OceanMessage()
        message_pb.ParseFromString(obj)
        message_id = message_pb.dialogue_message.message_id
        dialogue_reference = (
            message_pb.dialogue_message.dialogue_starter_reference,
            message_pb.dialogue_message.dialogue_responder_reference,
        )
        target = message_pb.dialogue_message.target

        ocean_pb.ParseFromString(message_pb.dialogue_message.content)
        performative = ocean_pb.WhichOneof("performative")
        performative_id = OceanMessage.Performative(str(performative))
        performative_content = dict()  # type: Dict[str, Any]
        if performative_id == OceanMessage.Performative.DEPLOY_DATA_DOWNLOAD:
            token0_name = ocean_pb.deploy_data_download.token0_name
            performative_content["token0_name"] = token0_name
            token1_name = ocean_pb.deploy_data_download.token1_name
            performative_content["token1_name"] = token1_name
            dataset_url = ocean_pb.deploy_data_download.dataset_url
            performative_content["dataset_url"] = dataset_url
            name = ocean_pb.deploy_data_download.name
            performative_content["name"] = name
            author = ocean_pb.deploy_data_download.author
            performative_content["author"] = author
            date_created = ocean_pb.deploy_data_download.date_created
            performative_content["date_created"] = date_created
            license = ocean_pb.deploy_data_download.license
            performative_content["license"] = license
            amount_to_mint = ocean_pb.deploy_data_download.amount_to_mint
            performative_content["amount_to_mint"] = amount_to_mint
        elif performative_id == OceanMessage.Performative.DEPLOY_C2D:
            token0_name = ocean_pb.deploy_c2d.token0_name
            performative_content["token0_name"] = token0_name
            token1_name = ocean_pb.deploy_c2d.token1_name
            performative_content["token1_name"] = token1_name
            dataset_url = ocean_pb.deploy_c2d.dataset_url
            performative_content["dataset_url"] = dataset_url
            name = ocean_pb.deploy_c2d.name
            performative_content["name"] = name
            author = ocean_pb.deploy_c2d.author
            performative_content["author"] = author
            date_created = ocean_pb.deploy_c2d.date_created
            performative_content["date_created"] = date_created
            license = ocean_pb.deploy_c2d.license
            performative_content["license"] = license
            amount_to_mint = ocean_pb.deploy_c2d.amount_to_mint
            performative_content["amount_to_mint"] = amount_to_mint
        elif performative_id == OceanMessage.Performative.DEPLOY_ALGORITHM:
            token0_name = ocean_pb.deploy_algorithm.token0_name
            performative_content["token0_name"] = token0_name
            token1_name = ocean_pb.deploy_algorithm.token1_name
            performative_content["token1_name"] = token1_name
            amount_to_mint = ocean_pb.deploy_algorithm.amount_to_mint
            performative_content["amount_to_mint"] = amount_to_mint
            language = ocean_pb.deploy_algorithm.language
            performative_content["language"] = language
            format = ocean_pb.deploy_algorithm.format
            performative_content["format"] = format
            version = ocean_pb.deploy_algorithm.version
            performative_content["version"] = version
            entrypoint = ocean_pb.deploy_algorithm.entrypoint
            performative_content["entrypoint"] = entrypoint
            image = ocean_pb.deploy_algorithm.image
            performative_content["image"] = image
            tag = ocean_pb.deploy_algorithm.tag
            performative_content["tag"] = tag
            files_url = ocean_pb.deploy_algorithm.files_url
            performative_content["files_url"] = files_url
            name = ocean_pb.deploy_algorithm.name
            performative_content["name"] = name
            author = ocean_pb.deploy_algorithm.author
            performative_content["author"] = author
            date_created = ocean_pb.deploy_algorithm.date_created
            performative_content["date_created"] = date_created
            license = ocean_pb.deploy_algorithm.license
            performative_content["license"] = license
        elif performative_id == OceanMessage.Performative.POOL_DEPLOYMENT_RECIEPT:
            pool_address = ocean_pb.pool_deployment_reciept.pool_address
            performative_content["pool_address"] = pool_address
        elif performative_id == OceanMessage.Performative.DEPLOYMENT_RECIEPT:
            type = ocean_pb.deployment_reciept.type
            performative_content["type"] = type
            did = ocean_pb.deployment_reciept.did
            performative_content["did"] = did
            datatoken_contract_address = (
                ocean_pb.deployment_reciept.datatoken_contract_address
            )
            performative_content[
                "datatoken_contract_address"
            ] = datatoken_contract_address
        elif performative_id == OceanMessage.Performative.CREATE_POOL:
            datatoken_address = ocean_pb.create_pool.datatoken_address
            performative_content["datatoken_address"] = datatoken_address
            datatoken_amt = ocean_pb.create_pool.datatoken_amt
            performative_content["datatoken_amt"] = datatoken_amt
            ocean_amt = ocean_pb.create_pool.ocean_amt
            performative_content["ocean_amt"] = ocean_amt
        elif performative_id == OceanMessage.Performative.DOWNLOAD_JOB:
            datatoken_address = ocean_pb.download_job.datatoken_address
            performative_content["datatoken_address"] = datatoken_address
            datatoken_amt = ocean_pb.download_job.datatoken_amt
            performative_content["datatoken_amt"] = datatoken_amt
            max_cost_ocean = ocean_pb.download_job.max_cost_ocean
            performative_content["max_cost_ocean"] = max_cost_ocean
            asset_did = ocean_pb.download_job.asset_did
            performative_content["asset_did"] = asset_did
            pool_address = ocean_pb.download_job.pool_address
            performative_content["pool_address"] = pool_address
        elif performative_id == OceanMessage.Performative.PERMISSION_DATASET:
            algo_did = ocean_pb.permission_dataset.algo_did
            performative_content["algo_did"] = algo_did
            data_did = ocean_pb.permission_dataset.data_did
            performative_content["data_did"] = data_did
        elif performative_id == OceanMessage.Performative.C2D_JOB:
            data_did = ocean_pb.c2d_job.data_did
            performative_content["data_did"] = data_did
            algo_did = ocean_pb.c2d_job.algo_did
            performative_content["algo_did"] = algo_did
        elif performative_id == OceanMessage.Performative.RESULTS:
            content = ocean_pb.results.content
            performative_content["content"] = content
        elif performative_id == OceanMessage.Performative.ERROR:
            pb2_error_code = ocean_pb.error.error_code
            error_code = ErrorCode.decode(pb2_error_code)
            performative_content["error_code"] = error_code
            error_msg = ocean_pb.error.error_msg
            performative_content["error_msg"] = error_msg
            error_data = ocean_pb.error.error_data
            error_data_dict = dict(error_data)
            performative_content["error_data"] = error_data_dict
        elif performative_id == OceanMessage.Performative.END:
            pass
        else:
            raise ValueError("Performative not valid: {}.".format(performative_id))

        return OceanMessage(
            message_id=message_id,
            dialogue_reference=dialogue_reference,
            target=target,
            performative=performative,
            **performative_content
        )
