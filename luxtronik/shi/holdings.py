"""Parse luxtronik Holdings."""

import logging
from typing import Final

from luxtronik.definitions.holdings import HOLDINGS_DEFINITIONS_LIST, HOLDINGS_OFFSET

from luxtronik.shi.constants import HOLDINGS_FIELD_NAME
from luxtronik.shi.definitions import LuxtronikDefinitionsList
from luxtronik.shi.vector import DataVectorSmartHome


HOLDINGS_DEFINITIONS: Final = LuxtronikDefinitionsList(
    HOLDINGS_DEFINITIONS_LIST,
    HOLDINGS_FIELD_NAME,
    HOLDINGS_OFFSET
)

class Holdings(DataVectorSmartHome):
    """Class that holds holding fields."""

    logger = logging.getLogger("Luxtronik.Holdings")
    name = HOLDINGS_FIELD_NAME
    definitions = HOLDINGS_DEFINITIONS