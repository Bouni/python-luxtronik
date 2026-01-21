
from luxtronik.collections import LuxtronikFieldsDictionary
from luxtronik.definitions import LuxtronikDefinition, LuxtronikDefinitionsDictionary
from luxtronik.datatypes import (
    Base,
    Unknown,
)


class TestLuxtronikFieldsDictionary:

    def test_init(self):
        d = LuxtronikFieldsDictionary()

        assert type(d._def_lookup) is LuxtronikDefinitionsDictionary
        assert type(d._field_lookup) is dict
        assert len(d._field_lookup.values()) == 0
        assert type(d._items) is list
        assert len(d._items) == 0

    def test_add(self):
        d = LuxtronikFieldsDictionary()
        assert len(d) == 0
        assert len(d._items) == 0

        u = LuxtronikDefinition.unknown(1, "test", 0)
        f = u.create_field()
        d.add(u, f)
        assert len(d) == 1
        assert len(d._items) == 1
        assert d._items[0][0] is u
        assert d._items[0][1] is f

        u = LuxtronikDefinition.unknown(2, "test", 0)
        f = u.create_field()
        d.add(u, f)
        assert len(d) == 2
        assert len(d._items) == 2
        assert d._items[1][0] is u
        assert d._items[1][1] is f

        u = LuxtronikDefinition.unknown(0, "test", 0)
        f = u.create_field()
        d.add_sorted(u, f)
        assert len(d) == 3
        assert len(d._items) == 3
        assert d._items[0][0] is u
        assert d._items[0][1] is f

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
        assert len(d._items) == 4

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