"""Parse luxtronik Inputs."""

import logging
from typing import Final

from luxtronik.definitions import LuxtronikDefinitionsList
from luxtronik.definitions.inputs import (
    INPUTS_DEFINITIONS_LIST,
    INPUTS_OFFSET,
    INPUTS_DEFAULT_DATA_TYPE,
)

from luxtronik.shi.constants import INPUTS_FIELD_NAME
from luxtronik.shi.vector import DataVectorSmartHome


LOGGER = logging.getLogger(__name__)

INPUTS_DEFINITIONS: Final = LuxtronikDefinitionsList(
    INPUTS_DEFINITIONS_LIST,
    INPUTS_FIELD_NAME,
    INPUTS_OFFSET,
    INPUTS_DEFAULT_DATA_TYPE,
)

class Inputs(DataVectorSmartHome):
    """Class that holds input fields."""

    name = INPUTS_FIELD_NAME
    definitions = INPUTS_DEFINITIONS

    @property
    def inputs(self):
        return self._data