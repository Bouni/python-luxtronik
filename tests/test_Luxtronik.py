from unittest.mock import patch

from luxtronik.shi import LuxtronikSmartHomeInterface
from luxtronik.shi.interface import LuxtronikSmartHomeData
from luxtronik import (
    LuxtronikData,
    Parameters,
    Holdings,
    LuxtronikSocketInterface,
    LuxtronikAllData,
    LuxtronikInterface,
    Luxtronik
)

###############################################################################
# Fake interfaces
###############################################################################

class FakeSocketInterface(LuxtronikSocketInterface):

    write_counter = 0
    read_counter = 0

    @classmethod
    def reset(cls):
        FakeSocketInterface.write_counter = 0
        FakeSocketInterface.read_counter = 0

    def read(self, data):
        FakeSocketInterface.read_parameters(self, data.parameters)
        FakeSocketInterface.read_visibilities(self, data.visibilities)
        FakeSocketInterface.read_calculations(self, data.calculations)

    def read_parameters(self, parameters):
        parameters.get(0).raw = 2
        FakeSocketInterface.read_counter += 1

    def read_visibilities(self, visibilities):
        visibilities.get(0).raw = 4
        FakeSocketInterface.read_counter += 1

    def read_calculations(self, calculations):
        calculations.get(0).raw = 6
        FakeSocketInterface.read_counter += 1

    def write(self, data):
        FakeSocketInterface.write_counter += 1

class FakeShiInterface(LuxtronikSmartHomeInterface):

    write_counter = 0
    read_counter = 0

    @classmethod
    def reset(cls):
        FakeShiInterface.write_counter = 0
        FakeShiInterface.read_counter = 0

    def read(self, data):
        FakeShiInterface.read_inputs(self, data.inputs)
        FakeShiInterface.read_holdings(self, data.holdings)

    def read_inputs(self, inputs):
        inputs[0].raw = 3
        FakeShiInterface.read_counter += 1

    def read_holdings(self, holdings):
        holdings[1].raw = 5
        FakeShiInterface.read_counter += 1

    def write(self, data):
        return FakeShiInterface.write_holdings(self, data.holdings)

    def write_holdings(self, holdings):
        FakeShiInterface.write_counter += 1
        return True

def fake_resolve_version(modbus_interface):
    return (3, 99, 11, 0)

###############################################################################
# Tests
###############################################################################

