# -*- coding: utf-8 -*-

import socket
import struct
import datetime
import ipaddress
from luxtronik.lut import LUT as lut

class Luxtronik(object):

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._lut = lut
        self._data = {}
        self._socket = None

    def __connect(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self._host,self._port))

    def __disconnect(self):
        self._socket.close()

    def get_data(self):
        self.__connect()
        self.__read_parameters()
        self.__read_calculations()
        self.__read_visibilities()
        self.__disconnect()
        return self._data

    def set_data(self, id, value):
        self.__connect()
        self.__write_parameter(id,value)
        self.__disconnect()

    def __read_parameters(self):
        data = []
        self._socket.sendall(struct.pack('>ii',3003,0))
        cmd = struct.unpack('>i',self._socket.recv(4))[0]
        len = struct.unpack('>i',self._socket.recv(4))[0]
        for i in range(0,len):
            data.append(struct.unpack('>i',self._socket.recv(4))[0])
        self.__parse(data, "parameters")

    def __write_parameter(self, id, value):
        (i, raw) = self.__compose(id, value, "parameters")
        self._socket.sendall(struct.pack('>iii',3002,i,raw))
        cmd = struct.unpack('>i',self._socket.recv(4))[0]
        ret = struct.unpack('>i',self._socket.recv(4))[0]
        assert(cmd == 3002 and ret == i)

    def __read_calculations(self):
        data = []
        self._socket.sendall(struct.pack('>ii',3004,0))
        cmd = struct.unpack('>i',self._socket.recv(4))[0]
        stat = struct.unpack('>i',self._socket.recv(4))[0]
        len = struct.unpack('>i',self._socket.recv(4))[0]
        for i in range(0,len):
            data.append(struct.unpack('>i',self._socket.recv(4))[0])
        self.__parse(data, "calculations")

    def __read_visibilities(self):
        data = []
        self._socket.sendall(struct.pack('>ii',3005,0))
        cmd = struct.unpack('>i',self._socket.recv(4))[0]
        len = struct.unpack('>i',self._socket.recv(4))[0]
        for i in range(0,len):
            data.append(struct.unpack('>b',self._socket.recv(1))[0])
        self.__parse(data, "visibilities")

    def __parse(self, data, target):
        if not target in self._data:
            self._data[target] = {}
        for i in range(0, len(data)):
            l = self._lut[target].get(i)
            raw = data[i]
            if not l:
                self._data[target][i] = {"id":None, "unit":"unknown", "value":raw}
                continue
            if isinstance(l["conversion"], dict):
                self._data[target][i] = {"id":l["id"], "unit":"info", "value":l["conversion"].get(raw, raw)}
            else:
                if l["conversion"] == "celsius":
                    self._data[target][i] = {"id":l["id"], "unit":"celsius", "value":raw/10}
                elif l["conversion"] == "bool":
                    self._data[target][i] = {"id":l["id"], "unit":"bool", "value":bool(raw)}
                elif l["conversion"] == "seconds":
                    self._data[target][i] = {"id":l["id"], "unit":"seconds", "value":raw}
                elif l["conversion"] == "pulses":
                    self._data[target][i] = {"id":l["id"], "unit":"pulses", "value":raw}
                elif l["conversion"] == "ipaddress":
                    self._data[target][i] = {"id":l["id"], "unit":"ipaddress", "value":f"{raw >> 24 & 0xFF}.{raw >> 16 & 0xFF}.{raw >> 8 & 0xFF}.{raw & 0xFF}"}
                elif l["conversion"] == "timestamp":
                    self._data[target][i] = {"id":l["id"], "unit":"datetime", "value": datetime.datetime.fromtimestamp(raw)} 
                elif l["conversion"] == "errorcode":
                    self._data[target][i] = {"id":l["id"], "unit":"errorcode", "value":raw} 
                elif l["conversion"] == "kelvin":
                    self._data[target][i] = {"id":l["id"], "unit":"kelvin", "value":raw/10}
                elif l["conversion"] == "pressure":
                    self._data[target][i] = {"id":l["id"], "unit":"bar", "value":raw/100}
                elif l["conversion"] == "percent":
                    self._data[target][i] = {"id":l["id"], "unit":"percent", "value":raw/10}
                elif l["conversion"] == "speed":
                    self._data[target][i] = {"id":l["id"], "unit":"rpm", "value":raw}
                elif l["conversion"] == "kwh":
                    self._data[target][i] = {"id":l["id"], "unit":"kWh", "value":raw/10}
                elif l["conversion"] == "voltage":
                    self._data[target][i] = {"id":l["id"], "unit":"volt", "value":raw/10}
                elif l["conversion"] == "version":
                    self._data[target][i] = {"id":l["id"], "unit":"version", "value":"".join([chr(c) for c in data[i:i+9]]).strip('\x00')}
                else:
                    self._data[target][i] = {"id":l["id"], "unit":"unknown", "value":raw}

    def __compose(self, id, value, target):
        for (i, item) in self._lut[target].items():
            if item["id"] == id:
                if item["conversion"] in ["celsius", "kelvin", "percent", "kWh", "volt"]:
                    raw = int(value * 10)
                elif item["conversion"] in ["bar"]:
                    raw = int(value * 100)
                elif item["conversion"] == "ipaddress":
                    raw = struct.unpack('>i',ipaddress.ip_address(value).packed)[0]
                elif item["conversion"] == "datetime":
                    raw = int(datetime.datetime.timestamp(value))
                else:
                    assert(item["conversion"] not in ["version"])
                    raw = int(value)
                if "writable" not in item:
                    raise ValueError(
                        "Writing value for '%s' not not yet tested. If you are sure to write value %d for ID %d, " % (id, raw, i) +
                        "please add 'writable':True to the corresponding dictionary in the lut.py file. " +
                        "Please contribute to this project whether writing was successful or not by setting 'writable' explicitly to " +
                        "True or False. Thanks!")
                if not item["writable"]:
                    raise ValueError("Value not writable.")
                return (i, raw)
        else:
            raise ValueError("Invalid id string.")


