from luxtronik.datatypes import Base
from luxtronik.definitions import LuxtronikDefinitionsList
from luxtronik.cfi.vector import DataVectorConfig


###############################################################################
# Tests
###############################################################################

def_list = [
    {
        "index": 5,
        "count": 1,
        "names": ["field_5_bit1"],
        "bit_offset": 0,
        "bit_count": 1,
        "type": Base,
        "writeable": False,
    },
    {
        "index": 5,
        "count": 1,
        "names": ["field_5_bit2"],
        "bit_offset": 1,
        "bit_count": 3,
        "type": Base,
        "writeable": False,
    },
    {
        "index": 5,
        "count": 1,
        "names": ["field_5_all"],
        "type": Base,
        "writeable": False,
    },
    {
        "index": 7,
        "count": 2,
        "names": ["field_7"],
        "type": Base,
        "writeable": True,
    },
    {
        "index": 9,
        "count": 2,
        "names": ["field_9"],
        "type": Base,
        "writeable": True,
    }
]
TEST_DEFINITIONS = LuxtronikDefinitionsList(def_list, 'foo', 100, 'INT32')

FIELD_11_DICT = {
    "index": 11,
    "count": 1,
    "names": ["field_11"],
    "type": Base,
    "writeable": True,
}
FIELD_12_DICT = {
    "index": 12,
    "count": 1,
    "names": ["field_12"],
    "type": Base,
    "writeable": True,
}

class DataVectorTest(DataVectorConfig):
    name = 'foo'
    definitions = TEST_DEFINITIONS

class TestDataVector:

    def test_add(self):
        data_vector = DataVectorTest.empty()
        assert len(data_vector) == 0

        # In case the definitions are added after the creation
        data_vector.definitions.add(FIELD_11_DICT)
        data_vector.definitions.add(FIELD_12_DICT)

        # Add available index
        field = data_vector.add(11)
        assert len(data_vector) == 1
        assert 11 in data_vector
        assert field.name == 'field_11'

        # Add not available index (not existing)
        field = data_vector.add(13)
        assert 'field_6' not in data_vector
        assert field is None
        assert len(data_vector) == 1

        # Re-add available index
        field = data_vector.add(11)
        assert len(data_vector) == 1
        assert field.name == 'field_11'

        # Add available field
        field_12 = Base('field_12', False)
        field = data_vector.add(field_12)
        assert 12 in data_vector
        assert len(data_vector) == 2
        assert field == field_12

        # Re-add available field
        field = data_vector.add(field_12)
        assert field_12 in data_vector
        assert len(data_vector) == 2
        assert field == field_12
