import datetime


class Base:

    unit = None

    def __init__(self, v):
        self._convert(v)

    def _convert(self, v):
        self.value = v

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)


class Celsius(Base):

    unit = "°C"

    def _convert(self, v):
        self.value = v / 10


class Bool(Base):
    def _convert(self, v):
        self.value = bool(v)


class Seconds(Base):

    unit = "s"

    def _convert(self, v):
        self.value = v


class Pulses(Base):
    def _convert(self, v):
        self.value = v


class IPAddress(Base):
    def _convert(self, v):
        self.value = f"{v >> 24 & 0xFF}.{v >> 16 & 0xFF}.{v >> 8 & 0xFF}.{v & 0xFF}"


class Timestamp(Base):
    def _convert(self, v):
        self.value = datetime.datetime.fromtimestamp(v)


class Errorcode(Base):
    def _convert(self, v):
        self.value = v


class Kelvin(Base):

    unit = "K"

    def _convert(self, v):
        self.value = v / 10


class Pressure(Base):

    unit = "bar"

    def _convert(self, v):
        self.value = v / 100


class Percent(Base):

    unit = "%"

    def _convert(self, v):
        self.value = v / 10


class Speed(Base):

    unit = "rpm"

    def _convert(self, v):
        self.value = v


class Energy(Base):

    unit = "kWh"

    def _convert(self, v):
        self.value = v / 10


class Voltage(Base):

    unit = "V"

    def _convert(self, v):
        self.value = v / 10


class Hours(Base):

    unit = "h"

    def _convert(self, v):
        self.value = v / 7200


class Flow(Base):

    unit = "l/h"

    def _convert(self, v):
        self.value = v


class Level(Base):
    def _convert(self, v):
        self.value = v


class Count(Base):
    def _convert(self, v):
        self.value = v


class Version(Base):
    def _convert(self, v):
        self.value = "".join([chr(c) for c in v]).strip("\x00")


class Icon(Base):
    def _convert(self, v):
        self.value = v


class Code_WP(Base):
    def _convert(self, v):
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
        self.value = codes.get(v, "Unknown")


class BivalenceLevel(Base):
    def _convert(self, v):
        codes = {
            1: "one compressor allowed to run",
            2: "two compressors allowed to run",
            3: "additional compressor allowed to run",
        }
        self.value = codes.get(v, "Unknown")


class OperationMode(Base):
    def _convert(self, v):
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

        self.value = codes.get(v, "Unknown")


class SwitchoffFile(Base):
    def _convert(self, v):
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
        self.value = codes.get(v, "Unknown")


class MainMenuStatusLine1(Base):
    def _convert(self, v):
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
        self.value = codes.get(v, "Unknown")


class MainMenuStatusLine2(Base):
    def _convert(self, v):
        codes = {0: "since", 1: "in"}
        self.value = codes.get(v, "Unknown")


class MainMenuStatusLine3(Base):
    def _convert(self, v):
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
        self.value = codes.get(v, "Unknown")


class SecOperationMode(Base):
    def _convert(self, v):
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
        self.value = codes.get(v, "Unknown")


class Unknown(Base):
    def _convert(self, v):
        self.value = v
