"""Test suite for datatypes module"""

# pylint: disable=too-few-public-methods,invalid-name,too-many-lines

import datetime

from luxtronik.constants import (
    LUXTRONIK_NAME_CHECK_NONE,
    LUXTRONIK_NAME_CHECK_PREFERRED,
    LUXTRONIK_NAME_CHECK_OBSOLETE,
)

from luxtronik.datatypes import (
    Base,
    SelectionBase,
    ScalingBase,
    Celsius,
    Bool,
    Frequency,
    Seconds,
    IPv4Address,
    Timestamp,
    Errorcode,
    Kelvin,
    Pressure,
    Percent,
    Percent2,
    Speed,
    Power,
    PowerLimit,
    Energy,
    Voltage,
    Hours,
    Hours2,
    Minutes,
    Flow,
    Level,
    Count,
    Character,
    MajorMinorVersion,
    FullVersion,
    Icon,
    HeatingMode,
    CoolingMode,
    HotWaterMode,
    PoolMode,
    MixedCircuitMode,
    SolarMode,
    VentilationMode,
    HeatpumpCode,
    BivalenceLevel,
    OperationMode,
    SwitchoffFile,
    MainMenuStatusLine1,
    MainMenuStatusLine2,
    SecOperationMode,
    AccessLevel,
    Unknown,
    TimerProgram,
    TimeOfDay,
    TimeOfDay2,
)


def check_pair(datatype, raw_value, value):
    """Checks whether a pair of values are converted to each other."""
    assert datatype.from_heatpump(raw_value) == value
    assert datatype.to_heatpump(value) == raw_value


def check_round_trip(datatype, val):
    """Check whether a raw value is persistent under a round-trip."""
    assert datatype.to_heatpump(datatype.from_heatpump(val)) == val


class TestBase:
    """Test suite for Base datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Base("base")
        assert a.name == "base"
        assert a.writeable is False

        b = Base("base", writeable=True)
        assert b.name == "base"
        assert b.writeable is True

        c = Base("base", True)
        assert c.name == "base"
        assert c.writeable is True

    def test_from_heatpump(self):
        """Test cases for from_heatpump function"""

        assert Base.from_heatpump(23) == 23

    def test_to_heatpump(self):
        """Test cases for to_heatpump function"""

        assert Base.to_heatpump(42) == 42

    def test_name(self):
        """Test cases for name property"""
        base = Base(["foo", "bar"])

        assert base.name == "foo"

    def test_empty_name(self):
        """Test cases for name property"""
        try:
            Base([])
            assert False
        except Exception:
            pass
        try:
            Base(None)
            assert False
        except Exception:
            pass

    def test_check_name(self):
        """Test cases for check_name() function"""
        base = Base(["foo", "bar"])

        assert base.check_name("foo") == LUXTRONIK_NAME_CHECK_PREFERRED
        assert base.check_name("bar") == LUXTRONIK_NAME_CHECK_OBSOLETE
        assert base.check_name("baz") == LUXTRONIK_NAME_CHECK_NONE

    def test_value_property(self):
        """Test case for value property"""

        a = Base("base")
        a._raw = 19
        assert a.value == 19

    def test_value_setter(self):
        """Test case for the value setter"""

        a = Base("base")
        a.value = 33
        assert a._raw == 33

    def test_raw_property(self):
        """Test case for raw property"""

        a = Base("base")
        a._raw = 45
        assert a.raw == 45

    def test_raw_setter(self):
        """Test case for the raw setter"""

        a = Base("base")
        a.raw = 6699
        assert a._raw == 6699

    def test_repr(self):
        """Test cases for __repr__ function"""

        a = Base("base")
        a.value = 123
        a.raw = 123

        assert a.__repr__() == "Base (name: base, writeable: False, value: 123, raw: 123, write_pending: False, class: None, unit: None)"

    def test_str(self):
        """Test cases for __str__ function"""

        a = Base("base")
        a.value = 99
        assert a.__str__() == "99"

        b = Base("base")
        b.value = None
        assert b.__str__() == "None"

    def test_eq(self):
        """Test cases for __eq__ function"""

        a = Base("base")
        b = Base("base")
        assert a == b

        c = Base("base")
        d = Bool("bool")
        assert c != d

    def test_lt(self):
        """Test cases for __lt__ function"""

        a = Base("base")
        a.value = 1
        b = Base("base")
        b.value = 2
        assert a < b
        assert not (b < a)

    # TODO: Test stability of converting back and forth, i.e.
    # luxtronik.datatypes.Celsius("").from_heatpump(luxtronik.datatypes.Celsius("").to_heatpump(0.11))


class TestSelectionBase:
    """Test suite for SelectionBase datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = SelectionBase("selection_base")
        assert a.name == "selection_base"
        assert not a.codes
        assert len(a.codes) == 0

    def test_options(self):
        """Test cases for options property"""

        a = SelectionBase("")
        assert len(a.options()) == 0
        assert a.options() == list(a.codes.values())

    def test_from_heatpump(self):
        """Test cases for from_heatpump function"""

        a = SelectionBase("")
        assert a.from_heatpump(0) is None

    def test_to_heatpump(self):
        """Test cases for to_heatpump function"""

        a = SelectionBase("")
        assert a.to_heatpump("a") is None


