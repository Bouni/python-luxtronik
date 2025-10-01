import pytest

from luxtronik.shi.common import (
    LuxtronikSmartHomeReadTelegram,
    LuxtronikSmartHomeReadHoldingsTelegram,
    LuxtronikSmartHomeReadInputsTelegram,
    LuxtronikSmartHomeWriteTelegram,
    LuxtronikSmartHomeWriteHoldingsTelegram,
)
from luxtronik.shi.modbus import LuxtronikModbusTcpInterface

###############################################################################
# Fake modbus client
###############################################################################

class FakeModbusClient:
    can_connect = True
    can_disconnect = True

    def __init__(self, host, port=0, timeout=0, *args, **kwargs):
        self._host = host
        self._port = port
        self._timeout = timeout
        self._connected = False
        self._error = 'None'

    def open(self):
        if self.can_connect:
            self._connected = True
        self._error = 'None' if self.can_connect else 'Connection error!'
        return self.can_connect

    def close(self):
        if self.can_disconnect:
            self._connected = False
        self._error = 'None' if self.can_disconnect else 'Disconnection error!'
        return self.can_disconnect

    @property
    def is_open(self):
        return self._connected

    @property
    def last_error_as_txt(self):
        return self._error

    def _read(self, addr, count):
        if addr == 1000:
            # Return None
            self._error = 'Read returned "None"!'
            return None
        elif addr == 1001:
            # Return empty data
            self._error = 'Read returned to less data!'
            return []
        elif addr == 1002:
            # Return too much data
            self._error = 'Read returned to few data!'
            return [0] * 16
        elif addr == 1003:
            # Exception
            self._error = 'Exception!'
            raise
        else:
            # Return the addr as value(s)
            self._error = 'None'
            values = []
            for i in range(count):
                values += [addr + i]
            return values

    def read_holding_registers(self, addr, count):
        return self._read(addr, count)

    def read_input_registers(self, addr, count):
        return self._read(addr, count)

    def write_multiple_registers(self, addr, data):
        if addr == 1000:
            # Return false
            self._error = 'Write error!'
            return False
        elif addr == 1001:
            # Exception
            self._error = 'Exception!'
            raise
        else:
            # Return true
            self._error = 'None'
            return True

###############################################################################
# Tests
###############################################################################

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

        result = self.modbus_interface._connect()
        assert result
        assert self.modbus_interface._client._connected

        # repeated connect
        result = self.modbus_interface._connect()
        assert result
        assert self.modbus_interface._client._connected

        result = self.modbus_interface._disconnect()
        assert result
        assert not self.modbus_interface._client._connected

        # repeated disconnect
        result = self.modbus_interface._disconnect()
        assert result
        assert not self.modbus_interface._client._connected

        FakeModbusClient.can_connect = False

        result = self.modbus_interface._connect()
        assert not result
        assert not self.modbus_interface._client._connected

        result = self.modbus_interface._disconnect()
        assert result
        assert not self.modbus_interface._client._connected

        FakeModbusClient.can_connect = True

        FakeModbusClient.can_disconnect = False

        result = self.modbus_interface._connect()
        assert result
        assert self.modbus_interface._client._connected

        result = self.modbus_interface._disconnect()
        assert not result
        assert self.modbus_interface._client._connected

        FakeModbusClient.can_disconnect = True

        result = self.modbus_interface._disconnect()
        assert result
        assert not self.modbus_interface._client._connected

    def test_no_connection(self):
        FakeModbusClient.can_connect = False

        data = LuxtronikSmartHomeReadHoldingsTelegram(0, 1)
        result = self.modbus_interface.send(data)
        print(data.data)
        assert not result

        data = LuxtronikSmartHomeWriteHoldingsTelegram(0, [1])
        result = self.modbus_interface.send(data)
        assert not result

        data = LuxtronikSmartHomeReadInputsTelegram(0, 1)
        result = self.modbus_interface.send(data)
        assert not result

        FakeModbusClient.can_connect = True

    def test_lock(self):
        assert self.modbus_interface.lock.acquire(blocking=False)
        assert self.modbus_interface.lock.acquire(blocking=False)
        assert self.modbus_interface.lock.acquire(blocking=False)
        self.modbus_interface.lock.release()
        self.modbus_interface.lock.release()
        self.modbus_interface.lock.release()

    def test_data_type(self):

        result = self.modbus_interface.send('data')
        assert not result

        result = self.modbus_interface.send(0)
        assert not result

        result = self.modbus_interface.send([2, 1])
        assert not result

        t = LuxtronikSmartHomeReadTelegram(1, 1)
        result = self.modbus_interface.send(t)
        assert not result

        t = LuxtronikSmartHomeReadHoldingsTelegram(1, 1)
        result = self.modbus_interface.send(t)
        assert result

        t = LuxtronikSmartHomeWriteTelegram(1, [1])
        result = self.modbus_interface.send(t)
        assert not result

        t = LuxtronikSmartHomeWriteHoldingsTelegram(1, [1])
        result = self.modbus_interface.send(t)
        assert result

    def test_no_holdings_read_data(self):
        data_list = [LuxtronikSmartHomeReadHoldingsTelegram(0, 0), LuxtronikSmartHomeReadHoldingsTelegram(0, 0)]

        result = self.modbus_interface.send(data_list)
        assert not result
        assert data_list[0].data == []
        assert data_list[1].data == []


    def test_no_holdings_write_data(self):
        data_list = [LuxtronikSmartHomeWriteHoldingsTelegram(0, []), LuxtronikSmartHomeWriteHoldingsTelegram(0, [])]

        result = self.modbus_interface.send(data_list)
        assert not result


    def test_no_inputs_read_data(self):
        data_list = [LuxtronikSmartHomeReadInputsTelegram(0, 0), LuxtronikSmartHomeReadInputsTelegram(0, 0)]

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

        result = self.modbus_interface.send(data_item)
        assert result == valid
        assert data_item.data == data

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

        result = self.modbus_interface.send(data_item)
        assert result == valid
        assert data_item.data == data

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

        result = self.modbus_interface.send(data_item)
        assert result == valid

        result = self.modbus_interface.write_holdings(addr, data)
        assert result == valid

    def test_list(self):
        list = [
            LuxtronikSmartHomeReadHoldingsTelegram(3, 7),
            LuxtronikSmartHomeWriteHoldingsTelegram(4, [11, 21]),
            LuxtronikSmartHomeReadInputsTelegram(2, 3),
        ]

        result = self.modbus_interface.send(list)
        assert result
        assert list[0].data == [3, 4, 5, 6, 7, 8, 9]
        assert list[1].data == [11, 21]
        assert list[2].data == [2, 3, 4]

        list[0].addr = 2
        list[0].count = 2
        list[2].count = 0

        result = self.modbus_interface.send(list)
        assert result
        assert list[0].data == [2, 3]
        assert list[1].data == [11, 21]
        assert list[2].data == []
