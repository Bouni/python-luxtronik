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
        data = sock.recv(
            LUXTRONIK_SOCKET_READ_SIZE_PEEK, socket.MSG_DONTWAIT | socket.MSG_PEEK
        )
        if len(data) == 0:
            return True
    except BlockingIOError:
        return False  # socket is open and reading from it would block
    except ConnectionResetError:  # pylint: disable=broad-except
        return True  # socket was closed for some other reason
    except Exception as err:  # pylint: disable=broad-except
        LOGGER.exception(
            "Unexpected exception when checking if socket is closed", exc_info=err
        )
        return False
    return False


class Luxtronik:
    """Main luxtronik class."""

    def __init__(self, host, port=LUXTRONIK_DEFAULT_PORT, safe=True):
        self._lock = threading.Lock()
        self._host = host
        self._port = port
        self._safe = safe
        self._socket = None
        self.read()

    def __del__(self):
        if self._socket is not None:
            if not is_socket_closed(self._socket):
                self._socket.close()
            self._socket = None
            LOGGER.info(
                "Disconnected from Luxtronik heatpump %s:%s", self._host, self._port
            )

    def read(self):
        """Read data from heatpump."""
        return self._read_after_write(parameters=None)

    def write(self, parameters):
        """Write parameter to heatpump."""
        return self._read_after_write(parameters=parameters)

    def _read_after_write(self, parameters):
        """
        Read and/or write value from and/or to heatpump.
        This method is essentially a wrapper for the _read() and _write()
        methods.
        Locking is being used to ensure that only a single socket operation is
        performed at any point in time. This helps to avoid issues with the
        Luxtronik controller, which seems unstable otherwise.
        If write is true, all parameters will be written to the heat pump
        prior to reading back in all data from the heat pump. If write is
        false, no data will be written, but all available data will be read
        from the heat pump.
        :param Parameters() parameters  Parameter dictionary to be written
                          to the heatpump before reading all available data
                          from the heatpump. At 'None' it is read only.
        """

        with self._lock:
            is_none = self._socket is None
            if is_none:
                self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if is_none or is_socket_closed(self._socket):
                self._socket.connect((self._host, self._port))
                LOGGER.info(
                    "Connected to Luxtronik heatpump %s:%s", self._host, self._port
                )
            if parameters is not None:
                return self._write(parameters)
            return self._read()

    def _read(self):
        parameters = self._read_parameters()
        calculations = self._read_calculations()
        visibilities = self._read_visibilities()
        return calculations, parameters, visibilities

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
        # Give the heatpump a short time to handle the value changes/calculations:
        time.sleep(WAIT_TIME_AFTER_PARAMETER_WRITE)
        # Read the new values based on our parameter changes:
        return self._read()

    def _read_parameters(self):
        data = []
        self._send_ints(LUXTRONIK_PARAMETERS_READ, 0)
        cmd = self._read_int()
        LOGGER.debug("%s: Command %s", self._host, cmd)
        length = self._read_int()
        LOGGER.debug("%s: Length %s", self._host, length)
        for _ in range(0, length):
            try:
                data.append(self._read_int())
            except struct.error as err:
                # not logging this as error as it would be logged on every read cycle
                LOGGER.debug("%s: %s", self._host, err)
        LOGGER.info("%s: Read %d parameters", self._host, length)
        parameters = Parameters(safe=self._safe)
        parameters.parse(data)
        return parameters

    def _read_calculations(self):
        data = []
        self._send_ints(LUXTRONIK_CALCULATIONS_READ, 0)
        cmd = self._read_int()
        LOGGER.debug("%s: Command %s", self._host, cmd)
        stat = self._read_int()
        LOGGER.debug("%s: Stat %s", self._host, stat)
        length = self._read_int()
        LOGGER.debug("%s: Length %s", self._host, length)
        for _ in range(0, length):
            try:
                data.append(self._read_int())
            except struct.error as err:
                # not logging this as error as it would be logged on every read cycle
                LOGGER.debug("%s: %s", self._host, err)
        LOGGER.info("%s: Read %d calculations", self._host, length)
        calculations = Calculations()
        calculations.parse(data)
        return calculations

    def _read_visibilities(self):
        data = []
        self._send_ints(LUXTRONIK_VISIBILITIES_READ, 0)
        cmd = self._read_int()
        LOGGER.debug("%s: Command %s", self._host, cmd)
        length = self._read_int()
        LOGGER.debug("%s: Length %s", self._host, length)
        for _ in range(0, length):
            try:
                data.append(self._read_char())
            except struct.error as err:
                # not logging this as error as it would be logged on every read cycle
                LOGGER.debug("%s: %s", self._host, err)
        LOGGER.info("%s: Read %d visibilities", self._host, length)
        visibilities = Visibilities()
        visibilities.parse(data)
        return visibilities

    def _send_ints(self, *ints):
        "Low-level helper to send a tuple of ints"
        data = struct.pack(">" + "i" * len(ints), *ints)
        LOGGER.debug("%s: sending %s", self._host, data)
        self._socket.sendall(data)

    def _read_int(self):
        "Low-level helper to receive an int"
        reading = self._socket.recv(LUXTRONIK_SOCKET_READ_SIZE_INTEGER)
        return struct.unpack(">i", reading)[0]

    def _read_char(self):
        "Low-level helper to receive a signed int"
        reading = self._socket.recv(LUXTRONIK_SOCKET_READ_SIZE_CHAR)
        return struct.unpack(">b", reading)[0]
