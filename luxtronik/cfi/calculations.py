"""Parse luxtronik calculations."""

import logging
from typing import Final

from luxtronik.definitions import LuxtronikDefinitionsList
from luxtronik.definitions.calculations import CALCULATIONS_DEFINITIONS_LIST, CALCULATIONS_OFFSET

from luxtronik.cfi.constants import CALCULATIONS_FIELD_NAME
from luxtronik.data_vector import DataVector
from luxtronik.datatypes import Base


CALCULATIONS_DEFINITIONS: Final = LuxtronikDefinitionsList(
    CALCULATIONS_DEFINITIONS_LIST,
    CALCULATIONS_FIELD_NAME,
    CALCULATIONS_OFFSET
)

class Calculations(DataVector):
    """Class that holds all calculations."""

    logger = logging.getLogger("Luxtronik.Calculations")
    name = CALCULATIONS_FIELD_NAME
    definitions = CALCULATIONS_DEFINITIONS

    _obsolete = {
        "ID_WEB_SoftStand": "get_firmware_version()"
    }

    def __init__(self):
        super().__init__()
        self._data = {d.index: d.create_field() for d in CALCULATIONS_DEFINITIONS}

    @property
    def calculations(self):
        return self._data

    def get_firmware_version(self):
        """Get the firmware version as string."""
        return "".join([super(Calculations, self).get(i).value for i in range(81, 91)])

    def _get_firmware_version(self):
        """Get the firmware version as string like in previous versions."""
        return self.get_firmware_version().strip("\x00")

    def get(self, target):
        """Treats certain names specially. For all others, the function of the base class is called."""
        if target == "ID_WEB_SoftStand":
            self.logger.debug("The name 'ID_WEB_SoftStand' is obsolete! Use 'get_firmware_version()' instead.")
            entry = Base("ID_WEB_SoftStand")
            entry.raw = self._get_firmware_version()
            return entry
        else:
            return super().get(target)
