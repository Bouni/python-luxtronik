import pytest
from unittest.mock import patch

from luxtronik.shi.common import (
    LuxtronikSmartHomeReadTelegram,
    LuxtronikSmartHomeReadHoldingsTelegram,
    LuxtronikSmartHomeReadInputsTelegram,
    LuxtronikSmartHomeWriteTelegram,
    LuxtronikSmartHomeWriteHoldingsTelegram,
    LuxtronikSmartHomeTelegrams,
)
from luxtronik.shi.modbus import LuxtronikModbusTcpInterface
from tests.fake import FakeModbusClient


class DummyTelegram(LuxtronikSmartHomeReadTelegram):
    pass


@patch("luxtronik.shi.modbus.LUXTRONIK_WAIT_TIME_AFTER_HOLDING_WRITE", 0)
@patch("luxtronik.shi.modbus.LuxtronikSmartHomeTelegrams", LuxtronikSmartHomeTelegrams | {DummyTelegram})
class TestModbusInterface:
    host = "local_host"
    port = 9876

    @classmethod
    def setup_class(cls):
        cls.modbus_interface = LuxtronikModbusTcpInterface(cls.host, cls.port)
        cls.modbus_interface._client = FakeModbusClient(cls.host, cls.port)
        assert isinstance(cls.modbus_interface._client, FakeModbusClient)

    def test_connect(self):
        FakeModbusClient.can_connect = True
        FakeModbusClient.can_disconnect = True

        # normal connect()
        result = self.modbus_interface._connect()
        assert result
        assert self.modbus_interface._client._connected

        # repeated connect()
        result = self.modbus_interface._connect()
        assert result
        assert self.modbus_interface._client._connected

        # normal disconnect()
        result = self.modbus_interface._disconnect()
        assert result
        assert not self.modbus_interface._client._connected

        # repeated disconnect()
        result = self.modbus_interface._disconnect()
        assert result
        assert not self.modbus_interface._client._connected

        FakeModbusClient.can_connect = False

        # faulty connect()
        result = self.modbus_interface._connect()
        assert not result
        assert not self.modbus_interface._client._connected

        # disconnect() after faulty connect()
        result = self.modbus_interface._disconnect()
        assert result
        assert not self.modbus_interface._client._connected

        FakeModbusClient.can_connect = True

        FakeModbusClient.can_disconnect = False

        # normal connect()
        result = self.modbus_interface._connect()
        assert result
        assert self.modbus_interface._client._connected

        # faulty disconnect()
        result = self.modbus_interface._disconnect()
        assert not result
        assert self.modbus_interface._client._connected

        FakeModbusClient.can_disconnect = True

        # normal disconnect(), reset internal states
        result = self.modbus_interface._disconnect()
        assert result
        assert not self.modbus_interface._client._connected

        FakeModbusClient.can_connect = True
        FakeModbusClient.can_disconnect = True

    def test_no_connection(self):
        FakeModbusClient.can_connect = False

        # Cannot connect to read holdings
        data = LuxtronikSmartHomeReadHoldingsTelegram(0, 1)
        result = self.modbus_interface.send(data)
        print(data.data)
        assert not result

        # Cannot connect to write holdings
        data = LuxtronikSmartHomeWriteHoldingsTelegram(0, [1])
        result = self.modbus_interface.send(data)
        assert not result

        # Cannot connect to read inputs
        data = LuxtronikSmartHomeReadInputsTelegram(0, 1)
        result = self.modbus_interface.send(data)
        assert not result

        FakeModbusClient.can_connect = True

    def test_lock(self):
        # Acquire lock multiple-times, afterwards release all
        assert self.modbus_interface.lock.acquire(blocking=False)
        assert self.modbus_interface.lock.acquire(blocking=False)
        assert self.modbus_interface.lock.acquire(blocking=False)
        self.modbus_interface.lock.release()
        self.modbus_interface.lock.release()
        self.modbus_interface.lock.release()

    def test_data_type(self):

        # str
        result = self.modbus_interface.send('data')
        assert not result

        # int
        result = self.modbus_interface.send(0)
        assert not result

        # list
        result = self.modbus_interface.send([2, 1])
        assert not result

        # Read-telegram base class
        t = LuxtronikSmartHomeReadTelegram(1, 1)
        result = self.modbus_interface.send(t)
        assert not result

        # Read-holdings-telegram class
        t = LuxtronikSmartHomeReadHoldingsTelegram(1, 1)
        result = self.modbus_interface.send(t)
        assert result

        # Write-telegram base class
        t = LuxtronikSmartHomeWriteTelegram(1, [1])
        result = self.modbus_interface.send(t)
        assert not result

        # Write-holdings-telegram class
        t = LuxtronikSmartHomeWriteHoldingsTelegram(1, [1])
        result = self.modbus_interface.send(t)
        assert result

    def test_no_holdings_read_data(self):
        data_list = [LuxtronikSmartHomeReadHoldingsTelegram(0, 0), LuxtronikSmartHomeReadHoldingsTelegram(0, 0)]

        # Read zero holdings
        result = self.modbus_interface.send(data_list)
        assert not result
        assert data_list[0].data == []
        assert data_list[1].data == []


    def test_no_holdings_write_data(self):
        data_list = [LuxtronikSmartHomeWriteHoldingsTelegram(0, []), LuxtronikSmartHomeWriteHoldingsTelegram(0, [])]

        # Write zero holdings
        result = self.modbus_interface.send(data_list)
        assert not result


    def test_no_inputs_read_data(self):
        data_list = [LuxtronikSmartHomeReadInputsTelegram(0, 0), LuxtronikSmartHomeReadInputsTelegram(0, 0)]

        # Read zero inputs
        result = self.modbus_interface.send(data_list)
        assert not result
        assert data_list[0].data == []
        assert data_list[1].data == []


    @pytest.mark.parametrize(
        "addr, count, valid, data",
        [
            (1,    2, True,  [1, 2]),
            (5,    3, True,  [5, 6, 7]),
            (0,    0, False, []),
            (1000, 2, False, None), # client has read error
            (1001, 3, False, None), # client returns to less data
            (1002, 4, False, None), # client returns to much data
            (1003, 1, False, None), # exception
        ]
    )
    def test_read_holdings(self, addr, count, valid, data):
        data_item = LuxtronikSmartHomeReadHoldingsTelegram(addr, count)

        # read holdings via send()
        result = self.modbus_interface.send(data_item)
        assert result == valid
        assert data_item.data == data

        # read holdings via read_holdings()
        data_arr = self.modbus_interface.read_holdings(addr, count)
        if valid:
            assert data_arr == data
        else:
            assert data_arr is None


    @pytest.mark.parametrize(
        "addr, count, valid, data",
        [
            (1,    2,  True, [1, 2]),
            (5,    3,  True, [5, 6, 7]),
            (0,    0, False, []),
            (1000, 2, False, None), # client has read error
            (1001, 3, False, None), # client returns to less data
            (1002, 4, False, None), # client returns to much data
            (1003, 1, False, None), # exception
        ]
    )
    def test_read_inputs(self, addr, count, valid, data):
        data_item = LuxtronikSmartHomeReadInputsTelegram(addr, count)

        # read inputs via send()
        result = self.modbus_interface.send(data_item)
        assert result == valid
        assert data_item.data == data

        # read holdings via read_inputs()
        data_arr = self.modbus_interface.read_inputs(addr, count)
        if valid:
            assert data_arr == data
        else:
            assert data_arr is None


    @pytest.mark.parametrize(
        "addr, data, valid",
        [
            (1,       [1, 2],  True),
            (5,    [5, 6, 7],  True),
            (0,           [], False),
            (1000,    [8, 9], False), # Write error
            (1001,      [11], False), # Exception
        ]
    )
    def test_write_holdings(self, addr, data, valid):
        data_item = LuxtronikSmartHomeWriteHoldingsTelegram(addr, data)

        # write holdings via send()
        result = self.modbus_interface.send(data_item)
        assert result == valid

        # write holdings via write_holdings()
        result = self.modbus_interface.write_holdings(addr, data)
        assert result == valid

    def test_list(self):
        list = [
            LuxtronikSmartHomeReadHoldingsTelegram(3, 7),
            LuxtronikSmartHomeWriteHoldingsTelegram(4, [11, 21]),
            LuxtronikSmartHomeReadInputsTelegram(2, 3),
        ]

        # all valid
        result = self.modbus_interface.send(list)
        assert result
        assert list[0].data == [3, 4, 5, 6, 7, 8, 9]
        assert list[1].data == [11, 21]
        assert list[2].data == [2, 3, 4]

        # item[2] requests no data
        list[0]._addr = 2
        list[0]._count = 2
        list[2]._count = 0
        result = self.modbus_interface.send(list)
        assert result
        assert list[0].data == [2, 3]
        assert list[1].data == [11, 21]
        assert list[2].data == []

    def test_not_defined(self):
        telegram = DummyTelegram(0, 1)

        try:
            self.modbus_interface.send(telegram)
            assert False
        except Exception:
            pass
