
from luxtronik.datatypes import Base
from luxtronik.shi.constants import LUXTRONIK_VALUE_FUNCTION_NOT_AVAILABLE
from luxtronik.shi.definitions import LuxtronikDefinition
from luxtronik.shi.contiguous import (
    ContiguousDataPart,
    ContiguousDataBlock,
    ContiguousDataBlockList,
)

"""
The test was originally written for "False".
Since "True" is already checked in "test_definitions.py",
we continue to use "False" consistently here.
"""
Base.concatenate_multiple_data_chunks = False


def_a1 = LuxtronikDefinition({
    'index': 1,
    'count': 1,
}, 'test', 100)
def_a = LuxtronikDefinition({
    'index': 1,
    'count': 2,
}, 'test', 100)
def_b = LuxtronikDefinition({
    'index': 3,
    'count': 1,
}, 'test', 100)
def_c = LuxtronikDefinition({
    'index': 4,
    'count': 3,
}, 'test', 100)
def_c1 = LuxtronikDefinition({
    'index': 4,
    'count': 1,
}, 'test', 100)
def_c2 = LuxtronikDefinition({
    'index': 5,
    'count': 1,
}, 'test', 100)
defs = []

field_a1 = Base('field_a')
field_a  = Base('field_a')
field_b  = Base('field_b')
field_c  = Base('field_c')
field_c1 = Base('field_c1')
field_c2 = Base('field_c2')


class TestContiguousDataPart:

    def test_init(self):
        part = ContiguousDataPart(def_a, field_a)
        assert part.index == 1
        assert part.addr == 101
        assert part.count == 2
        assert part.field == field_a
        assert part.definition == def_a

    def test_repr(self):
        part = ContiguousDataPart(def_a, None)
        assert repr(part) == "(1, 2)"

    def test_get_data(self):
        part = ContiguousDataPart(def_a, field_a)
        field_a.raw = [4, 2]
        assert part.get_data_arr() == [4, 2]

        field_a.raw = [1, 3, 5]
        assert part.get_data_arr() is None

        field_a.raw = [9]
        assert part.get_data_arr() is None

        part = ContiguousDataPart(def_a1, field_a1)

        field_a1.raw = [8]
        assert part.get_data_arr() == [8]

        field_a1.raw = 7
        assert part.get_data_arr() == [7]

    def test_integrate_data(self):
        part = ContiguousDataPart(def_a, field_a)

        part.integrate_data([1, 5, 7, 9], 0)
        assert part.field.raw == [1, 5]

        part.integrate_data([1, 5, 7, 9])
        assert part.field.raw == [5, 7]

        part.integrate_data([1, 5, 7, 9], 2)
        assert part.field.raw == [7, 9]

        part.integrate_data([1, 5, 7, 9], 3)
        assert part.field.raw is None

        part.integrate_data([1, 5, LUXTRONIK_VALUE_FUNCTION_NOT_AVAILABLE, 9], 1)
        assert part.field.raw is None

        part = ContiguousDataPart(def_c1, field_c1)

        part.integrate_data([2, 4, 6], 1)
        assert part.field.raw == 4

        part.integrate_data([2, 4, LUXTRONIK_VALUE_FUNCTION_NOT_AVAILABLE], 2)
        assert part.field.raw is None

        part.integrate_data([2, 4, 6], 5)
        assert part.field.raw is None


