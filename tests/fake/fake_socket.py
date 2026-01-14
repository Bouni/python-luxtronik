import socket
import struct

from luxtronik import Parameters, Calculations, Visibilities


def fake_parameter_value(i):
    return (5 * i**2 + 4 * i - 2) % 1001


def fake_calculation_value(i):
    return (23 * i**2 + 42 * i - 47) % 1001


def fake_visibility_value(i):
    return (90 * i**2 + 19 * i - 1) % 2


class FakeSocket:
    last_instance = None
    prev_instance = None

    # These code are hard coded here in order to prevent
    # accidential changes in constants.py
    code_write_parameter = 3002
    code_read_parameters = 3003
    code_read_calculations = 3004
    code_read_visibilities = 3005

    def __init__(self):
        FakeSocket.prev_instance = FakeSocket.last_instance
        FakeSocket.last_instance = self

        self._connected = False
        self._buffer = b""
        self._blocking = False

        # Offer some more entries
        self._num_paras = len(Parameters()._data) + 10
        self._num_calcs = len(Calculations()._data) + 10
        self._num_visis = len(Visibilities()._data) + 10

        self.written_values = {}

    def setblocking(self, blocking):
        self._blocking = blocking

    def connect(self):
        assert not self._connected
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

        if (not self._blocking) and len(self._buffer) < cnt:
            raise BlockingIOError("Not enough bytes in buffer.")

        assert len(self._buffer) >= cnt

        data = self._buffer[0:cnt]

        if not (flag & socket.MSG_PEEK):
            # Remove data from buffer
            self._buffer = self._buffer[cnt:]

        return data

# --- Context manager support ---
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
        return False

def fake_create_connection(info):
    return FakeSocket()