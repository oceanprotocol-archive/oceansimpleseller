from typing import Any, Optional, cast

from aea.helpers.search.models import Description
from aea.skills.base import Behaviour, Envelope
from aea.skills.behaviours import TickerBehaviour

from packages.eightballer.protocols.file_storage.message import \
    FileStorageMessage
from packages.eightballer.protocols.ocean.dialogues import (OceanDialogue,
                                                            OceanDialogues)
from packages.eightballer.protocols.ocean.message import OceanMessage
from packages.eightballer.skills.ocean_seller import PUBLIC_ID as SENDER_ID
from packages.eightballer.skills.ocean_seller.dialogues import (
    LedgerApiDialogues, OefSearchDialogues)
from packages.eightballer.skills.ocean_seller.strategy import GenericStrategy
from packages.fetchai.connections.ledger.base import \
    CONNECTION_ID as LEDGER_CONNECTION_PUBLIC_ID
from packages.fetchai.protocols.ledger_api.message import LedgerApiMessage
from packages.fetchai.protocols.oef_search.message import OefSearchMessage

DEFAULT_SERVICES_INTERVAL = 60.0
DEFAULT_MAX_SOEF_REGISTRATION_RETRIES = 5
LEDGER_API_ADDRESS = str(LEDGER_CONNECTION_PUBLIC_ID)


class GenericServiceRegistrationBehaviour(TickerBehaviour):
    """This class implements a behaviour."""

    def __init__(self, **kwargs: Any):
        """Initialise the behaviour."""
        services_interval = kwargs.pop(
            "services_interval", DEFAULT_SERVICES_INTERVAL
        )  # type: int
        self._max_soef_registration_retries = kwargs.pop(
            "max_soef_registration_retries", DEFAULT_MAX_SOEF_REGISTRATION_RETRIES
        )  # type: int
        super().__init__(tick_interval=services_interval, **kwargs)

        self.failed_registration_msg = None  # type: Optional[OefSearchMessage]
        self._nb_retries = 0

    def setup(self) -> None:
        """Implement the setup."""
        strategy = cast(GenericStrategy, self.context.strategy)
        if strategy.is_ledger_tx:
            ledger_api_dialogues = cast(
                LedgerApiDialogues, self.context.ledger_api_dialogues
            )
            ledger_api_msg, _ = ledger_api_dialogues.create(
                counterparty=LEDGER_API_ADDRESS,
                performative=LedgerApiMessage.Performative.GET_BALANCE,
                ledger_id=strategy.ledger_id,
                address=cast(str, self.context.agent_addresses.get(strategy.ledger_id)),
            )
            self.context.outbox.put_message(message=ledger_api_msg)
        self._registered = False

    def act(self) -> None:
        """Implement the act."""
        strategy = cast(GenericStrategy, self.context.strategy)
        if not strategy.is_seller_active:
            return
        if self._registered == False:
            self._register_agent()
            self._registered = True
            return
        self._retry_failed_registration()

    def teardown(self) -> None:
        """Implement the task teardown."""
        self._unregister_service()
        self._unregister_agent()

    def _retry_failed_registration(self) -> None:
        """Retry a failed registration."""
        if self.failed_registration_msg is not None:
            self._nb_retries += 1
            if self._nb_retries > self._max_soef_registration_retries:
                self.context.is_active = False
                return

            oef_search_dialogues = cast(
                OefSearchDialogues, self.context.oef_search_dialogues
            )
            oef_search_msg, _ = oef_search_dialogues.create(
                counterparty=self.failed_registration_msg.to,
                performative=self.failed_registration_msg.performative,
                service_description=self.failed_registration_msg.service_description,
            )
            self.context.outbox.put_message(message=oef_search_msg)
            self.context.logger.info(
                f"Retrying registration on SOEF. Retry {self._nb_retries} out of {self._max_soef_registration_retries}."
            )

            self.failed_registration_msg = None

    def _register(self, description: Description, logger_msg: str) -> None:
        """
        Register something on the SOEF.

        :param description: the description of what is being registered
        :param logger_msg: the logger message to print after the registration
        """
        oef_search_dialogues = cast(
            OefSearchDialogues, self.context.oef_search_dialogues
        )
        oef_search_msg, _ = oef_search_dialogues.create(
            counterparty=self.context.search_service_address,
            performative=OefSearchMessage.Performative.REGISTER_SERVICE,
            service_description=description,
        )
        self.context.outbox.put_message(message=oef_search_msg)
        self.context.logger.info(logger_msg)

    def _register_agent(self) -> None:
        """Register the agent's location."""
        strategy = cast(GenericStrategy, self.context.strategy)
        description = strategy.get_location_description()
        self._register(description, "registering agent on SOEF.")

    def register_service(self) -> None:
        """Register the agent's service."""
        strategy = cast(GenericStrategy, self.context.strategy)
        description = strategy.get_register_service_description()
        self._register(description, "registering agent's service on the SOEF.")

    def register_genus(self) -> None:
        """Register the agent's personality genus."""
        strategy = cast(GenericStrategy, self.context.strategy)
        description = strategy.get_register_personality_description()
        self._register(
            description, "registering agent's personality genus on the SOEF."
        )

    def register_classification(self) -> None:
        """Register the agent's personality classification."""
        strategy = cast(GenericStrategy, self.context.strategy)
        description = strategy.get_register_classification_description()
        self._register(
            description, "registering agent's personality classification on the SOEF."
        )

    def _unregister_service(self) -> None:
        """Unregister service from the SOEF."""
        strategy = cast(GenericStrategy, self.context.strategy)
        description = strategy.get_unregister_service_description()
        oef_search_dialogues = cast(
            OefSearchDialogues, self.context.oef_search_dialogues
        )
        oef_search_msg, _ = oef_search_dialogues.create(
            counterparty=self.context.search_service_address,
            performative=OefSearchMessage.Performative.UNREGISTER_SERVICE,
            service_description=description,
        )
        self.context.outbox.put_message(message=oef_search_msg)
        self.context.logger.info("unregistering service from SOEF.")

    def _unregister_agent(self) -> None:
        """Unregister agent from the SOEF."""
        strategy = cast(GenericStrategy, self.context.strategy)
        description = strategy.get_location_description()
        oef_search_dialogues = cast(
            OefSearchDialogues, self.context.oef_search_dialogues
        )
        oef_search_msg, _ = oef_search_dialogues.create(
            counterparty=self.context.search_service_address,
            performative=OefSearchMessage.Performative.UNREGISTER_SERVICE,
            service_description=description,
        )
        self.context.outbox.put_message(message=oef_search_msg)
        self.context.logger.info("unregistering agent from SOEF.")


