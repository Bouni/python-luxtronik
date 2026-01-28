import pytest
from unittest.mock import patch

from luxtronik.constants import LUXTRONIK_VALUE_FUNCTION_NOT_AVAILABLE
from luxtronik.datatypes import Base, Unknown
from luxtronik.definitions import LuxtronikDefinition

from luxtronik.shi.constants import (
    LUXTRONIK_LATEST_SHI_VERSION,
    LUXTRONIK_FIRST_VERSION_WITH_SHI,
)
from luxtronik.shi.common import (
    LuxtronikSmartHomeReadHoldingsTelegram,
    LuxtronikSmartHomeReadInputsTelegram,
    LuxtronikSmartHomeWriteHoldingsTelegram,
)
from luxtronik.shi.contiguous import (
    ContiguousDataBlock,
    ContiguousDataBlockList,
)
from luxtronik.shi import (
    HOLDINGS_DEFINITIONS,
    Holdings,
    INPUTS_DEFINITIONS,
    LuxtronikSmartHomeData,
    LuxtronikSmartHomeInterface,
    create_modbus_tcp,
)
from tests.fake import FakeModbus


class TestLuxtronikSmartHomeData:

    def test_init(self):
        data1 = LuxtronikSmartHomeData()
        assert data1.holdings is not None
        assert data1.holdings.version == LUXTRONIK_LATEST_SHI_VERSION
        assert data1.holdings.safe
        assert data1.inputs is not None
        assert data1.inputs.version == LUXTRONIK_LATEST_SHI_VERSION
        assert data1.inputs.safe

        data2 = LuxtronikSmartHomeData(data1.holdings)
        assert data2.holdings is data1.holdings
        assert data2.inputs is not data1.inputs

    def test_empty(self):
        data = LuxtronikSmartHomeData.empty((1, 2, 0, 0), False)
        assert data.holdings is not None
        assert not data.holdings.safe
        assert data.holdings.version == (1, 2, 0, 0)
        assert data.inputs is not None
        assert data.inputs.safe
        assert data.inputs.version == (1, 2, 0, 0)


