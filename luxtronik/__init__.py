"""Luxtronik heatpump interface."""

# -*- coding: utf-8 -*-
# region Imports
from __future__ import annotations

import logging
import socket
import struct
import threading
import time

from luxtronik.calculations import Calculations
from luxtronik.parameters import Parameters
from luxtronik.visibilities import Visibilities
from luxtronik.discover import discover  # noqa: F401
from luxtronik.constants import (
    LUXTRONIK_DEFAULT_PORT,
    LUXTRONIK_PARAMETERS_WRITE,
    LUXTRONIK_PARAMETERS_READ,
    LUXTRONIK_CALCULATIONS_READ,
    LUXTRONIK_VISIBILITIES_READ,
    LUXTRONIK_SOCKET_READ_SIZE_PEEK,
    LUXTRONIK_SOCKET_READ_SIZE_INTEGER,
    LUXTRONIK_SOCKET_READ_SIZE_CHAR,
)

# endregion Imports

LOGGER = logging.getLogger("Luxtronik")

# Wait time (in seconds) after writing parameters to give controller
# some time to re-calculate values, etc.
WAIT_TIME_AFTER_PARAMETER_WRITE = 1


def is_socket_closed(sock: socket.socket) -> bool:
    """Check is socket closed."""
    try:
        # this will try to read bytes without blocking and also without removing them from buffer
        data = sock.recv(LUXTRONIK_SOCKET_READ_SIZE_PEEK, socket.MSG_DONTWAIT | socket.MSG_PEEK)
        if len(data) == 0:
            return True
    except BlockingIOError:
        return False  # socket is open and reading from it would block
    except ConnectionResetError:  # pylint: disable=broad-except
        return True  # socket was closed for some other reason
    except Exception as err:  # pylint: disable=broad-except
        LOGGER.exception("Unexpected exception when checking if socket is closed", exc_info=err)
        return False
    return False


class LuxtronikData:
    """
    Collection of parameters, calculations and visiblities.
    Also provide some high level access functions to their data values.
    """

    def __init__(self, parameters=None, calculations=None, visibilities=None, safe=True):
        self.parameters = Parameters(safe) if parameters is None else parameters
        self.calculations = Calculations() if calculations is None else calculations
        self.visibilities = Visibilities() if visibilities is None else visibilities

    def get_firmware_version(self):
        return "".join([self.calculations.get(i).value for i in range(81, 91)])


