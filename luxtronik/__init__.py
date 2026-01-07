"""Luxtronik heatpump interface."""

# -*- coding: utf-8 -*-
# region Imports
from __future__ import annotations

import logging

from luxtronik.common import get_host_lock
from luxtronik.discover import discover  # noqa: F401

from luxtronik.cfi import (
    LUXTRONIK_DEFAULT_PORT,
    Calculations,  # noqa: F401
    Parameters,  # noqa: F401
    Visibilities,  # noqa: F401
    LuxtronikData,
    LuxtronikSocketInterface,
)
from luxtronik.shi import (
    LUXTRONIK_DEFAULT_MODBUS_PORT,
    LuxtronikModbusTcpInterface,
    Holdings,  # noqa: F401
    Inputs,  # noqa: F401
    LuxtronikSmartHomeData,
    LuxtronikSmartHomeInterface,
    resolve_version,
)
# endregion Imports


LOGGER = logging.getLogger(__name__)


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
            data (LuxtronikAllData | LuxtronikData | LuxtronikSmartHomeData |
                Parameters | Holdings): The data vector (collection) containing field data.
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
        elif type(data) is LuxtronikData:
            with self.lock:
                LuxtronikSocketInterface.write(self, data.parameters)
                shi_result = True
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
            write_data (LuxtronikAllData | LuxtronikData | LuxtronikSmartHomeData |
                Parameters | Holdings): The data vector (collection) containing field data.
                If None is provided, the write is aborted.
            read_data (LuxtronikAllData | None): Optional existing data vector collection
                for the read data. If None is provided, a new instance is created.

        Returns:
            LuxtronikAllData: The passed / created data vector collection for the read data.
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