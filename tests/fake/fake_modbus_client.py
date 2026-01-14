
from pyModbusTCP.client import ModbusClient


class FakeModbusClient(ModbusClient):
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