"""Parse luxtronik parameters."""

import logging
from typing import Final

from luxtronik.definitions import LuxtronikDefinitionsList
from luxtronik.definitions.parameters import (
    PARAMETERS_DEFINITIONS_LIST,
    PARAMETERS_OFFSET,
    PARAMETERS_DEFAULT_DATA_TYPE,
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

    def __init__(self, safe=True):
        """Initialize parameters class."""
        super().__init__()
        self.safe = safe
        for d in PARAMETERS_DEFINITIONS:
            self._data.add(d, d.create_field())

    @property
    def parameters(self):
        return self._data
