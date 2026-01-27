from luxtronik.datatypes import Base, Unknown
from luxtronik.definitions import (
    LuxtronikDefinition,
    LuxtronikDefinitionsDictionary,
    LuxtronikDefinitionsList,
)

###############################################################################
# Tests
###############################################################################

class TestDefinition:

    TEST_DATA = {
        'index': 4,
        'count': 3,
        'type': Base,
        'writeable': True,
        'names': ['test1', 'test2'],
        'datatype': 'INT16',
        'since': '1.1',
        'until': '3.16.7',
        'description': 'foo',
    }
    DEFAULT_DATA = LuxtronikDefinition.DEFAULT_DATA
    TEST_FIELD = Base('TestField', True)
    TEST_ARRAY = [13, 10, 14, 12, 18, 11, 16, 15, 17, 19]

    def test_init(self):
        definition = LuxtronikDefinition(self.TEST_DATA, 'Bar', 20)

        names = self.TEST_DATA['names']
        assert definition.index == self.TEST_DATA['index']
        assert definition.count == self.TEST_DATA['count']
        assert definition.field_type == self.TEST_DATA['type']
        assert definition.writeable == self.TEST_DATA['writeable']
        assert definition.names == names
        assert definition.name == names[0]
        assert definition.valid
        assert definition
        assert definition.type_name == 'bar'
        assert definition.offset == 20
        assert definition.addr == 20 + self.TEST_DATA['index']
        assert definition.num_bits == 16
        assert definition.aliases == []
        assert definition.since == (1, 1, 0, 0)
        assert definition.until == (3, 16, 7, 0)

        definition = LuxtronikDefinition({
            'index': 10,
            'names': []
        }, 'Bar', 20)
        assert definition.valid
        assert definition.index == 10
        assert definition.name == '_invalid_'
        assert not definition.writeable

    def test_init_unknown(self):
        definition = LuxtronikDefinition.unknown(2, 'Foo', 30)

        names = ['unknown_foo_2']
        assert definition.index == 2
        assert definition.count == self.DEFAULT_DATA['count']
        assert definition.field_type == self.DEFAULT_DATA['type']
        assert definition.writeable == self.DEFAULT_DATA['writeable']
        assert definition.names == names
        assert definition.name == names[0]
        assert definition.valid
        assert definition
        assert definition.type_name == 'foo'
        assert definition.offset == 30
        assert definition.addr == 30 + 2
        assert definition.aliases == []
        assert definition.since is None
        assert definition.until is None

    def test_init_invalid(self):
        # create invalid
        definition = LuxtronikDefinition.unknown(-3, '', 10)
        assert not definition.valid

        # trigger exception
        try:
            definition = LuxtronikDefinition.unknown(-3, '', 'foo')
            assert False
        except Exception:
            pass

    def test_create_field(self):
        # create from normal
        definition = LuxtronikDefinition(self.TEST_DATA, 'Bar', 0)
        field = definition.create_field()
        assert field.name == definition.name
        assert field.writeable == definition.writeable
        assert type(field) is Base

        # create from unknown
        definition = LuxtronikDefinition.unknown(2, 'Foo', 30)
        field = definition.create_field()
        assert field.name == 'unknown_foo_2'
        assert not field.writeable
        assert type(field) is Unknown

        # create from invalid
        definition = LuxtronikDefinition.unknown(-3, '', 10)
        field = definition.create_field()
        assert field is None

    def test_repr(self):
        definition = LuxtronikDefinition.unknown(2, 'Foo', 30)
        text = repr(definition)
        assert text