class SelectionBaseChild(SelectionBase):
    """Child class of SelectionBase containing codes to test it in the context of TestSelectionBaseChild"""

    codes = {
        0: "a",
        1: "b",
        2: "c",
    }


class TestSelectionBaseChild:
    """Test suite for SelectionBase datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = SelectionBaseChild("selection_base_child")
        assert a.name == "selection_base_child"
        assert a.codes
        assert len(a.codes) == 3

    def test_options(self):
        """Test cases for options property"""

        a = SelectionBaseChild("")
        assert len(a.options()) == 3
        assert a.options() == list(a.codes.values())

    def test_from_heatpump(self):
        """Test cases for from_heatpump function"""

        a = SelectionBaseChild("")
        assert a.from_heatpump(0) == "a"
        assert a.from_heatpump(1) == "b"
        assert a.from_heatpump(2) == "c"
        assert a.from_heatpump(3) is None

    def test_to_heatpump(self):
        """Test cases for to_heatpump function"""

        a = SelectionBaseChild("")
        assert a.to_heatpump("a") == 0
        assert a.to_heatpump("b") == 1
        assert a.to_heatpump("c") == 2
        assert a.to_heatpump("d") is None


class TestScalingBase:
    """Test suite for ScalingBase datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = ScalingBase("scaling_base")
        assert a.name == "scaling_base"
        assert a.scaling_factor == 1

    def test_from_heatpump(self):
        """Test cases for from_heatpump function"""

        a = ScalingBase("")
        assert a.from_heatpump(1) == 1
        assert a.from_heatpump(42) == 42
        assert a.from_heatpump(None) is None

    def test_to_heatpump(self):
        """Test cases for to_heatpump function"""

        a = ScalingBase("")
        assert a.to_heatpump(1) == 1
        assert a.to_heatpump(42) == 42


class ScalingBaseChild(ScalingBase):
    """Child class of ScalingBase containing a scaling_factor to test it in the context of TestScalingBaseChild"""

    scaling_factor = 13


class TestScalingBaseChild:
    """Test suite for ScalingBase datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = ScalingBaseChild("scaling_base_child")
        assert a.name == "scaling_base_child"
        assert a.scaling_factor == 13

    def test_from_heatpump(self):
        """Test cases for from_heatpump function"""

        a = ScalingBaseChild("")
        assert a.from_heatpump(0) == 0
        assert a.from_heatpump(1) == 13
        assert a.from_heatpump(2) == 26
        assert a.from_heatpump(-4) == -52

    def test_to_heatpump(self):
        """Test cases for to_heatpump function"""

        a = ScalingBaseChild("")
        assert a.to_heatpump(0) == 0
        assert a.to_heatpump(26) == 2
        assert a.to_heatpump(40) == 3
        assert a.to_heatpump(-100) == -8


class TestCelsius:
    """Test suite for Celsius datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Celsius("celsius")
        assert a.name == "celsius"
        assert a.datatype_class == "temperature"
        assert a.datatype_unit == "°C"

    def test_from_heatpump(self):
        """Test cases for from_heatpump function"""

        assert Celsius.from_heatpump(None) is None

        assert Celsius.from_heatpump(10) == 1
        assert Celsius.from_heatpump(11) == 1.1

        assert Celsius.from_heatpump(-10) == -1
        assert Celsius.from_heatpump(-11) == -1.1

    def test_to_heatpump(self):
        """Test cases for to_heatpump function"""

        assert Celsius.to_heatpump(1) == 10
        assert Celsius.to_heatpump(1.1) == 11

        assert Celsius.to_heatpump(-1) == -10
        assert Celsius.to_heatpump(-1.1) == -11


