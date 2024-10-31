"""datatype conversions."""

import datetime
import socket
import struct

from functools import total_ordering


@total_ordering
class Base:
    """Base datatype, no conversions."""

    datatype_class = None
    datatype_unit = None

    def __init__(self, name, writeable=False):
        """Initialize the base data field class. Set the initial raw value to None"""
        # save the raw value only since the user value
        # could be build at any time
        self._raw = None
        self.name = name
        self.writeable = writeable

    @classmethod
    def to_heatpump(cls, value):
        """Converts value into heatpump units."""
        return value

    @classmethod
    def from_heatpump(cls, value):
        """Converts value from heatpump units."""
        return value

    @property
    def value(self):
        """Return the stored value converted from heatpump units."""
        return self.from_heatpump(self._raw)

    @value.setter
    def value(self, value):
        """Converts the value into heatpump units and store it."""
        self._raw = self.to_heatpump(value)

    @property
    def raw(self):
        """Return the stored raw data."""
        return self._raw

    @raw.setter
    def raw(self, raw):
        """Store the raw data."""
        self._raw = raw

    def __repr__(self):
        """Returns a printable representation of the datatype object"""

        return (
            f"{self.__class__.__name__} "
            f"("
            f"name: {self.name}, "
            f"writeable: {self.writeable}, "
            f"value: {self.value}, "
            f"raw: {self._raw}, "
            f"class: {self.datatype_class}, "
            f"unit: {self.datatype_unit}"
            f")"
        )

    def __str__(self):
        """Returns a human-readable string representation of the datatype object"""

        value = self.value
        if value is not None:
            return str(value)
        return str(self.raw)

    def __eq__(self, other):
        """Tests for equality of two datatype objects"""

        if not isinstance(other, Base):
            return False

        return (
            self.value == other.value
            and self.datatype_class == other.datatype_class
            and self.datatype_unit == other.datatype_unit
        )

    def __lt__(self, other):
        """Compares two datatype objects and returns which one contains the lower value"""

        return (
            self.value < other.value
            and self.datatype_class == other.datatype_class
            and self.datatype_unit == other.datatype_unit
        )


class SelectionBase(Base):
    """Selection base datatype, converts from and to list of codes."""

    datatype_class = "selection"

    codes = {}

    @classmethod
    def options(cls):
        """Return list of all available options."""
        return [value for _, value in cls.codes.items()]

    @classmethod
    def from_heatpump(cls, value):
        if value in cls.codes:
            return cls.codes.get(value)
        return None

    @classmethod
    def to_heatpump(cls, value):
        for index, code in cls.codes.items():
            if code == value:
                return index
        return None


class ScalingBase(Base):
    """Scaling base datatype, converts via a scaling factor."""

    datatype_class = "scaling"

    scaling_factor = 1

    @classmethod
    def from_heatpump(cls, value):
        if value is None:
            return None
        value = value * cls.scaling_factor
        return value

    @classmethod
    def to_heatpump(cls, value):
        raw = round(float(value) / cls.scaling_factor)
        return raw


class Celsius(ScalingBase):
    """Celsius datatype, converts from and to Celsius."""

    datatype_class = "temperature"
    datatype_unit = "°C"
    scaling_factor = 0.1


class Bool(Base):
    """Boolean datatype, converts from and to Boolean."""

    datatype_class = "boolean"

    @classmethod
    def from_heatpump(cls, value):
        return bool(value)

    @classmethod
    def to_heatpump(cls, value):
        return int(value)


class Frequency(Base):
    """Frequency datatype, converts from and to Frequency in Hz."""

    datatype_class = "frequency"
    datatype_unit = "Hz"


class Seconds(Base):
    """Seconds datatype, converts from and to Seconds."""

    datatype_class = "timespan"
    datatype_unit = "s"


class IPv4Address(Base):
    """IPv4 address datatype, converts from and to an IPv4 address."""

    datatype_class = "ipv4_address"

    @classmethod
    def from_heatpump(cls, value):
        return socket.inet_ntoa(struct.pack(">i", value))

    @classmethod
    def to_heatpump(cls, value):
        return struct.unpack(">i", socket.inet_aton(value))[0]


class Timestamp(Base):
    """Timestamp datatype, converts from and to Timestamp."""

    datatype_class = "timestamp"

    @classmethod
    def from_heatpump(cls, value):
        if value is None:
            return None
        if value <= 0:
            return datetime.datetime.fromtimestamp(0)
        return datetime.datetime.fromtimestamp(value)

    @classmethod
    def to_heatpump(cls, value):
        return datetime.datetime.timestamp(value)