class TestDefinitionsDict:

    def test_add_get(self):
        def_dict = LuxtronikDefinitionsDictionary()
        assert len(def_dict._index_dict) == 0
        assert len(def_dict._name_dict) == 0

        # add unknown definition
        d1 = LuxtronikDefinition.unknown(1, 'def', 0)
        def_dict.add(d1)
        assert len(def_dict._index_dict) == 1
        assert len(def_dict._name_dict) == 1

        # get via index
        assert 1 in def_dict
        d_out = def_dict.get(1)
        assert d1 == d_out

        # get via name
        assert 'unknown_def_1' in def_dict
        d_out = def_dict['unknown_def_1']
        assert d1 == d_out

        # get non-existing
        assert 2 not in def_dict
        d_out = def_dict.get(2)
        assert d_out is None

        # get via index as string
        assert '1' in def_dict
        d_out = def_dict.get('1')
        assert d1 == d_out

        # add normal definition
        d2 = LuxtronikDefinition({'index': 2, 'names': ['foo', 'bar', '4']}, 'def', 0)
        def_dict.add(d2)
        assert len(def_dict._index_dict) == 2
        assert len(def_dict._name_dict) == 4

        # get via name
        assert 'FOO' in def_dict
        d_out = def_dict.get('FOO')
        assert d2 == d_out

        # get via alternative name
        assert 'Bar' in def_dict
        d_out = def_dict['Bar']
        assert d2 == d_out

        # get non-existing
        assert 'Barf' not in def_dict
        d_out = def_dict['Barf']
        assert d_out is None

        # '4' cannot be found as name
        assert 4 not in def_dict
        d_out = def_dict[4]
        assert d_out is None
        assert '4' not in def_dict
        d_out = def_dict['4']
        assert d_out is None

        # add unknown definition (covers previously added definition)
        d3 = LuxtronikDefinition.unknown(1, 'def', 0)
        def_dict.add(d3)
        assert len(def_dict._index_dict) == 2
        assert len(def_dict._name_dict) == 4

        # get via index
        assert 1 in def_dict
        d_out = def_dict.get(1)
        assert d3 == d_out

        # invalid float
        assert 1.3 not in def_dict
        d_out = def_dict.get(1.3)
        assert d_out is None

        # invalid list
        assert list() not in def_dict
        d_out = def_dict.get(list())
        assert d_out is None

    def test_alias(self):
        def_dict = LuxtronikDefinitionsDictionary()

        # add via "global"
        d1 = LuxtronikDefinition.unknown(1, 'def', 0)
        d1._aliases = [0xDEAD, 123456, 'Unknown_Def_2']
        def_dict.add(d1)
        assert len(def_dict._alias_dict) == 3

        # override via "global"
        d2 = LuxtronikDefinition.unknown(2, 'def', 0)
        d2._aliases = [123456]
        def_dict.add(d2, 'foo')
        assert len(def_dict._alias_dict) == 4

        # add nothing
        d_alias = def_dict.register_alias(d2, None)
        assert d_alias is None
        assert len(def_dict._alias_dict) == 4

        # add via method
        d_alias = def_dict.register_alias('UNKNOWN_DEF_1', 'abc')
        assert d_alias == d1
        assert len(def_dict._alias_dict) == 5

        # use a number as alias (which covers the original index)
        d_alias = def_dict.register_alias(2, 1)
        assert d_alias == d2
        assert len(def_dict._alias_dict) == 6

        # add nothing
        d_alias = def_dict.register_alias(3, 0xAFFE)
        assert d_alias is None
        assert len(def_dict._alias_dict) == 6

        # get via alias (which covers the original index)
        assert 1 in def_dict
        d_out = def_dict.get(1)
        assert d_out == d2

        # get via index
        assert 2 in def_dict
        d_out = def_dict.get(2)
        assert d_out == d2

        # get non-existing
        assert 3 not in def_dict
        d_out = def_dict.get(3)
        assert d_out is None

        # get via name
        assert 'unknown_def_1' in def_dict
        d_out = def_dict.get('unknown_def_1')
        assert d_out == d1

        # get via name
        assert 'foo' in def_dict
        d_out = def_dict.get('foo')
        assert d_out == d2

        # get via alias (which covers the original name)
        assert 'unknown_def_2' in def_dict
        d_out = def_dict.get('unknown_def_2')
        assert d_out == d1

        # get via string-alias
        assert 'abc' in def_dict
        d_out = def_dict.get('abc')
        assert d_out == d1

        # get via hex-alias
        assert 0xDEAD in def_dict
        d_out = def_dict.get(0xDEAD)
        assert d_out == d1

        # get via int-alias
        assert 123456 in def_dict
        d_out = def_dict.get(123456)
        assert d_out == d2

        # get non-existing
        assert 0xBEEF not in def_dict
        d_out = def_dict.get(0xBEEF)
        assert d_out is None

        # add via definition object
        d_alias = def_dict.register_alias(d1, 'foo')
        assert d_alias == d1
        assert len(def_dict._alias_dict) == 6

        # get via overwritten alias
        assert 'foo' in def_dict
        d_out = def_dict.get('foo')
        assert d_out == d1


