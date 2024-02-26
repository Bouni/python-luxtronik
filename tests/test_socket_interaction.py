"""Test suite for the socket interaction of LuxtronikSocketInterface and Luxtronik"""

import unittest.mock as mock

import socket
import struct

from luxtronik import Luxtronik, LuxtronikSocketInterface, Parameters, Calculations, Visibilities


def fake_parameter_value(i):
    return (5 * i**2 + 4 * i - 2) % 1001


def fake_calculation_value(i):
    return (23 * i**2 + 42 * i - 47) % 1001


def fake_visibility_value(i):
    return (90 * i**2 + 19 * i - 1) % 2


class FakeSocket:
    last_instance = None

    # These code are hard coded here in order to prevent
    # accidential changes in constants.py
    code_write_parameter = 3002
    code_read_parameters = 3003
    code_read_calculations = 3004
    code_read_visibilities = 3005

    def __init__(self, prot, stream):
        FakeSocket.last_instance = self
        assert prot == socket.AF_INET
        assert stream == socket.SOCK_STREAM
        self._connected = False
        self._buffer = b""

        # Offer some more entries
        self._num_paras = len(Parameters()._data) + 10
        self._num_calcs = len(Calculations()._data) + 10
        self._num_visis = len(Visibilities()._data) + 10

        self.written_values = {}

    def connect(self, info):
        assert not self._connected

        self._host = info[0]
        self._port = info[1]
        self._connected = True

    def close(self):
        self._connected = False

    def sendall(self, data):
        assert self._connected

        cnt = len(data) // 4
        content = struct.unpack(">" + "i" * cnt, data)

        # Next, we compute our response, which is saved in self._buffer.
        # The client can read the response with self.recv()

        if content[0] == FakeSocket.code_write_parameter:
            # Client wants to write a parameters
            assert cnt == 3
            idx = content[1]
            value = content[2]

            # Remember the written values, so we can test them later on
            self.written_values[idx] = value

            # Respond with code and idx of parameter
            self._buffer += struct.pack(">i", FakeSocket.code_write_parameter)
            self._buffer += struct.pack(">i", idx)

        elif content[0] == FakeSocket.code_read_parameters:
            # Client wants to read parameters
            assert cnt == 2

            # Respond with code...
            self._buffer += struct.pack(">i", FakeSocket.code_read_parameters)

            # ... length of the response...
            response_cnt = self._num_paras
            self._buffer += struct.pack(">i", response_cnt)

            # ... and the payload
            for i in range(response_cnt):
                self._buffer += struct.pack(">i", fake_parameter_value(i))

        elif content[0] == FakeSocket.code_read_calculations:
            # Client wants to read calculations
            assert cnt == 2

            # Respond with code...
            self._buffer += struct.pack(">i", FakeSocket.code_read_calculations)

            # ...for calculations, we need a 'status' response...
            self._buffer += struct.pack(">i", 0)

            # ... length of the response...
            response_cnt = self._num_calcs
            self._buffer += struct.pack(">i", response_cnt)

            # ... and the payload
            for i in range(response_cnt):
                self._buffer += struct.pack(">i", fake_calculation_value(i))

        elif content[0] == FakeSocket.code_read_visibilities:
            # Client wants to read visibilities
            assert cnt == 2

            # Respond with code...
            self._buffer += struct.pack(">i", FakeSocket.code_read_visibilities)

            # ... length of the response...
            response_cnt = self._num_visis
            self._buffer += struct.pack(">i", response_cnt)

            # ... and the payload
            for i in range(response_cnt):
                self._buffer += struct.pack(">b", fake_visibility_value(i))

    def recv(self, cnt, flag=0):
        assert self._connected

        if (flag & socket.MSG_DONTWAIT) and len(self._buffer) < cnt:
            raise BlockingIOError("Not enough bytes in buffer.")

        assert len(self._buffer) >= cnt

        data = self._buffer[0:cnt]

        if not (flag & socket.MSG_PEEK):
            # Remove data from buffer
            self._buffer = self._buffer[cnt:]

        return data


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
        if type(data_vector) == Parameters:
            fct = fake_parameter_value
        elif type(data_vector) == Calculations:
            fct = fake_calculation_value
        elif type(data_vector) == Visibilities:
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

        with mock.patch("socket.socket", FakeSocket):
            # Create the connection
            lux = LuxtronikSocketInterface(host, port)

            # Check the connection
            s = FakeSocket.last_instance
            assert s._connected
            assert s._host == host
            assert s._port == port

            # Read parameters
            p = lux.read_parameters()
            assert type(p) == Parameters
            assert len(s._buffer) == 0
            assert self.check_data_vector(p)

            self.clear_data_vector(p)
            assert not self.check_data_vector(p)

            # Read parameters
            c = lux.read_calculations()
            assert type(c) == Calculations
            assert len(s._buffer) == 0
            assert self.check_data_vector(c)

            self.clear_data_vector(c)
            assert not self.check_data_vector(c)

            # Read parameters
            v = lux.read_visibilities()
            assert type(v) == Visibilities
            assert len(s._buffer) == 0
            assert self.check_data_vector(v)

            self.clear_data_vector(v)
            assert not self.check_data_vector(v)

            # Now, for the read() routine
            data = lux.read()
            assert len(s._buffer) == 0
            assert self.check_luxtronik_data(data)

            # Finally, writing
            p = Parameters()
            p.queue = {0: 100, 1: 200}
            lux.write(p)
            assert s.written_values[0] == 100
            assert s.written_values[1] == 200
            assert len(p.queue) == 0

            p = Parameters()
            p.queue = {2: 300, 3: "test"}
            d = lux.write_and_read(p)
            assert s.written_values[2] == 300
            # Make sure that the non-int value is not written:
            assert 3 not in s.written_values
            assert len(p.queue) == 0
            assert self.check_luxtronik_data(d)

    def test_luxtronik(self):
        host = "my_heatpump"
        port = 4711

        with mock.patch("socket.socket", FakeSocket):
            # Create the connection
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

            s = FakeSocket.last_instance
            assert len(s._buffer) == 0

            self.clear_luxtronik_data(lux)

            ##########################
            # Test the write routine #
            ##########################
            lux.parameters.queue = {0: 500}
            lux.write()
            assert s.written_values[0] == 500

            p = Parameters()
            p.queue = {1: 501}
            lux.write(p)
            assert s.written_values[1] == 501

            # lux.write() and lux.write(p) should not read:
            assert self.check_luxtronik_data(lux, False)

            ###################################
            # Test the write_and_read routine #
            ###################################
            lux.parameters.queue = {2: 502}
            lux.write_and_read()
            assert s.written_values[2] == 502

            # Now, the values should be read
            assert self.check_luxtronik_data(lux)

            self.clear_luxtronik_data(lux)

            p.queue = {3: 503}
            lux.write_and_read(p)
            assert s.written_values[3] == 503

            # Now, the values should be read
            assert self.check_luxtronik_data(lux)
