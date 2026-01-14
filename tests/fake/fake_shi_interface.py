from luxtronik.shi import (
    LuxtronikSmartHomeInterface,
    LuxtronikSmartHomeData,
    Inputs,
    Holdings,
)


class FakeShiInterface(LuxtronikSmartHomeInterface):

    write_counter = 0
    read_counter = 0

    class dummy:
        pass

    @classmethod
    def for_script_test(cls):
        obj = cls.__new__(cls)
        obj._interface = cls.dummy()
        obj._interface._client = cls.dummy()
        obj._interface._client._host = "host"
        obj._interface._client._port = "port"
        return obj

    @classmethod
    def reset(cls):
        FakeShiInterface.write_counter = 0
        FakeShiInterface.read_counter = 0

    def read(self, data):
        if not data:
            data = LuxtronikSmartHomeData()
        FakeShiInterface.read_inputs(self, data.inputs)
        FakeShiInterface.read_holdings(self, data.holdings)
        return data

    def read_inputs(self, inputs=None):
        if inputs is None:
            inputs = Inputs()
        inputs[0].raw = 3
        FakeShiInterface.read_counter += 1
        return inputs

    def read_holdings(self, holdings=None):
        if not holdings:
            holdings = Holdings()
        holdings[1].raw = 5
        FakeShiInterface.read_counter += 1
        return holdings

    def write(self, data):
        return FakeShiInterface.write_holdings(self, data.holdings)

    def write_holdings(self, holdings):
        FakeShiInterface.write_counter += 1
        return True