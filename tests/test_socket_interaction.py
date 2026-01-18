"""Test suite for the socket interaction of LuxtronikSocketInterface and Luxtronik"""

import unittest.mock as mock

from luxtronik import Luxtronik, LuxtronikSocketInterface, Parameters, Calculations, Visibilities
from tests.fake import (
    fake_create_connection,
    fake_parameter_value,
    fake_calculation_value,
    fake_visibility_value,
    FakeSocket,
    FakeModbus,
)


@mock.patch("socket.create_connection", fake_create_connection)
@mock.patch("luxtronik.LuxtronikModbusTcpInterface", FakeModbus)
class TestSocketInteraction:
    def check_luxtronik_data(self, lux, check_for_true=True):
        cp = self.check_data_vector(lux.parameters)
        cc = self.check_data_vector(lux.calculations)
        cv = self.check_data_vector(lux.visibilities)
        if check_for_true:
            return cp and cc and cv
        else:
            return not cp and not cc and not cv

    def check_data_vector(self, data_vector):
        if type(data_vector) is Parameters:
            fct = fake_parameter_value
        elif type(data_vector) is Calculations:
            fct = fake_calculation_value
        elif type(data_vector) is Visibilities:
            fct = fake_visibility_value
        for idx, entry in data_vector:
            if entry.raw != fct(idx):
                return False
        return True

    def clear_luxtronik_data(self, lux):
        self.clear_data_vector(lux.parameters)
        self.clear_data_vector(lux.calculations)
        self.clear_data_vector(lux.visibilities)

    def clear_data_vector(self, data_vector):
        for idx, entry in data_vector:
            entry.raw = 0

    def test_luxtronik_socket_interface(self):
        host = "my_heatpump"
        port = 4711

        lux = LuxtronikSocketInterface(host, port)

        # Read parameters
        p = lux.read_parameters()
        s = FakeSocket.last_instance
        assert type(p) is Parameters
        assert len(s._buffer) == 0
        assert self.check_data_vector(p)

        self.clear_data_vector(p)
        assert not self.check_data_vector(p)

        # Read parameters
        c = lux.read_calculations()
        s = FakeSocket.last_instance
        assert type(c) is Calculations
        assert len(s._buffer) == 0
        assert self.check_data_vector(c)

        self.clear_data_vector(c)
        assert not self.check_data_vector(c)

        # Read parameters
        v = lux.read_visibilities()
        s = FakeSocket.last_instance
        assert type(v) is Visibilities
        assert len(s._buffer) == 0
        assert self.check_data_vector(v)

        self.clear_data_vector(v)
        assert not self.check_data_vector(v)

        # Now, for the read() routine
        data = lux.read()
        s = FakeSocket.last_instance
        assert len(s._buffer) == 0
        assert self.check_luxtronik_data(data)

        # Finally, writing
        p = Parameters()
        p.queue = {0: 100, 1: 200}
        lux.write(p)
        s = FakeSocket.last_instance
        assert s.written_values[0] == 100
        assert s.written_values[1] == 200
        assert len(p.queue) == 0

        p = Parameters()
        p.queue = {2: 300, 3: "test"}
        d = lux.write_and_read(p)
        s = FakeSocket.last_instance
        assert s.written_values[2] == 300
        # Make sure that the non-int value is not written:
        assert 3 not in s.written_values
        assert len(p.queue) == 0
        assert self.check_luxtronik_data(d)

    def test_luxtronik(self):
        host = "my_heatpump"
        port = 4711

        lux = Luxtronik(host, port)
        assert self.check_luxtronik_data(lux)

        self.clear_luxtronik_data(lux)

        assert self.check_luxtronik_data(lux, False)

        ##########################
        # Test the read routines #
        ##########################
        lux.read_parameters()
        assert self.check_data_vector(lux.parameters)

        lux.read_calculations()
        assert self.check_data_vector(lux.calculations)

        lux.read_visibilities()
        assert self.check_data_vector(lux.visibilities)

        self.clear_luxtronik_data(lux)

        ##########################
        # Test the write routine #
        ##########################
        lux.parameters.queue = {0: 500}
        lux.write()
        s = FakeSocket.last_instance
        assert s.written_values[0] == 500

        p = Parameters()
        p.queue = {1: 501}
        lux.write(p)
        s = FakeSocket.last_instance
        assert s.written_values[1] == 501

        # lux.write() and lux.write(p) should not read:
        assert self.check_luxtronik_data(lux, False)

        ###################################
        # Test the write_and_read routine #
        ###################################
        lux.parameters.queue = {2: 502}
        lux.write_and_read()
        # Currently write_and_read triggers two separate connections/operations
        s = FakeSocket.prev_instance
        assert s.written_values[2] == 502

        # Now, the values should be read
        assert self.check_luxtronik_data(lux)

        self.clear_luxtronik_data(lux)

        p.queue = {3: 503}
        lux.write_and_read(p)
        # Currently write_and_read triggers two separate connections/operations
        s = FakeSocket.prev_instance
        assert s.written_values[3] == 503

        # Now, the values should be read
        assert self.check_luxtronik_data(lux)
