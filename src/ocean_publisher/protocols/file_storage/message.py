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

"""This module contains file_storage's message definition."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,too-many-branches,not-an-iterable,unidiomatic-typecheck,unsubscriptable-object
import logging
from typing import Any, Dict, Set, Tuple, cast

from aea.configurations.base import PublicId
from aea.exceptions import AEAEnforceError, enforce
from aea.protocols.base import Message

from packages.eightballer.protocols.file_storage.custom_types import (
    ErrorCode as CustomErrorCode,
)


_default_logger = logging.getLogger(
    "aea.packages.eightballer.protocols.file_storage.message"
)

DEFAULT_BODY_SIZE = 4


class FileStorageMessage(Message):
    """A protocol for exchanging any bytes message."""

    protocol_id = PublicId.from_str("eightballer/file_storage:0.1.0")
    protocol_specification_id = PublicId.from_str("mobix/file_storage:0.1.0")

    ErrorCode = CustomErrorCode

    class Performative(Message.Performative):
        """Performatives for the file_storage protocol."""

        END = "end"
        ERROR = "error"
        FILE_DOWNLOAD = "file_download"
        FILE_UPLOAD = "file_upload"

        def __str__(self) -> str:
            """Get the string representation."""
            return str(self.value)

    _performatives = {"end", "error", "file_download", "file_upload"}
    __slots__: Tuple[str, ...] = tuple()

    class _SlotsCls:
        __slots__ = (
            "access_url",
            "content",
            "dialogue_reference",
            "error_code",
            "error_data",
            "error_msg",
            "key",
            "message_id",
            "performative",
            "target",
        )

    def __init__(
        self,
        performative: Performative,
        dialogue_reference: Tuple[str, str] = ("", ""),
        message_id: int = 1,
        target: int = 0,
        **kwargs: Any,
    ):
        """
        Initialise an instance of FileStorageMessage.

        :param message_id: the message id.
        :param dialogue_reference: the dialogue reference.
        :param target: the message target.
        :param performative: the message performative.
        """
        super().__init__(
            dialogue_reference=dialogue_reference,
            message_id=message_id,
            target=target,
            performative=FileStorageMessage.Performative(performative),
            **kwargs,
        )

    @property
    def valid_performatives(self) -> Set[str]:
        """Get valid performatives."""
        return self._performatives

    @property
    def dialogue_reference(self) -> Tuple[str, str]:
        """Get the dialogue_reference of the message."""
        enforce(self.is_set("dialogue_reference"), "dialogue_reference is not set.")
        return cast(Tuple[str, str], self.get("dialogue_reference"))

    @property
    def message_id(self) -> int:
        """Get the message_id of the message."""
        enforce(self.is_set("message_id"), "message_id is not set.")
        return cast(int, self.get("message_id"))

    @property
    def performative(self) -> Performative:  # type: ignore # noqa: F821
        """Get the performative of the message."""
        enforce(self.is_set("performative"), "performative is not set.")
        return cast(FileStorageMessage.Performative, self.get("performative"))

    @property
    def target(self) -> int:
        """Get the target of the message."""
        enforce(self.is_set("target"), "target is not set.")
        return cast(int, self.get("target"))

    @property
    def access_url(self) -> str:
        """Get the 'access_url' content from the message."""
        enforce(self.is_set("access_url"), "'access_url' content is not set.")
        return cast(str, self.get("access_url"))

    @property
    def content(self) -> bytes:
        """Get the 'content' content from the message."""
        enforce(self.is_set("content"), "'content' content is not set.")
        return cast(bytes, self.get("content"))

    @property
    def error_code(self) -> CustomErrorCode:
        """Get the 'error_code' content from the message."""
        enforce(self.is_set("error_code"), "'error_code' content is not set.")
        return cast(CustomErrorCode, self.get("error_code"))

    @property
    def error_data(self) -> Dict[str, bytes]:
        """Get the 'error_data' content from the message."""
        enforce(self.is_set("error_data"), "'error_data' content is not set.")
        return cast(Dict[str, bytes], self.get("error_data"))

    @property
    def error_msg(self) -> str:
        """Get the 'error_msg' content from the message."""
        enforce(self.is_set("error_msg"), "'error_msg' content is not set.")
        return cast(str, self.get("error_msg"))

    @property
    def key(self) -> str:
        """Get the 'key' content from the message."""
        enforce(self.is_set("key"), "'key' content is not set.")
        return cast(str, self.get("key"))

    def _is_consistent(self) -> bool:
        """Check that the message follows the file_storage protocol."""
        try:
            enforce(
                isinstance(self.dialogue_reference, tuple),
                "Invalid type for 'dialogue_reference'. Expected 'tuple'. Found '{}'.".format(
                    type(self.dialogue_reference)
                ),
            )
            enforce(
                isinstance(self.dialogue_reference[0], str),
                "Invalid type for 'dialogue_reference[0]'. Expected 'str'. Found '{}'.".format(
                    type(self.dialogue_reference[0])
                ),
            )
            enforce(
                isinstance(self.dialogue_reference[1], str),
                "Invalid type for 'dialogue_reference[1]'. Expected 'str'. Found '{}'.".format(
                    type(self.dialogue_reference[1])
                ),
            )
            enforce(
                type(self.message_id) is int,
                "Invalid type for 'message_id'. Expected 'int'. Found '{}'.".format(
                    type(self.message_id)
                ),
            )
            enforce(
                type(self.target) is int,
                "Invalid type for 'target'. Expected 'int'. Found '{}'.".format(
                    type(self.target)
                ),
            )

            # Light Protocol Rule 2
            # Check correct performative
            enforce(
                isinstance(self.performative, FileStorageMessage.Performative),
                "Invalid 'performative'. Expected either of '{}'. Found '{}'.".format(
                    self.valid_performatives, self.performative
                ),
            )

            # Check correct contents
            actual_nb_of_contents = len(self._body) - DEFAULT_BODY_SIZE
            expected_nb_of_contents = 0
            if self.performative == FileStorageMessage.Performative.FILE_UPLOAD:
                expected_nb_of_contents = 2
                enforce(
                    isinstance(self.content, bytes),
                    "Invalid type for content 'content'. Expected 'bytes'. Found '{}'.".format(
                        type(self.content)
                    ),
                )
                enforce(
                    isinstance(self.key, str),
                    "Invalid type for content 'key'. Expected 'str'. Found '{}'.".format(
                        type(self.key)
                    ),
                )
            elif self.performative == FileStorageMessage.Performative.FILE_DOWNLOAD:
                expected_nb_of_contents = 2
                enforce(
                    isinstance(self.access_url, str),
                    "Invalid type for content 'access_url'. Expected 'str'. Found '{}'.".format(
                        type(self.access_url)
                    ),
                )
                enforce(
                    isinstance(self.content, bytes),
                    "Invalid type for content 'content'. Expected 'bytes'. Found '{}'.".format(
                        type(self.content)
                    ),
                )
            elif self.performative == FileStorageMessage.Performative.ERROR:
                expected_nb_of_contents = 3
                enforce(
                    isinstance(self.error_code, CustomErrorCode),
                    "Invalid type for content 'error_code'. Expected 'ErrorCode'. Found '{}'.".format(
                        type(self.error_code)
                    ),
                )
                enforce(
                    isinstance(self.error_msg, str),
                    "Invalid type for content 'error_msg'. Expected 'str'. Found '{}'.".format(
                        type(self.error_msg)
                    ),
                )
                enforce(
                    isinstance(self.error_data, dict),
                    "Invalid type for content 'error_data'. Expected 'dict'. Found '{}'.".format(
                        type(self.error_data)
                    ),
                )
                for key_of_error_data, value_of_error_data in self.error_data.items():
                    enforce(
                        isinstance(key_of_error_data, str),
                        "Invalid type for dictionary keys in content 'error_data'. Expected 'str'. Found '{}'.".format(
                            type(key_of_error_data)
                        ),
                    )
                    enforce(
                        isinstance(value_of_error_data, bytes),
                        "Invalid type for dictionary values in content 'error_data'. Expected 'bytes'. Found '{}'.".format(
                            type(value_of_error_data)
                        ),
                    )
            elif self.performative == FileStorageMessage.Performative.END:
                expected_nb_of_contents = 0

            # Check correct content count
            enforce(
                expected_nb_of_contents == actual_nb_of_contents,
                "Incorrect number of contents. Expected {}. Found {}".format(
                    expected_nb_of_contents, actual_nb_of_contents
                ),
            )

            # Light Protocol Rule 3
            if self.message_id == 1:
                enforce(
                    self.target == 0,
                    "Invalid 'target'. Expected 0 (because 'message_id' is 1). Found {}.".format(
                        self.target
                    ),
                )
        except (AEAEnforceError, ValueError, KeyError) as e:
            _default_logger.error(str(e))
            return False

        return True
