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
import glob
import os
import pathlib
from typing import cast

from aea.mail.base import Envelope
from aea.skills.behaviours import TickerBehaviour
from packages.eightballer.skills.storj_file_uploader import \
    PUBLIC_ID as SENDER_ID
from packages.eightballer.skills.storj_file_uploader.dialogues import \
    DefaultDialogues
from packages.fetchai.protocols.default.message import DefaultMessage
from packages.eightballer.protocols.file_storage.message import FileStorageMessage
from hashlib import md5

from packages.eightballer.skills.storj_file_uploader.strategy import Strategy

class StorjFileUploadBehaviour(TickerBehaviour):
    """This class scaffolds a behaviour."""

    @property
    def uploaded_ids(self) -> list:
        """store uploaded file hashs"""
        cast(Strategy, self.context.strategy)
        return self._uploaded_ids

    def __init__(self, *args, **kwargs):
        self._upload_dir = kwargs.pop("upload_dir")
        self._uploaded_ids = kwargs.pop("uploaded_ids")
        super().__init__(*args, **kwargs)

    def setup(self) -> None:
        """Implement the setup."""
        self.log = self.context.logger.info
        self.log(f"setting up storj behaviour")

    def act(self) -> None:
        """Implement the act."""
        available_files = glob.glob(self._upload_dir)
        for file in available_files:
            file_bytes = open(file, "rb").read()
            id = md5(file_bytes).hexdigest()
            if id not in self._uploaded_ids:
                self.log(f"Not already uploaded file.. Uploading.")
                self.__create_envelope(file_bytes, id)
                self._uploaded_ids.append(id)
            else:
                continue

    def __create_envelope(self, bytes, filename) -> None:
        receiver_id = "eightballer/storj_file_transfer:0.1.0"
        self.log(f"Sender ID {SENDER_ID}")
        msg = FileStorageMessage(
            performative=FileStorageMessage.Performative.FILE_UPLOAD,
            content=bytes,
            key=filename
        )
        msg.sender = str(SENDER_ID)
        msg.to = receiver_id
        file_upload_envolope = Envelope(
            to=receiver_id, sender=str(SENDER_ID), message=msg
        )
        self.context.outbox.put(file_upload_envolope)

    def teardown(self) -> None:
        """Implement the task teardown."""
        self.log(f"Tearing down storj behaviour")
