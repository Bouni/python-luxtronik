"""datatype conversions."""
import datetime
import ipaddress


class Base:
    """Base datatype, no conversions."""

    measurement_type = None

    def __init__(self, name, writeable=False):
        self.value = None
        self.name = name
        self.writeable = writeable

    def to_heatpump(self, value):
        """Convert a value into heatpump units."""
        return value

    def from_heatpump(self, value):
        """Convert a value from heatpump units."""
        return value

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)


class SelectionBase(Base):
    """Selection base datatype, converts from an to list of codes."""

    codes = {}

    @property
    def options(self):
        """Return List of all available options."""
        return [value for _, value in self.codes.items()]

    def from_heatpump(self, value):
        if value in self.codes:
            return self.codes.get(value)
        return None

    def to_heatpump(self, value):
        for index, code in self.codes.items():
            if code == value:
                return index
        return None


class Celsius(Base):
    """Celsius datatype, converts from and to Celsius."""

    measurement_type = "celsius"

    def from_heatpump(self, value):
        return value / 10

    def to_heatpump(self, value):
        return int(float(value) * 10)


class Bool(Base):
    """Boolean datatype, converts from and to Boolean."""

    measurement_type = "boolean"

    def from_heatpump(self, value):
        return bool(value)

    def to_heatpump(self, value):
        return int(value)


class Frequency(Base):
    """Frequency datatype, converts from and to Frequency in Hz."""

    measurement_type = "Hz"


class Seconds(Base):
    """Seconds datatype, converts from and to Seconds."""

    measurement_type = "seconds"


class Pulses(Base):
    """Pulses datatype, converts from and to Pulses."""

    measurement_type = "pulses"


class IPAddress(Base):
    """IP Address datatype, converts from and to an IP Address."""

    measurement_type = "ipaddress"

    def from_heatpump(self, value):
        if value < 0:
            return str(ipaddress.IPv4Address(value + 2 ** 32))
        if value > 2 ** 32:
            return str(ipaddress.IPv4Address(value - 2 ** 32))
        return str(ipaddress.IPv4Address(value))

    def to_heatpump(self, value):
        result = int(ipaddress.IPv4Address(value))
        if result > 2 ** 32:
            return result - 2 ** 32
        return result


class Timestamp(Base):
    """Timestamp datatype, converts from and to Timestamp."""

    measurement_type = "timestamp"

    def from_heatpump(self, value):
        return datetime.datetime.fromtimestamp(value)

    def to_heatpump(self, value):
        return datetime.datetime.timestamp(value)


class Errorcode(Base):
    """Errorcode datatype, converts from and to Errorcode."""

    measurement_type = "errorcode"


class Kelvin(Base):
    """Kelvin datatype, converts from and to Kelvin."""

    measurement_type = "kelvin"

    def from_heatpump(self, value):
        return value / 10

    def to_heatpump(self, value):
        return int(value * 10)


class Pressure(Base):
    """Preassure datatype, converts from and to Pressure."""

    measurement_type = "bar"

    def from_heatpump(self, value):
        return value / 100

    def to_heatpump(self, value):
        return int(value * 100)


class Percent(Base):
    """Percent datatype, converts from and to Percent."""

    measurement_type = "percent"

    def from_heatpump(self, value):
        return value / 10

    def to_heatpump(self, value):
        return int(value * 10)


class Percent2(Base):
    """Percent datatype, converts from and to Percent with a differnet scale factor."""

    measurement_type = "percent"

    def from_heatpump(self, value):
        return value

    def to_heatpump(self, value):
        return int(value)


class Speed(Base):
    """Speed datatype, converts from and to Speed."""

    measurement_type = "rpm"


class Power(Base):
    """Power datatype, converts from and to Power."""

    measurement_type = "W"


class Energy(Base):
    """Energy datatype, converts from and to Energy."""

    measurement_type = "energy"

    def from_heatpump(self, value):
        return value / 10

    def to_heatpump(self, value):
        return int(value * 10)


