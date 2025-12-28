"""Luxtronik heatpump interface."""

# -*- coding: utf-8 -*-
# region Imports
from __future__ import annotations

import logging
import socket
import struct
import time

from luxtronik.common import get_host_lock
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
    LUXTRONIK_SOCKET_READ_SIZE_INTEGER,
    LUXTRONIK_SOCKET_READ_SIZE_CHAR,
)
from luxtronik.shi import resolve_version
from luxtronik.shi.modbus import LuxtronikModbusTcpInterface
from luxtronik.shi.holdings import Holdings
from luxtronik.shi.interface import LuxtronikSmartHomeData, LuxtronikSmartHomeInterface
from luxtronik.shi.constants import (
    LUXTRONIK_DEFAULT_MODBUS_PORT,
)

# endregion Imports

LOGGER = logging.getLogger("Luxtronik")

# Wait time (in seconds) after writing parameters to give controller
# some time to re-calculate values, etc.
WAIT_TIME_AFTER_PARAMETER_WRITE = 1


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
        return self.calculations.get_firmware_version()


class LuxtronikSocketInterface:
    """Luxtronik read/write interface via socket."""

    def __init__(self, host, port=LUXTRONIK_DEFAULT_PORT):
        # Acquire a lock object for this host to ensure thread safety
        self._lock = get_host_lock(host)

        self._host = host
        self._port = port
        self._socket = None

    @property
    def lock(self):
        return self._lock

    def _with_lock_and_connect(self, func, *args, **kwargs):
        """
        Decorator around various read/write functions to connect first.

        This method is essentially a wrapper for the _read() and _write() methods.
        Locking is being used to ensure that only a single socket operation is
        performed at any point in time. This helps to avoid issues with the
        Luxtronik controller, which seems unstable otherwise.
        """
        with self.lock:
            try:
                ret_val = None
                with socket.create_connection((self._host, self._port)) as sock:
                    self._socket = sock
                    LOGGER.info("Connected to Luxtronik heat pump %s:%s", self._host, self._port)
                    ret_val = func(*args, **kwargs)
            except socket.gaierror as e:
                LOGGER.error("Failed to connect to Luxtronik heat pump %s:%s. %s.",
                    self._host, self._port, f"Address-related error: {e}")
            except socket.timeout as e:
                LOGGER.error("Failed to connect to Luxtronik heat pump %s:%s. %s.",
                    self._host, self._port, f"Connection timed out: {e}")
            except ConnectionRefusedError as e:
                LOGGER.error("Failed to connect to Luxtronik heat pump %s:%s. %s.",
                    self._host, self._port, f"Connection refused: {e}")
            except OSError as e:
                LOGGER.error("Failed to connect to Luxtronik heat pump %s:%s. %s.",
                    self._host, self._port, f"OS error during connect: {e}")
            except Exception as e:
                LOGGER.error("Failed to connect to Luxtronik heat pump %s:%s. %s.",
                    self._host, self._port, f"Unknown exception: {e}")
        self._socket = None
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
        # Give the heatpump a short time to handle the value changes/calculations:
        time.sleep(WAIT_TIME_AFTER_PARAMETER_WRITE)

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


class LuxtronikAllData(LuxtronikData, LuxtronikSmartHomeData):
    """
    Data-vector collection for all luxtronik data vectors.

    The collection currently consists of:
    - `parameters`
    - `calculations`
    - `visibilities`
    - `holdings`
    - `inputs`
    """

    def __init__(
        self,
        parameters=None,
        calculations=None,
        visibilities=None,
        holdings=None,
        inputs=None,
        version=None,
        safe=True
    ):
        """
        Initialize a LuxtronikAllData instance.

        Args:
            parameters (Parameters): Optional parameters data vector. If not provided,
                a new `Parameters` instance is created.
            calculations (Calculations): Optional calculations data vector. If not provided,
                a new `Calculations` instance is created.
            visibilities (Visibilities): Optional visibilities data vector. If not provided,
                a new `Visibilities` instance is created.
            holdings (Holdings): Optional holdings data vector. If not provided,
                a new `Holdings` instance is created.
            inputs (Inputs): Optional inputs data vector. If not provided,
                a new `Inputs` instance is created.
            version (tuple[int] | None): Version to be used for creating the data vectors.
                This ensures that the data vectors only contain valid fields.
                If None is passed, all available fields are added.
            safe (bool): If true, prevent parameter and holding fields marked as
                not secure from being written to.
        """
        LuxtronikData.__init__(self, parameters, calculations, visibilities, safe)
        LuxtronikSmartHomeData.__init__(self, holdings, inputs, version, safe)