class TestDefinitionsList:

    def_list = [
        {
            "index": 5,
            "count": 1,
            "names": ["field_5"],
            "type": Base,
            "writeable": True,
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

    def test_init(self):
        definitions = LuxtronikDefinitionsList(self.def_list, 'foo', 100, '')

        # only valid
        assert len(definitions) == 4
        assert definitions.name == 'foo'
        assert definitions.offset == 100
        assert definitions._version is None
        assert 5 in definitions
        assert 'field_9a' in definitions
        assert definitions[7] in definitions

        # correct fields
        assert definitions[5].name == "field_5"
        assert definitions["field_7"].index == 7
        assert definitions.get(9).addr == 109
        assert definitions.get(9).name == "field_9"

    def test_filtered(self):
        definitions = LuxtronikDefinitionsList(self.def_list, 'foo', 100, '')

        filtered1 = LuxtronikDefinitionsList.filtered(definitions, (1, 1, 0, 0))
        assert filtered1.name == 'foo'
        assert filtered1.offset == 100
        assert filtered1._version == (1, 1, 0, 0)
        assert 'field_5' in filtered1            # 1.1 - 1.2
        assert 'field_7' not in filtered1        # 3.1 -
        assert 'field_9a' in filtered1           #     - 1.3
        assert 'field_9' in filtered1            #     - 3.3
        assert 'field_invalid' not in filtered1  # invalid

        filtered1 = LuxtronikDefinitionsList.filtered(definitions, (3, 2, 0, 0))
        assert filtered1._version == (3, 2, 0, 0)
        assert 'field_5' not in filtered1        # 1.1 - 1.2
        assert 'field_7' in filtered1            # 3.1 -
        assert 'field_9a' not in filtered1       #     - 1.3
        assert 'field_9' in filtered1            #     - 3.3
        assert 'field_invalid' not in filtered1  # invalid

    def test_iter(self):
        definitions = LuxtronikDefinitionsList(self.def_list, 'foo', 100, '')

        for index, d in enumerate(definitions):
            if index == 0:
                assert d.index == 5
            if index == 1:
                assert d.index == 7
            if index == 2:
                assert d.index == 9
            if index == 3:
                assert d.index == 9

    def test_create(self):
        definitions = LuxtronikDefinitionsList(self.def_list, 'foo', 100, '')

        # create unknown definition
        definition = definitions.create_unknown_definition(4)
        assert definition.index == 4
        assert definition.count == 1
        assert definition.field_type is Unknown
        assert not definition.writeable
        assert definition.names == ['unknown_foo_4']
        assert definition.valid
        assert definition.type_name == 'foo'
        assert definition.offset == 100
        assert definition.addr == 100 + 4
        assert definition.aliases == []
        assert definition.since is None
        assert definition.until is None

    def test_alias(self):
        definitions = LuxtronikDefinitionsList(self.def_list, 'foo', 100, '')

        # add alias
        d = definitions.register_alias(5, 'bar')
        assert d.name == 'field_5'

        # get via alias
        d = definitions[5]
        assert d.name == 'field_5'

        # add nothing
        d = definitions.register_alias(4, 'baz')
        assert d is None

    def test_add(self):
        definitions = LuxtronikDefinitionsList(self.def_list, 'foo', 100, '')
        assert len(definitions) == 4

        # add custom definition
        added_1 = definitions.add({
            "index": 5,
            "count": 2,
            "names": "baz"
        })
        assert len(definitions) == 5
        assert definitions.get(5) == added_1
        assert definitions.get("baz") == added_1

        # add custom definition (partly covers previously added)
        added_2 = definitions.add({
            "index": 10,
            "count": 2,
            "names": "baz"
        })
        assert len(definitions) == 6
        assert definitions.get(5) == added_1
        assert definitions.get("baz") == added_2

        # add invalid definition (not valid)
        added_3 = definitions.add({
            "index": -1,
            "count": 2,
            "names": "baz"
        })
        assert added_3 is None

        # add invalid definition (exception)
        added_4 = definitions.add({
            "index": "foo",
            "count": 2,
            "names": 1
        })
        assert added_4 is None

    def test_repr(self):
        definitions = LuxtronikDefinitionsList(self.def_list, 'foo', 100, '')
        text = repr(definitions)
        assert text