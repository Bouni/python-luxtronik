"""Parse luxtronik visibilities."""

import logging
from typing import Final

from luxtronik.definitions import LuxtronikDefinitionsList
from luxtronik.definitions.visibilities import (
    VISIBILITIES_DEFINITIONS_LIST,
    VISIBILITIES_OFFSET,
    VISIBILITIES_DEFAULT_DATA_TYPE,
)

from luxtronik.cfi.constants import VISIBILITIES_FIELD_NAME
from luxtronik.data_vector import DataVector


LOGGER = logging.getLogger(__name__)

VISIBILITIES_DEFINITIONS: Final = LuxtronikDefinitionsList(
    VISIBILITIES_DEFINITIONS_LIST,
    VISIBILITIES_FIELD_NAME,
    VISIBILITIES_OFFSET,
    VISIBILITIES_DEFAULT_DATA_TYPE,
)

class Visibilities(DataVector):
    """Class that holds all visibilities."""

    name = VISIBILITIES_FIELD_NAME
    definitions = VISIBILITIES_DEFINITIONS

    def __init__(self):
        super().__init__()
        for d in VISIBILITIES_DEFINITIONS:
            self._data.add(d, d.create_field())

    @property
    def visibilities(self):
        return self._data
