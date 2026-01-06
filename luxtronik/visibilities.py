"""Parse luxtronik visibilities."""

import logging
from typing import Final

from luxtronik.definitions.visibilities import VISIBILITIES_DEFINITIONS_LIST, VISIBILITIES_OFFSET

from luxtronik.constants import VISIBILITIES_FIELD_NAME
from luxtronik.shi.definitions import LuxtronikDefinitionsList
from luxtronik.data_vector import DataVector


VISIBILITIES_DEFINITIONS: Final = LuxtronikDefinitionsList(
    VISIBILITIES_DEFINITIONS_LIST,
    VISIBILITIES_FIELD_NAME,
    VISIBILITIES_OFFSET
)

class Visibilities(DataVector):
    """Class that holds all visibilities."""

    logger = logging.getLogger("Luxtronik.Visibilities")
    name = VISIBILITIES_FIELD_NAME
    definitions = VISIBILITIES_DEFINITIONS

    def __init__(self):
        super().__init__()
        self._data = {d.index: d.create_field() for d in VISIBILITIES_DEFINITIONS}

    @property
    def visibilities(self):
        return self._data