class Errorcode(SelectionBase):
    """Errorcode datatype, converts from and to Errorcode."""

    datatype_class = "errorcode"

    codes = {
        700: "sensor external return",
        701: "error low pressure",
        702: "low pressure blockade",
        703: "frost protection",
        704: "error hot gas",
        705: "motor protection",
        706: "motor protection BSUP",
        707: "encoding heat pump",
        708: "sensor return",
        709: "sensor flow",
        710: "sensor hot gas",
        711: "sensor outdoor temp.",
        712: "sensor DHW",
        713: "sensor heat source in",
        714: "hot gas DHW",
        715: "high pressure switch-off",
        716: "error high pressure",
        717: "flow rate",
        718: "max. outdoor temp.",
        719: "min. outdoor temp.",
        720: "min. heat source temp.",
        721: "low pressure switch-off",
        722: "temp. difference heating",
        723: "temp. difference DHW",
        724: "temp. difference defrosting",
        725: "error DHW",
        726: "sensor mixing circuit 1",
        727: "brine pressure",
        728: "sensor heat source out",
        729: "error phase sequence",
        730: "capacity screed heating",
        731: "interruption TDI",
        732: "error cooling",
        733: "error electrical anode",
        734: "electrical anode DHW",
        735: "sensor external energy",
        736: "sensor solar panel",
        737: "sensor solar tank",
        738: "sensor mixing circuit 2",
        739: "sensor mixing circuit 3",
        750: "sensor return external",
        751: "phase sequence monitoring",
        752: "power supply / flow",
        755: "connection to slave lost",
        756: "connection to master lost",
        757: "low pressure block",
        758: "error defrosting",
        759: "fault TDI",
        760: "error defrosting",
        761: "LIN-connection lost",
        762: "suction compressor",
        763: "suction evaporator",
        764: "compressor oil sump",
        765: "overheating",
        766: "operating limits-compressor",
        767: "STL immersion heater",
        768: "flow rate control",
        769: "pump control",
        770: "low overheat",
        771: "high overheat",
        772: "OL too low condensation",
        773: "OL too high condensation",
        774: "OL too low evaporation",
        775: "expansion valve EVI",
        776: "operating limits-compressor",
        777: "expansion valve",
        778: "sensor low pressure",
        779: "sensor high pressure",
        780: "sensor EVI",
        781: "sensor liquid ahead exp. valve",
        782: "sensor EVi suction gas",
        783: "communication SEC - Inverter",
        784: "inverter blocked",
        785: "SEC-Board defect",
        786: "communication SEC - Inverter",
        787: "VD alert",
        788: "serious inverter error",
        789: "LIN/encoding not found",
        790: "serious inverter error",
        791: "Modbus inverter",
        792: "LIN-connection lost",
        793: "serious inverter error",
        794: "overvoltage",
        795: "undervoltage",
        796: "safety shutdown",
        797: "MLRH is not supported",
        798: "Modbus fan",
        799: "Modbus ASB",
        800: "safety stop desuperheater",
        802: "switch box fan",
        803: "switch box fan",
        804: "sensor switch box",
        805: "sensor desuperheater",
        806: "Modbus SEC",
        807: "Lost modbus connection",
    }


class Kelvin(ScalingBase):
    """Kelvin datatype, converts from and to Kelvin."""

    datatype_class = "temperature"
    datatype_unit = "K"
    scaling_factor = 0.1


class Pressure(ScalingBase):
    """Pressure datatype, converts from and to Pressure."""

    datatype_class = "pressure"
    datatype_unit = "bar"
    scaling_factor = 0.01


class Percent(ScalingBase):
    """Percent datatype, converts from and to Percent."""

    datatype_class = "percent"
    datatype_unit = "%"
    scaling_factor = 0.1


class Percent2(Base):
    """Percent datatype, converts from and to Percent with a different scaling factor."""

    datatype_class = "percent"
    datatype_unit = "%"


class Speed(Base):
    """Speed datatype, converts from and to Speed."""

    datatype_class = "speed"
    datatype_unit = "rpm"


class Power(Base):
    """Power datatype, converts from and to Power."""

    datatype_class = "power"
    datatype_unit = "W"


class Energy(ScalingBase):
    """Energy datatype, converts from and to Energy."""

    datatype_class = "energy"
    datatype_unit = "kWh"
    scaling_factor = 0.1