class TestContiguousDataBlock:

    def test_clear(self):
        block = ContiguousDataBlock()
        block.add(def_a, None)
        block.add(def_b, None)
        block.add(def_c, None)
        block.clear()
        assert len(block) == 0
        assert block._last_idx == -1

    def test_iter(self):
        block = ContiguousDataBlock.create_and_add(def_a, None)
        block.add(def_b, None)
        block.add(def_c, None)
        for index, part in enumerate(block):
            if index == 0:
                assert part.index == 1
                assert part.count == 2
            if index == 1:
                assert part.index == 3
                assert part.count == 1
            if index == 2:
                assert part.index == 4
                assert part.count == 3

    def test_add(self):
        block = ContiguousDataBlock()

        can_add = block.can_add(def_b)
        assert can_add
        block.add(def_b, None)
        assert len(block) == 1

        can_add = block.can_add(def_c2)
        assert not can_add
        block.add(def_c2, None)
        assert len(block) == 2

        can_add = block.can_add(def_a)
        assert not can_add
        block.add(def_a, None)
        assert len(block) == 3

    def test_first_index(self):
        block = ContiguousDataBlock()
        assert block.first_index == 0

        block.add(def_b,field_b)
        block.add(def_c, field_c)

        assert block.first_index == 3
        assert block.first_addr == 103
        assert block.overall_count == 4

    def test_overall_count(self):
        block = ContiguousDataBlock()
        assert block.overall_count == 0

        # Several parts for one register
        block.add(def_a1, field_a1)
        block.add(def_a, field_a)
        block.add(def_b, field_b)
        block.add(def_c, field_c)
        block.add(def_c1, field_c1)
        block.add(def_c2, field_c2)

        assert block.first_index == 1
        assert block.first_addr == 101
        assert block.overall_count == 6

    def test_integrate_data(self):
        block = ContiguousDataBlock()

        block.add(def_a1, field_a1)
        block.add(def_a, field_a)
        block.add(def_b, field_b)

        valid = block.integrate_data(None)
        assert not valid

        valid = block.integrate_data([11, 12, 13])
        assert valid
        assert block[0].field.raw == 11
        assert block[1].field.raw == [11, 12]
        assert block[2].field.raw == 13

        block.add(def_c, field_c)

        block.integrate_data([7, 6, 5, 4, 3, 2])
        assert valid
        assert block[0].field.raw == 7
        assert block[1].field.raw == [7, 6]
        assert block[2].field.raw == 5
        assert block[3].field.raw == [4, 3, 2]

        block.add(def_c1, field_c1)
        block.add(def_c2, field_c2)

        block.integrate_data([21, 22, 23, 24, 25, 26])
        assert valid
        assert block[0].field.raw == 21
        assert block[1].field.raw == [21, 22]
        assert block[2].field.raw == 23
        assert block[3].field.raw == [24, 25, 26]
        assert block[4].field.raw == 24
        assert block[5].field.raw == 25

        valid = block.integrate_data([5, 4, 3])
        assert not valid

    def test_get_data(self):
        block = ContiguousDataBlock()

        data_arr = block.get_data_arr()
        assert data_arr is None

        # Multiple data for a single register #1
        field_a1.raw = 35
        field_a.raw = [56, 57]
        block.add(def_a1, field_a1)
        block.add(def_a, field_a)

        data_arr = block.get_data_arr()
        assert data_arr is None

        block = ContiguousDataBlock()
        field_b.raw = 11
        field_c.raw = [21, 22, 23]
        block.add(def_b, field_b)
        block.add(def_c, field_c)

        data_arr = block.get_data_arr()
        assert data_arr == [11, 21, 22, 23]

        # provided data greater than overall count
        orig_last = block._last_idx
        block._last_idx = orig_last - 1
        data_arr = block.get_data_arr()
        assert data_arr is None
        block._last_idx = orig_last

        # To less data for one register
        field_c.raw = [21, 22]
        data_arr = block.get_data_arr()
        assert data_arr is None

        # Multiple data for a single register #2
        field_b.raw = 11
        field_c.raw = [21, 22, 23]
        field_c1.raw = 6
        field_c2.raw = 7
        block.add(def_c1, field_c1)
        block.add(def_c2, field_c2)

        data_arr = block.get_data_arr()
        assert data_arr is None

    def test_repr(self):
        block = ContiguousDataBlock()
        text_empty = repr(block)
        assert text_empty

        block.add(def_a1, field_a1)
        block.add(def_a, field_a)
        text = repr(block)
        assert text
        assert text > text_empty


class TestContiguousDataBlockList:

    def test_init(self):
        blocks = ContiguousDataBlockList('foo', True)
        assert len(blocks) == 0
        assert blocks.type_name == 'foo'
        assert blocks.read_not_write

    def test_iter(self):
        blocks = ContiguousDataBlockList('foo', True)
        blocks.append_single(def_a, None)
        blocks.append_single(def_b, None)
        blocks.collect(def_c1, None)
        blocks.collect(def_c2, None)
        assert len(blocks) == 3
        for index, block in enumerate(blocks):
            if index == 0:
                assert len(block) == 1
                assert block.first_index == 1
                assert block.overall_count == 2
            if index == 1:
                assert len(block) == 1
                assert block.first_index == 3
                assert block.overall_count == 1
            if index == 2:
                assert len(block) == 2
                assert block.first_index == 4
                assert block.overall_count == 2

        blocks.clear()
        assert len(blocks) == 0

    def test_collect(self):
        blocks = ContiguousDataBlockList('foo', True)
        # First block
        blocks.collect(def_c1, None)
        blocks.collect(def_c2, None)
        # Second block
        blocks.collect(def_b, None)
        blocks.collect(def_c, None)
        # Third block
        blocks.collect(def_a1, None)
        blocks.collect(def_a, None)
        # Fourth block
        blocks.append_single(def_b, None)
        # Fifth block
        blocks.collect(def_c, None)

        assert len(blocks) == 5
        assert blocks[0].first_index == 4
        assert blocks[0].overall_count == 2
        assert blocks[1].first_index == 3
        assert blocks[1].overall_count == 4
        assert blocks[2].first_index == 1
        assert blocks[2].overall_count == 2
        assert blocks[3].first_index == 3
        assert blocks[3].overall_count == 1
        assert blocks[4].first_index == 4
        assert blocks[4].overall_count == 3

    def test_append(self):
        blocks = ContiguousDataBlockList('foo', True)

        block = ContiguousDataBlock()
        block.add(def_a, None)
        block.add(def_b, None)
        block.add(def_c, None)

        blocks.append(block)
        assert len(blocks) == 1
        assert blocks[0].first_index == 1
        assert blocks[0].overall_count == 6

    def test_repr(self):
        blocks = ContiguousDataBlockList('foo', True)
        text_empty = repr(blocks)
        assert text_empty

        block = ContiguousDataBlock()
        block.add(def_a, None)
        block.add(def_b, None)
        block.add(def_c, None)

        blocks.append(block)

        text = repr(blocks)
        assert text
        assert len(text) > len(text_empty)
