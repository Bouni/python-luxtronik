# -*- coding: utf-8 -*-

import socket
import struct
from luxtronik.calculations import Calculations
from luxtronik.parameters import Parameters
from luxtronik.visibilities import Visibilities


class Luxtronik(object):
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._socket = None

    def _connect(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self._host, self._port))

    def _disconnect(self):
        self._socket.close()

    def read(self):
        self._connect()
        self._read_parameters()
        self._read_calculations()
        self._read_visibilities()
        self._disconnect()

    def _read_parameters(self):
        data = []
        self._socket.sendall(struct.pack(">ii", 3003, 0))
        cmd = struct.unpack(">i", self._socket.recv(4))[0]
        len = struct.unpack(">i", self._socket.recv(4))[0]
        for i in range(0, len):
            data.append(struct.unpack(">i", self._socket.recv(4))[0])
        self.parameters = Parameters(data)
        

    def _read_calculations(self):
        data = []
        self._socket.sendall(struct.pack(">ii", 3004, 0))
        cmd = struct.unpack(">i", self._socket.recv(4))[0]
        stat = struct.unpack(">i", self._socket.recv(4))[0]
        len = struct.unpack(">i", self._socket.recv(4))[0]
        for i in range(0, len):
            data.append(struct.unpack(">i", self._socket.recv(4))[0])
        self.calculations = Calculations(data)

    def _read_visibilities(self):
        data = []
        self._socket.sendall(struct.pack(">ii", 3005, 0))
        cmd = struct.unpack(">i", self._socket.recv(4))[0]
        len = struct.unpack(">i", self._socket.recv(4))[0]
        for i in range(0, len):
            data.append(struct.unpack(">b", self._socket.recv(1))[0])
        self.visibilities = Visibilities(data)
