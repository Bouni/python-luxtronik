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
        return f"{self.__class__.__name__} (name: {self.name}, writeable: {self.writeable}, value: {self.value}, raw: {self._raw}, data class: {self.datatype_class}, unit: {self.datatype_unit})"

    def __str__(self):
        value = self.value
        if value is not None:
            return str(value)
        return str(self.raw)

    def __eq__(self, other):
        return (
            self.value == other.value
            and self.datatype_class == other.datatype_class
            and self.datatype_unit == other.datatype_unit
        )

    def __lt__(self, other):
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


class Celsius(Base):
    """Celsius datatype, converts from and to Celsius."""

    datatype_class = "temperature"
    datatype_unit = "°C"

    @classmethod
    def from_heatpump(cls, value):
        if value is None:
            return None
        return value / 10

    @classmethod
    def to_heatpump(cls, value):
        return int(float(value) * 10)


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


class Errorcode(Base):
    """Errorcode datatype, converts from and to Errorcode."""

    datatype_class = "errorcode"


class Kelvin(Base):
    """Kelvin datatype, converts from and to Kelvin."""

    datatype_class = "temperature"
    datatype_unit = "K"

    @classmethod
    def from_heatpump(cls, value):
        if value is None:
            return None
        return value / 10

    @classmethod
    def to_heatpump(cls, value):
        return int(float(value) * 10)


class Pressure(Base):
    """Pressure datatype, converts from and to Pressure."""

    datatype_class = "pressure"
    datatype_unit = "bar"

    @classmethod
    def from_heatpump(cls, value):
        if value is None:
            return None
        return value / 100

    @classmethod
    def to_heatpump(cls, value):
        return int(value * 100)


class Percent(Base):
    """Percent datatype, converts from and to Percent."""

    datatype_class = "percent"
    datatype_unit = "%"

    @classmethod
    def from_heatpump(cls, value):
        if value is None:
            return None
        return value / 10

    @classmethod
    def to_heatpump(cls, value):
        return int(value * 10)


class Percent2(Base):
    """Percent datatype, converts from and to Percent with a different scale factor."""

    datatype_class = "percent"
    datatype_unit = "%"

    @classmethod
    def from_heatpump(cls, value):
        return value

    @classmethod
    def to_heatpump(cls, value):
        return int(value)


class Speed(Base):
    """Speed datatype, converts from and to Speed."""

    datatype_class = "speed"
    datatype_unit = "rpm"


class Power(Base):
    """Power datatype, converts from and to Power."""

    datatype_class = "power"
    datatype_unit = "W"


class Energy(Base):
    """Energy datatype, converts from and to Energy."""

    datatype_class = "energy"
    datatype_unit = "kWh"

    @classmethod
    def from_heatpump(cls, value):
        if value is None:
            return None
        return value / 10

    @classmethod
    def to_heatpump(cls, value):
        return int(value * 10)


class Voltage(Base):
    """Voltage datatype, converts from and to Voltage."""

    datatype_class = "voltage"
    datatype_unit = "V"

    @classmethod
    def from_heatpump(cls, value):
        if value is None:
            return None
        return value / 10

    @classmethod
    def to_heatpump(cls, value):
        return int(value * 10)


class Hours(Base):
    """Hours datatype, converts from and to Hours."""

    datatype_class = "timespan"
    datatype_unit = "h"

    @classmethod
    def from_heatpump(cls, value):
        if value is None:
            return None
        return value / 10

    @classmethod
    def to_heatpump(cls, value):
        return int(value * 10)


class Hours2(Base):
    """Hours datatype, converts from and to Hours with a different scale factor."""

    datatype_class = "timespan"
    datatype_unit = "h"

    @classmethod
    def from_heatpump(cls, value):
        if value is None:
            return None
        return 1 + value / 2

    @classmethod
    def to_heatpump(cls, value):
        return int((value - 1) * 2)


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


class Version(Base):
    """Version datatype, converts from and to a Heatpump Version."""

    datatype_class = "version"

    @classmethod
    def from_heatpump(cls, value):
        return "".join([chr(c) for c in value]).strip("\x00")


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
        1: "heatpump error",
        2: "system error",
        3: "evu lock",
        4: "operation mode second heat generator",
        5: "air defrost",
        6: "maximal usage temperature",
        7: "minimal usage temperature",
        8: "lower usage limit",
        9: "no request",
        11: "flow rate",
        19: "PV max",
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


class Unknown(Base):
    """Unknown datatype, fallback for unknown data."""

    datatype_class = None
