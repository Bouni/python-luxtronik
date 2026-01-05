"""Parse luxtronik parameters."""

import logging
from typing import Final

from luxtronik.definitions.parameters import PARAMETERS_DEFINITIONS_LIST, PARAMETERS_OFFSET

from luxtronik.constants import PARAMETERS_FIELD_NAME
from luxtronik.shi.definitions import LuxtronikDefinitionsList
from luxtronik.data_vector import DataVector


PARAMETERS_DEFINITIONS: Final = LuxtronikDefinitionsList(
    PARAMETERS_DEFINITIONS_LIST,
    PARAMETERS_FIELD_NAME,
    PARAMETERS_OFFSET
)

class Parameters(DataVector):
    """Class that holds all parameters."""

    logger = logging.getLogger("Luxtronik.Parameters")
    name = PARAMETERS_FIELD_NAME
    definitions = PARAMETERS_DEFINITIONS

    def __init__(self, safe=True):
        """Initialize parameters class."""
        super().__init__()
        self.safe = safe
        self.queue = {}
        self._data = {d.index: d.create_field() for d in PARAMETERS_DEFINITIONS}

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
                    self.logger.error("Value '%s' for Parameter '%s' not valid!", value, parameter.name)
            else:
                self.logger.warning("Parameter '%s' not safe for writing!", parameter.name)
        else:
            self.logger.warning("Parameter '%s' not found", target)