class TestBool:
    """Test suite for Bool datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Bool("bool")
        assert a.name == "bool"
        assert a.datatype_class == "boolean"
        assert a.datatype_unit is None

    def test_from_heatpump(self):
        """Test cases for from_heatpump function"""

        assert Bool.from_heatpump(0) is False
        assert Bool.from_heatpump(1) is True

    def test_to_heatpump(self):
        """Test cases for to_heatpump function"""

        assert Bool.to_heatpump(False) == 0
        assert Bool.to_heatpump(True) == 1


class TestFrequency:
    """Test suite for Frequency datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Frequency("frequency")
        assert a.name == "frequency"
        assert a.datatype_class == "frequency"
        assert a.datatype_unit == "Hz"


class TestSeconds:
    """Test suite for Seconds datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Seconds("seconds")
        assert a.name == "seconds"
        assert a.datatype_class == "timespan"
        assert a.datatype_unit == "s"


class TestIPv4Address:
    """Test suite for IPv4Address datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = IPv4Address("ipv4_address")
        assert a.name == "ipv4_address"
        assert a.datatype_class == "ipv4_address"
        assert a.datatype_unit is None

    def test_from_heatpump(self):
        """Test cases for from_heatpump function"""

        assert IPv4Address.from_heatpump(0) == "0.0.0.0"
        assert IPv4Address.from_heatpump(16909060) == "1.2.3.4"
        assert IPv4Address.from_heatpump(-1062731775) == "192.168.0.1"
        assert IPv4Address.from_heatpump(-256) == "255.255.255.0"
        assert IPv4Address.from_heatpump(-1) == "255.255.255.255"

    def test_to_heatpump(self):
        """Test cases for to_heatpump function"""

        assert IPv4Address.to_heatpump("0.0.0.0") == 0
        assert IPv4Address.to_heatpump("1.2.3.4") == 16909060
        assert IPv4Address.to_heatpump("192.168.0.1") == -1062731775
        assert IPv4Address.to_heatpump("255.255.255.0") == -256
        assert IPv4Address.to_heatpump("255.255.255.255") == -1


class TestTimestamp:
    """Test suite for Timestamp datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Timestamp("timestamp")
        assert a.name == "timestamp"
        assert a.datatype_class == "timestamp"
        assert a.datatype_unit is None

    def test_from_heatpump(self):
        """Test cases for from_heatpump function"""

        a = Timestamp("")
        assert a.from_heatpump(None) is None

        assert a.from_heatpump(-1) == datetime.datetime.fromtimestamp(0)
        assert a.from_heatpump(0) == datetime.datetime.fromtimestamp(0)
        assert a.from_heatpump(1) == datetime.datetime.fromtimestamp(1)
        # pylint: disable=fixme
        # TODO Consider to drop microseconds when dealing with this datatype?
        b = datetime.datetime.now()
        assert a.from_heatpump(datetime.datetime.timestamp(b)) == b

    def test_to_heatpump(self):
        """Test cases for to_heatpump function"""

        a = Timestamp("")
        assert a.to_heatpump(datetime.datetime.fromtimestamp(0)) == 0
        assert a.to_heatpump(datetime.datetime.fromtimestamp(1)) == 1
        # pylint: disable=fixme
        # TODO Consider to drop microseconds when dealing with this datatype?
        b = datetime.datetime.now()
        assert a.to_heatpump(b) == datetime.datetime.timestamp(b)


class TestErrorcode:
    """Test suite for Errorcode datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Errorcode("errorcode")
        assert a.name == "errorcode"
        assert a.datatype_class == "errorcode"
        assert a.datatype_unit is None