class Voltage(ScalingBase):
    """Voltage datatype, converts from and to Voltage."""

    datatype_class = "voltage"
    datatype_unit = "V"
    scaling_factor = 0.1


class Hours(ScalingBase):
    """Hours datatype, converts from and to Hours."""

    datatype_class = "timespan"
    datatype_unit = "h"
    scaling_factor = 0.1


class Hours2(Base):
    """Hours datatype, converts from and to Hours with a different scaling factor."""

    datatype_class = "timespan"
    datatype_unit = "h"

    @classmethod
    def from_heatpump(cls, value):
        if value is None:
            return None
        return 1 + value / 2

    @classmethod
    def to_heatpump(cls, value):
        return round((value - 1) * 2)


class Minutes(Base):
    """Minutes datatype, converts from and to Minutes."""

    datatype_class = "timespan"
    datatype_unit = "min"


class Flow(Base):
    """Flow datatype, converts from and to Flow."""

    datatype_class = "flow"
    datatype_unit = "l/h"


class Level(Base):
    """Level datatype, converts from and to Level."""

    datatype_class = "level"


class Count(Base):
    """Count datatype, converts from and to Count."""

    datatype_class = "count"


class Character(Base):
    """Character datatype, converts from and to a Character."""

    datatype_class = "character"

    @classmethod
    def from_heatpump(cls, value):
        if value == 0:
            return ""
        return chr(value)


class MajorMinorVersion(Base):
    """MajorMinorVersion datatype, converts from and to a RBEVersion"""

    datatype_class = "version"

    @classmethod
    def from_heatpump(cls, value):
        if value > 0:
            major = value // 100
            minor = value % 100
            return f"{major}.{minor}"
        return "0"


class Icon(Base):
    """Icon datatype, converts from and to Icon."""

    datatype_class = "icon"


class HeatingMode(SelectionBase):
    """HeatingMode datatype, converts from and to list of HeatingMode codes."""

    datatype_class = "selection"

    codes = {
        0: "Automatic",
        1: "Second heatsource",
        2: "Party",
        3: "Holidays",
        4: "Off",
    }


class CoolingMode(SelectionBase):
    """CoolingMode datatype, converts from and to list of CoolingMode codes."""

    datatype_class = "selection"

    codes = {0: "Off", 1: "Automatic"}


class HotWaterMode(SelectionBase):
    """HotWaterMode datatype, converts from and to list of HotWaterMode codes."""

    datatype_class = "selection"

    codes = {
        0: "Automatic",
        1: "Second heatsource",
        2: "Party",
        3: "Holidays",
        4: "Off",
    }


class PoolMode(SelectionBase):
    """PoolMode datatype, converts from and to list of PoolMode codes."""

    datatype_class = "selection"

    codes = {0: "Automatic", 2: "Party", 3: "Holidays", 4: "Off"}


class MixedCircuitMode(SelectionBase):
    """MixCircuitMode datatype, converts from and to list of MixCircuitMode codes."""

    datatype_class = "selection"

    codes = {0: "Automatic", 2: "Party", 3: "Holidays", 4: "Off"}


class SolarMode(SelectionBase):
    """SolarMode datatype, converts from and to list of SolarMode codes."""

    datatype_class = "selection"

    codes = {
        0: "Automatic",
        1: "Second heatsource",
        2: "Party",
        3: "Holidays",
        4: "Off",
    }


class VentilationMode(SelectionBase):
    """VentilationMode datatype, converts from and to list of VentilationMode codes."""

    datatype_class = "selection"

    codes = {0: "Automatic", 1: "Party", 2: "Holidays", 3: "Off"}


class HeatpumpCode(SelectionBase):
    """HeatpumpCode datatype, converts from and to list of Heatpump codes."""

    datatype_class = "selection"

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
        32: "ERC",
        33: "ERC",
        34: "ERC",
        35: "ERC",
        36: "ERC",
        37: "ERC",
        38: "ERC",
        39: "ERC",
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
        72: "MSW 12S",
        73: "MSW 16S",
        74: "MSW2-6S",
        75: "MSW4-16",
        76: "LD2AG",
        77: "LD9V",
        78: "MSW3-12",
        79: "MSW3-12S",
        80: "MSW2-9S",
        81: "LW 8",
        82: "LW 12",
        83: "HZ_HMD",
        84: "LW V4",
        85: "LW SEC 2",
        86: "MSW1-4S",
        87: "LP5V",
        88: "LP8V",
    }