class LuxtronikInterface(LuxtronikSocketInterface, LuxtronikSmartHomeInterface):
    """
    Combined interface that can be used to control both
    the configuration interface and the smart home interface.

    For simplicity, only the basic functions are offered.

    Attention! It must be ensured that `LuxtronikSocketInterface` and
    `LuxtronikSmartHomeInterface` do not instantiate the same fields.
    Otherwise, the derivations will overwrite each other.
    """

    def __init__(
        self,
        host,
        port_config=LUXTRONIK_DEFAULT_PORT,
        port_shi=LUXTRONIK_DEFAULT_MODBUS_PORT
    ):
        """
        Initialize the "combined" luxtronik interface.

        Args:
            host (str): Hostname or IP address of the heat pump.
            port_config (int): TCP port for the config interface
                  (default: LUXTRONIK_DEFAULT_PORT).
            port_shi (int): TCP port for the smart home interface (via modbusTCP)
                  (default: LUXTRONIK_DEFAULT_MODBUS_PORT).
        """
        self._lock = get_host_lock(host)

        self._host = host
        LuxtronikSocketInterface.__init__(self, host, port_config)
        modbus_interface = LuxtronikModbusTcpInterface(host, port_shi)
        resolved_version = resolve_version(modbus_interface)
        LuxtronikSmartHomeInterface.__init__(self, modbus_interface, resolved_version)

    @property
    def lock(self):
        return self._lock

    def create_all_data(self, safe=True):
        """
        Create a data vector collection only with fields that match the stored version.

        Args:
            safe (bool): If true, prevent holding fields marked as
                not secure from being written to.

        Returns:
            LuxtronikAllData: The created data-collection.
        """
        return LuxtronikAllData(None, None, None, None, None, self._version, safe)

    def read_all(self, data=None):
        """
        Read the data of all fields within the data vector collection
        that are supported by the controller.

        Args:
            data (LuxtronikAllData | None): Optional existing data vector collection.
                If None is provided, a new instance is created.

        Returns:
            LuxtronikAllData: The passed / created data vector collection.
        """
        if not isinstance(data, LuxtronikAllData):
            data = self.create_all_data(True)

        with self.lock:
            LuxtronikSocketInterface.read(self, data)
            LuxtronikSmartHomeInterface.read(self, data)
        return data

    def read(self, data=None):
        """
        Calls `read_all()`. Please check its documentation.
        Exists mainly to standardize the various interfaces.
        """
        return self.read_all(data)

    def write_all(self, data):
        """
        Write the data of all fields within the data vector (collection)
        that are supported by the controller.

        Args:
            data (LuxtronikAllData | Parameters | Holdings): The data vector (collection) containing field data.
                If None is provided, the write is aborted.

        Returns:
            bool: True if no errors occurred, otherwise False.
        """
        if isinstance(data, Parameters):
            with self.lock:
                LuxtronikSocketInterface.write(self, data)
                shi_result = True
        elif isinstance(data, Holdings):
            with self.lock:
                shi_result = LuxtronikSmartHomeInterface.write_holdings(self, data)
        # Because of LuxtronikAllData(LuxtronikSmartHomeData) we must use type(..)
        elif type(data) is LuxtronikSmartHomeData:
            with self.lock:
                shi_result = LuxtronikSmartHomeInterface.write(self, data)
        elif isinstance(data, LuxtronikAllData):
            with self.lock:
                LuxtronikSocketInterface.write(self, data.parameters)
                shi_result = LuxtronikSmartHomeInterface.write(self, data)
        else:
            LOGGER.warning("Abort write! No data to write provided.")
            return False
        return shi_result

    def write(self, data):
        """
        Calls `write_all()`. Please check its documentation.
        Exists mainly to standardize the various interfaces.
        """
        return self.write_all(data)

    def write_and_read(self, write_data, read_data=None):
        """
        Write and then read the data of all fields within the data vector collection
        that are supported by the controller.

        Args:
            data (LuxtronikAllData): The data vector collection containing field data.
                If None is provided, the write and read is aborted.

        Returns:
            bool: True if no errors occurred, otherwise False.
        """
        with self.lock:
            self.write_all(write_data)
            data = self.read_all(read_data)
        return data


class Luxtronik(LuxtronikAllData):
    """
    Wrapper around the data and the read/write interface.
    Mainly to ensure backwards compatibility
    of the read/write interface to other projects.
    """

    def __init__(
        self,
        host,
        port=LUXTRONIK_DEFAULT_PORT,
        safe=True,
        port_shi=LUXTRONIK_DEFAULT_MODBUS_PORT
    ):
        self._interface = LuxtronikInterface(host, port, port_shi)
        super().__init__(version=self._interface.version, safe=safe)
        self.read()

    @property
    def interface(self):
        return self._interface

    def read(self):
        return self._interface.read(self)

    def read_parameters(self):
        return self._interface.read_parameters(self.parameters)

    def read_calculations(self):
        return self._interface.read_calculations(self.calculations)

    def read_visibilities(self):
        return self._interface.read_visibilities(self.visibilities)

    def read_holdings(self):
        return self._interface.read_holdings(self.holdings)

    def read_inputs(self):
        return self._interface.read_inputs(self.inputs)

    def write(self, data=None):
        if data is None:
            return self._interface.write(self)
        else:
            return self._interface.write(data)

    def write_and_read(self, data=None):
        if data is None:
            return self._interface.write_and_read(self, self)
        else:
            return self._interface.write_and_read(data, self)