class TestKelvin:
    """Test suite for Errorcode datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Kelvin("kelvin")
        assert a.name == "kelvin"
        assert a.datatype_class == "temperature"
        assert a.datatype_unit == "K"

    def test_from_heatpump(self):
        """Test cases for from_heatpump function"""

        assert Kelvin.from_heatpump(None) is None

        assert Kelvin.from_heatpump(10) == 1
        assert Kelvin.from_heatpump(11) == 1.1

    def test_to_heatpump(self):
        """Test cases for to_heatpump function"""

        assert Kelvin.to_heatpump(1) == 10
        assert Kelvin.to_heatpump(1.1) == 11


class TestPressure:
    """Test suite for Pressure datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Pressure("pressure")
        assert a.name == "pressure"
        assert a.datatype_class == "pressure"
        assert a.datatype_unit == "bar"

    def test_from_heatpump(self):
        """Test cases for from_heatpump function"""

        assert Pressure.from_heatpump(None) is None

        assert Pressure.from_heatpump(100) == 1
        assert Pressure.from_heatpump(101) == 1.01

    def test_to_heatpump(self):
        """Test cases for to_heatpump function"""

        assert Pressure.to_heatpump(1) == 100
        assert Pressure.to_heatpump(1.01) == 101


class TestPercent:
    """Test suite for Percent datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Percent("percent")
        assert a.name == "percent"
        assert a.datatype_class == "percent"
        assert a.datatype_unit == "%"

    def test_percent_from_heatpump(self):
        """Test cases for from_heatpump function"""

        assert Percent.from_heatpump(None) is None

        assert Percent.from_heatpump(10) == 1
        assert Percent.from_heatpump(11) == 1.1

    def test_percent_to_heatpump(self):
        """Test cases for to_heatpump function"""

        assert Percent.to_heatpump(1) == 10
        assert Percent.to_heatpump(1.1) == 11


class TestPercent2:
    """Test suite for Percent2 datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Percent2("percent2")
        assert a.name == "percent2"
        assert a.datatype_class == "percent"
        assert a.datatype_unit == "%"

    def test_from_heatpump(self):
        """Test cases for from_heatpump function"""

        assert Percent2.from_heatpump(10) == 10
        assert Percent2.from_heatpump(11) == 11

    def test_to_heatpump(self):
        """Test cases for to_heatpump function"""

        assert Percent2.to_heatpump(10) == 10
        assert Percent2.to_heatpump(11) == 11


class TestSpeed:
    """Test suite for Speed datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Speed("speed")
        assert a.name == "speed"
        assert a.datatype_class == "speed"
        assert a.datatype_unit == "rpm"


class TestPower:
    """Test suite for Power datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Power("power")
        assert a.name == "power"
        assert a.datatype_class == "power"
        assert a.datatype_unit == "W"

class TestPowerLimit:
    """Test suite for PowerLimit datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = PowerLimit("power_limit")
        assert a.name == "power_limit"
        assert a.datatype_class == "power"
        assert a.datatype_unit == "kW"

    def test_from_heatpump(self):
        """Test cases for from_heatpump function"""

        a = PowerLimit("")
        assert a.from_heatpump(15) == 1.5
        assert a.from_heatpump(525) == 52.5
        assert a.from_heatpump(None) is None

    def test_to_heatpump(self):
        """Test cases for to_heatpump function"""

        a = PowerLimit("")
        assert a.to_heatpump(1.5) == 15
        assert a.to_heatpump(5.6) == 56


class TestEnergy:
    """Test suite for Energy datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Energy("energy")
        assert a.name == "energy"
        assert a.datatype_class == "energy"
        assert a.datatype_unit == "kWh"

    def test_energy_from_heatpump(self):
        """Test cases for from_heatpump function"""

        assert Energy.from_heatpump(None) is None

        assert Energy.from_heatpump(10) == 1
        assert Energy.from_heatpump(11) == 1.1

    def test_energy_to_heatpump(self):
        """Test cases for to_heatpump function"""

        assert Energy.to_heatpump(1) == 10
        assert Energy.to_heatpump(1.1) == 11


