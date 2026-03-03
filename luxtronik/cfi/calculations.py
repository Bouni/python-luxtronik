"""Parse luxtronik calculations."""

import logging
from typing import Final

from luxtronik.definitions import LuxtronikDefinitionsList
from luxtronik.definitions.calculations import (
    CALCULATIONS_DEFINITIONS_LIST,
    CALCULATIONS_OFFSET,
    CALCULATIONS_DEFAULT_DATA_TYPE,
    CALCULATIONS_OUTDATED,
)

from luxtronik.cfi.constants import CALCULATIONS_FIELD_NAME
from luxtronik.cfi.vector import DataVectorConfig


LOGGER = logging.getLogger(__name__)

CALCULATIONS_DEFINITIONS: Final = LuxtronikDefinitionsList(
    CALCULATIONS_DEFINITIONS_LIST,
    CALCULATIONS_FIELD_NAME,
    CALCULATIONS_OFFSET,
    CALCULATIONS_DEFAULT_DATA_TYPE
)

class Calculations(DataVectorConfig):
    """Class that holds all calculations."""

    name = CALCULATIONS_FIELD_NAME
    definitions = CALCULATIONS_DEFINITIONS
    _outdated = CALCULATIONS_OUTDATED

    def get_firmware_version(self):
        """Get the firmware version as string."""
        return "".join([super(Calculations, self).get(i).value for i in range(81, 91)])

    def _get_firmware_version(self):
        """Get the firmware version as string like in previous versions."""
        return self.get_firmware_version().strip("\x00")
