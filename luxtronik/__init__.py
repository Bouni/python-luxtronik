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

# endregion Imports

LOGGER = logging.getLogger("Luxtronik")

# Wait time (in seconds) after writing parameters to give controller some time to re-calculate values, etc.
WAIT_TIME_BETWEEN_WRITE_READ_PARAMETER = 1


def is_socket_closed(sock: socket.socket) -> bool:
    try:
        # this will try to read bytes without blocking and also without removing them from buffer (peek only)
        data = sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
        if len(data) == 0:
            return True
    except BlockingIOError:
        return False  # socket is open and reading from it would block
    except ConnectionResetError:
        return True  # socket was closed for some other reason
    except Exception as err:
        LOGGER.exception(
            "Unexpected exception when checking if a socket is closed", exc_info=err
        )
        return False
    return False


class Luxtronik:
    """Main luxtronik class."""

    def __init__(self, host, port, safe=True):
        self._lock = threading.Lock()
        self._host = host
        self._port = port
        self._socket = None
        self.calculations = Calculations()
        self.parameters = Parameters(safe=safe)
        self.visibilities = Visibilities()
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
        self._read_write(write=False)

    def write(self):
        """Write parameter to heatpump."""
        self._read_write(write=True)

    def _read_write(self, write=False):
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
        :param bool write Indicates whether parameters should be written to heat pump prior to reading in all available data from heatpump
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
            if write:
                return self._write()
            self._read()

    def _read(self):
        self._read_parameters()
        self._read_calculations()
        self._read_visibilities()

    def _write(self):
        for index, value in self.parameters.queue.items():
            if not isinstance(index, int) or not isinstance(value, int):
                LOGGER.warning("Parameter id '%s' or value '%s' invalid!", index, value)
                continue
            LOGGER.info("Parameter '%d' set to '%s'", index, value)
            data = struct.pack(">iii", 3002, index, value)
            LOGGER.debug("Data %s", data)
            self._socket.sendall(data)
            cmd = struct.unpack(">i", self._socket.recv(4))[0]
            LOGGER.debug("Command %s", cmd)
            val = struct.unpack(">i", self._socket.recv(4))[0]
            LOGGER.debug("Value %s", val)
        # Flush queue after writing all values
        self.parameters.queue = {}
        # Give the heatpump a short time to handle the value changes/calculations:
        time.sleep(WAIT_TIME_BETWEEN_WRITE_READ_PARAMETER)
        # Read the new values based on our parameter changes:
        self._read_parameters()
        self._read_calculations()
        LOGGER.warning("New: '%s'", self.calculations.get(12))
        self._read_visibilities()

    def _read_parameters(self):
        data = []
        self._socket.sendall(struct.pack(">ii", 3003, 0))
        cmd = struct.unpack(">i", self._socket.recv(4))[0]
        LOGGER.debug("Command %s", cmd)
        length = struct.unpack(">i", self._socket.recv(4))[0]
        LOGGER.debug("Length %s", length)
        for _ in range(0, length):
            try:
                data.append(struct.unpack(">i", self._socket.recv(4))[0])
            except struct.error as err:
                # not logging this as error as it would be logged on every read cycle
                LOGGER.debug(err)
        LOGGER.info("Read %d parameters", length)
        self.parameters.parse(data)

    def _read_calculations(self):
        data = []
        self._socket.sendall(struct.pack(">ii", 3004, 0))
        cmd = struct.unpack(">i", self._socket.recv(4))[0]
        LOGGER.debug("Command %s", cmd)
        stat = struct.unpack(">i", self._socket.recv(4))[0]
        LOGGER.debug("Stat %s", stat)
        length = struct.unpack(">i", self._socket.recv(4))[0]
        LOGGER.debug("Length %s", length)
        for _ in range(0, length):
            try:
                data.append(struct.unpack(">i", self._socket.recv(4))[0])
            except struct.error as err:
                # not logging this as error as it would be logged on every read cycle
                LOGGER.debug(err)
        LOGGER.info("Read %d calculations", length)
        self.calculations.parse(data)

    def _read_visibilities(self):
        data = []
        self._socket.sendall(struct.pack(">ii", 3005, 0))
        cmd = struct.unpack(">i", self._socket.recv(4))[0]
        LOGGER.debug("Command %s", cmd)
        length = struct.unpack(">i", self._socket.recv(4))[0]
        LOGGER.debug("Length %s", length)
        for _ in range(0, length):
            try:
                data.append(struct.unpack(">b", self._socket.recv(1))[0])
            except struct.error as err:
                # not logging this as error as it would be logged on every read cycle
                LOGGER.debug(err)
        LOGGER.info("Read %d visibilities", length)
        self.visibilities.parse(data)