class TestVoltage:
    """Test suite for Voltage datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Voltage("voltage")
        assert a.name == "voltage"
        assert a.datatype_class == "voltage"
        assert a.datatype_unit == "V"

    def test_voltage_from_heatpump(self):
        """Test cases for from_heatpump function"""

        assert Voltage.from_heatpump(None) is None

        assert Voltage.from_heatpump(10) == 1
        assert Voltage.from_heatpump(11) == 1.1

    def test_voltage_to_heatpump(self):
        """Test cases for to_heatpump function"""

        assert Voltage.to_heatpump(1) == 10
        assert Voltage.to_heatpump(1.1) == 11


class TestHours:
    """Test suite for Hours datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Hours("hours")
        assert a.name == "hours"
        assert a.datatype_class == "timespan"
        assert a.datatype_unit == "h"

    def test_hours_from_heatpump(self):
        """Test cases for from_heatpump function"""

        assert Hours.from_heatpump(None) is None

        assert Hours.from_heatpump(10) == 1
        assert Hours.from_heatpump(11) == 1.1

    def test_hours_to_heatpump(self):
        """Test cases for to_heatpump function"""

        assert Hours.to_heatpump(1) == 10
        assert Hours.to_heatpump(1.1) == 11


class TestHours2:
    """Test suite for Hours2 datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Hours2("hours2")
        assert a.name == "hours2"
        assert a.datatype_class == "timespan"
        assert a.datatype_unit == "h"

    def test_hours2_from_heatpump(self):
        """Test cases for from_heatpump function"""

        assert Hours2.from_heatpump(None) is None

        assert Hours2.from_heatpump(2) == 2
        assert Hours2.from_heatpump(8) == 5

    def test_hours2_to_heatpump(self):
        """Test cases for to_heatpump function"""

        assert Hours2.to_heatpump(2) == 2
        assert Hours2.to_heatpump(5) == 8


class TestMinutes:
    """Test suite for Minutes datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Minutes("minutes")
        assert a.name == "minutes"
        assert a.datatype_class == "timespan"
        assert a.datatype_unit == "min"


class TestFlow:
    """Test suite for Flow datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Flow("flow")
        assert a.name == "flow"
        assert a.datatype_class == "flow"
        assert a.datatype_unit == "l/h"


class TestLevel:
    """Test suite for Level datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Level("level")
        assert a.name == "level"
        assert a.datatype_class == "level"
        assert a.datatype_unit is None


class TestCount:
    """Test suite for Count datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Count("count")
        assert a.name == "count"
        assert a.datatype_class == "count"
        assert a.datatype_unit is None


class TestCharacter:
    """Test suite for Character datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Character("my_name")
        assert a.name == "my_name"
        assert a.datatype_class == "character"
        assert a.datatype_unit is None

    def test_from_heatpump(self):
        """Test cases for from_heatpump function"""

        assert Character.from_heatpump(0) == ""
        assert Character.from_heatpump(51) == "3"
        assert Character.from_heatpump(46) == "."
        assert Character.from_heatpump(56) == "8"
        assert Character.from_heatpump(48) == "0"


class TestMajorMinorVersion:
    """Test suite for MajorMinorVersion datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = MajorMinorVersion("numeric_version")
        assert a.name == "numeric_version"
        assert a.datatype_class == "version"
        assert a.datatype_unit is None

    def test_from_heatpump(self):
        """Test cases for from_heatpump function"""

        # Reported value from https://github.com/Bouni/python-luxtronik/issues/99
        assert MajorMinorVersion.from_heatpump(112) == "1.12"

        # Reported value when RBE is not installed
        assert MajorMinorVersion.from_heatpump(0) == "0"

        # Other values (not seen in the wild yet)
        assert MajorMinorVersion.from_heatpump(12) == "0.12"
        assert MajorMinorVersion.from_heatpump(-1) == "0"

class TestFullVersion:
    """Test suite for FullVersion datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = FullVersion("full_version")
        assert a.name == "full_version"
        assert a.datatype_class == "version"
        assert a.datatype_unit is None

    def test_from_heatpump(self):
        """Test cases for from_heatpump function"""

        assert FullVersion.from_heatpump(112) == "0"
        assert FullVersion.from_heatpump(0) == "0"
        assert FullVersion.from_heatpump([0, 12]) == "0"
        assert FullVersion.from_heatpump([0, 12, 3]) == "0.12.3"

