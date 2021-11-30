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

"""Serialization module for file_storage protocol."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,redefined-builtin
from typing import Any, Dict, cast

from aea.mail.base_pb2 import DialogueMessage
from aea.mail.base_pb2 import Message as ProtobufMessage
from aea.protocols.base import Message, Serializer

from packages.eightballer.protocols.file_storage import file_storage_pb2
from packages.eightballer.protocols.file_storage.custom_types import ErrorCode
from packages.eightballer.protocols.file_storage.message import \
    FileStorageMessage


class FileStorageSerializer(Serializer):
    """Serialization for the 'file_storage' protocol."""

    @staticmethod
    def encode(msg: Message) -> bytes:
        """
        Encode a 'FileStorage' message into bytes.

        :param msg: the message object.
        :return: the bytes.
        """
        msg = cast(FileStorageMessage, msg)
        message_pb = ProtobufMessage()
        dialogue_message_pb = DialogueMessage()
        file_storage_msg = file_storage_pb2.FileStorageMessage()

        dialogue_message_pb.message_id = msg.message_id
        dialogue_reference = msg.dialogue_reference
        dialogue_message_pb.dialogue_starter_reference = dialogue_reference[0]
        dialogue_message_pb.dialogue_responder_reference = dialogue_reference[1]
        dialogue_message_pb.target = msg.target

        performative_id = msg.performative
        if performative_id == FileStorageMessage.Performative.FILE_UPLOAD:
            performative = file_storage_pb2.FileStorageMessage.File_Upload_Performative()  # type: ignore
            content = msg.content
            performative.content = content
            filename = msg.filename
            performative.filename = filename
            key = msg.key
            performative.key = key
            file_storage_msg.file_upload.CopyFrom(performative)
        elif performative_id == FileStorageMessage.Performative.FILE_DOWNLOAD:
            performative = file_storage_pb2.FileStorageMessage.File_Download_Performative()  # type: ignore
            access_url = msg.access_url
            performative.access_url = access_url
            content = msg.content
            performative.content = content
            file_storage_msg.file_download.CopyFrom(performative)
        elif performative_id == FileStorageMessage.Performative.ERROR:
            performative = file_storage_pb2.FileStorageMessage.Error_Performative()  # type: ignore
            error_code = msg.error_code
            ErrorCode.encode(performative.error_code, error_code)
            error_msg = msg.error_msg
            performative.error_msg = error_msg
            error_data = msg.error_data
            performative.error_data.update(error_data)
            file_storage_msg.error.CopyFrom(performative)
        elif performative_id == FileStorageMessage.Performative.END:
            performative = file_storage_pb2.FileStorageMessage.End_Performative()  # type: ignore
            file_storage_msg.end.CopyFrom(performative)
        else:
            raise ValueError("Performative not valid: {}".format(performative_id))

        dialogue_message_pb.content = file_storage_msg.SerializeToString()

        message_pb.dialogue_message.CopyFrom(dialogue_message_pb)
        message_bytes = message_pb.SerializeToString()
        return message_bytes

    @staticmethod
    def decode(obj: bytes) -> Message:
        """
        Decode bytes into a 'FileStorage' message.

        :param obj: the bytes object.
        :return: the 'FileStorage' message.
        """
        message_pb = ProtobufMessage()
        file_storage_pb = file_storage_pb2.FileStorageMessage()
        message_pb.ParseFromString(obj)
        message_id = message_pb.dialogue_message.message_id
        dialogue_reference = (
            message_pb.dialogue_message.dialogue_starter_reference,
            message_pb.dialogue_message.dialogue_responder_reference,
        )
        target = message_pb.dialogue_message.target

        file_storage_pb.ParseFromString(message_pb.dialogue_message.content)
        performative = file_storage_pb.WhichOneof("performative")
        performative_id = FileStorageMessage.Performative(str(performative))
        performative_content = dict()  # type: Dict[str, Any]
        if performative_id == FileStorageMessage.Performative.FILE_UPLOAD:
            content = file_storage_pb.file_upload.content
            performative_content["content"] = content
            filename = file_storage_pb.file_upload.filename
            performative_content["filename"] = filename
            key = file_storage_pb.file_upload.key
            performative_content["key"] = key
        elif performative_id == FileStorageMessage.Performative.FILE_DOWNLOAD:
            access_url = file_storage_pb.file_download.access_url
            performative_content["access_url"] = access_url
            content = file_storage_pb.file_download.content
            performative_content["content"] = content
        elif performative_id == FileStorageMessage.Performative.ERROR:
            pb2_error_code = file_storage_pb.error.error_code
            error_code = ErrorCode.decode(pb2_error_code)
            performative_content["error_code"] = error_code
            error_msg = file_storage_pb.error.error_msg
            performative_content["error_msg"] = error_msg
            error_data = file_storage_pb.error.error_data
            error_data_dict = dict(error_data)
            performative_content["error_data"] = error_data_dict
        elif performative_id == FileStorageMessage.Performative.END:
            pass
        else:
            raise ValueError("Performative not valid: {}.".format(performative_id))

        return FileStorageMessage(
            message_id=message_id,
            dialogue_reference=dialogue_reference,
            target=target,
            performative=performative,
            **performative_content
        )
