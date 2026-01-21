from luxtronik.collections import (
    get_data_arr,
    check_data,
    integrate_data,
)
from luxtronik.definitions import LuxtronikDefinition
from luxtronik.shi.constants import LUXTRONIK_VALUE_FUNCTION_NOT_AVAILABLE

###############################################################################
# Tests
###############################################################################

class TestDefinitionFieldPair:

    def test_data_arr(self):
        definition = LuxtronikDefinition.unknown(2, 'Foo', 30)
        field = definition.create_field()
        field.concatenate_multiple_data_chunks = False

        # get from value
        definition._count = 1
        field.raw = 5
        arr = get_data_arr(definition, field)
        assert arr == [5]
        assert check_data(definition, field)

        # get from array
        definition._count = 2
        field.raw = [7, 3]
        arr = get_data_arr(definition, field)
        assert arr == [7, 3]
        assert check_data(definition, field)

        # too much data
        definition._count = 2
        field.raw = [4, 8, 1]
        arr = get_data_arr(definition, field)
        assert arr is None
        assert not check_data(definition, field)

        # insufficient data
        definition._count = 2
        field.raw = [9]
        arr = get_data_arr(definition, field)
        assert arr is None
        assert not check_data(definition, field)

        field.concatenate_multiple_data_chunks = True

        # get from array
        definition._count = 2
        field.raw = 0x0007_0003
        arr = get_data_arr(definition, field)
        assert arr == [7, 3]
        assert check_data(definition, field)

        # too much data
        definition._count = 2
        field.raw = 0x0004_0008_0001
        arr = get_data_arr(definition, field)
        assert arr == [8, 1]
        assert check_data(definition, field)

        # insufficient data
        definition._count = 2
        field.raw = 0x0009
        arr = get_data_arr(definition, field)
        assert arr == [0, 9]
        assert check_data(definition, field)

    def test_integrate(self):
        definition = LuxtronikDefinition.unknown(2, 'Foo', 30)
        field = definition.create_field()
        field.concatenate_multiple_data_chunks = False

        data = [1, LUXTRONIK_VALUE_FUNCTION_NOT_AVAILABLE, 3, 4, 5, 6, 7]

        # set array
        definition._count = 2
        integrate_data(definition, field, data)
        assert field.raw == [3, 4]
        integrate_data(definition, field, data, 4)
        assert field.raw == [5, 6]
        integrate_data(definition, field, data, 7)
        assert field.raw is None
        integrate_data(definition, field, data, 0)
        assert field.raw is None

        # set value
        definition._count = 1
        integrate_data(definition, field, data)
        assert field.raw == 3
        integrate_data(definition, field, data, 5)
        assert field.raw == 6
        integrate_data(definition, field, data, 9)
        assert field.raw is None
        integrate_data(definition, field, data, 1)
        assert field.raw is None

        field.concatenate_multiple_data_chunks = True

        # set array
        definition._count = 2
        integrate_data(definition, field, data)
        assert field.raw == 0x0003_0004
        integrate_data(definition, field, data, 4)
        assert field.raw == 0x0005_0006
        integrate_data(definition, field, data, 7)
        assert field.raw is None
        integrate_data(definition, field, data, 0)
        assert field.raw is None

        # set value
        definition._count = 1
        integrate_data(definition, field, data)
        assert field.raw == 0x0003
        integrate_data(definition, field, data, 5)
        assert field.raw == 0x0006
        integrate_data(definition, field, data, 9)
        assert field.raw is None
        integrate_data(definition, field, data, 1)
        assert field.raw is None