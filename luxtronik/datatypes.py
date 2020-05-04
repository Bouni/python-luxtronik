import datetime
import ipaddress


class Base:

    measurement_type = None

    def __init__(self, n, w=False):
        self.value = None
        self.name = n
        self.writeable = w

    def _from(self, v):
        return v

    def _to(self, v):
        return v

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)


class SelectionBase(Base):
    @property
    def options(self):
        return [v for k, v in self.codes.items()]

    def _to(self, v):
        if v in self.codes:
            return self.codes.get(v)

    def _from(self, v):
        for i, c in self.codes.items():
            if c == v:
                return i
        return None


class Celsius(Base):

    measurement_type = "celsius"

    def _to(self, v):
        return v / 10

    def _from(self, v):
        return int(float(v) * 10)


class Bool(Base):

    measurement_type = "boolean"

    def _to(self, v):
        return bool(v)

    def _from(self, v):
        return int(v)


class Frequency(Base):

    measurement_type = "Hz"


class Seconds(Base):

    measurement_type = "seconds"


class Pulses(Base):

    measurement_type = "pulses"


class IPAddress(Base):

    measurement_type = "ipaddress"

    def _to(self, v):
        if v<0:
            return str(ipaddress.IPv4Address(v + 2 ** 32))
        if v>2**32:
            return str(ipaddress.IPv4Address(v - 2 ** 32))
        return str(ipaddress.IPv4Address(v))

    def _from(self, v):
        result = int(ipaddress.IPv4Address(v))
        if result > 2 ** 32:
            return result - 2 ** 32
        return result

class Timestamp(Base):

    measurement_type = "timestamp"

    def _to(self, v):
        return datetime.datetime.fromtimestamp(v)

    def _from(self, v):
        return datetime.datetime.timestamp(v)


class Errorcode(Base):

    measurement_type = "errorcode"


class Kelvin(Base):

    measurement_type = "kelvin"

    def _to(self, v):
        return v / 10

    def _from(self, v):
        return int(v * 10)


class Pressure(Base):

    measurement_type = "bar"

    def _to(self, v):
        return v / 100

    def _from(self, v):
        return int(v * 100)


class Percent(Base):

    measurement_type = "percent"

    def _to(self, v):
        return v / 10

    def _from(self, v):
        return int(v * 10)


class Percent2(Base):

    measurement_type = "percent"

    def _to(self, v):
        return v

    def _from(self, v):
        return int(v)




class Speed(Base):

    measurement_type = "rpm"


class Power(Base):

    measurement_type = "W"


class Energy(Base):

    measurement_type = "energy"

    def _to(self, v):
        return v / 10

    def _from(self, v):
        return int(v * 10)


class Voltage(Base):

    measurement_type = "voltage"

    def _to(self, v):
        return v / 10

    def _from(self, v):
        return int(v * 10)


class Hours(Base):

    measurement_type = "hours"

    def _to(self, v):
        return v / 10

    def _from(self, v):
        return int(v * 10)


class Flow(Base):

    measurement_type = "flow"


class Level(Base):

    measurement_type = "level"


class Count(Base):

    measurement_type = "count"


class Version(Base):

    measurement_type = "version"

    def _to(self, v):
        return "".join([chr(c) for c in v]).strip("\x00")

    def _from(self):
        return None


class Icon(Base):

    measurement_type = "icon"


class HeatingMode(SelectionBase):

    measurement_type = "selection"

    codes = {
        0: "Automatic",
        1: "Second heatsource",
        2: "Party",
        3: "Holidays",
        4: "Off",
    }


class CoolingMode(SelectionBase):

    measurement_type = "selection"

    codes = {0: "Off", 1: "Automatic"}


class HotWaterMode(SelectionBase):

    measurement_type = "selection"

    codes = {
        0: "Automatic",
        1: "Second heatsource",
        2: "Party",
        3: "Holidays",
        4: "Off",
    }


class PoolMode(SelectionBase):

    measurement_type = "selection"

    codes = {0: "Automatic", 2: "Party", 3: "Holidays", 4: "Off"}


class MixedCircuitMode(SelectionBase):

    measurement_type = "selection"

    codes = {0: "Automatic", 2: "Party", 3: "Holidays", 4: "Off"}


class SolarMode(SelectionBase):

    measurement_type = "selection"

    codes = {
        0: "Automatic",
        1: "Second heatsource",
        2: "Party",
        3: "Holidays",
        4: "Off",
    }