class BivalenceLevel(SelectionBase):
    """BivalanceLevel datatype, converts from and to list of BivalanceLevel codes."""

    datatype_class = "selection"

    codes = {
        1: "one compressor allowed to run",
        2: "two compressors allowed to run",
        3: "additional heat generator allowed to run",
    }


class OperationMode(SelectionBase):
    """OperationMode datatype, converts from and to list of OperationMode codes."""

    datatype_class = "selection"

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
    """SwitchOff datatype, converts from and to list of SwitchOff codes."""

    datatype_class = "selection"

    codes = {
        0: "heatpump error",
        1: "system error",
        2: "operation mode second heat generator",
        3: "evu lock",
        5: "air defrost",
        6: "maximal usage temperature",
        7: "minimal usage temperature",
        8: "lower usage limit",
        9: "no request",
        10 : "external energy source",
        11: "flow rate",
        12 : "low pressure pause",
        13 : "superheating pause",
        14 : "inverter pause",
        15 : "desuperheater pause",
        16 : "operation mode for switching over",
        17 : "other shutdown",
        18 : "min.flow cooling",
        19: "PV max",
        20 : "hot gas pause",
        21 : "overheating hot gas pause",
        22 : "no request",
        23 : "min. heat source out cooling",
        24 : "LPC",
        25 : "restart",
    }


class MainMenuStatusLine1(SelectionBase):
    """MenuStatusLine datatype, converts from and to list of MenuStatusLine codes."""

    datatype_class = "selection"

    codes = {
        0: "heatpump running",
        1: "heatpump idle",
        2: "heatpump coming",
        3: "errorcode slot 0",
        4: "defrost",
        5: "waiting on LIN connection",
        6: "compressor heating up",
        7: "pump forerun",
    }


class MainMenuStatusLine2(SelectionBase):
    """MenuStatusLine datatype, converts from and to list of MenuStatusLine codes."""

    datatype_class = "selection"

    codes = {0: "since", 1: "in"}


class MainMenuStatusLine3(SelectionBase):
    """MenuStatusLine datatype, converts from and to list of MenuStatusLine codes."""

    datatype_class = "selection"

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
        13: "heating external energy source",
        14: "domestic water external energy source",
        16: "flow monitoring",
        17: "second heat generator 1 active",
    }


class SecOperationMode(SelectionBase):
    """SecOperationMode datatype, converts from and to list of SecOperationMode codes."""

    datatype_class = "selection"

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


class AccessLevel(SelectionBase):
    """AccessLevel datatype, converts from and to list of AccessLevel codes"""

    datatype_class = "selection"

    codes = {
        0: "user",
        1: "after sales service",
        2: "manufacturer",
        3: "installer",
    }


class TimerProgram(SelectionBase):
    """TimerProgram datatype, converts from and to list of TimerProgram codes"""

    datatype_class = "selection"

    codes = {
        0: "week",
        1: "5+2",
        2: "days",
    }


class TimeOfDay(Base):
    """TimeOfDay datatype, converts from and to TimeOfDay."""

    datatype_class = "timeofday"

    @classmethod
    def from_heatpump(cls, value):
        if value is None:
            return None
        hours = value // 3600
        minutes = (value // 60) % 60
        seconds = value % 60

        return f"{hours}:{minutes:02d}" + (f":{seconds:02d}" if seconds > 0 else "")

    @classmethod
    def to_heatpump(cls, value):
        d = [int(v) for v in value.split(":")]

        val = d[0] * 3600 + d[1] * 60
        if len(d) == 3:
            val += d[2]

        return val


class TimeOfDay2(Base):
    """TimeOfDay2 datatype, converts from and to a range of two times of day."""

    datatype_class = "timeofday2"

    @classmethod
    def from_heatpump(cls, value):
        if value is None:
            return None

        value_low = value & 0xFFFF
        value_high = value >> 16
        hours1 = value_low // 60
        minutes1 = value_low % 60
        hours2 = value_high // 60
        minutes2 = value_high % 60

        return f"{hours1}:{minutes1:02d}-{hours2}:{minutes2:02d}"

    @classmethod
    def to_heatpump(cls, value):
        d = value.split("-")
        low = [int(v) for v in d[0].split(":")]
        high = [int(v) for v in d[1].split(":")]

        val = ((high[0] * 60 + high[1]) << 16) + low[0] * 60 + low[1]

        return val


class Unknown(Base):
    """Unknown datatype, fallback for unknown data."""

    datatype_class = None