class LuxtronikSocketInterface:
    """Luxtronik read/write interface via socket."""

    def __init__(self, host, port=LUXTRONIK_DEFAULT_PORT):
        self._lock = threading.Lock()
        self._host = host
        self._port = port
        self._socket = None
        self._connect()

    def __del__(self):
        self._disconnect()

    def _connect(self):
        """Connect the socket if not already done."""
        is_none = self._socket is None
        if is_none:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if is_none or is_socket_closed(self._socket):
            self._socket.connect((self._host, self._port))
            LOGGER.info("Connected to Luxtronik heat pump %s:%s", self._host, self._port)

    def _disconnect(self):
        """Disconnect the socket if not already done."""
        if self._socket is not None:
            if not is_socket_closed(self._socket):
                self._socket.close()
            self._socket = None
            LOGGER.info("Disconnected from Luxtronik heatpump %s:%s", self._host, self._port)

    def _with_lock_and_connect(self, func, *args, **kwargs):
        """
        Decorator around various read/write functions to connect first.

        This method is essentially a wrapper for the _read() and _write() methods.
        Locking is being used to ensure that only a single socket operation is
        performed at any point in time. This helps to avoid issues with the
        Luxtronik controller, which seems unstable otherwise.
        """
        with self._lock:
            self._connect()
            ret_val = func(*args, **kwargs)
            return ret_val

    def read(self, data=None):
        """
        All available data will be read from the heat pump
        and integrated to the passed data object.
        This data object is returned afterwards, mainly for access to a newly created.
        """
        if data is None:
            data = LuxtronikData()
        return self._with_lock_and_connect(self._read, data)

    def read_parameters(self, parameters=None):
        """
        Read parameters from heat pump and integrate them to the passed dictionary.
        This dictionary is returned afterwards, mainly for access to a newly created.
        """
        if parameters is None:
            parameters = Parameters()
        return self._with_lock_and_connect(self._read_parameters, parameters)

    def read_calculations(self, calculations=None):
        """
        Read calculations from heat pump and integrate them to the passed dictionary.
        This dictionary is returned afterwards, mainly for access to a newly created.
        """
        if calculations is None:
            calculations = Calculations()
        return self._with_lock_and_connect(self._read_calculations, calculations)

    def read_visibilities(self, visibilities=None):
        """
        Read visibilities from heat pump and integrate them to the passed dictionary.
        This dictionary is returned afterwards, mainly for access to a newly created.
        """
        if visibilities is None:
            visibilities = Visibilities()
        return self._with_lock_and_connect(self._read_visibilities, visibilities)

    def write(self, parameters):
        """
        Write all set parameters to the heat pump.
        :param Parameters() parameters  Parameter dictionary to be written
                          to the heatpump before reading all available data
                          from the heat pump.
        """
        self._with_lock_and_connect(self._write, parameters)

    def write_and_read(self, parameters, data=None):
        """
        Write all set parameter to the heat pump (see write())
        prior to reading back in all data from the heat pump (see read())
        after a short wait time
        """
        if data is None:
            data = LuxtronikData()
        return self._with_lock_and_connect(self._write_and_read, parameters, data)

    def _read(self, data):
        self._read_parameters(data.parameters)
        self._read_calculations(data.calculations)
        self._read_visibilities(data.visibilities)
        return data

    def _write_and_read(self, parameters, data):
        self._write(parameters)
        # Give the heatpump a short time to handle the value changes/calculations:
        time.sleep(WAIT_TIME_AFTER_PARAMETER_WRITE)
        return self._read(data)

    def _write(self, parameters):
        for index, value in parameters.queue.items():
            if not isinstance(index, int) or not isinstance(value, int):
                LOGGER.warning(
                    "%s: Parameter id '%s' or value '%s' invalid!",
                    self._host,
                    index,
                    value,
                )
                continue
            LOGGER.info("%s: Parameter '%d' set to '%s'", self._host, index, value)
            self._send_ints(LUXTRONIK_PARAMETERS_WRITE, index, value)
            cmd = self._read_int()
            LOGGER.debug("%s: Command %s", self._host, cmd)
            val = self._read_int()
            LOGGER.debug("%s: Value %s", self._host, val)
        # Flush queue after writing all values
        parameters.queue = {}

    def _read_parameters(self, parameters):
        data = []
        self._send_ints(LUXTRONIK_PARAMETERS_READ, 0)
        cmd = self._read_int()
        LOGGER.debug("%s: Command %s", self._host, cmd)
        length = self._read_int()
        LOGGER.debug("%s: Length %s", self._host, length)
        for _ in range(0, length):
            data.append(self._read_int())
        LOGGER.info("%s: Read %d parameters", self._host, length)
        parameters.parse(data)
        return parameters

    def _read_calculations(self, calculations):
        data = []
        self._send_ints(LUXTRONIK_CALCULATIONS_READ, 0)
        cmd = self._read_int()
        LOGGER.debug("%s: Command %s", self._host, cmd)
        stat = self._read_int()
        LOGGER.debug("%s: Stat %s", self._host, stat)
        length = self._read_int()
        LOGGER.debug("%s: Length %s", self._host, length)
        for _ in range(0, length):
            data.append(self._read_int())
        LOGGER.info("%s: Read %d calculations", self._host, length)
        calculations.parse(data)
        return calculations

    def _read_visibilities(self, visibilities):
        data = []
        self._send_ints(LUXTRONIK_VISIBILITIES_READ, 0)
        cmd = self._read_int()
        LOGGER.debug("%s: Command %s", self._host, cmd)
        length = self._read_int()
        LOGGER.debug("%s: Length %s", self._host, length)
        for _ in range(0, length):
            data.append(self._read_char())
        LOGGER.info("%s: Read %d visibilities", self._host, length)
        visibilities.parse(data)
        return visibilities

    def _send_ints(self, *ints):
        "Low-level helper to send a tuple of ints"
        data = struct.pack(">" + "i" * len(ints), *ints)
        LOGGER.debug("%s: sending %s", self._host, data)
        self._socket.sendall(data)

    def _read_bytes(self, count):
        "Low-level helper to receive a precise number of bytes"
        total_reading = b""

        while len(total_reading) is not count:
            missing = count - len(total_reading)

            reading = self._socket.recv( missing )

            if len(reading) == 0:
                LOGGER.error("%s: Connection died.", self._host)
                raise ConnectionError("Connection to %s died." % self._host)

            total_reading += reading

            if len(reading) is not missing:
                LOGGER.debug("%s: received %s bytes out of %s bytes. Will read again.", self._host, len(reading), missing)

        return total_reading

    def _read_int(self):
        "Low-level helper to receive an int"
        reading = self._read_bytes(LUXTRONIK_SOCKET_READ_SIZE_INTEGER)
        return struct.unpack(">i", reading)[0]

    def _read_char(self):
        "Low-level helper to receive a signed int"
        reading = self._read_bytes(LUXTRONIK_SOCKET_READ_SIZE_CHAR)
        return struct.unpack(">b", reading)[0]


class Luxtronik(LuxtronikData):
    """
    Wrapper around the data and the read/write interface.
    Mainly to ensure backwards compatibility
    of the read/write interface to other projects.
    """

    def __init__(self, host, port=LUXTRONIK_DEFAULT_PORT, safe=True):
        super().__init__(safe=safe)
        self.interface = LuxtronikSocketInterface(host, port)
        self.read()

    def read(self):
        return self.interface.read(self)

    def read_parameters(self):
        return self.interface.read_parameters(self.parameters)

    def read_calculations(self):
        return self.interface.read_calculations(self.calculations)

    def read_visibilities(self):
        return self.interface.read_visibilities(self.visibilities)

    def write(self, parameters=None):
        if parameters is None:
            self.interface.write(self.parameters)
        else:
            self.interface.write(parameters)

    def write_and_read(self, parameters=None):
        if parameters is None:
            return self.interface.write_and_read(self.parameters, self)
        else:
            return self.interface.write_and_read(parameters, self)
