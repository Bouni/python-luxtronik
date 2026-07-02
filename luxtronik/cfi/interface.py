"""Main components of the Luxtronik config interface."""

import logging
import socket
import struct
import time

from luxtronik.collections import integrate_data
from luxtronik.common import get_host_lock
from luxtronik.datatypes import Base
from luxtronik.definitions import LuxtronikDefinition
from luxtronik.cfi.constants import (
    LUXTRONIK_DEFAULT_PORT,
    LUXTRONIK_PARAMETERS_WRITE,
    LUXTRONIK_PARAMETERS_READ,
    LUXTRONIK_CALCULATIONS_READ,
    LUXTRONIK_VISIBILITIES_READ,
    LUXTRONIK_SOCKET_READ_SIZE_INTEGER,
    LUXTRONIK_SOCKET_READ_SIZE_CHAR,
    WAIT_TIME_AFTER_PARAMETER_WRITE,
    LUXTRONIK_CFI_REGISTER_BIT_SIZE,
)
from luxtronik.cfi.calculations import Calculations
from luxtronik.cfi.parameters import Parameters
from luxtronik.cfi.visibilities import Visibilities


LOGGER = logging.getLogger(__name__)

###############################################################################
# Config interface data
###############################################################################

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

###############################################################################
# Config interface
###############################################################################

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
                    LOGGER.info("Connected to CFI of Luxtronik heat pump %s:%s", self._host, self._port)
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

    def write_parameter(self, def_field_name_or_idx, value=None, safe=True):
        """Calls `_write_parameter` with the lock-and-connect decorator."""
        self._with_lock_and_connect(self._write_parameter, def_field_name_or_idx, value, safe)

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
        if not isinstance(parameters, Parameters):
            LOGGER.error("Only parameters are writable!")
            return
        count = 0
        for definition, field in parameters.items():
            if field.write_pending:
                if self._do_write_field(LUXTRONIK_PARAMETERS_WRITE, \
                        definition.index, field, parameters.safe):
                    count += 1
        LOGGER.info("%s: Write %d parameters", self._host, count)
        # Give the heatpump a short time to handle the value changes/calculations:
        time.sleep(WAIT_TIME_AFTER_PARAMETER_WRITE)

    def _do_write_field(self, cmd, index, field, safe=True):
        """
        Write a single field to the Luxtronik controller.

        This method checks whether the field can be safely written,
        resets its write-pending flag, validates the raw value, and
        delegates the actual write operation to _do_write_raw().

        Args:
            cmd (int): Command specifying the type of write operation.
            index (int): Index of the field to write.
            field (Field): Field object containing the raw value and metadata.
            safe (bool): If True, perform safety checks before writing.

        Returns:
            bool: True if the write operation was executed, otherwise False.
        """
        # Reset the write_pending flag
        field.write_pending = False
        value = field.raw
        if not field.check_for_write(safe):
            LOGGER.warning(f"{self._host} - Write: Parameter id '{index}'" \
                + f" or value '{value}' invalid!")
            return False
        return self._do_write_raw(cmd, index, value)

    def _do_write_raw(self, cmd, index, value):
        """
        Write a single raw value to the Luxtronik controller.

        Args:
            cmd (int): Command specifying the type of data to write.
                Currently only LUXTRONIK_PARAMETERS_WRITE is supported.
            index (int): Index of the field to write.
            value (int): Value to write.

        Returns:
            bool: True if the write operation was executed, otherwise False.
        """
        if not isinstance(cmd, int):
            LOGGER.error(f"{self._host} - Write: Command '{cmd}' invalid! Must be an integer.")
            return False
        if not isinstance(index, int):
            LOGGER.error(f"{self._host} - Write: Index '{index}' invalid! Must be an integer.")
            return False
        if not isinstance(value, int):
            LOGGER.error(f"{self._host} - Write: Value '{value}' invalid! Must be an integer.")
            return False
        LOGGER.debug(f"{self._host} - Write: Index '{index}' set to '{value}'")
        self._send_ints(cmd, index, value)
        command = self._read_int()
        LOGGER.debug(f"{self._host} - Write: Command {command}")
        idx = self._read_int()
        LOGGER.debug(f"{self._host} - Write: Index {idx}")
        return (command == cmd) and (index == idx)

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
        self._parse(parameters, data)
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
        self._parse(calculations, data)
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
        self._parse(visibilities, data)
        return visibilities

    def _write_parameter(self, def_field_name_or_idx, value=None, safe=True):
        """
        Write a single parameter to the Luxtronik controller. Primarily used for debug purposes.

        Args:
            def_field_name_or_idx (LuxtronikDefinition | Base | str | int):
                Target to write to. May be a definition, a field, a name, or an index.
                Unknown fields can be written, but no safety checks are possible.
            value (int): Value to write. Overrides the field's value if a field is provided.
            safe (bool): If True, perform safety checks before non-raw writing.

        Returns:
            bool: True if the write operation was executed, otherwise False.
        """
        if isinstance(def_field_name_or_idx, LuxtronikDefinition):
            # input parameter is a definition
            definition = def_field_name_or_idx
            field = definition.create_field()
            field.value = value
            self._do_write_field(LUXTRONIK_PARAMETERS_WRITE, definition.index, field, safe)
        elif isinstance(def_field_name_or_idx, Base):
            # input parameter is a field
            field = def_field_name_or_idx
            definition = Parameters.definitions.get(field.name)
            if value is not None:
                field.value = value
            self._do_write_field(LUXTRONIK_PARAMETERS_WRITE, definition.index, field, safe)
        else:
            # input parameter is either a name or an index
            definition = Parameters.definitions.get(def_field_name_or_idx)
            if definition is not None:
                field = definition.create_field()
                field.value = value
                self._do_write_field(LUXTRONIK_PARAMETERS_WRITE, definition.index, field, safe)
            else:
                # check for an integer string
                try:
                    def_field_name_or_idx = int(def_field_name_or_idx)
                except ValueError:
                    pass
                if isinstance(def_field_name_or_idx, int):
                    index = def_field_name_or_idx
                    self._do_write_raw(LUXTRONIK_PARAMETERS_WRITE, index, value)
                else:
                    LOGGER.warning(f"{self._host} - Write: Target '{def_field_name_or_idx}' invalid!")

        # Give the heatpump a short time to handle the value changes/calculations:
        time.sleep(WAIT_TIME_AFTER_PARAMETER_WRITE)

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

    def _parse(self, data_vector, raw_data):
        """
        Parse raw data into the corresponding fields.

        Args:
            data_vector (DataVector): Data vector in which
                the raw data is to be integrated.
            raw_data (list[int]): List of raw register values.
                The raw data must start at register index 0.
        """
        raw_len = len(raw_data)
        # Prepare a list of undefined indices
        undefined = {i for i in range(0, raw_len)}

        # integrate the data into the fields
        for pair in data_vector.data.items():
            definition, field = pair
            # skip this field if there are not enough data
            next_idx = definition.index + definition.count
            if next_idx > raw_len:
                # not enough registers
                field.clear()
                continue
            # remove all used indices from the list of undefined indices
            for index in range(definition.index, next_idx):
                undefined.discard(index)
            # integrate_data() also resets the write_pending flag,
            # intentionally only for read fields
            pair.integrate_data(raw_data, LUXTRONIK_CFI_REGISTER_BIT_SIZE)

        # create an unknown field for additional data
        for index in undefined:
            # LOGGER.warning(f"Entry '%d' not in list of {self.name}", index)
            definition = data_vector.definitions.create_unknown_definition(index)
            field = definition.create_field()
            integrate_data(definition, field, raw_data, LUXTRONIK_CFI_REGISTER_BIT_SIZE, index)
            data_vector.data.add_sorted(definition, field)
