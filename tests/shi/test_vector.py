
from luxtronik.datatypes import Base, Unknown
from luxtronik.shi.common import parse_version
from luxtronik.shi.vector import DataVectorSmartHome
from luxtronik.shi.definitions import LuxtronikDefinitionsList


###############################################################################
# Tests
###############################################################################

def_list = [
    {
        "index": 5,
        "count": 1,
        "names": ["field_5"],
        "type": Base,
        "writeable": False,
        "since": "1.1",
        "until": "1.2",
    },
    {
        "index": 7,
        "count": 2,
        "names": ["field_7"],
        "type": Base,
        "writeable": True,
        "since": "3.1",
    },
    {
        "index": 9,
        "count": 1,
        "names": ["field_9a"],
        "type": Base,
        "writeable": True,
        "until": "1.3",
    },
    {
        "index": 9,
        "count": 2,
        "names": ["field_9"],
        "type": Base,
        "writeable": True,
        "until": "3.3",
    },
    {
        "index": -1,
        "count": 1,
        "names": ["field_invalid"],
        "type": Base,
        "writeable": True,
        "until": "3.3",
    },
]
TEST_DEFINITIONS = LuxtronikDefinitionsList(def_list, 'foo', 100)

class DataVectorTest(DataVectorSmartHome):
    name = 'foo'
    definitions = TEST_DEFINITIONS

