"""Parse luxtronik Holdings."""

import logging
from typing import Final

from luxtronik.definitions import LuxtronikDefinitionsList
from luxtronik.definitions.holdings import (
    HOLDINGS_DEFINITIONS_LIST,
    HOLDINGS_OFFSET,
    HOLDINGS_DEFAULT_DATA_TYPE,
)

from luxtronik.shi.constants import HOLDINGS_FIELD_NAME
from luxtronik.shi.vector import DataVectorSmartHome


LOGGER = logging.getLogger(__name__)

HOLDINGS_DEFINITIONS: Final = LuxtronikDefinitionsList(
    HOLDINGS_DEFINITIONS_LIST,
    HOLDINGS_FIELD_NAME,
    HOLDINGS_OFFSET,
    HOLDINGS_DEFAULT_DATA_TYPE,
)

class Holdings(DataVectorSmartHome):
    """Class that holds holding fields."""

    logger = LOGGER
    name = HOLDINGS_FIELD_NAME
    definitions = HOLDINGS_DEFINITIONS

    @property
    def holdings(self):
        return self._data