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

# endregion Imports

LOGGER = logging.getLogger("Luxtronik")

# Wait time (in seconds) after writing parameters to give controller
# some time to re-calculate values, etc.
WAIT_TIME_AFTER_PARAMETER_WRITE = 1


def is_socket_closed(sock: socket.socket) -> bool:
    """Check is socket closed."""
    try:
        # this will try to read bytes without blocking and also without removing them from buffer
        data = sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
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

    def __init__(self, host, port=8889, safe=True):
        self._lock = threading.Lock()
        self._host = host
        self._port = port
        self._safe = safe
        self._socket = None
        # TODO: Field will be removed in future
        self._calculations = Calculations()
        # TODO: Field will be removed in future
        self._parameters = Parameters(safe=safe)
        # TODO: Field will be removed in future
        self._visibilities = Visibilities()
        self.read()

    def __del__(self):
        if self._socket is not None:
            if not is_socket_closed(self._socket):
                self._socket.close()
            self._socket = None
            LOGGER.info(
                "Disconnected from Luxtronik heatpump %s:%s", self._host, self._port
            )

    @property
    def calculations(self):
        LOGGER.debug("%s: 'calculations' is outdated. Please use the return value of 'read()' instead", self._host)
        return self._calculations

    @property
    def parameters(self):
        LOGGER.debug("%s: 'parameters' is outdated. Please use the return value of 'read()' or 'write(params)' instead", self._host)
        return self._parameters

    @property
    def visibilities(self):
        LOGGER.debug("%s: 'visibilities' is outdated. Please use the return value of 'read()' instead", self._host)
        return self._visibilities

    def read(self):
        """Read data from heatpump."""
        return self._read_after_write(write=False, parameters=None)

    def write(self, parameters=None):
        """Write parameter to heatpump."""
        return self._read_after_write(write=True, parameters=parameters)

    def _read_after_write(self, write=False, parameters=None):
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
        :param bool write Indicates whether parameters should be written to heatpump
                          prior to reading in all available data from heatpump
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
                return self._write(parameters)
            return self._read()

    def _read(self):
        parameters = self._read_parameters()
        calculations = self._read_calculations()
        visibilities = self._read_visibilities()
        return calculations, parameters, visibilities

    def _write(self, parameters):
        # TODO: Remove switch to local field in future. Also change the parameters input to mandatory
        if parameters is None:
          queue = self._parameters.queue
        else:
          queue = parameters.queue
        for index, value in queue.items():
            if not isinstance(index, int) or not isinstance(value, int):
                LOGGER.warning("%s: Parameter id '%s' or value '%s' invalid!", self._host, index, value)
                continue
            LOGGER.info("%s: Parameter '%d' set to '%s'", self._host, index, value)
            data = struct.pack(">iii", 3002, index, value)
            LOGGER.debug("%s: Data %s", self._host, data)
            self._socket.sendall(data)
            cmd = struct.unpack(">i", self._socket.recv(4))[0]
            LOGGER.debug("%s: Command %s", self._host, cmd)
            val = struct.unpack(">i", self._socket.recv(4))[0]
            LOGGER.debug("%s: Value %s", self._host, val)
        # Flush queue after writing all values
        queue = {}
        # Give the heatpump a short time to handle the value changes/calculations:
        time.sleep(WAIT_TIME_AFTER_PARAMETER_WRITE)
        # Read the new values based on our parameter changes:
        parameters = self._read_parameters()
        calculations = self._read_calculations()
        visibilities = self._read_visibilities()
        return calculations, parameters, visibilities

    def _read_parameters(self):
        data = []
        self._socket.sendall(struct.pack(">ii", 3003, 0))
        cmd = struct.unpack(">i", self._socket.recv(4))[0]
        LOGGER.debug("%s: Command %s", self._host, cmd)
        length = struct.unpack(">i", self._socket.recv(4))[0]
        LOGGER.debug("%s: Length %s", self._host, length)
        for _ in range(0, length):
            try:
                data.append(struct.unpack(">i", self._socket.recv(4))[0])
            except struct.error as err:
                # not logging this as error as it would be logged on every read cycle
                LOGGER.debug("%s: %s", self._host, err)
        LOGGER.info("%s: Read %d parameters", self._host, length)
        # TODO: Update of the private field will be removed in future
        self._parameters.parse(data)
        parameters = Parameters(safe=self._safe)
        parameters.parse(data)
        return parameters

    def _read_calculations(self):
        data = []
        self._socket.sendall(struct.pack(">ii", 3004, 0))
        cmd = struct.unpack(">i", self._socket.recv(4))[0]
        LOGGER.debug("%s: Command %s", self._host, cmd)
        stat = struct.unpack(">i", self._socket.recv(4))[0]
        LOGGER.debug("%s: Stat %s", self._host, stat)
        length = struct.unpack(">i", self._socket.recv(4))[0]
        LOGGER.debug("%s: Length %s", self._host, length)
        for _ in range(0, length):
            try:
                data.append(struct.unpack(">i", self._socket.recv(4))[0])
            except struct.error as err:
                # not logging this as error as it would be logged on every read cycle
                LOGGER.debug("%s: %s", self._host, err)
        LOGGER.info("%s: Read %d calculations", self._host, length)
        # TODO: Update of the private field will be removed in future
        self._calculations.parse(data)
        calculations = Calculations()
        calculations.parse(data)
        return calculations

    def _read_visibilities(self):
        data = []
        self._socket.sendall(struct.pack(">ii", 3005, 0))
        cmd = struct.unpack(">i", self._socket.recv(4))[0]
        LOGGER.debug("%s: Command %s", self._host, cmd)
        length = struct.unpack(">i", self._socket.recv(4))[0]
        LOGGER.debug("%s: Length %s", self._host, length)
        for _ in range(0, length):
            try:
                data.append(struct.unpack(">b", self._socket.recv(1))[0])
            except struct.error as err:
                # not logging this as error as it would be logged on every read cycle
                LOGGER.debug("%s: %s", self._host, err)
        LOGGER.info("%s: Read %d visibilities", self._host, length)
        # TODO: Update of the private field will be removed in future
        self._visibilities.parse(data)
        visibilities = Visibilities()
        visibilities.parse(data)
        return visibilities