class TestDataVector:

    def test_create(self):
        # create unknown field
        field = DataVectorTest.create_unknown_field(10)
        assert field.name == 'unknown_foo_10'
        assert not field.writeable
        assert type(field) is Unknown

        # create invalid field (not available)
        field = DataVectorTest.create_any_field('field_invalid')
        assert field is None

        # create available field
        field = DataVectorTest.create_any_field(7)
        assert field.name == 'field_7'
        assert field.writeable
        assert type(field) is Base

        # create not available field
        field = DataVectorTest.create_any_field('BAR')
        assert field is None

        # create versioned data vector
        data_vector = DataVectorTest(parse_version("1.2"))
        assert data_vector.version == (1, 2, 0, 0)
        assert len(data_vector) == 3

        # create version-dependent field
        field = data_vector.create_field(5)
        assert field.name == 'field_5'
        assert not field.writeable
        assert type(field) is Base

        # create not available field (not available)
        field = data_vector.create_field(6)
        assert field is None

        # create not available field (version invalid)
        field = data_vector.create_field(7)
        assert field is None

        # create another version-dependent field
        field = data_vector.create_field(9)
        assert field.name == 'field_9'
        assert field.writeable
        assert type(field) is Base

        # create index-overloaded version-dependent field
        field = data_vector.create_field('field_9a')
        assert field.name == 'field_9a'
        assert field.writeable
        assert type(field) is Base

        # create versioned data vector
        data_vector = DataVectorTest(parse_version("3.0"))
        assert data_vector.version == (3, 0, 0, 0)
        assert len(data_vector) == 1

        # create not available field (invalid version)
        field = data_vector.create_field(5)
        assert field is None

        # create not available field (not available)
        field = data_vector.create_field(6)
        assert field is None

        # create not available field (invalid version)
        field = data_vector.create_field(7)
        assert field is None

        # create version-dependent field
        field = data_vector.create_field(9)
        assert field.name == 'field_9'
        assert field.writeable
        assert type(field) is Base

        # create invalid field (not available)
        field = data_vector.create_field('field_invalid')
        assert field is None

        # create empty data vector
        data_vector = DataVectorTest.empty(parse_version("3.0"))
        assert data_vector.version == (3, 0, 0, 0)
        assert len(data_vector) == 0

        # create not available field (not available)
        field = data_vector.create_field(9)
        assert field is None

    def test_add(self):
        data_vector = DataVectorTest.empty(parse_version("1.1.2"))
        assert len(data_vector) == 0

        # Add available index
        field = data_vector.add(5)
        assert len(data_vector) == 1
        assert 5 in data_vector
        assert field.name == 'field_5'

        # Add not available index (not existing)
        field = data_vector.add(6)
        assert 'field_6' not in data_vector
        assert field is None
        assert len(data_vector) == 1

        # Add not available index (invalid version)
        field = data_vector.add(7)
        assert 7 not in data_vector
        assert field is None
        assert len(data_vector) == 1

        # Re-add available index
        field = data_vector.add(5)
        assert len(data_vector) == 1
        assert field.name == 'field_5'

        # Add available field
        field_9 = Base('field_9', False)
        field = data_vector.add(field_9)
        assert 9 in data_vector
        assert len(data_vector) == 2
        assert field == field_9

        # Re-add available field
        field = data_vector.add(field_9)
        assert field_9 in data_vector
        assert len(data_vector) == 2
        assert field == field_9

        # Add available field with same name
        field_9_2 = Base('field_9', False)
        field = data_vector.add(field_9_2)
        assert field_9_2 not in data_vector
        assert len(data_vector) == 2
        assert field is field_9

        # Add available definition
        def_9a = data_vector.definitions['field_9a']
        field = data_vector.add(def_9a)
        assert def_9a in data_vector
        assert len(data_vector) == 3
        assert field.name == 'field_9a'

        # Get via index (last added)
        field = data_vector.get(9)
        assert field.name == 'field_9a'

        # Get via name
        field = data_vector.get('field_9')
        assert field == field_9

        # Get via definition
        field = data_vector.get(def_9a)
        assert field.name == 'field_9a'

        # Get via None
        field = data_vector.get(None)
        assert field is None

        # Get via invalid name
        field = data_vector.get('field_10')
        assert field is None

        # Get via invalid index
        field = data_vector.get(2)
        assert field is None

    def test_iter(self):
        data_vector = DataVectorTest.empty(parse_version("1.1.2"))
        data_vector.add('field_9a')
        data_vector.add(5)
        data_vector.add(9)

        for index, definition in enumerate(data_vector):
            if index == 0:
                assert definition.index == 5
                assert definition.name == 'field_5'
            if index == 1:
                assert definition.index == 9
                assert definition.name == 'field_9a'
            if index == 2:
                assert definition.index == 9
                assert definition.name == 'field_9'

        for index, field in enumerate(data_vector.values()):
            if index == 0:
                assert field.name == 'field_5'
            if index == 1:
                assert field.name == 'field_9a'
            if index == 2:
                assert field.name == 'field_9'

        for index, (definition, field) in enumerate(data_vector.items()):
            if index == 0:
                assert definition.index == 5
                assert definition.name == 'field_5'
                assert field.name == 'field_5'
            if index == 1:
                assert definition.index == 9
                assert definition.name == 'field_9a'
                assert field.name == 'field_9a'
            if index == 2:
                assert definition.index == 9
                assert definition.name == 'field_9'
                assert field.name == 'field_9'

    def test_set(self):
        data_vector = DataVectorTest(parse_version("1.1.2"))
        field_5 = data_vector[5]
        field_9 = data_vector[9]

        # set via property (writeable)
        data_vector['field_9'] = [2, 8]
        assert field_5.value is None
        assert field_9.value == [2, 8]

        # set via method (non-writeable)
        data_vector.set(5, 1)
        assert field_5.value == 1
        assert field_9.value == [2, 8]

        # set via field
        field_5.value = [4, 3]
        field_9.value = 6
        assert field_5.value == [4, 3]
        assert field_9.value == 6

    def test_parse(self):
        data_vector = DataVectorTest(parse_version("1.1.2"))
        field_5 = data_vector[5]
        field_9 = data_vector[9]
        field_9a = data_vector['field_9a']

        # not enough data
        data = [1]
        data_vector.parse(data)
        assert field_5.value is None
        assert field_9.value is None
        assert field_9a.value is None

        # data only for field 5
        data = [1, 2, 3, 4, 5, 6, 7]
        data_vector.parse(data)
        assert field_5.value == 6
        assert field_9.value is None
        assert field_9a.value is None

        # data for all fields
        data = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2]
        data_vector.parse(data)
        assert field_5.value == 4
        assert field_9.value == [0, -1]
        assert field_9a.value == 0

    def test_alias(self):
        TEST_DEFINITIONS.register_alias('field_9a', 10)
        data_vector = DataVectorTest(parse_version("1.1.2"))

        # global alias
        def_9a = TEST_DEFINITIONS[10]
        field_9a = data_vector[10]
        assert def_9a is not None
        assert field_9a is not None
        assert field_9a.name == 'field_9a'

        # local alias
        data_vector.register_alias(5, 6)
        def_5 = TEST_DEFINITIONS[6]
        field_5 = data_vector[6]
        assert def_5 is None
        assert field_5 is not None
        assert field_5.name == 'field_5'

        # alias of alias
        data_vector.register_alias(6, 7)
        field_5 = data_vector[7]
        assert field_5 is not None
        assert field_5.name == 'field_5'

        # alias of field
        data_vector.register_alias(field_9a, 11)
        field_9a = data_vector[11]
        assert field_9a is not None
        assert field_9a.name == 'field_9a'

        # alias of field
        field = data_vector.register_alias(2, 7)
        assert field is None

        # alias 7 still valid
        field_5 = data_vector[7]
        assert field_5 is not None
        assert field_5.name == 'field_5'

    def test_global_alias(self):
        data_vector = DataVectorTest(parse_version("1.1.2"))

        # persistent alias
        def_9a = TEST_DEFINITIONS[10]
        field_9a = data_vector[10]
        assert def_9a is not None
        assert field_9a is not None
        assert field_9a.name == 'field_9a'

    def test_version_none(self):
        data_vector = DataVectorTest.empty(None)
        assert len(data_vector) == 0

        data_vector.add(5)
        assert len(data_vector) == 1
        data_vector.add(7)
        assert len(data_vector) == 2
        data_vector.add(9)
        assert len(data_vector) == 3
        data_vector.add("field_invalid")
        assert len(data_vector) == 3
        data_vector.add(10) # field_9a alias
        assert len(data_vector) == 4
