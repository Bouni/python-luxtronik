# -*- coding: utf-8 -*-

import socket
import struct
import logging
from luxtronik.calculations import Calculations
from luxtronik.parameters import Parameters
from luxtronik.visibilities import Visibilities

LOGGER = logging.getLogger("Luxtronik")


class Luxtronik:
    def __init__(self, host, port, safe=True):
        self._host = host
        self._port = port
        self._socket = None
        self.calculations = Calculations()
        self.parameters = Parameters(safe=safe)
        self.visibilities = Visibilities()
        self.read()

    def _connect(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self._host, self._port))
        LOGGER.info(f"Connected to Luxtronik heatpump {self._host}:{self._port}")

    def _disconnect(self):
        self._socket.close()
        LOGGER.info(f"Disconnected from Luxtronik heatpump {self._host}:{self._port}")

    def read(self):
        self._connect()
        self._read_parameters()
        self._read_calculations()
        self._read_visibilities()
        self._disconnect()

    def write(self):
        self._connect()
        for id, value in self.parameters._queue.items():
            if not isinstance(id, int) or not isinstance(value, int):
                LOGGER.warn(f"Parameter id '{id}' or value '{value}' invalid!")
                continue
            LOGGER.info(f"Parameter '{id}' set to '{value}'")
            data = struct.pack(">iii", 3002, id, value)
            self._socket.sendall(data)
            cmd = struct.unpack(">i", self._socket.recv(4))[0]
            val = struct.unpack(">i", self._socket.recv(4))[0]
        self._disconnect()
        # flush queue after writing all values
        self.parameters._queue = {}

    def _read_parameters(self):
        data = []
        self._socket.sendall(struct.pack(">ii", 3003, 0))
        cmd = struct.unpack(">i", self._socket.recv(4))[0]
        len = struct.unpack(">i", self._socket.recv(4))[0]
        for i in range(0, len):
            data.append(struct.unpack(">i", self._socket.recv(4))[0])
        LOGGER.info(f"Read {len} parameters")
        self.parameters._parse(data)

    def _read_calculations(self):
        data = []
        self._socket.sendall(struct.pack(">ii", 3004, 0))
        cmd = struct.unpack(">i", self._socket.recv(4))[0]
        stat = struct.unpack(">i", self._socket.recv(4))[0]
        len = struct.unpack(">i", self._socket.recv(4))[0]
        for i in range(0, len):
            data.append(struct.unpack(">i", self._socket.recv(4))[0])
        LOGGER.info(f"Read {len} calculations")
        self.calculations._parse(data)

    def _read_visibilities(self):
        data = []
        self._socket.sendall(struct.pack(">ii", 3005, 0))
        cmd = struct.unpack(">i", self._socket.recv(4))[0]
        len = struct.unpack(">i", self._socket.recv(4))[0]
        for i in range(0, len):
            data.append(struct.unpack(">b", self._socket.recv(1))[0])
        LOGGER.info(f"Read {len} visibilities")
        self.visibilities._parse(data)