@patch("luxtronik.shi.LuxtronikModbusTcpInterface", FakeModbus)
class TestLuxtronikSmartHomeInterface:

    @classmethod
    def setup_class(cls):
        cls.interface = LuxtronikSmartHomeInterface(FakeModbus(), LUXTRONIK_FIRST_VERSION_WITH_SHI)

    def test_init(self):
        assert isinstance(self.interface._interface, FakeModbus)
        assert self.interface._blocks_list == []
        assert self.interface.version == LUXTRONIK_FIRST_VERSION_WITH_SHI
        assert len(self.interface._filtered_holdings) > 0
        assert len(self.interface._filtered_inputs) > 0

    def test_get(self):
        assert self.interface.holdings is HOLDINGS_DEFINITIONS
        assert self.interface.holdings is self.interface.get_holdings(True)
        assert self.interface.holdings is not self.interface.get_holdings(False)
        assert self.interface.inputs is INPUTS_DEFINITIONS
        assert self.interface.inputs is self.interface.get_inputs(True)
        assert self.interface.inputs is not self.interface.get_inputs(False)

        # via index
        definition = self.interface._get_definition(2, HOLDINGS_DEFINITIONS)
        assert definition is HOLDINGS_DEFINITIONS[2]

        # via name
        definition, field = self.interface._get_def_field_pair("hot_water_mode", HOLDINGS_DEFINITIONS)
        assert definition is HOLDINGS_DEFINITIONS[5]
        assert isinstance(field, Base)
        assert field.name == definition.name

        # via definition
        definition = self.interface._get_definition(HOLDINGS_DEFINITIONS[6], HOLDINGS_DEFINITIONS)
        assert definition is HOLDINGS_DEFINITIONS[6]

        # via field
        field_52 = Base("lock_cooling", False)
        definition, field = self.interface._get_def_field_pair(field_52, HOLDINGS_DEFINITIONS)
        assert definition is HOLDINGS_DEFINITIONS[52]
        assert field is field_52
        assert field.name == definition.name

        # unsupported via index
        definition, field = self.interface._get_def_field_pair(109, INPUTS_DEFINITIONS)
        assert definition is None
        assert field is None

        definition = self.interface.inputs.get(109)
        assert definition is INPUTS_DEFINITIONS[109]

        # unsupported via name
        definition = self.interface._get_definition("mc1_heat_level", HOLDINGS_DEFINITIONS)
        assert definition is None

        definition = self.interface.holdings.get("mc1_heat_level")
        assert definition is HOLDINGS_DEFINITIONS["mc1_heat_level"]

        # unsupported via definition
        definition, field = self.interface._get_def_field_pair(HOLDINGS_DEFINITIONS[23], HOLDINGS_DEFINITIONS)
        assert definition is None
        assert field is None

        # unsupported via field
        field_500 = Base("unknown_input_500", False)
        definition, field = self.interface._get_def_field_pair(field_500, INPUTS_DEFINITIONS)
        assert definition is None
        assert field is None

    @pytest.mark.parametrize(
        "name, index",
        [
            ("UNKNOWNINPUT",       None),
            ("UNKNOWN_INPUT",      None),
            ("UNKNOWN_INPUT_4",       4),
            ("UNKNOWN_INPUT_4_5",  None),
            ("UNKNOWN_INPUT_four", None),
            ("unknown_input_8",       8),
            ("foo_bar_2",             2),
        ]
    )
    def test_index_from_name(self, name, index):
        idx = self.interface._get_index_from_name(name)
        assert idx == index

    def test_try_create(self):
        # get unsupported via name
        definition = self.interface._try_create_definition("heating_level", HOLDINGS_DEFINITIONS)
        assert definition is HOLDINGS_DEFINITIONS["heating_level"]

        # get unsupported via definition
        definition = self.interface._try_create_definition(HOLDINGS_DEFINITIONS[8], HOLDINGS_DEFINITIONS)
        assert definition is HOLDINGS_DEFINITIONS[8]

        # create by name
        definition = self.interface._try_create_definition("unKnOWn_foo_4", HOLDINGS_DEFINITIONS)
        assert definition not in HOLDINGS_DEFINITIONS
        assert definition.name == "unknown_holding_4"
        assert definition.index == 4
        assert definition.count == 1
        assert not definition.writeable
        assert definition.field_type is Unknown

        # fail by name
        definition = self.interface._try_create_definition("unKnOWn_foo4", HOLDINGS_DEFINITIONS)
        assert definition is None

        definition = self.interface._try_create_definition("nKnOWn_foo_4", HOLDINGS_DEFINITIONS)
        assert definition is None

        # create by index
        definition = self.interface._try_create_definition(9, HOLDINGS_DEFINITIONS)
        assert definition not in HOLDINGS_DEFINITIONS
        assert definition.name == "unknown_holding_9"
        assert definition.index == 9
        assert definition.count == 1
        assert not definition.writeable
        assert definition.field_type is Unknown

        # fail by else
        definition = self.interface._try_create_definition(Base, HOLDINGS_DEFINITIONS)
        assert definition is None

        # create by index as name
        definition = self.interface._try_create_definition("14", HOLDINGS_DEFINITIONS)
        assert definition not in HOLDINGS_DEFINITIONS
        assert definition.name == "unknown_holding_14"
        assert definition.index == 14
        assert definition.count == 1
        assert not definition.writeable
        assert definition.field_type is Unknown

    def test_create_telegram(self):
        block = ContiguousDataBlock()
        field_1 = HOLDINGS_DEFINITIONS[10].create_field()
        block.add(HOLDINGS_DEFINITIONS[10], field_1)
        field_2 = HOLDINGS_DEFINITIONS[11].create_field()
        block.add(HOLDINGS_DEFINITIONS[11], field_2)
        addr = HOLDINGS_DEFINITIONS[10].addr
        count = HOLDINGS_DEFINITIONS[10].count + HOLDINGS_DEFINITIONS[11].count

        # read holdings
        telegram = self.interface._create_read_telegram(block, LuxtronikSmartHomeReadHoldingsTelegram)
        assert type(telegram) is LuxtronikSmartHomeReadHoldingsTelegram
        assert telegram.addr == addr
        assert telegram.count == count
        assert telegram.data == []

        telegram = self.interface._create_telegram(block, "holding", True)
        assert type(telegram) is LuxtronikSmartHomeReadHoldingsTelegram
        assert telegram.addr == addr
        assert telegram.count == count
        assert telegram.data == []

        # read inputs
        telegram = self.interface._create_read_telegram(block, LuxtronikSmartHomeReadInputsTelegram)
        assert type(telegram) is LuxtronikSmartHomeReadInputsTelegram
        assert telegram.addr == addr
        assert telegram.count == count
        assert telegram.data == []

        telegram = self.interface._create_telegram(block, "input", True)
        assert type(telegram) is LuxtronikSmartHomeReadInputsTelegram
        assert telegram.addr == addr
        assert telegram.count == count
        assert telegram.data == []

        # fail on create
        field_1.raw = 21
        telegram = self.interface._create_write_telegram(block, LuxtronikSmartHomeWriteHoldingsTelegram)
        assert telegram is None

        # write holdings
        field_2.raw = 5
        telegram = self.interface._create_write_telegram(block, LuxtronikSmartHomeWriteHoldingsTelegram)
        assert type(telegram) is LuxtronikSmartHomeWriteHoldingsTelegram
        assert telegram.addr == addr
        assert telegram.count == count
        assert telegram.data == [21, 5]

        telegram = self.interface._create_telegram(block, "holding", False)
        assert type(telegram) is LuxtronikSmartHomeWriteHoldingsTelegram
        assert telegram.addr == addr
        assert telegram.count == count
        assert telegram.data == [21, 5]

        # fail on create
        telegram = self.interface._create_telegram(block, "input", False)
        assert telegram is None

    def test_create_telegrams(self):
        blocks_list = []
        blocks = ContiguousDataBlockList("holding", True)

        # block 1
        block = ContiguousDataBlock()
        block.add(HOLDINGS_DEFINITIONS[10], HOLDINGS_DEFINITIONS[10].create_field())
        block.add(HOLDINGS_DEFINITIONS[11], HOLDINGS_DEFINITIONS[11].create_field())
        blocks.append(block)

        # block 2
        blocks.append_single(HOLDINGS_DEFINITIONS[17], HOLDINGS_DEFINITIONS[17].create_field())

        # block 3
        blocks.append_single(HOLDINGS_DEFINITIONS[10], HOLDINGS_DEFINITIONS[10].create_field())

        blocks_list.append(blocks)

        blocks = ContiguousDataBlockList("holding", False)

        # invalid block
        blocks.append_single(HOLDINGS_DEFINITIONS[12], HOLDINGS_DEFINITIONS[12].create_field())
        # block 4
        field3 = HOLDINGS_DEFINITIONS[17].create_field()
        blocks.append_single(HOLDINGS_DEFINITIONS[17], field3)

        blocks_list.append(blocks)

        field3.raw = 17

        telegram_data = self.interface._create_telegrams(blocks_list)
        assert len(telegram_data) == 4
        # blocks
        assert len(telegram_data[0][0]) == 2
        assert telegram_data[0][0].first_index == 10
        assert telegram_data[0][0].overall_count == 2
        assert len(telegram_data[1][0]) == 1
        assert telegram_data[1][0].first_index == 17
        assert telegram_data[1][0].overall_count == 1
        assert len(telegram_data[2][0]) == 1
        assert telegram_data[2][0].first_index == 10
        assert telegram_data[2][0].overall_count == 1
        assert len(telegram_data[3][0]) == 1
        assert telegram_data[3][0].first_index == 17
        assert telegram_data[3][0].overall_count == 1
        # telegrams
        assert telegram_data[0][1].count == 2
        assert telegram_data[1][1].count == 1
        assert telegram_data[2][1].count == 1
        assert telegram_data[3][1].count == 1
        # read not write
        assert telegram_data[0][2]
        assert telegram_data[1][2]
        assert telegram_data[2][2]
        assert not telegram_data[3][2]

        # integrate
        telegram_data[0][1].data = [18, 4]
        telegram_data[1][1].data = [9]
        telegram_data[2][1].data = [27]
        telegram_data[3][0][0].field.write_pending = True
        valid = self.interface._integrate_data(telegram_data)
        assert valid
        # [index data, index for blocks, index for part]
        assert telegram_data[0][0][0].field.raw == 18
        assert telegram_data[0][0][1].field.raw == 4
        assert telegram_data[1][0][0].field.raw == 9
        assert telegram_data[2][0][0].field.raw == 27
        assert not telegram_data[3][0][0].field.write_pending
        assert telegram_data[3][0][0].field.raw == 17 # no update

        # integrate not available / None -> no error
        telegram_data[0][1].data = [18, 4]
        telegram_data[1][1].data = [LUXTRONIK_VALUE_FUNCTION_NOT_AVAILABLE]
        telegram_data[2][1].data = [None]
        valid = self.interface._integrate_data(telegram_data)
        assert valid
        # [index data, index for blocks, index for part]
        assert telegram_data[0][0][0].field.raw == 18
        assert telegram_data[0][0][1].field.raw == 4
        assert telegram_data[1][0][0].field.raw is None
        assert telegram_data[2][0][0].field.raw is None
        assert telegram_data[3][0][0].field.raw == 17 # no update

        # integrate too less -> error
        telegram_data[0][1].data = [18]
        telegram_data[1][1].data = [1]
        telegram_data[2][1].data = [None]
        valid = self.interface._integrate_data(telegram_data)
        assert not valid
        # [index data, index for blocks, index for part]
        assert telegram_data[0][0][0].field.raw == 18
        assert telegram_data[0][0][1].field.raw == 4 # no update
        assert telegram_data[1][0][0].field.raw == 1
        assert telegram_data[2][0][0].field.raw is None
        assert telegram_data[3][0][0].field.raw == 17 # no update

    def test_prepare(self):
        definition = HOLDINGS_DEFINITIONS[2]
        field = definition.create_field()
        field.raw = 2

        # supported valid read
        valid = self.interface._prepare_read_field(definition, field)
        assert valid
        assert field.raw == 2

        # supported valid write
        field.raw = 5
        field.write_pending = True
        valid = self.interface._prepare_write_field(definition, field, False, None)
        assert valid
        assert field.raw == 5

        # supported invalid write via safe
        field.raw = 6
        field.write_pending = True
        field.writeable = False
        valid = self.interface._prepare_write_field(definition, field, True, None)
        assert not valid
        assert field.raw == 6
        field.writeable = True

        # supported invalid write via write_pending
        field.raw = 7
        field.write_pending = False
        valid = self.interface._prepare_write_field(definition, field, False, None)
        assert not valid
        assert field.raw == 7

        # supported valid write with data
        field.raw = 8
        field.write_pending = False
        valid = self.interface._prepare_write_field(definition, field, False, 9)
        assert valid
        assert field.value == 9

        # supported invalid write via data
        field.raw = []
        field.write_pending = True
        valid = self.interface._prepare_write_field(definition, field, False, None)
        assert not valid
        assert field.raw == []

        definition = HOLDINGS_DEFINITIONS[3]
        field = definition.create_field()
        field.raw = 1

        # not supported read
        valid = self.interface._prepare_read_field(definition, field)
        assert not valid
        assert field.raw is None

        # not supported write
        field.raw = 1
        valid = self.interface._prepare_write_field(definition, field, False, None)
        assert not valid
        assert field.raw == 1

    def test_collect_field(self):
        blocks_list = []

        # could not collect via None
        field = self.interface._collect_field(blocks_list, None, HOLDINGS_DEFINITIONS, True, True, None)
        assert field is None
        assert len(blocks_list) == 0

        # could not collect via string
        field = self.interface._collect_field(blocks_list, 'foo', HOLDINGS_DEFINITIONS, True, True, None)
        assert field is None
        assert len(blocks_list) == 0

        # could not collect, not supported read
        field = self.interface._collect_field(blocks_list, 3, HOLDINGS_DEFINITIONS, True, True, None)
        assert field is None
        assert len(blocks_list) == 0

        # could not collect, safe
        field = self.interface._collect_field(blocks_list, 0, INPUTS_DEFINITIONS, False, True, None)
        assert field is None
        assert len(blocks_list) == 0

        # collected read
        field = self.interface._collect_field(blocks_list, 2, HOLDINGS_DEFINITIONS, True, True, None)
        assert field is not None
        assert field.name == "heating_offset"
        assert len(blocks_list) == 1
        # blocks
        assert blocks_list[0].type_name == "holding"
        assert blocks_list[0].read_not_write
        assert len(blocks_list[0]) == 1
        # block
        assert blocks_list[0][0].first_index == 2
        assert blocks_list[0][0].overall_count == 1
        assert len(blocks_list[0][0]) == 1
        # part
        assert blocks_list[0][0][0].definition.index == 2
        assert blocks_list[0][0][0].field is field

        # could not collect, not supported write
        field = self.interface._collect_field(blocks_list, 3, HOLDINGS_DEFINITIONS, False, True, None)
        assert field is None
        assert len(blocks_list) == 1

        # collected write
        field = self.interface._collect_field(blocks_list, 1, HOLDINGS_DEFINITIONS, False, True, 20)
        assert field is not None
        assert field.name == "heating_setpoint"
        assert field.value == 20
        assert len(blocks_list) == 2
        # blocks
        assert blocks_list[1].type_name == "holding"
        assert not blocks_list[1].read_not_write
        assert len(blocks_list[1]) == 1
        # block
        assert blocks_list[1][0].first_index == 1
        assert blocks_list[1][0].overall_count == 1
        assert len(blocks_list[1][0]) == 1
        # part
        assert blocks_list[1][0][0].definition.index == 1
        assert blocks_list[1][0][0].field is field

        valid = self.interface._send_and_integrate(blocks_list)
        assert valid
        assert len(FakeModbus.telegram_list) == 2
        assert type(FakeModbus.telegram_list[0]) is LuxtronikSmartHomeReadHoldingsTelegram
        assert FakeModbus.telegram_list[0].addr == 10000 + 2
        assert FakeModbus.telegram_list[0].count == 1
        assert type(FakeModbus.telegram_list[1]) is LuxtronikSmartHomeWriteHoldingsTelegram
        assert FakeModbus.telegram_list[1].addr == 10000 + 1
        assert FakeModbus.telegram_list[1].count == 1

    def test_collect_fields(self):
        blocks_list = []

        # could not collect via None
        self.interface._collect_fields(blocks_list, None, HOLDINGS_DEFINITIONS, True)
        assert len(blocks_list) == 0

        data_vector = Holdings.empty(LUXTRONIK_FIRST_VERSION_WITH_SHI)
        data_vector.add(0)
        data_vector.add(2)
        data_vector.add(3) # not supported
        data_vector.add(4) # does not exist
        data_vector.add(5)
        data_vector.add(6)
        data_vector.add(7)
        data_vector.update_read_blocks()

        # collect read
        self.interface._collect_fields(blocks_list, data_vector, HOLDINGS_DEFINITIONS, True)
        assert len(blocks_list) == 1
        # blocks
        assert blocks_list[0].type_name == "holding"
        assert blocks_list[0].read_not_write
        assert len(blocks_list[0]) == 3
        # block
        assert blocks_list[0][0].first_index == 0
        assert blocks_list[0][0].overall_count == 1
        assert blocks_list[0][1].first_index == 2
        assert blocks_list[0][1].overall_count == 1
        assert blocks_list[0][2].first_index == 5
        assert blocks_list[0][2].overall_count == 3
        assert len(blocks_list[0][2]) == 3
        # part
        assert blocks_list[0][2][0].definition.index == 5
        assert blocks_list[0][2][1].definition.index == 6
        assert blocks_list[0][2][2].definition.index == 7

        data_vector[0].value = 'Setpoint'
        data_vector[1] = 20 # not added
        data_vector.set(5, 'Setpoint')
        data_vector[6] = 40

        # collect write
        self.interface._collect_fields(blocks_list, data_vector, HOLDINGS_DEFINITIONS, False)
        assert len(blocks_list) == 2
        # blocks
        assert blocks_list[1].type_name == "holding"
        assert not blocks_list[1].read_not_write
        assert len(blocks_list[1]) == 2
        # block
        assert blocks_list[1][0].first_index == 0
        assert blocks_list[1][0].overall_count == 1
        assert blocks_list[1][1].first_index == 5
        assert blocks_list[1][1].overall_count == 2
        assert len(blocks_list[1][1]) == 2
        # part
        assert blocks_list[1][1][0].field.value == 'Setpoint'
        assert blocks_list[1][1][1].field.value == 40

        self.interface._send_and_integrate(blocks_list)
        assert len(FakeModbus.telegram_list) == 5
        assert type(FakeModbus.telegram_list[0]) is LuxtronikSmartHomeReadHoldingsTelegram
        assert FakeModbus.telegram_list[0].addr == 10000 + 0
        assert FakeModbus.telegram_list[0].count == 1
        assert type(FakeModbus.telegram_list[1]) is LuxtronikSmartHomeReadHoldingsTelegram
        assert FakeModbus.telegram_list[1].addr == 10000 + 2
        assert FakeModbus.telegram_list[1].count == 1
        assert type(FakeModbus.telegram_list[2]) is LuxtronikSmartHomeReadHoldingsTelegram
        assert FakeModbus.telegram_list[2].addr == 10000 + 5
        assert FakeModbus.telegram_list[2].count == 3
        assert type(FakeModbus.telegram_list[3]) is LuxtronikSmartHomeWriteHoldingsTelegram
        assert FakeModbus.telegram_list[3].addr == 10000 + 0
        assert FakeModbus.telegram_list[3].count == 1
        assert type(FakeModbus.telegram_list[4]) is LuxtronikSmartHomeWriteHoldingsTelegram
        assert FakeModbus.telegram_list[4].addr == 10000 + 5
        assert FakeModbus.telegram_list[4].count == 2


    def test_collect_field2(self):
        self.interface._blocks_list = []

        h2 = self.interface.holdings.get(2).create_field()
        h3 = self.interface.holdings.get(3).create_field()
        i105 = self.interface.inputs.get(105).create_field()
        i109 = self.interface.inputs.get(109).create_field()

        # collect supported
        h2.raw = 2
        field = self.interface.collect_holding_for_read(h2)
        assert len(self.interface._blocks_list) == 1
        assert self.interface._blocks_list[0].type_name == "holding"
        assert self.interface._blocks_list[0].read_not_write
        assert field == h2
        assert field.raw == 2

        h2.raw = 2
        h2.write_pending = True
        field = self.interface.collect_holding_for_write(h2)
        assert len(self.interface._blocks_list) == 2
        assert self.interface._blocks_list[1].type_name == "holding"
        assert not self.interface._blocks_list[1].read_not_write
        assert field == h2
        assert field.raw == 2
        assert field.write_pending

        h2.raw = 2
        h2.write_pending = True
        field = self.interface.collect_holding(h2)
        assert len(self.interface._blocks_list) == 4
        assert self.interface._blocks_list[2].type_name == "holding"
        assert not self.interface._blocks_list[2].read_not_write
        assert self.interface._blocks_list[3].type_name == "holding"
        assert self.interface._blocks_list[3].read_not_write
        assert field == h2
        assert field.raw == 2
        assert field.write_pending

        i105.raw = 105
        field = self.interface.collect_input(i105)
        assert len(self.interface._blocks_list) == 5
        assert self.interface._blocks_list[4].type_name == "input"
        assert self.interface._blocks_list[4].read_not_write
        assert field == i105
        assert field.raw == 105

        # not collect not supported
        h3.raw = 3
        field = self.interface.collect_holding_for_read(h3)
        assert len(self.interface._blocks_list) == 5
        assert field is None
        assert h3.raw is None

        h3.raw = 3
        h3.write_pending = True
        field = self.interface.collect_holding_for_write(h3)
        assert len(self.interface._blocks_list) == 5
        assert field is None
        assert h3.raw == 3
        assert h3.write_pending

        h3.raw = 3
        h3.write_pending = True
        field = self.interface.collect_holding(h3)
        assert len(self.interface._blocks_list) == 5
        assert field is None
        assert h3.raw == 3
        assert h3.write_pending

        i109.raw = 109
        field = self.interface.collect_input(i109)
        assert len(self.interface._blocks_list) == 5
        assert field is None
        assert i109.raw is None

        # not collect not existing
        field = self.interface.collect_holding_for_read(4)
        assert len(self.interface._blocks_list) == 5
        assert field is None

        field = self.interface.collect_holding_for_write(4)
        assert len(self.interface._blocks_list) == 5
        assert field is None

        field = self.interface.collect_holding(4)
        assert len(self.interface._blocks_list) == 5
        assert field is None

        field = self.interface.collect_input(115)
        assert len(self.interface._blocks_list) == 5
        assert field is None

        self.interface.send()
        assert len(self.interface._blocks_list) == 0

    def test_collect_fields2(self):
        self.interface._blocks_list = []

        h = self.interface.create_holdings()
        self.interface.collect_holdings_for_read(h)
        assert len(self.interface._blocks_list) == 1
        assert self.interface._blocks_list[0].type_name == "holding"
        assert self.interface._blocks_list[0].read_not_write

        self.interface.collect_holdings_for_read(h[0])
        assert len(self.interface._blocks_list) == 1

        # nothing to write
        self.interface.collect_holdings_for_write(self.interface.create_holdings())
        assert len(self.interface._blocks_list) == 1

        self.interface.collect_holdings_for_write(h[0])
        assert len(self.interface._blocks_list) == 1

        h[0] = 'Setpoint'
        self.interface.collect_holdings(h)
        assert len(self.interface._blocks_list) == 3
        assert self.interface._blocks_list[1].type_name == "holding"
        assert not self.interface._blocks_list[1].read_not_write
        assert self.interface._blocks_list[2].type_name == "holding"
        assert self.interface._blocks_list[2].read_not_write

        self.interface.collect_holdings(h[0])
        assert len(self.interface._blocks_list) == 3

        i = self.interface.create_inputs()
        self.interface.collect_inputs(i)
        assert len(self.interface._blocks_list) == 4
        assert self.interface._blocks_list[3].type_name == "input"
        assert self.interface._blocks_list[3].read_not_write

        self.interface.collect_inputs(i[0])
        assert len(self.interface._blocks_list) == 4

        d = self.interface.create_data()
        self.interface.collect_data_for_read(d)
        assert len(self.interface._blocks_list) == 6
        assert self.interface._blocks_list[4].type_name == "holding"
        assert self.interface._blocks_list[4].read_not_write
        assert self.interface._blocks_list[5].type_name == "input"
        assert self.interface._blocks_list[5].read_not_write

        self.interface.collect_data_for_read(i)
        assert len(self.interface._blocks_list) == 6

        d.holdings[0] = 'Setpoint'
        self.interface.collect_data_for_write(d)
        assert len(self.interface._blocks_list) == 7
        assert self.interface._blocks_list[6].type_name == "holding"
        assert not self.interface._blocks_list[6].read_not_write

        self.interface.collect_data_for_write(h)
        assert len(self.interface._blocks_list) == 7

        self.interface.collect_data(d)
        assert len(self.interface._blocks_list) == 10
        assert self.interface._blocks_list[7].type_name == "holding"
        assert not self.interface._blocks_list[7].read_not_write
        assert self.interface._blocks_list[8].type_name == "holding"
        assert self.interface._blocks_list[8].read_not_write
        assert self.interface._blocks_list[9].type_name == "input"
        assert self.interface._blocks_list[9].read_not_write

        self.interface.collect_data(None)
        assert len(self.interface._blocks_list) == 10

        self.interface.send()
        assert len(self.interface._blocks_list) == 0

    def test_create_holding(self):

        # supported
        def_2 = self.interface.holdings.get(2)
        field_2 = self.interface.create_holding(2)
        assert isinstance(def_2, LuxtronikDefinition)
        assert isinstance(field_2, Base)
        assert def_2.name == field_2.name

        # not supported
        def_3 = self.interface.holdings.get(3)
        field_3 = self.interface.create_holding(3)
        assert isinstance(def_3, LuxtronikDefinition)
        assert field_3 is None

        # not existing
        def_4 = self.interface.holdings.get(4)
        field_4 = self.interface.create_holding(4)
        assert def_4 is None
        assert field_4 is None

        vector = self.interface.create_holdings(False)
        assert not vector.safe
        # supported
        field = vector[2]
        assert isinstance(field, Base)
        assert field_2.name == field.name
        # not supported
        field = vector[3]
        assert field is None

        vector = self.interface.create_holdings(True)
        assert vector.safe
        # not existing
        field = vector[4]
        assert field is None

        vector = self.interface.create_empty_holdings(False)
        assert not vector.safe
        assert len(vector) == 0
        # supported but not added
        field = vector[2]
        assert field is None

    def test_read_holding(self):
        FakeModbus.result = False

        # read field with error
        field = self.interface.read_holding(2)
        assert field is None

        # read vector with error
        vector = self.interface.read_holdings()
        assert vector.safe
        # provided data will be integrated
        assert vector[2].raw == 2

        # read empty vector
        vector = self.interface.create_empty_holdings(False)
        self.interface.read_holdings(vector)
        assert not vector.safe
        assert vector[2] is None

        FakeModbus.result = True

        # read field
        field = self.interface.read_holding(2)
        assert field is not None
        assert field.raw == 2

        # read vector
        vector = self.interface.read_holdings()
        assert vector.safe
        assert vector[2].raw == 2

        # read empty vector
        vector = self.interface.create_empty_holdings(False)
        self.interface.read_holdings(vector)
        assert not vector.safe
        assert vector[2] is None

    def test_write_holding(self):

        # prepare
        vector = self.interface.create_empty_holdings(True)
        field_2 = vector.add(2)
        assert len(vector) == 1

        FakeModbus.result = False

        # write field with error
        field = self.interface.write_holding(2, 19)
        assert field is None

        # write vector with error
        field_2.value = 20
        success = self.interface.write_holdings(vector)
        assert not success

        # write None
        success = self.interface.write_holdings(2)
        assert not success

        # write and read vector with error
        field_2.value = 20
        success = self.interface.write_and_read_holdings(vector)
        assert not success

        # write and read None
        success = self.interface.write_and_read_holdings(4)
        assert not success

        FakeModbus.result = True

        # write field
        field = self.interface.write_holding(2, 19)
        assert isinstance(field, Base)
        assert field.value == 19

        # write vector
        field_2.value = 20
        success = self.interface.write_holdings(vector)
        assert success

        # write and read vector
        field_2.value = 20
        success = self.interface.write_and_read_holdings(vector)
        assert success

        # write none
        success = self.interface.write_holdings(None)
        assert not success
        success = self.interface.write_holdings(7)
        assert not success

        # write and read none
        success = self.interface.write_and_read_holdings(None)
        assert not success
        success = self.interface.write_and_read_holdings(18)
        assert not success

    def test_create_input(self):

        # supported
        def_105 = self.interface.inputs.get(105)
        field_105 = self.interface.create_input(105)
        assert isinstance(def_105, LuxtronikDefinition)
        assert isinstance(field_105, Base)
        assert def_105.name == field_105.name

        # not supported
        def_109 = self.interface.inputs.get(109)
        field_109 = self.interface.create_input(109)
        assert isinstance(def_109, LuxtronikDefinition)
        assert field_109 is None

        # not existing
        def_115 = self.interface.inputs.get(115)
        field_115 = self.interface.create_input(115)
        assert def_115 is None
        assert field_115 is None

        vector = self.interface.create_inputs()
        assert vector.safe
        # supported
        field = vector[105]
        assert isinstance(field, Base)
        assert field_105.name == field.name
        # not supported
        field = vector[109]
        assert field is None
        # not existing
        field = vector[115]
        assert field is None

        vector = self.interface.create_empty_holdings()
        assert vector.safe
        assert len(vector) == 0
        # supported but not added
        field = vector[105]
        assert field is None

    def test_read_input(self):
        FakeModbus.result = False

        # read field with error
        field = self.interface.read_input(105)
        assert field is None

        # read vector with error
        vector = self.interface.read_inputs()
        assert vector.safe
        # provided data will be integrated
        assert vector[105].raw == 105

        # read empty vector
        vector = self.interface.create_empty_inputs()
        self.interface.read_inputs(vector)
        assert vector.safe
        assert vector[105] is None

        FakeModbus.result = True

        # read field
        field = self.interface.read_input(105)
        assert field is not None
        assert field.raw == 105

        # read vector
        vector = self.interface.read_inputs()
        assert vector.safe
        assert vector[105].raw == 105

        # read empty vector
        vector = self.interface.create_empty_inputs()
        self.interface.read_inputs(vector)
        assert vector.safe
        assert vector[105] is None

    def test_create_data(self):

        data = self.interface.create_data(False)
        assert not data.holdings.safe
        # supported
        field = data.holdings[2]
        assert isinstance(field, Base)
        # not supported
        field = data.holdings[3]
        assert field is None

        data = self.interface.create_data(True)
        assert data.holdings.safe
        # not existing
        field = data.holdings[4]
        assert field is None

        data = self.interface.create_empty_data(False)
        assert not data.holdings.safe
        assert len(data.holdings) == 0
        assert len(data.inputs) == 0
        # supported but not added
        field = data.holdings[2]
        assert field is None

    def test_read_data(self):
        FakeModbus.result = False

        # read data with error
        data = self.interface.read_data()
        assert data.holdings.safe
        # provided data will be integrated
        assert data.holdings[2].raw == 2

        data = self.interface.read()
        assert data.holdings.safe
        # provided data will be integrated
        assert data.holdings[2].raw == 2

        # read empty data
        data = self.interface.create_empty_data(False)
        self.interface.read_data(data)
        assert not data.holdings.safe
        assert data.holdings[2] is None

        FakeModbus.result = True

        # read data
        data = self.interface.read_data()
        assert data.holdings.safe
        assert data.holdings[2].raw == 2

        data = self.interface.read()
        assert data.holdings.safe
        assert data.holdings[2].raw == 2

        # read empty data
        data = self.interface.create_empty_data(False)
        self.interface.read_data(data)
        assert not data.holdings.safe
        assert data.holdings[2] is None

    def test_write_data(self):

        # prepare
        data = self.interface.create_empty_data(True)
        field_2 = data.holdings.add(2)
        assert len(data.holdings) == 1

        FakeModbus.result = False

        # write data with error
        field_2.value = 20
        success = self.interface.write_data(data)
        assert not success

        field_2.value = 20
        success = self.interface.write(data)
        assert not success

        # write None
        success = self.interface.write(None)
        assert not success

        # write and read data with error
        field_2.value = 20
        success = self.interface.write_and_read_data(data)
        assert not success

        field_2.value = 20
        success = self.interface.write_and_read(data)
        assert not success

        # write and read None
        success = self.interface.write_and_read(None)
        assert not success

        FakeModbus.result = True

        # write vector
        field_2.value = 20
        success = self.interface.write_data(data)
        assert success

        field_2.value = 20
        success = self.interface.write(data)
        assert success

        # write and read data
        field_2.value = 20
        success = self.interface.write_and_read_data(data)
        assert success

        field_2.value = 20
        success = self.interface.write_and_read(data)
        assert success

        # write none
        success = self.interface.write_data(None)
        assert not success

        success = self.interface.write(None)
        assert not success

        # write and read none
        success = self.interface.write_and_read_data(None)
        assert not success

        success = self.interface.write_and_read(None)
        assert not success

    def test_raw(self):
        FakeModbus.result = False

        data = self.interface.read_holding_raw(1, 3)
        assert data is None

        success = self.interface.write_holding_raw(1, [7, 6, 3])
        assert not success

        data = self.interface.read_input_raw(2, 5)
        assert data is None

        FakeModbus.result = True

        data = self.interface.read_holding_raw(1, 3)
        assert data == [1, 2, 3]

        success = self.interface.write_holding_raw(1, [7, 6, 3])
        assert success

        data = self.interface.read_input_raw(2, 5)
        assert data == [2, 3, 4, 5, 6]

    def test_read_then_write(self):
        field = self.interface.create_holding(2)

        field.value = 20
        self.interface.collect_holding_for_read(field)
        assert field.value == 20

        self.interface.collect_holding_for_write(field, 32)
        assert field.value == 32

        self.interface.read_input(0)
        assert len(FakeModbus.telegram_list) == 3
        assert FakeModbus.telegram_list[0].data == [2]
        assert FakeModbus.telegram_list[1].data == [32 * 10]
        assert FakeModbus.telegram_list[2].data == [0]

        assert field.raw == 2

    def test_write_then_read(self):
        field = self.interface.create_holding(2)

        self.interface.collect_holding_for_write(field, 32)
        assert field.value == 32

        self.interface.collect_holding_for_read(field)
        assert field.value == 32

        field.value = 42

        self.interface.read_input(0)
        assert len(FakeModbus.telegram_list) == 3
        assert FakeModbus.telegram_list[0].data == [42 * 10]
        assert FakeModbus.telegram_list[1].data == [2]
        assert FakeModbus.telegram_list[2].data == [0]

        assert field.raw == 2

    def test_trial_and_error_mode(self):

        # prepare
        interface = LuxtronikSmartHomeInterface(FakeModbus(), None)

        holdings = Holdings.empty(None)
        h0 = holdings.add(0) # 3.90.1
        h1 = holdings.add(1) # 3.90.1
        h2 = holdings.add(2) # 3.90.1
        h3 = holdings.add(3) # 3.92.0
        h4 = holdings.add(4)
        assert h4 is None

        # add vector for read
        interface.collect_holdings_for_read(holdings)
        assert len(interface._blocks_list) == 1
        assert len(interface._blocks_list[0]) == 4
        assert len(interface._blocks_list[0][0]) == 1
        assert interface._blocks_list[0][0][0].field == h0
        assert len(interface._blocks_list[0][1]) == 1
        assert interface._blocks_list[0][1][0].field == h1
        assert len(interface._blocks_list[0][2]) == 1
        assert interface._blocks_list[0][2][0].field == h2
        assert len(interface._blocks_list[0][3]) == 1
        assert interface._blocks_list[0][3][0].field == h3

        # add vector for write
        h1.raw = 10
        h1.write_pending = True
        h3.raw = 1
        h3.write_pending = True
        interface.collect_holdings_for_write(holdings)
        assert len(interface._blocks_list) == 2
        assert len(interface._blocks_list[1]) == 2
        assert len(interface._blocks_list[1][0]) == 1
        assert interface._blocks_list[1][0][0].field == h1
        assert len(interface._blocks_list[1][1]) == 1
        assert interface._blocks_list[1][1][0].field == h3

        # add not existing read (success)
        field = interface.collect_holding_for_read('unknown_foo_4')
        assert type(field) is Unknown
        assert len(interface._blocks_list) == 3
        assert len(interface._blocks_list[2]) == 1
        assert len(interface._blocks_list[2][0]) == 1
        assert interface._blocks_list[2][0][0].definition.name == 'unknown_holding_4'
        assert interface._blocks_list[2][0][0].definition.index == 4
        assert interface._blocks_list[2][0][0].definition.count == 1
        assert interface._blocks_list[2][0][0].field.name == 'unknown_holding_4'
        assert not interface._blocks_list[2][0][0].field.writeable

        # add not existing read (fail)
        field = interface.collect_holding_for_read('bar_foo_4')
        assert field is None
        assert len(interface._blocks_list) == 3

        # add not existing write (success)
        field = interface.collect_holding_for_write('unknown_bar_4', 16, False)
        assert type(field) is Unknown
        assert len(interface._blocks_list) == 4
        assert len(interface._blocks_list[3]) == 1
        assert len(interface._blocks_list[3][0]) == 1
        assert interface._blocks_list[3][0][0].field.name == 'unknown_holding_4'
        assert not interface._blocks_list[3][0][0].field.writeable

        # add not existing write (success)
        field = interface.collect_holding_for_write('unknown_bar_4', 17, True)
        assert field is None
        assert len(interface._blocks_list) == 4

        interface.send()
        offset = interface.holdings.offset
        assert len(FakeModbus.telegram_list) == 8
        assert type(FakeModbus.telegram_list[0]) is LuxtronikSmartHomeReadHoldingsTelegram
        assert FakeModbus.telegram_list[0].addr == offset + 0
        assert FakeModbus.telegram_list[0].count == 1
        assert type(FakeModbus.telegram_list[1]) is LuxtronikSmartHomeReadHoldingsTelegram
        assert FakeModbus.telegram_list[1].addr == offset + 1
        assert FakeModbus.telegram_list[1].count == 1
        assert type(FakeModbus.telegram_list[2]) is LuxtronikSmartHomeReadHoldingsTelegram
        assert FakeModbus.telegram_list[2].addr == offset + 2
        assert FakeModbus.telegram_list[2].count == 1
        assert type(FakeModbus.telegram_list[3]) is LuxtronikSmartHomeReadHoldingsTelegram
        assert FakeModbus.telegram_list[3].addr == offset + 3
        assert FakeModbus.telegram_list[3].count == 1
        assert type(FakeModbus.telegram_list[4]) is LuxtronikSmartHomeWriteHoldingsTelegram
        assert FakeModbus.telegram_list[4].addr == offset + 1
        assert FakeModbus.telegram_list[4].count == 1
        assert FakeModbus.telegram_list[4].data == [10]
        assert type(FakeModbus.telegram_list[5]) is LuxtronikSmartHomeWriteHoldingsTelegram
        assert FakeModbus.telegram_list[5].addr == offset + 3
        assert FakeModbus.telegram_list[5].count == 1
        assert FakeModbus.telegram_list[5].data == [1]
        assert type(FakeModbus.telegram_list[6]) is LuxtronikSmartHomeReadHoldingsTelegram
        assert FakeModbus.telegram_list[6].addr == offset + 4
        assert FakeModbus.telegram_list[6].count == 1
        assert type(FakeModbus.telegram_list[7]) is LuxtronikSmartHomeWriteHoldingsTelegram
        assert FakeModbus.telegram_list[7].addr == offset + 4
        assert FakeModbus.telegram_list[7].count == 1
        assert FakeModbus.telegram_list[7].data == [16]


    def check_definitions(self, interface):
        definitions = interface.get_holdings(False)
        vector = interface.create_holdings()
        assert definitions._version == vector.version
        assert len(definitions) <= len(interface.holdings)
        for d in definitions:
            assert d.name in vector
            assert d in interface.holdings
        for f in vector:
            assert f.name in definitions
            assert f.name in interface.holdings

        definitions = interface.get_inputs(False)
        vector = interface.create_inputs()
        assert definitions._version == vector.version
        assert len(definitions) <= len(interface.inputs)
        for d in definitions:
            assert d.name in vector
            assert d in interface.inputs
        for f in vector:
            assert f.name in definitions
            assert f.name in interface.inputs

    def test_create_modbus(self):
        interface = create_modbus_tcp('host', version=None)
        assert interface.version is None
        self.check_definitions(interface)

        interface = create_modbus_tcp('host', version=1)
        assert interface.version is None
        self.check_definitions(interface)

        interface = create_modbus_tcp('host', version="1.2.3")
        assert interface.version == (1, 2, 3, 0)
        self.check_definitions(interface)

        interface = create_modbus_tcp('host', version="latest")
        assert interface.version == LUXTRONIK_LATEST_SHI_VERSION
        self.check_definitions(interface)

        interface = create_modbus_tcp('host', version=LUXTRONIK_FIRST_VERSION_WITH_SHI)
        assert interface.version == LUXTRONIK_FIRST_VERSION_WITH_SHI
        self.check_definitions(interface)

        interface = create_modbus_tcp('host')
        assert interface.version == (400, 401, 402, 0)
        self.check_definitions(interface)

        FakeModbus.result = False

        interface = create_modbus_tcp('host')
        assert interface.version is None
        self.check_definitions(interface)

        FakeModbus.result = True
