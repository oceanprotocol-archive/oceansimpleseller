import json
import uuid
from typing import Any, Dict, Optional, Tuple

from aea.common import Address
from aea.crypto.ledger_apis import LedgerApis
from aea.exceptions import enforce
from aea.helpers.search.generic import (AGENT_LOCATION_MODEL,
                                        AGENT_PERSONALITY_MODEL,
                                        AGENT_REMOVE_SERVICE_MODEL,
                                        AGENT_SET_SERVICE_MODEL,
                                        SIMPLE_SERVICE_MODEL)
from aea.helpers.search.models import Description, Location, Query
from aea.helpers.transaction.base import Terms
from aea.skills.base import Model

DEFAULT_IS_LEDGER_TX = True

DEFAULT_UNIT_PRICE = 4
DEFAULT_SERVICE_ID = "generic_service"

DEFAULT_LOCATION = {"longitude": 0.1270, "latitude": 51.5194}
DEFAULT_SERVICE_DATA = {"key": "seller_service", "value": "generic_service"}
DEFAULT_PERSONALITY_DATA = {"piece": "genus", "value": "data"}
DEFAULT_CLASSIFICATION = {"piece": "classification", "value": "seller"}

DEFAULT_HAS_DATA_SOURCE = False
DEFAULT_DATA_FOR_SALE = {
    "some_generic_data_key": "some_generic_data_value"
}  # type: Optional[Dict[str, Any]]


