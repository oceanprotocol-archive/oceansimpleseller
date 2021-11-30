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

"""This module contains ocean's message definition."""

# pylint: disable=too-many-statements,too-many-locals,no-member,too-few-public-methods,too-many-branches,not-an-iterable,unidiomatic-typecheck,unsubscriptable-object
import logging
from typing import Any, Dict, Set, Tuple, cast

from aea.configurations.base import PublicId
from aea.exceptions import AEAEnforceError, enforce
from aea.protocols.base import Message

from packages.eightballer.protocols.ocean.custom_types import (
    ErrorCode as CustomErrorCode,
)


_default_logger = logging.getLogger("aea.packages.eightballer.protocols.ocean.message")

DEFAULT_BODY_SIZE = 4


class OceanMessage(Message):
    """A protocol for interacting with the ocean protocol."""

    protocol_id = PublicId.from_str("eightballer/ocean:0.1.0")
    protocol_specification_id = PublicId.from_str("eightballer/ocean:0.1.0")

    ErrorCode = CustomErrorCode

    class Performative(Message.Performative):
        """Performatives for the ocean protocol."""

        CREATE_POOL = "create_pool"
        D2C_JOB = "d2c_job"
        DEPLOY_ALGORITHM = "deploy_algorithm"
        DEPLOY_D2C = "deploy_d2c"
        DEPLOY_DATA_DOWNLOAD = "deploy_data_download"
        DEPLOYMENT_RECIEPT = "deployment_reciept"
        DOWNLOAD_JOB = "download_job"
        END = "end"
        ERROR = "error"
        PERMISSION_DATASET = "permission_dataset"
        POOL_DEPLOYMENT_RECIEPT = "pool_deployment_reciept"
        RESULTS = "results"

        def __str__(self) -> str:
            """Get the string representation."""
            return str(self.value)

    _performatives = {
        "create_pool",
        "d2c_job",
        "deploy_algorithm",
        "deploy_d2c",
        "deploy_data_download",
        "deployment_reciept",
        "download_job",
        "end",
        "error",
        "permission_dataset",
        "pool_deployment_reciept",
        "results",
    }
    __slots__: Tuple[str, ...] = tuple()

    class _SlotsCls:
        __slots__ = (
            "algo_did",
            "amount_to_mint",
            "asset_did",
            "author",
            "content",
            "data_did",
            "dataset_url",
            "datatoken_address",
            "datatoken_amt",
            "datatoken_contract_address",
            "date_created",
            "dialogue_reference",
            "did",
            "entrypoint",
            "error_code",
            "error_data",
            "error_msg",
            "files_url",
            "format",
            "image",
            "language",
            "license",
            "max_cost_ocean",
            "message_id",
            "name",
            "ocean_amt",
            "performative",
            "pool_address",
            "tag",
            "target",
            "token0_name",
            "token1_name",
            "type",
            "version",
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
        Initialise an instance of OceanMessage.

        :param message_id: the message id.
        :param dialogue_reference: the dialogue reference.
        :param target: the message target.
        :param performative: the message performative.
        """
        super().__init__(
            dialogue_reference=dialogue_reference,
            message_id=message_id,
            target=target,
            performative=OceanMessage.Performative(performative),
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
        return cast(OceanMessage.Performative, self.get("performative"))

    @property
    def target(self) -> int:
        """Get the target of the message."""
        enforce(self.is_set("target"), "target is not set.")
        return cast(int, self.get("target"))

    @property
    def algo_did(self) -> str:
        """Get the 'algo_did' content from the message."""
        enforce(self.is_set("algo_did"), "'algo_did' content is not set.")
        return cast(str, self.get("algo_did"))

    @property
    def amount_to_mint(self) -> int:
        """Get the 'amount_to_mint' content from the message."""
        enforce(self.is_set("amount_to_mint"), "'amount_to_mint' content is not set.")
        return cast(int, self.get("amount_to_mint"))

    @property
    def asset_did(self) -> str:
        """Get the 'asset_did' content from the message."""
        enforce(self.is_set("asset_did"), "'asset_did' content is not set.")
        return cast(str, self.get("asset_did"))

    @property
    def author(self) -> str:
        """Get the 'author' content from the message."""
        enforce(self.is_set("author"), "'author' content is not set.")
        return cast(str, self.get("author"))

    @property
    def content(self) -> bytes:
        """Get the 'content' content from the message."""
        enforce(self.is_set("content"), "'content' content is not set.")
        return cast(bytes, self.get("content"))

    @property
    def data_did(self) -> str:
        """Get the 'data_did' content from the message."""
        enforce(self.is_set("data_did"), "'data_did' content is not set.")
        return cast(str, self.get("data_did"))

    @property
    def dataset_url(self) -> str:
        """Get the 'dataset_url' content from the message."""
        enforce(self.is_set("dataset_url"), "'dataset_url' content is not set.")
        return cast(str, self.get("dataset_url"))

    @property
    def datatoken_address(self) -> str:
        """Get the 'datatoken_address' content from the message."""
        enforce(
            self.is_set("datatoken_address"), "'datatoken_address' content is not set."
        )
        return cast(str, self.get("datatoken_address"))

    @property
    def datatoken_amt(self) -> int:
        """Get the 'datatoken_amt' content from the message."""
        enforce(self.is_set("datatoken_amt"), "'datatoken_amt' content is not set.")
        return cast(int, self.get("datatoken_amt"))

    @property
    def datatoken_contract_address(self) -> str:
        """Get the 'datatoken_contract_address' content from the message."""
        enforce(
            self.is_set("datatoken_contract_address"),
            "'datatoken_contract_address' content is not set.",
        )
        return cast(str, self.get("datatoken_contract_address"))

    @property
    def date_created(self) -> str:
        """Get the 'date_created' content from the message."""
        enforce(self.is_set("date_created"), "'date_created' content is not set.")
        return cast(str, self.get("date_created"))

    @property
    def did(self) -> str:
        """Get the 'did' content from the message."""
        enforce(self.is_set("did"), "'did' content is not set.")
        return cast(str, self.get("did"))

    @property
    def entrypoint(self) -> str:
        """Get the 'entrypoint' content from the message."""
        enforce(self.is_set("entrypoint"), "'entrypoint' content is not set.")
        return cast(str, self.get("entrypoint"))

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
    def files_url(self) -> str:
        """Get the 'files_url' content from the message."""
        enforce(self.is_set("files_url"), "'files_url' content is not set.")
        return cast(str, self.get("files_url"))

    @property
    def format(self) -> str:
        """Get the 'format' content from the message."""
        enforce(self.is_set("format"), "'format' content is not set.")
        return cast(str, self.get("format"))

    @property
    def image(self) -> str:
        """Get the 'image' content from the message."""
        enforce(self.is_set("image"), "'image' content is not set.")
        return cast(str, self.get("image"))

    @property
    def language(self) -> str:
        """Get the 'language' content from the message."""
        enforce(self.is_set("language"), "'language' content is not set.")
        return cast(str, self.get("language"))

    @property
    def license(self) -> str:
        """Get the 'license' content from the message."""
        enforce(self.is_set("license"), "'license' content is not set.")
        return cast(str, self.get("license"))

    @property
    def max_cost_ocean(self) -> int:
        """Get the 'max_cost_ocean' content from the message."""
        enforce(self.is_set("max_cost_ocean"), "'max_cost_ocean' content is not set.")
        return cast(int, self.get("max_cost_ocean"))

    @property
    def name(self) -> str:
        """Get the 'name' content from the message."""
        enforce(self.is_set("name"), "'name' content is not set.")
        return cast(str, self.get("name"))

    @property
    def ocean_amt(self) -> int:
        """Get the 'ocean_amt' content from the message."""
        enforce(self.is_set("ocean_amt"), "'ocean_amt' content is not set.")
        return cast(int, self.get("ocean_amt"))

    @property
    def pool_address(self) -> str:
        """Get the 'pool_address' content from the message."""
        enforce(self.is_set("pool_address"), "'pool_address' content is not set.")
        return cast(str, self.get("pool_address"))

    @property
    def tag(self) -> str:
        """Get the 'tag' content from the message."""
        enforce(self.is_set("tag"), "'tag' content is not set.")
        return cast(str, self.get("tag"))

    @property
    def token0_name(self) -> str:
        """Get the 'token0_name' content from the message."""
        enforce(self.is_set("token0_name"), "'token0_name' content is not set.")
        return cast(str, self.get("token0_name"))

    @property
    def token1_name(self) -> str:
        """Get the 'token1_name' content from the message."""
        enforce(self.is_set("token1_name"), "'token1_name' content is not set.")
        return cast(str, self.get("token1_name"))

    @property
    def type(self) -> str:
        """Get the 'type' content from the message."""
        enforce(self.is_set("type"), "'type' content is not set.")
        return cast(str, self.get("type"))

    @property
    def version(self) -> str:
        """Get the 'version' content from the message."""
        enforce(self.is_set("version"), "'version' content is not set.")
        return cast(str, self.get("version"))

    def _is_consistent(self) -> bool:
        """Check that the message follows the ocean protocol."""
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
                isinstance(self.performative, OceanMessage.Performative),
                "Invalid 'performative'. Expected either of '{}'. Found '{}'.".format(
                    self.valid_performatives, self.performative
                ),
            )

            # Check correct contents
            actual_nb_of_contents = len(self._body) - DEFAULT_BODY_SIZE
            expected_nb_of_contents = 0
            if self.performative == OceanMessage.Performative.DEPLOY_DATA_DOWNLOAD:
                expected_nb_of_contents = 8
                enforce(
                    isinstance(self.token0_name, str),
                    "Invalid type for content 'token0_name'. Expected 'str'. Found '{}'.".format(
                        type(self.token0_name)
                    ),
                )
                enforce(
                    isinstance(self.token1_name, str),
                    "Invalid type for content 'token1_name'. Expected 'str'. Found '{}'.".format(
                        type(self.token1_name)
                    ),
                )
                enforce(
                    isinstance(self.dataset_url, str),
                    "Invalid type for content 'dataset_url'. Expected 'str'. Found '{}'.".format(
                        type(self.dataset_url)
                    ),
                )
                enforce(
                    isinstance(self.name, str),
                    "Invalid type for content 'name'. Expected 'str'. Found '{}'.".format(
                        type(self.name)
                    ),
                )
                enforce(
                    isinstance(self.author, str),
                    "Invalid type for content 'author'. Expected 'str'. Found '{}'.".format(
                        type(self.author)
                    ),
                )
                enforce(
                    isinstance(self.date_created, str),
                    "Invalid type for content 'date_created'. Expected 'str'. Found '{}'.".format(
                        type(self.date_created)
                    ),
                )
                enforce(
                    isinstance(self.license, str),
                    "Invalid type for content 'license'. Expected 'str'. Found '{}'.".format(
                        type(self.license)
                    ),
                )
                enforce(
                    type(self.amount_to_mint) is int,
                    "Invalid type for content 'amount_to_mint'. Expected 'int'. Found '{}'.".format(
                        type(self.amount_to_mint)
                    ),
                )
            elif self.performative == OceanMessage.Performative.DEPLOY_D2C:
                expected_nb_of_contents = 8
                enforce(
                    isinstance(self.token0_name, str),
                    "Invalid type for content 'token0_name'. Expected 'str'. Found '{}'.".format(
                        type(self.token0_name)
                    ),
                )
                enforce(
                    isinstance(self.token1_name, str),
                    "Invalid type for content 'token1_name'. Expected 'str'. Found '{}'.".format(
                        type(self.token1_name)
                    ),
                )
                enforce(
                    isinstance(self.dataset_url, str),
                    "Invalid type for content 'dataset_url'. Expected 'str'. Found '{}'.".format(
                        type(self.dataset_url)
                    ),
                )
                enforce(
                    isinstance(self.name, str),
                    "Invalid type for content 'name'. Expected 'str'. Found '{}'.".format(
                        type(self.name)
                    ),
                )
                enforce(
                    isinstance(self.author, str),
                    "Invalid type for content 'author'. Expected 'str'. Found '{}'.".format(
                        type(self.author)
                    ),
                )
                enforce(
                    isinstance(self.date_created, str),
                    "Invalid type for content 'date_created'. Expected 'str'. Found '{}'.".format(
                        type(self.date_created)
                    ),
                )
                enforce(
                    isinstance(self.license, str),
                    "Invalid type for content 'license'. Expected 'str'. Found '{}'.".format(
                        type(self.license)
                    ),
                )
                enforce(
                    type(self.amount_to_mint) is int,
                    "Invalid type for content 'amount_to_mint'. Expected 'int'. Found '{}'.".format(
                        type(self.amount_to_mint)
                    ),
                )
            elif self.performative == OceanMessage.Performative.DEPLOY_ALGORITHM:
                expected_nb_of_contents = 14
                enforce(
                    isinstance(self.token0_name, str),
                    "Invalid type for content 'token0_name'. Expected 'str'. Found '{}'.".format(
                        type(self.token0_name)
                    ),
                )
                enforce(
                    isinstance(self.token1_name, str),
                    "Invalid type for content 'token1_name'. Expected 'str'. Found '{}'.".format(
                        type(self.token1_name)
                    ),
                )
                enforce(
                    type(self.amount_to_mint) is int,
                    "Invalid type for content 'amount_to_mint'. Expected 'int'. Found '{}'.".format(
                        type(self.amount_to_mint)
                    ),
                )
                enforce(
                    isinstance(self.language, str),
                    "Invalid type for content 'language'. Expected 'str'. Found '{}'.".format(
                        type(self.language)
                    ),
                )
                enforce(
                    isinstance(self.format, str),
                    "Invalid type for content 'format'. Expected 'str'. Found '{}'.".format(
                        type(self.format)
                    ),
                )
                enforce(
                    isinstance(self.version, str),
                    "Invalid type for content 'version'. Expected 'str'. Found '{}'.".format(
                        type(self.version)
                    ),
                )
                enforce(
                    isinstance(self.entrypoint, str),
                    "Invalid type for content 'entrypoint'. Expected 'str'. Found '{}'.".format(
                        type(self.entrypoint)
                    ),
                )
                enforce(
                    isinstance(self.image, str),
                    "Invalid type for content 'image'. Expected 'str'. Found '{}'.".format(
                        type(self.image)
                    ),
                )
                enforce(
                    isinstance(self.tag, str),
                    "Invalid type for content 'tag'. Expected 'str'. Found '{}'.".format(
                        type(self.tag)
                    ),
                )
                enforce(
                    isinstance(self.files_url, str),
                    "Invalid type for content 'files_url'. Expected 'str'. Found '{}'.".format(
                        type(self.files_url)
                    ),
                )
                enforce(
                    isinstance(self.name, str),
                    "Invalid type for content 'name'. Expected 'str'. Found '{}'.".format(
                        type(self.name)
                    ),
                )
                enforce(
                    isinstance(self.author, str),
                    "Invalid type for content 'author'. Expected 'str'. Found '{}'.".format(
                        type(self.author)
                    ),
                )
                enforce(
                    isinstance(self.date_created, str),
                    "Invalid type for content 'date_created'. Expected 'str'. Found '{}'.".format(
                        type(self.date_created)
                    ),
                )
                enforce(
                    isinstance(self.license, str),
                    "Invalid type for content 'license'. Expected 'str'. Found '{}'.".format(
                        type(self.license)
                    ),
                )
            elif self.performative == OceanMessage.Performative.POOL_DEPLOYMENT_RECIEPT:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.pool_address, str),
                    "Invalid type for content 'pool_address'. Expected 'str'. Found '{}'.".format(
                        type(self.pool_address)
                    ),
                )
            elif self.performative == OceanMessage.Performative.DEPLOYMENT_RECIEPT:
                expected_nb_of_contents = 3
                enforce(
                    isinstance(self.type, str),
                    "Invalid type for content 'type'. Expected 'str'. Found '{}'.".format(
                        type(self.type)
                    ),
                )
                enforce(
                    isinstance(self.did, str),
                    "Invalid type for content 'did'. Expected 'str'. Found '{}'.".format(
                        type(self.did)
                    ),
                )
                enforce(
                    isinstance(self.datatoken_contract_address, str),
                    "Invalid type for content 'datatoken_contract_address'. Expected 'str'. Found '{}'.".format(
                        type(self.datatoken_contract_address)
                    ),
                )
            elif self.performative == OceanMessage.Performative.CREATE_POOL:
                expected_nb_of_contents = 3
                enforce(
                    isinstance(self.datatoken_address, str),
                    "Invalid type for content 'datatoken_address'. Expected 'str'. Found '{}'.".format(
                        type(self.datatoken_address)
                    ),
                )
                enforce(
                    type(self.datatoken_amt) is int,
                    "Invalid type for content 'datatoken_amt'. Expected 'int'. Found '{}'.".format(
                        type(self.datatoken_amt)
                    ),
                )
                enforce(
                    type(self.ocean_amt) is int,
                    "Invalid type for content 'ocean_amt'. Expected 'int'. Found '{}'.".format(
                        type(self.ocean_amt)
                    ),
                )
            elif self.performative == OceanMessage.Performative.DOWNLOAD_JOB:
                expected_nb_of_contents = 5
                enforce(
                    isinstance(self.datatoken_address, str),
                    "Invalid type for content 'datatoken_address'. Expected 'str'. Found '{}'.".format(
                        type(self.datatoken_address)
                    ),
                )
                enforce(
                    type(self.datatoken_amt) is int,
                    "Invalid type for content 'datatoken_amt'. Expected 'int'. Found '{}'.".format(
                        type(self.datatoken_amt)
                    ),
                )
                enforce(
                    type(self.max_cost_ocean) is int,
                    "Invalid type for content 'max_cost_ocean'. Expected 'int'. Found '{}'.".format(
                        type(self.max_cost_ocean)
                    ),
                )
                enforce(
                    isinstance(self.asset_did, str),
                    "Invalid type for content 'asset_did'. Expected 'str'. Found '{}'.".format(
                        type(self.asset_did)
                    ),
                )
                enforce(
                    isinstance(self.pool_address, str),
                    "Invalid type for content 'pool_address'. Expected 'str'. Found '{}'.".format(
                        type(self.pool_address)
                    ),
                )
            elif self.performative == OceanMessage.Performative.PERMISSION_DATASET:
                expected_nb_of_contents = 2
                enforce(
                    isinstance(self.algo_did, str),
                    "Invalid type for content 'algo_did'. Expected 'str'. Found '{}'.".format(
                        type(self.algo_did)
                    ),
                )
                enforce(
                    isinstance(self.data_did, str),
                    "Invalid type for content 'data_did'. Expected 'str'. Found '{}'.".format(
                        type(self.data_did)
                    ),
                )
            elif self.performative == OceanMessage.Performative.D2C_JOB:
                expected_nb_of_contents = 2
                enforce(
                    isinstance(self.data_did, str),
                    "Invalid type for content 'data_did'. Expected 'str'. Found '{}'.".format(
                        type(self.data_did)
                    ),
                )
                enforce(
                    isinstance(self.algo_did, str),
                    "Invalid type for content 'algo_did'. Expected 'str'. Found '{}'.".format(
                        type(self.algo_did)
                    ),
                )
            elif self.performative == OceanMessage.Performative.RESULTS:
                expected_nb_of_contents = 1
                enforce(
                    isinstance(self.content, bytes),
                    "Invalid type for content 'content'. Expected 'bytes'. Found '{}'.".format(
                        type(self.content)
                    ),
                )
            elif self.performative == OceanMessage.Performative.ERROR:
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
            elif self.performative == OceanMessage.Performative.END:
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