@patch("luxtronik.LuxtronikSocketInterface", FakeSocketInterface)
@patch("luxtronik.LuxtronikSocketInterface.read_parameters", FakeSocketInterface.read_parameters)
@patch("luxtronik.LuxtronikSocketInterface.read_visibilities", FakeSocketInterface.read_visibilities)
@patch("luxtronik.LuxtronikSocketInterface.read_calculations", FakeSocketInterface.read_calculations)
@patch("luxtronik.LuxtronikSmartHomeInterface", FakeShiInterface)
@patch("luxtronik.LuxtronikSmartHomeInterface.read_inputs", FakeShiInterface.read_inputs)
@patch("luxtronik.LuxtronikSmartHomeInterface.read_holdings", FakeShiInterface.read_holdings)
@patch("luxtronik.resolve_version", fake_resolve_version)
class TestLuxtronik:

    def test_if_init(self):
        lux = LuxtronikInterface('host', 1234, 5678)

        assert lux._host == 'host'
        assert lux._port == 1234
        assert lux._interface._client._port == 5678
        assert lux.version == (3, 99, 11, 0)

    def test_if_lock(self):
        lux = LuxtronikInterface('host', 1234, 5678)
        lux.lock.acquire(blocking=False)
        lux.lock.acquire(blocking=False)
        lux.lock.release()
        lux.lock.release()

    def test_if_create_all_data(self):
        lux = LuxtronikInterface('host', 1234, 5678)

        data = lux.create_all_data()
        assert type(data) is LuxtronikAllData

    def test_if_read_all(self):
        FakeSocketInterface.reset()
        FakeShiInterface.reset()
        lux = LuxtronikInterface('host', 1234, 5678)

        assert FakeSocketInterface.read_counter == 0
        assert FakeShiInterface.read_counter == 0

        data1 = lux.read_all()
        assert type(data1) is LuxtronikAllData
        assert data1.parameters.get(0).raw == 2
        assert data1.inputs[0].raw == 3
        assert FakeSocketInterface.read_counter == 3
        assert FakeShiInterface.read_counter == 2

        data2 = lux.read(data1)
        assert data1 == data2
        assert FakeSocketInterface.read_counter == 6
        assert FakeShiInterface.read_counter == 4

    def test_if_write_all(self):
        FakeSocketInterface.reset()
        FakeShiInterface.reset()
        lux = LuxtronikInterface('host', 1234, 5678)

        assert FakeSocketInterface.write_counter == 0
        assert FakeShiInterface.write_counter == 0

        p = Parameters()
        result = lux.write_all(p)
        assert result
        assert FakeSocketInterface.write_counter == 1
        assert FakeShiInterface.write_counter == 0

        d = LuxtronikAllData()
        data = lux.write_and_read(p, d)
        assert data == d
        assert data.inputs[0].raw == 3
        assert FakeSocketInterface.write_counter == 2
        assert FakeShiInterface.write_counter == 0

        h = Holdings()
        result = lux.write_all(h)
        assert result
        assert FakeSocketInterface.write_counter == 2
        assert FakeShiInterface.write_counter == 1

        s = LuxtronikSmartHomeData()
        result = lux.write(s)
        assert result
        assert FakeSocketInterface.write_counter == 2
        assert FakeShiInterface.write_counter == 2

        a = LuxtronikData()
        result = lux.write(a)
        assert result
        assert FakeSocketInterface.write_counter == 3
        assert FakeShiInterface.write_counter == 2

        result = lux.write_all(None)
        assert not result
        assert FakeSocketInterface.write_counter == 3
        assert FakeShiInterface.write_counter == 2

        d = LuxtronikAllData()
        data = lux.write_and_read(d, d)
        assert data == d
        assert data.inputs[0].raw == 3
        assert FakeSocketInterface.write_counter == 4
        assert FakeShiInterface.write_counter == 3

    def test_lux_init(self):
        lux = Luxtronik('host', 1234, 5678)

        assert isinstance(lux, LuxtronikAllData)
        assert isinstance(lux.interface, LuxtronikInterface)

    def test_read(self):
        FakeSocketInterface.reset()
        FakeShiInterface.reset()
        lux = Luxtronik('host', 1234, 5678)

        assert FakeSocketInterface.read_counter == 3
        assert FakeShiInterface.read_counter == 2

        lux.read()
        assert lux.parameters.get(0).raw == 2
        assert lux.inputs[0].raw == 3
        assert FakeSocketInterface.read_counter == 6
        assert FakeShiInterface.read_counter == 4

    def test_read_parameters(self):
        FakeSocketInterface.reset()
        FakeShiInterface.reset()
        lux = Luxtronik('host', 1234, 5678)

        assert FakeSocketInterface.read_counter == 3
        assert FakeShiInterface.read_counter == 2

        lux.read_parameters()
        assert lux.parameters.get(0).raw == 2
        assert lux.inputs[0].raw == 3
        assert FakeSocketInterface.read_counter == 4
        assert FakeShiInterface.read_counter == 2

    def test_read_visibilities(self):
        FakeSocketInterface.reset()
        FakeShiInterface.reset()
        lux = Luxtronik('host', 1234, 5678)

        assert FakeSocketInterface.read_counter == 3
        assert FakeShiInterface.read_counter == 2

        lux.read_visibilities()
        assert lux.visibilities.get(0).raw == 4
        assert lux.inputs[0].raw == 3
        assert FakeSocketInterface.read_counter == 4
        assert FakeShiInterface.read_counter == 2

    def test_read_calculations(self):
        FakeSocketInterface.reset()
        FakeShiInterface.reset()
        lux = Luxtronik('host', 1234, 5678)

        assert FakeSocketInterface.read_counter == 3
        assert FakeShiInterface.read_counter == 2

        lux.read_calculations()
        assert lux.calculations.get(0).raw == 6
        assert lux.inputs[0].raw == 3
        assert FakeSocketInterface.read_counter == 4
        assert FakeShiInterface.read_counter == 2

    def test_read_inputs(self):
        FakeSocketInterface.reset()
        FakeShiInterface.reset()
        lux = Luxtronik('host', 1234, 5678)

        assert FakeSocketInterface.read_counter == 3
        assert FakeShiInterface.read_counter == 2

        lux.read_inputs()
        assert lux.parameters.get(0).raw == 2
        assert lux.inputs[0].raw == 3
        assert FakeSocketInterface.read_counter == 3
        assert FakeShiInterface.read_counter == 3

    def test_read_holdings(self):
        FakeSocketInterface.reset()
        FakeShiInterface.reset()
        lux = Luxtronik('host', 1234, 5678)

        assert FakeSocketInterface.read_counter == 3
        assert FakeShiInterface.read_counter == 2

        lux.read_holdings()
        assert lux.parameters.get(0).raw == 2
        assert lux.holdings[1].raw == 5
        assert FakeSocketInterface.read_counter == 3
        assert FakeShiInterface.read_counter == 3

    def test_write(self):
        FakeSocketInterface.reset()
        FakeShiInterface.reset()
        lux = Luxtronik('host', 1234, 5678)

        assert FakeSocketInterface.write_counter == 0
        assert FakeSocketInterface.read_counter == 3
        assert FakeShiInterface.write_counter == 0
        assert FakeShiInterface.read_counter == 2

        result = lux.write()
        assert result
        assert FakeSocketInterface.write_counter == 1
        assert FakeSocketInterface.read_counter == 3
        assert FakeShiInterface.write_counter == 1
        assert FakeShiInterface.read_counter == 2

        data = LuxtronikAllData()
        result = lux.write(data)
        assert result
        assert FakeSocketInterface.write_counter == 2
        assert FakeSocketInterface.read_counter == 3
        assert FakeShiInterface.write_counter == 2
        assert FakeShiInterface.read_counter == 2

    def test_write_and_read(self):
        FakeSocketInterface.reset()
        FakeShiInterface.reset()
        lux = Luxtronik('host', 1234, 5678)

        assert FakeSocketInterface.write_counter == 0
        assert FakeSocketInterface.read_counter == 3
        assert FakeShiInterface.write_counter == 0
        assert FakeShiInterface.read_counter == 2

        result = lux.write_and_read()
        assert result
        assert FakeSocketInterface.write_counter == 1
        assert FakeSocketInterface.read_counter == 6
        assert FakeShiInterface.write_counter == 1
        assert FakeShiInterface.read_counter == 4

        data = LuxtronikAllData()
        result = lux.write_and_read(data)
        assert result
        assert FakeSocketInterface.write_counter == 2
        assert FakeSocketInterface.read_counter == 9
        assert FakeShiInterface.write_counter == 2
        assert FakeShiInterface.read_counter == 6
