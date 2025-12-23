#! /usr/bin/env python3
# pylint: disable=invalid-name
"""
Script to measure different access methods of the Smart-Home-Interface.
"""

import time

from luxtronik.scripts import (
    create_default_args_parser
)
from luxtronik.shi import create_modbus_tcp
from luxtronik.shi.constants import LUXTRONIK_DEFAULT_MODBUS_PORT
from luxtronik.shi.common import LuxtronikSmartHomeReadInputsTelegram

class TimeMeasurement:
    def __init__(self):
        self.duration = 0
        self._start = 0

    def __enter__(self):
        self._start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb):
        end = time.perf_counter()
        self.duration = end - self._start

def performance_shi():
    parser = create_default_args_parser(
        "Measure different access methods of the Smart-Home-Interface.",
        LUXTRONIK_DEFAULT_MODBUS_PORT
    )
    args = parser.parse_args()
    print(f"Measure SHI performance of {args.ip}:{args.port}")

    shi = create_modbus_tcp(args.ip, args.port)
    client = shi._interface
    num_inputs = len(shi.inputs)

    with TimeMeasurement() as t:
        client._connect()
        for _ in range(0, 100):
            client._client.read_input_registers(10002, 1)
        client._disconnect()
    print(f"Read inputs with bare modbus interface: {100 / t.duration:.1f} fields/s")

    with TimeMeasurement() as t:
        for _ in range(0, 100):
            client.read_inputs(10002, 1)
    print(f"Read inputs one after another with re-connect every time: {100 / t.duration:.1f} fields/s")

    with TimeMeasurement() as t:
        telegrams = []
        for _ in range(0, 100):
            telegrams.append(LuxtronikSmartHomeReadInputsTelegram(10002, 1))
        client.send(telegrams)
    print(f"Read inputs within one telegram list: {100 / t.duration:.1f} fields/s")

    with TimeMeasurement() as t:
        telegrams = []
        for definition in shi.inputs:
            telegrams.append(LuxtronikSmartHomeReadInputsTelegram(definition.addr, definition.count))
        for _ in range(0, 10):
            client.send(telegrams)
    print(f"Read whole input vector field by field: {(10 * num_inputs) / t.duration:.1f} fields/s")

    with TimeMeasurement() as t:
        inputs = shi.create_inputs()
        for _ in range(0, 10):
            shi.read_inputs(inputs)
    print(f"Read whole input vector with data blocks (same data vector): {(10 * num_inputs) / t.duration:.1f} fields/s")

    with TimeMeasurement() as t:
        for _ in range(0, 10):
            shi.read_inputs()
    print(f"Read whole input vector with data blocks (create new data vectors): {(10 * num_inputs) / t.duration:.1f} fields/s")

    with TimeMeasurement() as t:
        inputs = shi.create_inputs()
        for _ in range(0, 5):
            for _ in range(0, 5):
                shi.collect_inputs(inputs)
            shi.send()
    print(f"Collect and send multiple input vectors: {(5 * 5 * num_inputs) / t.duration:.1f} fields/s")


if __name__ == "__main__":
    performance_shi()