class Voltage(Base):
    """Voltage datatype, converts from and to Voltage."""

    measurement_type = "voltage"

    def from_heatpump(self, value):
        return value / 10

    def to_heatpump(self, value):
        return int(value * 10)


class Hours(Base):
    """Hours datatype, converts from and to Hours."""

    measurement_type = "hours"

    def from_heatpump(self, value):
        return value / 10

    def to_heatpump(self, value):
        return int(value * 10)


class Flow(Base):
    """Flow datatype, converts from and to Flow."""

    measurement_type = "flow"


class Level(Base):
    """Level datatype, converts from and to Level."""

    measurement_type = "level"


class Count(Base):
    """Count datatype, converts from and to Count."""

    measurement_type = "count"


class Version(Base):
    """Version datatype, converts from and to a Heatpump Version."""

    measurement_type = "version"

    def from_heatpump(self, value):
        return "".join([chr(c) for c in value]).strip("\x00")


class Icon(Base):
    """Icon datatype, converts from and to Icon."""

    measurement_type = "icon"


class HeatingMode(SelectionBase):
    """HeatingMode datatype, converts from an to list of HeatingMode codes."""

    measurement_type = "selection"

    codes = {
        0: "Automatic",
        1: "Second heatsource",
        2: "Party",
        3: "Holidays",
        4: "Off",
    }


class CoolingMode(SelectionBase):
    """CoolingMode datatype, converts from an to list of CoolingMode codes."""

    measurement_type = "selection"

    codes = {0: "Off", 1: "Automatic"}


class HotWaterMode(SelectionBase):
    """HotWaterMode datatype, converts from an to list of HotWaterMode codes."""

    measurement_type = "selection"

    codes = {
        0: "Automatic",
        1: "Second heatsource",
        2: "Party",
        3: "Holidays",
        4: "Off",
    }


class PoolMode(SelectionBase):
    """PoolMode datatype, converts from an to list of PoolMode codes."""

    measurement_type = "selection"

    codes = {0: "Automatic", 2: "Party", 3: "Holidays", 4: "Off"}


class MixedCircuitMode(SelectionBase):
    """MixCircuitMode datatype, converts from an to list of MixCircuitMode codes."""

    measurement_type = "selection"

    codes = {0: "Automatic", 2: "Party", 3: "Holidays", 4: "Off"}


class SolarMode(SelectionBase):
    """SolarMode datatype, converts from an to list of SolarMode codes."""

    measurement_type = "selection"

    codes = {
        0: "Automatic",
        1: "Second heatsource",
        2: "Party",
        3: "Holidays",
        4: "Off",
    }


class VentilationMode(SelectionBase):
    """VentilationMode datatype, converts from an to list of VentilationMode codes."""

    measurement_type = "selection"

    codes = {0: "Automatic", 1: "Party", 2: "Holidays", 3: "Off"}


class HeatpumpCode(SelectionBase):
    """HeatpumpCode datatype, converts from an to list of Heatpump codes."""

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
    """BivalanceLevel datatype, converts from an to list of BivalanceLevel codes."""

    measurement_type = "selection"

    codes = {
        1: "one compressor allowed to run",
        2: "two compressors allowed to run",
        3: "additional compressor allowed to run",
    }


class OperationMode(SelectionBase):
    """OperationMode datatype, converts from an to list of OperationMode codes."""

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
    """SwitchOff datatype, converts from an to list of SwitchOff codes."""

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
    """MenuStatusLine datatype, converts from an to list of MenuStatusLine codes."""

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
    """MenuStatusLine datatype, converts from an to list of MenuStatusLine codes."""

    measurement_type = "selection"

    codes = {0: "since", 1: "in"}


class MainMenuStatusLine3(SelectionBase):
    """MenuStatusLine datatype, converts from an to list of MenuStatusLine codes."""

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
    """SecOperationMode datatype, converts from an to list of SecOperationMode codes."""

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
    """Unknown datatype, fallback for unknown data."""

    measurement_type = None