class TestIcon:
    """Test suite for Icon datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Icon("icon")
        assert a.name == "icon"
        assert a.datatype_class == "icon"
        assert a.datatype_unit is None


class TestHeatingMode:
    """Test suite for HeatingMode datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = HeatingMode("heating_mode")
        assert a.name == "heating_mode"
        assert a.datatype_class == "selection"
        assert a.datatype_unit is None
        assert len(a.codes) == 5

    def test_options(self):
        """Test cases for options property"""

        a = HeatingMode("")
        assert len(a.options()) == 5
        assert a.options() == list(a.codes.values())


class TestCoolingMode:
    """Test suite for CoolingMode datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = CoolingMode("cooling_mode")
        assert a.name == "cooling_mode"
        assert a.datatype_class == "selection"
        assert a.datatype_unit is None
        assert len(a.codes) == 2

    def test_options(self):
        """Test cases for options property"""

        a = CoolingMode("")
        assert len(a.options()) == 2


class TestHotWaterMode:
    """Test suite for HotWaterMode datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = HotWaterMode("hot_water_mode")
        assert a.name == "hot_water_mode"
        assert a.datatype_class == "selection"
        assert a.datatype_unit is None
        assert len(a.codes) == 5

    def test_options(self):
        """Test cases for options property"""

        a = HotWaterMode("")
        assert len(a.options()) == 5
        assert a.options() == list(a.codes.values())


class TestPoolMode:
    """Test suite for PoolMode datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = PoolMode("hot_water_mode")
        assert a.name == "hot_water_mode"
        assert a.datatype_class == "selection"
        assert a.datatype_unit is None
        assert len(a.codes) == 4

    def test_options(self):
        """Test cases for options property"""

        a = PoolMode("")
        assert len(a.options()) == 4
        assert a.options() == list(a.codes.values())


class TestMixedCircuitMode:
    """Test suite for MixedCircuitMode datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = MixedCircuitMode("mixed_circuit_mode")
        assert a.name == "mixed_circuit_mode"
        assert a.datatype_class == "selection"
        assert a.datatype_unit is None
        assert len(a.codes) == 4

    def test_options(self):
        """Test cases for options property"""

        a = MixedCircuitMode("")
        assert len(a.options()) == 4
        assert a.options() == list(a.codes.values())


class TestSolarMode:
    """Test suite for SolarMode datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = SolarMode("solar_mode")
        assert a.name == "solar_mode"
        assert a.datatype_class == "selection"
        assert a.datatype_unit is None
        assert len(a.codes) == 5

    def test_options(self):
        """Test cases for options property"""

        a = SolarMode("")
        assert len(a.options()) == 5
        assert a.options() == list(a.codes.values())


class TestVentilationMode:
    """Test suite for VentilationMode datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = VentilationMode("ventilation_mode")
        assert a.name == "ventilation_mode"
        assert a.datatype_class == "selection"
        assert a.datatype_unit is None
        assert len(a.codes) == 4

    def test_options(self):
        """Test cases for options property"""

        a = VentilationMode("")
        assert len(a.options()) == 4
        assert a.options() == list(a.codes.values())


class TestHeatpumpCode:
    """Test suite for HeatpumpCode datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = HeatpumpCode("heatpump_code")
        assert a.name == "heatpump_code"
        assert a.datatype_class == "selection"
        assert a.datatype_unit is None
        assert len(a.codes) == 89

    def test_options(self):
        """Test cases for options property"""

        a = HeatpumpCode("")
        assert len(a.options()) == 89
        assert a.options() == list(a.codes.values())


class TestBivalenceLevel:
    """Test suite for BivalenceLevel datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = BivalenceLevel("bivalence_level")
        assert a.name == "bivalence_level"
        assert a.datatype_class == "selection"
        assert a.datatype_unit is None
        assert len(a.codes) == 3

    def test_options(self):
        """Test cases for options property"""

        a = BivalenceLevel("")
        assert len(a.options()) == 3
        assert a.options() == list(a.codes.values())


class TestOperationMode:
    """Test suite for OperationMode datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = OperationMode("operation_mode")
        assert a.name == "operation_mode"
        assert a.datatype_class == "selection"
        assert a.datatype_unit is None
        assert len(a.codes) == 8

    def test_options(self):
        """Test cases for options property"""

        a = OperationMode("")
        assert len(a.options()) == 8
        assert a.options() == list(a.codes.values())


class TestSwitchoffFile:
    """Test suite for SwitchoffFile datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = SwitchoffFile("switchoff_file")
        assert a.name == "switchoff_file"
        assert a.datatype_class == "selection"
        assert a.datatype_unit is None
        assert len(a.codes) == 25

    def test_options(self):
        """Test cases for options property"""

        a = SwitchoffFile("")
        assert len(a.options()) == 25
        assert a.options() == list(a.codes.values())


