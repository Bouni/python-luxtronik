"""Parse luxtronik parameters."""

import logging
from typing import Final

from luxtronik.definitions import LuxtronikDefinitionsList
from luxtronik.definitions.parameters import (
    PARAMETERS_DEFINITIONS_LIST,
    PARAMETERS_OFFSET,
    PARAMETERS_DEFAULT_DATA_TYPE,
    PARAMETERS_OUTDATED,
)

from luxtronik.cfi.constants import PARAMETERS_FIELD_NAME
from luxtronik.data_vector import DataVector


LOGGER = logging.getLogger(__name__)

PARAMETERS_DEFINITIONS: Final = LuxtronikDefinitionsList(
    PARAMETERS_DEFINITIONS_LIST,
    PARAMETERS_FIELD_NAME,
    PARAMETERS_OFFSET,
    PARAMETERS_DEFAULT_DATA_TYPE
)

class Parameters(DataVector):
    """Class that holds all parameters."""

    name = PARAMETERS_FIELD_NAME
    definitions = PARAMETERS_DEFINITIONS
    _outdated = PARAMETERS_OUTDATED

    def __init__(self, safe=True):
        """Initialize parameters class."""
        super().__init__()
        self.safe = safe
        self.queue = {}
        for d in PARAMETERS_DEFINITIONS:
            self._data.add(d, d.create_field())

    @property
    def parameters(self):
        return self._data

    def set(self, target, value):
        """Set parameter to new value."""
        index, parameter = self._lookup(target, with_index=True)
        if index is not None:
            if parameter.writeable or not self.safe:
                raw = parameter.to_heatpump(value)
                if isinstance(raw, int):
                    self.queue[index] = raw
                else:
                    LOGGER.error("Value '%s' for Parameter '%s' not valid!", value, parameter.name)
            else:
                LOGGER.warning("Parameter '%s' not safe for writing!", parameter.name)
        else:
            LOGGER.warning("Parameter '%s' not found", target)