class GenericStrategy(Model):
    """This class defines a strategy for the agent."""

    _is_data_to_compute_deployed = False
    _is_data_to_compute_minted = False
    _is_data_to_compute_published = False

    _deployments = {}

    _is_fixed_rate_exchange_deployed = False

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
    _data_exchange_params = {}

    _is_d2c_active = False
    _is_download_active = False

    @property
    def is_d2c_active(self):
        return self._is_d2c_active

    @is_d2c_active.setter
    def is_d2c_active(self, value):
        self._is_d2c_active = value

    @property
    def is_seller_active(self):
        return self._is_seller_active

    @is_seller_active.setter
    def is_seller_active(self, value):
        self._is_seller_active = value

    @property
    def is_download_active(self):
        return self._is_download_active

    @is_download_active.setter
    def is_download_active(self, value):
        self._is_download_active = value

    @property
    def is_fixed_rate_exchange_deployed(self):
        return self._is_download_active

    @is_fixed_rate_exchange_deployed.setter
    def is_fixed_rate_exchange_deployed(self, value):
        self._is_fixed_rate_exchange_deployed = value

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
        return self._deployments["algorithm"]

    @algorithm_address.setter
    def algorithm_address(self, value):
        self._deployments["algorithm"] = value

    @property
    def data_to_compute_address(self):
        return self._deployments["data_to_compute"]

    @data_to_compute_address.setter
    def data_to_compute_address(self, value):
        self._deployments["data_to_compute"] = value

    @property
    def data_download_address(self):
        return self._deployments["data_download"]

    @data_download_address.setter
    def data_download_address(self, value):
        self._deployments["data_download"] = value

    @property
    def is_fixed_rate_exchange_deployed(self):
        return self._is_fixed_rate_exchange_deployed

    @is_fixed_rate_exchange_deployed.setter
    def is_fixed_rate_exchange_deployed(self, value):
        self._is_fixed_rate_exchange_deployed = value

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
    def data_exchange_params(self):
        return self._data_exchange_params

    @data_exchange_params.setter
    def data_exchange_params(self, value):
        self._data_exchange_params = value

    @property
    def download_params(self):
        return self._download_params

    @download_params.setter
    def download_params(self, value):
        self._download_params = value

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize the strategy of the agent.

        :param kwargs: keyword arguments
        """
        ledger_id = kwargs.pop("ledger_id", None)
        currency_id = kwargs.pop("currency_id", None)
        self._is_ledger_tx = kwargs.pop("is_ledger_tx", DEFAULT_IS_LEDGER_TX)

        self._unit_price = kwargs.pop("unit_price", DEFAULT_UNIT_PRICE)
        self._service_id = kwargs.pop("service_id", DEFAULT_SERVICE_ID)

        location = kwargs.pop("location", DEFAULT_LOCATION)
        self._agent_location = {
            "location": Location(
                latitude=location["latitude"], longitude=location["longitude"]
            )
        }
        self._set_personality_data = kwargs.pop(
            "personality_data", DEFAULT_PERSONALITY_DATA
        )
        enforce(
            len(self._set_personality_data) == 2
            and "piece" in self._set_personality_data
            and "value" in self._set_personality_data,
            "personality_data must contain keys `key` and `value`",
        )
        self._set_classification = kwargs.pop("classification", DEFAULT_CLASSIFICATION)
        enforce(
            len(self._set_classification) == 2
            and "piece" in self._set_classification
            and "value" in self._set_classification,
            "classification must contain keys `key` and `value`",
        )
        self._set_service_data = kwargs.pop("service_data", DEFAULT_SERVICE_DATA)
        enforce(
            len(self._set_service_data) == 2
            and "key" in self._set_service_data
            and "value" in self._set_service_data,
            "service_data must contain keys `key` and `value`",
        )
        self._remove_service_data = {"key": self._set_service_data["key"]}
        self._simple_service_data = {
            self._set_service_data["key"]: self._set_service_data["value"]
        }

        self._has_data_source = kwargs.pop("has_data_source", DEFAULT_HAS_DATA_SOURCE)
        data_for_sale_ordered = kwargs.pop("data_for_sale", DEFAULT_DATA_FOR_SALE)
        data_for_sale = {
            str(key): str(value) for key, value in data_for_sale_ordered.items()
        }

        self._data_to_compute_params = kwargs.pop("data_to_compute_params")
        self._algorithm_params = kwargs.pop("algorithm_params")
        self._download_params = kwargs.pop("download_params")
        self._data_exchange_params = kwargs.pop("data_exchange_params")
        self._deployments = kwargs.pop("deployments")

        self._is_seller_active = False
        self.upload_data = True
        self.has_uploaded_data = False

        super().__init__(**kwargs)
        self._ledger_id = (
            ledger_id if ledger_id is not None else self.context.default_ledger_id
        )
        if currency_id is None:
            currency_id = self.context.currency_denominations.get(self._ledger_id, None)
            enforce(
                currency_id is not None,
                f"Currency denomination for ledger_id={self._ledger_id} not specified.",
            )
        self._currency_id = currency_id
        enforce(
            self.context.agent_addresses.get(self._ledger_id, None) is not None,
            "Wallet does not contain cryptos for provided ledger id.",
        )
        self._data_for_sale = data_for_sale

    def setup(self):
        self.log = self.context.logger
        self.log.info(f"Initialised the strategy.")
        if self.data_to_compute_address != {}:
            self.is_data_to_compute_deployed = True
        if self.algorithm_address != {}:
            self.is_algorithm_deployed = True

        self.is_d2c_active = False
        self.is_download_active = False
        self.is_processing = False

    @property
    def data_for_sale(self) -> Dict[str, str]:
        """Get the data for sale."""
        return {
            "data": json.dumps(
                {
                    "algo_did": self.algorithm_address.get("did", None),
                    "data_did": self.data_to_compute_address.get("did", None),
                }
            )
        }
        if self._has_data_source:
            return self.collect_from_data_source()  # pragma: nocover
        return self._data_for_sale

    @property
    def ledger_id(self) -> str:
        """Get the ledger id."""
        return self._ledger_id

    @property
    def is_ledger_tx(self) -> bool:
        """Check whether or not tx are settled on a ledger."""
        return self._is_ledger_tx

    def get_location_description(self) -> Description:
        """
        Get the location description.

        :return: a description of the agent's location
        """
        description = Description(
            self._agent_location,
            data_model=AGENT_LOCATION_MODEL,
        )
        return description

    def get_register_service_description(self) -> Description:
        """
        Get the register service description.

        :return: a description of the offered services
        """
        description = Description(
            self._set_service_data,
            data_model=AGENT_SET_SERVICE_MODEL,
        )
        return description

    def get_register_personality_description(self) -> Description:
        """
        Get the register personality description.

        :return: a description of the personality
        """
        description = Description(
            self._set_personality_data,
            data_model=AGENT_PERSONALITY_MODEL,
        )
        return description

    def get_register_classification_description(self) -> Description:
        """
        Get the register classification description.

        :return: a description of the classification
        """
        description = Description(
            self._set_classification,
            data_model=AGENT_PERSONALITY_MODEL,
        )
        return description

    def get_service_description(self) -> Description:
        """
        Get the simple service description.

        :return: a description of the offered services
        """
        description = Description(
            self._simple_service_data,
            data_model=SIMPLE_SERVICE_MODEL,
        )
        return description

    def get_unregister_service_description(self) -> Description:
        """
        Get the unregister service description.

        :return: a description of the to be removed service
        """
        description = Description(
            self._remove_service_data,
            data_model=AGENT_REMOVE_SERVICE_MODEL,
        )
        return description

    def is_matching_supply(self, query: Query) -> bool:
        """
        Check if the query matches the supply.

        :param query: the query
        :return: bool indicating whether matches or not
        """
        return query.check(self.get_service_description())

    def generate_proposal_terms_and_data(  # pylint: disable=unused-argument
        self, query: Query, counterparty_address: Address
    ) -> Tuple[Description, Terms, Dict[str, str]]:
        """
        Generate a proposal matching the query.

        :param query: the query
        :param counterparty_address: the counterparty of the proposal.
        :return: a tuple of proposal, terms and the weather data
        """
        data_for_sale = self.data_for_sale
        sale_quantity = len(data_for_sale)
        seller_address = self.context.agent_addresses[self.ledger_id]
        total_price = sale_quantity * self._unit_price
        if self.is_ledger_tx:
            tx_nonce = LedgerApis.generate_tx_nonce(
                identifier=self.ledger_id,
                seller=seller_address,
                client=counterparty_address,
            )
        else:
            tx_nonce = uuid.uuid4().hex  # pragma: nocover
        proposal = Description(
            {
                "ledger_id": self.ledger_id,
                "price": total_price,
                "currency_id": self._currency_id,
                "service_id": self._service_id,
                "quantity": sale_quantity,
                "tx_nonce": tx_nonce,
            }
        )
        terms = Terms(
            ledger_id=self.ledger_id,
            sender_address=seller_address,
            counterparty_address=counterparty_address,
            amount_by_currency_id={self._currency_id: total_price},
            quantities_by_good_id={self._service_id: -sale_quantity},
            is_sender_payable_tx_fee=False,
            nonce=tx_nonce,
            fee_by_currency_id={self._currency_id: 0},
        )
        return proposal, terms, data_for_sale

    def collect_from_data_source(self) -> Dict[str, str]:
        """Implement the logic to communicate with the sensor."""
        raise NotImplementedError

    def get_permission_request(self):
        algo_did = self.algorithm_address.get("did", None)
        if algo_did is None:
            raise ValueError(
                "Agent does not have algo did! make sure it has been deployed."
            )
        data_did = self.data_to_compute_address.get("did", None)
        if data_did is None:
            raise ValueError(
                "Agent does not have data did! make sure it has been deployed."
            )
        return {"algo_did": algo_did, "data_did": data_did}

    def get_create_fixed_rate_exchange_request(self, is_data=True): # TODO: remove hardcoded values
        if is_data:
            data_did = self.data_to_compute_address.get("datatoken_contract_address", None)
        else:
            data_did = self.algorithm_address.get("datatoken_contract_address", None)

        if data_did is None:
            raise ValueError(
                "Agent does not have data did! make sure it has been deployed."
            )
        return {
            "datatoken_address": data_did,
            "datatoken_amt": 50,
            "ocean_amt": 1,
            "rate": 1
        }