class TestMainMenuStatusLine1:
    """Test suite for MainMenuStatusLine1 datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = MainMenuStatusLine1("main_menu_status_line1")
        assert a.name == "main_menu_status_line1"
        assert a.datatype_class == "selection"
        assert a.datatype_unit is None
        assert len(a.codes) == 8

    def test_options(self):
        """Test cases for options property"""

        a = MainMenuStatusLine1("")
        assert len(a.options()) == 8
        assert a.options() == list(a.codes.values())


class TestMainMenuStatusLine2:
    """Test suite for MainMenuStatusLine2 datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = MainMenuStatusLine2("main_menu_status_line2")
        assert a.name == "main_menu_status_line2"
        assert a.datatype_class == "selection"
        assert a.datatype_unit is None
        assert len(a.codes) == 2

    def test_options(self):
        """Test cases for options property"""

        a = MainMenuStatusLine2("")
        assert len(a.options()) == 2
        assert a.options() == list(a.codes.values())


class TestSecOperationMode:
    """Test suite for SecOperationMode datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = SecOperationMode("sec_operation_mode")
        assert a.name == "sec_operation_mode"
        assert a.datatype_class == "selection"
        assert a.datatype_unit is None
        assert len(a.codes) == 13

    def test_options(self):
        """Test cases for options property"""

        a = SecOperationMode("")
        assert len(a.options()) == 13
        assert a.options() == list(a.codes.values())


class TestAccessLevel:
    """Test suite for AccessLevel datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = AccessLevel("access_level")
        assert a.name == "access_level"
        assert a.datatype_class == "selection"
        assert a.datatype_unit is None
        assert len(a.codes) == 4

    def test_options(self):
        """Test cases for options property"""

        a = AccessLevel("")
        assert len(a.options()) == 4
        assert a.options() == list(a.codes.values())


class TestUnknown:
    """Test suite for Unknown datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Unknown("unknown")
        assert a.name == "unknown"
        assert a.datatype_class is None
        assert a.datatype_unit is None


class TestTimerProgram:
    """Test suite for TimerProgram datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = TimerProgram("timer_program")
        assert a.name == "timer_program"
        assert a.datatype_class == "selection"
        assert a.datatype_unit is None
        assert len(a.codes) == 3

    def test_options(self):
        """Test cases for options property"""

        a = TimerProgram("")
        assert len(a.options()) == 3
        assert a.options() == list(a.codes.values())


class TestTimeOfDay:
    """Test suite for TimeOfDay datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = TimeOfDay("timeofday")
        assert a.name == "timeofday"
        assert a.datatype_class == "timeofday"
        assert a.datatype_unit is None

    def test_timeofday_conversion(self):
        """Test cases for from_heatpump function"""

        assert TimeOfDay.from_heatpump(None) is None

        check_pair(TimeOfDay, 7 * 3600 + 30 * 60, "7:30")
        check_pair(TimeOfDay, 7 * 3600 + 30 * 60 + 50, "7:30:50")
        check_pair(TimeOfDay, 19 * 3600 + 30 * 60 + 50, "19:30:50")

        for val in [12495, 34099, 82148]:
            check_round_trip(TimeOfDay, val)


class TestTimeOfDay2:
    """Test suite for TimeOfDay2 datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = TimeOfDay2("timeofday2")
        assert a.name == "timeofday2"
        assert a.datatype_class == "timeofday2"
        assert a.datatype_unit is None

    def test_timeofday_conversion(self):
        """Test cases for from_heatpump function"""

        assert TimeOfDay2.from_heatpump(None) is None

        check_pair(TimeOfDay2, ((19 * 60) << 16) + 7 * 60 + 30, "7:30-19:00")
        check_pair(TimeOfDay2, ((19 * 60 + 30) << 16) + 5 * 60 + 23, "5:23-19:30")

        for val in [0x02520143, 0x04160318, 0x05120445]:
            check_round_trip(TimeOfDay2, val)