class OceanBehaviourBase(Behaviour):
    """This class scaffolds a behaviour."""

    def setup(self) -> None:
        """Implement the setup."""
        self.log = self.context.logger

    def teardown(self) -> None:
        """Implement the task teardown."""
        self.log.debug(f"Tearing down the behaviour")


class OceanC2DBehaviour(OceanBehaviourBase):
    def act(self) -> None:
        """Implement the act."""
        strategy = cast(GenericStrategy, self.context.strategy)

        if strategy.is_in_flight or not strategy.is_d2c_active:
            return

        if (
            not strategy.is_data_to_compute_deployed
            and strategy.data_to_compute_address == {}
        ):
            self.log.info(f"Initialising deploying the data_to_compute!!")
            self.__create_envelope(
                OceanMessage.Performative.DEPLOY_D2C, **strategy.data_to_compute_params
            )
            return

        if not strategy.is_algorithm_deployed and strategy.algorithm_address == {}:
            self.log.info(f"Initialising deploying the algorithm!")
            self.__create_envelope(
                OceanMessage.Performative.DEPLOY_ALGORITHM, **strategy.algorithm_params
            )
            return

        if (
            not strategy.is_data_permissioned
            and strategy.is_algorithm_deployed
            and strategy.is_data_to_compute_deployed
        ):
            self.log.info(f"permissioning the dataset to allow d 2 c !")
            self.__create_envelope(
                OceanMessage.Performative.PERMISSION_DATASET,
                **strategy.get_permission_request(),
            )
            return

        if (
            strategy.is_data_permissioned
            and strategy.is_algorithm_deployed
            and strategy.is_data_to_compute_deployed
            and not strategy.download_params.get("datapool_address", None)
        ):
            self.log.info(f"creating the datapool")
            self.__create_envelope(
                OceanMessage.Performative.CREATE_POOL,
                **strategy.get_create_pool_request(),
            )

            return
        if (
                strategy.is_data_permissioned
                and strategy.is_algorithm_deployed
                and strategy.is_data_to_compute_deployed
                and strategy.download_params.get("datapool_address", None)
                and not strategy.download_params.get("algpool_address", None)
        ):
            self.log.info(f"creating the algpool")
            self.__create_envelope(
                OceanMessage.Performative.CREATE_POOL,
                **strategy.get_create_pool_request(False),
            )

            return

        if (
            strategy.is_data_permissioned
            and strategy.is_algorithm_deployed
            and strategy.is_data_to_compute_deployed
            and strategy.is_pool_deployed
        ):
            self.log.info(f"Completed the c2d deployment.")
            strategy.is_d2c_active = False
            strategy.is_processing = False
            strategy.has_completed_d2c_job = True

    def __create_envelope(
        self, performative: OceanMessage.Performative, **kwargs
    ) -> None:
        strategy = cast(GenericStrategy, self.context.strategy)
        receiver_id = "eightballer/ocean:0.1.0"
        msg = OceanMessage(performative=performative, **kwargs)
        msg.sender = str(SENDER_ID)
        msg.to = receiver_id
        file_upload_envolope = Envelope(
            to=receiver_id, sender=str(SENDER_ID), message=msg
        )
        self.context.outbox.put(file_upload_envolope)
        strategy.is_in_flight = True


class OceanSellerBehaviour(Behaviour):
    def act(self):
        strategy = cast(GenericStrategy, self.context.strategy)

        if strategy.is_processing:
            return

        if strategy.upload_data and not strategy.has_uploaded_data:
            self.context.logger.info(f"uploading file. active")
            strategy.is_processing = True
            self.__upload_data()

        if not strategy.has_completed_d2c_job:
            self.context.logger.info(f"Setting D2C Behaviour to active")
            strategy.is_processing = True
            strategy.is_d2c_active = True
            return

        self.context.logger.info(f"Seller behaviour to active")
        strategy.is_processing = True
        strategy.is_seller_active = True

    def teardown(self):
        pass

    def setup(self):
        self.log = self.context.logger
        return

    def __upload_data(
        self,
    ) -> None:
        with open("../EXAMPLE_DATA.csv", "rb") as f:
            bytes = f.read()
            filename = "EXAMPLE_FILE"
            fileid = "EXAMPLE_ID"

        receiver_id = "eightballer/storj_file_transfer:0.1.0"
        msg = FileStorageMessage(
            performative=FileStorageMessage.Performative.FILE_UPLOAD,
            content=bytes,
            key=fileid,
            filename=filename,
        )
        msg.sender = str(SENDER_ID)
        msg.to = receiver_id
        file_upload_envolope = Envelope(
            to=receiver_id, sender=str(SENDER_ID), message=msg
        )
        self.context.outbox.put(file_upload_envolope)