class VentilationMode(SelectionBase):

    measurement_type = "selection"

    codes = {0: "Automatic", 1: "Party", 2: "Holidays", 3: "Off"}


class Code_WP(SelectionBase):

    measurement_type = "selection"

    codes = {
        0: "ERC",
        1: "SW1",
        2: "SW2",
        3: "WW1",
        4: "WW2",
        5: "L1I",
        6: "L2I",
        7: "L1A",
        8: "L2A",
        9: "KSW",
        10: "KLW",
        11: "SWC",
        12: "LWC",
        13: "L2G",
        14: "WZS",
        15: "L1I407",
        16: "L2I407",
        17: "L1A407",
        18: "L2A407",
        19: "L2G407",
        20: "LWC407",
        21: "L1AREV",
        22: "L2AREV",
        23: "WWC1",
        24: "WWC2",
        25: "L2G404",
        26: "WZW",
        27: "L1S",
        28: "L1H",
        29: "L2H",
        30: "WZWD",
        31: "ERC",
        40: "WWB_20",
        41: "LD5",
        42: "LD7",
        43: "SW 37_45",
        44: "SW 58_69",
        45: "SW 29_56",
        46: "LD5 (230V)",
        47: "LD7 (230 V)",
        48: "LD9",
        49: "LD5 REV",
        50: "LD7 REV",
        51: "LD5 REV 230V",
        52: "LD7 REV 230V",
        53: "LD9 REV 230V",
        54: "SW 291",
        55: "LW SEC",
        56: "HMD 2",
        57: "MSW 4",
        58: "MSW 6",
        59: "MSW 8",
        60: "MSW 10",
        61: "MSW 12",
        62: "MSW 14",
        63: "MSW 17",
        64: "MSW 19",
        65: "MSW 23",
        66: "MSW 26",
        67: "MSW 30",
        68: "MSW 4S",
        69: "MSW 6S",
        70: "MSW 8S",
        71: "MSW 10S",
        72: "MSW 13S",
        73: "MSW 16S",
        74: "MSW2-6S",
        75: "MSW4-16",
    }


class BivalenceLevel(SelectionBase):

    measurement_type = "selection"

    codes = {
        1: "one compressor allowed to run",
        2: "two compressors allowed to run",
        3: "additional compressor allowed to run",
    }


class OperationMode(SelectionBase):

    measurement_type = "selection"

    codes = {
        0: "heating",
        1: "hot water",
        2: "swimming pool/solar",
        3: "evu",
        4: "defrost",
        5: "no request",
        6: "heating external source",
        7: "cooling",
    }


class SwitchoffFile(SelectionBase):

    measurement_type = "selection"

    codes = {
        1: "heatpump error",
        2: "system error",
        3: "evu lock",
        4: "operation mode second heat generator",
        5: "air defrost",
        6: "maximal usage temprature",
        7: "minimal usage temperature",
        8: "lower usage limit",
        9: "no request",
    }


class MainMenuStatusLine1(SelectionBase):

    measurement_type = "selection"

    codes = {
        0: "heatpump running",
        1: "heatpump idle",
        2: "heatpump coming",
        3: "errorcode slot 0",
        4: "defrost",
        5: "witing on LIN connection",
        6: "compressor heating up",
        7: "pump forerun",
    }


class MainMenuStatusLine2(SelectionBase):

    measurement_type = "selection"

    codes = {0: "since", 1: "in"}


class MainMenuStatusLine3(SelectionBase):

    measurement_type = "selection"

    codes = {
        0: "heating",
        1: "no request",
        2: "grid switch on delay",
        3: "cycle lock",
        4: "lock time",
        5: "domestic water",
        6: "info bake out program",
        7: "defrost",
        8: "pump forerun",
        9: "thermal desinfection",
        10: "cooling",
        12: "swimming pool/solar",
        13: "heating external engery source",
        14: "domestic water external energy source",
        16: "flow monitoring",
        17: "second heat generator 1 active",
    }


class SecOperationMode(SelectionBase):

    measurement_type = "selection"

    codes = {
        0: "off",
        1: "cooling",
        2: "heating",
        3: "fault",
        4: "transition",
        5: "defrost",
        6: "waiting",
        7: "waiting",
        8: "transition",
        9: "stop",
        10: "manual",
        11: "simulation start",
        12: "evu lock",
    }


class Unknown(Base):

    measurement_type = None
