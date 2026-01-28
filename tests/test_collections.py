
from luxtronik.collections import (
    get_data_arr,
    integrate_data,
    LuxtronikDefFieldPair,
    LuxtronikFieldsDictionary,
)
from luxtronik.definitions import LuxtronikDefinition, LuxtronikDefinitionsDictionary
from luxtronik.datatypes import (
    Base,
    Unknown,
)
from luxtronik.constants import LUXTRONIK_VALUE_FUNCTION_NOT_AVAILABLE


###############################################################################
# Tests
###############################################################################

class TestDefinitionFieldPair:

    def test_init(self):
        definition = LuxtronikDefinition.unknown(2, 'Foo', 30)
        field = definition.create_field()
        pair = LuxtronikDefFieldPair(definition, field)

        assert pair.definition is definition
        assert pair.field is field
        d, f = pair
        assert d is definition
        assert f is field

    def test_data_arr(self):
        definition = LuxtronikDefinition.unknown(2, 'Foo', 30)
        field = definition.create_field()
        pair = LuxtronikDefFieldPair(definition, field)

        field.concatenate_multiple_data_chunks = False

        # get from value
        definition._count = 1
        field.raw = 5
        arr = get_data_arr(definition, field, 32)
        assert arr == [5]
        assert arr == pair.get_data_arr(32)

        # get from value
        definition._count = 1
        field.raw = 5
        arr = get_data_arr(definition, field, 16)
        assert arr == [5]
        assert arr == pair.get_data_arr(16)

        # get from array
        definition._count = 2
        field.raw = [7, 3]
        arr = get_data_arr(definition, field, 32)
        assert arr == [7, 3]
        assert arr == pair.get_data_arr(32)

        # get from array
        definition._count = 2
        field.raw = [7, 3]
        arr = get_data_arr(definition, field, 16)
        assert arr == [7, 3]
        assert arr == pair.get_data_arr(16)

        # too much data
        definition._count = 2
        field.raw = [4, 8, 1]
        arr = get_data_arr(definition, field, 16)
        assert arr is None
        assert arr == pair.get_data_arr(16)

        # insufficient data
        definition._count = 2
        field.raw = [9]
        arr = get_data_arr(definition, field, 16)
        assert arr is None
        assert arr == pair.get_data_arr(16)

        field.concatenate_multiple_data_chunks = True

        # get from array
        definition._count = 2
        field.raw = 0x00000007_00000003
        arr = get_data_arr(definition, field, 32)
        assert arr == [7, 3]
        assert arr == pair.get_data_arr(32)

        # get from array
        definition._count = 2
        field.raw = 0x0007_0003
        arr = get_data_arr(definition, field, 16)
        assert arr == [7, 3]
        assert arr == pair.get_data_arr(16)

        # too much data
        definition._count = 2
        field.raw = 0x0004_0008_0001
        arr = get_data_arr(definition, field, 16)
        assert arr == [8, 1]
        assert arr == pair.get_data_arr(16)

        # insufficient data
        definition._count = 2
        field.raw = 0x0009
        arr = get_data_arr(definition, field, 16)
        assert arr == [0, 9]
        assert arr == pair.get_data_arr(16)

    def test_integrate(self):
        definition = LuxtronikDefinition.unknown(2, 'Foo', 30)
        field = definition.create_field()
        pair = LuxtronikDefFieldPair(definition, field)
        data = [1, LUXTRONIK_VALUE_FUNCTION_NOT_AVAILABLE, 3, 4, 5, 6, 7]

        field.concatenate_multiple_data_chunks = False

        # set array
        definition._count = 2
        definition._data_type = 'INT64'
        integrate_data(definition, field, data, 32)
        assert field.raw == [3, 4]
        pair.integrate_data(data, 32, 4)
        assert field.raw == [5, 6]
        integrate_data(definition, field, data, 32, 7)
        assert field.raw is None
        pair.integrate_data(data, 32, 0)
        assert field.raw == [1, LUXTRONIK_VALUE_FUNCTION_NOT_AVAILABLE]

        # set array
        definition._count = 2
        definition._data_type = 'INT32'
        integrate_data(definition, field, data, 16)
        assert field.raw == [3, 4]
        pair.integrate_data(data, 16, 4)
        assert field.raw == [5, 6]
        integrate_data(definition, field, data, 16, 7)
        assert field.raw is None
        pair.integrate_data(data, 16, 0)
        assert field.raw == [1, LUXTRONIK_VALUE_FUNCTION_NOT_AVAILABLE]

        # set value
        definition._count = 1
        definition._data_type = 'INT32'
        integrate_data(definition, field, data, 32)
        assert field.raw == 3
        pair.integrate_data(data, 32, 5)
        assert field.raw == 6
        integrate_data(definition, field, data, 32, 9)
        assert field.raw is None
        pair.integrate_data(data, 32, 1)
        # Currently there is no magic "not available" value for 32 bit values -> not None
        # This applies also to similar lines below
        assert field.raw == LUXTRONIK_VALUE_FUNCTION_NOT_AVAILABLE

        # set value
        definition._count = 1
        definition._data_type = 'INT16'
        integrate_data(definition, field, data, 16)
        assert field.raw == 3
        pair.integrate_data(data, 16, 5)
        assert field.raw == 6
        integrate_data(definition, field, data, 16, 9)
        assert field.raw is None
        pair.integrate_data(data, 16, 1)
        assert field.raw is None

        field.concatenate_multiple_data_chunks = True

        # set array
        definition._count = 2
        definition._data_type = 'INT64'
        integrate_data(definition, field, data, 32)
        assert field.raw == 0x00000003_00000004
        pair.integrate_data(data, 32, 4)
        assert field.raw == 0x00000005_00000006
        integrate_data(definition, field, data, 32, 7)
        assert field.raw is None
        pair.integrate_data(data, 32, 0)
        assert field.raw == 0x00000001_00007FFF

        # set array
        definition._count = 2
        definition._data_type = 'INT32'
        integrate_data(definition, field, data, 16)
        assert field.raw == 0x0003_0004
        pair.integrate_data(data, 16, 4)
        assert field.raw == 0x0005_0006
        integrate_data(definition, field, data, 16, 7)
        assert field.raw is None
        pair.integrate_data(data, 16, 0)
        assert field.raw == 0x0001_7FFF

        # set value
        definition._count = 1
        definition._data_type = 'INT32'
        integrate_data(definition, field, data, 32)
        assert field.raw == 0x00000003
        pair.integrate_data(data, 32, 5)
        assert field.raw == 0x00000006
        integrate_data(definition, field, data, 32, 9)
        assert field.raw is None
        pair.integrate_data(data, 32, 1)
        assert field.raw == 0x00007FFF

        # set value
        definition._count = 1
        definition._data_type = 'INT16'
        integrate_data(definition, field, data, 16)
        assert field.raw == 0x0003
        pair.integrate_data(data, 16, 5)
        assert field.raw == 0x0006
        integrate_data(definition, field, data, 16, 9)
        assert field.raw is None
        pair.integrate_data(data, 16, 1)
        assert field.raw is None

        field.concatenate_multiple_data_chunks = False


class TestLuxtronikFieldsDictionary:

    def test_init(self):
        d = LuxtronikFieldsDictionary()

        assert type(d._def_lookup) is LuxtronikDefinitionsDictionary
        assert type(d._field_lookup) is dict
        assert len(d._field_lookup.values()) == 0
        assert type(d._pairs) is list
        assert len(d._pairs) == 0

    def test_add(self):
        d = LuxtronikFieldsDictionary()
        assert len(d) == 0
        assert len(d.pairs()) == 0

        u = LuxtronikDefinition.unknown(1, "test", 0)
        f = u.create_field()
        d.add(u, f)
        assert len(d) == 1
        assert len(d._pairs) == 1
        assert d._pairs[0].definition is u
        assert d._pairs[0].field is f

        u = LuxtronikDefinition.unknown(2, "test", 0)
        f = u.create_field()
        d.add(u, f)
        assert len(d) == 2
        assert len(d._pairs) == 2
        assert d._pairs[1].definition is u
        assert d._pairs[1].field is f

        u = LuxtronikDefinition.unknown(0, "test", 0)
        f = u.create_field()
        d.add_sorted(u, f)
        assert len(d) == 3
        assert len(d._pairs) == 3
        assert d._pairs[0].definition is u
        assert d._pairs[0].field is f

    def create_instance(self):
        d = LuxtronikFieldsDictionary()
        u = LuxtronikDefinition.unknown(1, "test", 0)
        d.add(u, u.create_field())
        u = LuxtronikDefinition.unknown(2, "test", 0)
        d.add(u, u.create_field())
        b = LuxtronikDefinition({
            "index": 2,
            "type": Base,
            "names": ["base2"],
        }, "test", 0)
        f = b.create_field()
        d.add(b, f)
        b = LuxtronikDefinition({
            "index": 3,
            "type": Base,
            "names": ["base3"],
        }, "test", 0)
        d.add(b, b.create_field(), "base4")
        return d, u, f

    def test_len(self):
        d, _, _ = self.create_instance()
        # 3 different indices
        assert len(d) == 3
        assert len(d.pairs()) == 4

    def test_get_contains(self):
        d, u, f = self.create_instance()
        assert "1" in d
        assert d["1"].name == "unknown_test_1"
        assert "unknown_test_1" in d
        assert d["unknown_test_1"].name == "unknown_test_1"
        assert 2 in d
        assert d[2].name == "base2"
        assert "unknown_test_2" in d
        assert d["unknown_test_2"].name == "unknown_test_2"
        assert "base2" in d
        assert d["base2"].name == "base2"
        assert "base3" in d
        assert d.get("base3").name == "base3"
        assert "base4" in d
        assert d.get("base4").name == "base3"
        assert u in d
        assert d[u].name == "unknown_test_2"
        assert f in d
        assert d[f].name == "base2"
        assert 4 not in d

    def test_iter(self):
        d, _, _ = self.create_instance()
        for idx, key in enumerate(d):
            if idx == 0:
                assert key == 1
            if idx == 1:
                assert key == 2
            if idx == 2:
                assert key == 3

    def test_values(self):
        d, _, _ = self.create_instance()
        for idx, value in enumerate(d.values()):
            if idx == 0:
                assert type(value) is Unknown
                assert value.name == "unknown_test_1"
            if idx == 1:
                assert type(value) is Base
                assert value.name == "base2"
            if idx == 2:
                assert type(value) is Base
                assert value.name == "base3"

    def test_items(self):
        d, _, _ = self.create_instance()
        for idx, (key, value) in enumerate(d.items()):
            if idx == 0:
                assert key == 1
                assert type(value) is Unknown
                assert value.name == "unknown_test_1"
            if idx == 1:
                assert key == 2
                assert type(value) is Base
                assert value.name == "base2"
            if idx == 2:
                assert key == 3
                assert type(value) is Base
                assert value.name == "base3"

    class MyTestClass:
        pass

    def test_alias(self):
        d, u, f = self.create_instance()
        my = self.MyTestClass()

        d.register_alias(0, "abc")
        assert d["abc"] is d[0]

        field = d.register_alias("unknown_test_1", 6)
        assert d[6] is field

        field = d.register_alias(u, my)
        assert d[my] is d[u]

        d.register_alias(f, my)
        assert d[my] is not d[u]
        assert d[my] is d[f]

        field = d.register_alias(9, my)
        assert field is None
        assert d[my] is d[f]