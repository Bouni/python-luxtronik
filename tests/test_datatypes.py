"""Test suite for datatypes module"""

# pylint: disable=too-few-public-methods,invalid-name

import datetime
import pytest

from luxtronik.datatypes import (
    Base,
    SelectionBase,
    Celsius,
    Bool,
    Frequency,
    Seconds,
    Pulses,
    IPAddress,
    Timestamp,
    Errorcode,
    Kelvin,
    Pressure,
    Percent,
    Percent2,
    Speed,
    Power,
    Energy,
    Voltage,
    Hours,
    Hours2,
    Minutes,
    Flow,
    Level,
    Count,
    Version,
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
)


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

        assert Base("").from_heatpump(1) == 1

    def test_to_heatpump(self):
        """Test cases for to_heatpump function"""

        assert Base("").to_heatpump(1) == 1

    def test_repr(self):
        """Test cases for __repr__ function"""

        # unsure what to test and whether this method is needed at all
        pytest.skip("Not yet implemented")

    def test_str(self):
        """Test cases for __str__ function"""

        # unsure what to test and whether this method is needed at all
        pytest.skip("Not yet implemented")


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


class TestCelsius:
    """Test suite for Celsius datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Celsius("celsius")
        assert a.name == "celsius"
        assert a.measurement_type == "celsius"

    def test_from_heatpump(self):
        """Test cases for from_heatpump function"""

        assert Celsius("").from_heatpump(None) is None

        assert Celsius("").from_heatpump(10) == 1
        assert Celsius("").from_heatpump(11) == 1.1

        assert Celsius("").from_heatpump(-10) == -1
        assert Celsius("").from_heatpump(-11) == -1.1

    def test_to_heatpump(self):
        """Test cases for to_heatpump function"""

        assert Celsius("").to_heatpump(1) == 10
        assert Celsius("").to_heatpump(1.1) == 11

        assert Celsius("").to_heatpump(-1) == -10
        assert Celsius("").to_heatpump(-1.1) == -11


class TestBool:
    """Test suite for Bool datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Bool("bool")
        assert a.name == "bool"
        assert a.measurement_type == "boolean"

    def test_from_heatpump(self):
        """Test cases for from_heatpump function"""

        assert Bool("").from_heatpump(0) is False
        assert Bool("").from_heatpump(1) is True

    def test_to_heatpump(self):
        """Test cases for to_heatpump function"""

        assert Bool("").to_heatpump(False) == 0
        assert Bool("").to_heatpump(True) == 1


class TestFrequency:
    """Test suite for Frequency datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Frequency("frequency")
        assert a.name == "frequency"
        assert a.measurement_type == "Hz"


class TestSeconds:
    """Test suite for Seconds datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Seconds("seconds")
        assert a.name == "seconds"
        assert a.measurement_type == "seconds"


class TestPulses:
    """Test suite for Pulses datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Pulses("pulses")
        assert a.name == "pulses"
        assert a.measurement_type == "pulses"


class TestIPAddress:
    """Test suite for IPAddress datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = IPAddress("ipaddress")
        assert a.name == "ipaddress"
        assert a.measurement_type == "ipaddress"

    def test_from_heatpump(self):
        """Test cases for from_heatpump function"""

        assert IPAddress("").from_heatpump(0) == "0.0.0.0"
        assert IPAddress("").from_heatpump(16909060) == "1.2.3.4"
        assert IPAddress("").from_heatpump(-1062731775) == "192.168.0.1"
        assert IPAddress("").from_heatpump(-256) == "255.255.255.0"
        assert IPAddress("").from_heatpump(-1) == "255.255.255.255"

    def test_to_heatpump(self):
        """Test cases for to_heatpump function"""

        assert IPAddress("").to_heatpump("0.0.0.0") == 0
        assert IPAddress("").to_heatpump("1.2.3.4") == 16909060
        assert IPAddress("").to_heatpump("192.168.0.1") == -1062731775
        assert IPAddress("").to_heatpump("255.255.255.0") == -256
        assert IPAddress("").to_heatpump("255.255.255.255") == -1


class TestTimestamp:
    """Test suite for Timestamp datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Timestamp("timestamp")
        assert a.name == "timestamp"
        assert a.measurement_type == "timestamp"

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
        assert a.measurement_type == "errorcode"


class TestKelvin:
    """Test suite for Errorcode datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Kelvin("kelvin")
        assert a.name == "kelvin"
        assert a.measurement_type == "kelvin"

    def test_from_heatpump(self):
        """Test cases for from_heatpump function"""

        assert Kelvin("").from_heatpump(None) is None

        assert Kelvin("").from_heatpump(10) == 1
        assert Kelvin("").from_heatpump(11) == 1.1

    def test_to_heatpump(self):
        """Test cases for to_heatpump function"""

        assert Kelvin("").to_heatpump(1) == 10
        assert Kelvin("").to_heatpump(1.1) == 11


class TestPressure:
    """Test suite for Pressure datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Pressure("pressure")
        assert a.name == "pressure"
        assert a.measurement_type == "bar"

    def test_from_heatpump(self):
        """Test cases for from_heatpump function"""

        assert Pressure("").from_heatpump(None) is None

        assert Pressure("").from_heatpump(100) == 1
        assert Pressure("").from_heatpump(101) == 1.01

    def test_to_heatpump(self):
        """Test cases for to_heatpump function"""

        assert Pressure("").to_heatpump(1) == 100
        assert Pressure("").to_heatpump(1.01) == 101


class TestPercent:
    """Test suite for Percent datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Percent("percent")
        assert a.name == "percent"
        assert a.measurement_type == "percent"

    def test_percent_from_heatpump(self):
        """Test cases for from_heatpump function"""

        assert Percent("").from_heatpump(None) is None

        assert Percent("").from_heatpump(10) == 1
        assert Percent("").from_heatpump(11) == 1.1

    def test_percent_to_heatpump(self):
        """Test cases for to_heatpump function"""

        assert Percent("").to_heatpump(1) == 10
        assert Percent("").to_heatpump(1.1) == 11


class TestPercent2:
    """Test suite for Percent2 datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Percent2("percent2")
        assert a.name == "percent2"
        assert a.measurement_type == "percent"

    def test_from_heatpump(self):
        """Test cases for from_heatpump function"""

        assert Percent2("").from_heatpump(10) == 10
        assert Percent2("").from_heatpump(11) == 11

    def test_to_heatpump(self):
        """Test cases for to_heatpump function"""

        assert Percent2("").to_heatpump(10) == 10
        assert Percent2("").to_heatpump(11) == 11


class TestSpeed:
    """Test suite for Speed datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Speed("speed")
        assert a.name == "speed"
        assert a.measurement_type == "rpm"


class TestPower:
    """Test suite for Power datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Power("power")
        assert a.name == "power"
        assert a.measurement_type == "W"


class TestEnergy:
    """Test suite for Energy datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Energy("energy")
        assert a.name == "energy"
        assert a.measurement_type == "energy"

    def test_energy_from_heatpump(self):
        """Test cases for from_heatpump function"""

        assert Energy("").from_heatpump(None) is None

        assert Energy("").from_heatpump(10) == 1
        assert Energy("").from_heatpump(11) == 1.1

    def test_energy_to_heatpump(self):
        """Test cases for to_heatpump function"""

        assert Energy("").to_heatpump(1) == 10
        assert Energy("").to_heatpump(1.1) == 11


class TestVoltage:
    """Test suite for Voltage datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Voltage("voltage")
        assert a.name == "voltage"
        assert a.measurement_type == "voltage"

    def test_voltage_from_heatpump(self):
        """Test cases for from_heatpump function"""

        assert Voltage("").from_heatpump(None) is None

        assert Voltage("").from_heatpump(10) == 1
        assert Voltage("").from_heatpump(11) == 1.1

    def test_voltage_to_heatpump(self):
        """Test cases for to_heatpump function"""

        assert Voltage("").to_heatpump(1) == 10
        assert Voltage("").to_heatpump(1.1) == 11


class TestHours:
    """Test suite for Hours datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Hours("hours")
        assert a.name == "hours"
        assert a.measurement_type == "hours"

    def test_hours_from_heatpump(self):
        """Test cases for from_heatpump function"""

        assert Hours("").from_heatpump(None) is None

        assert Hours("").from_heatpump(10) == 1
        assert Hours("").from_heatpump(11) == 1.1

    def test_hours_to_heatpump(self):
        """Test cases for to_heatpump function"""

        assert Hours("").to_heatpump(1) == 10
        assert Hours("").to_heatpump(1.1) == 11


class TestHours2:
    """Test suite for Hours2 datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Hours2("hours2")
        assert a.name == "hours2"
        assert a.measurement_type == "hours"

    def test_hours2_from_heatpump(self):
        """Test cases for from_heatpump function"""

        assert Hours2("").from_heatpump(None) is None

        assert Hours2("").from_heatpump(2) == 2
        assert Hours2("").from_heatpump(8) == 5

    def test_hours2_to_heatpump(self):
        """Test cases for to_heatpump function"""

        assert Hours2("").to_heatpump(2) == 2
        assert Hours2("").to_heatpump(5) == 8


class TestMinutes:
    """Test suite for Minutes datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Minutes("minutes")
        assert a.name == "minutes"
        assert a.measurement_type == "Minutes"


class TestFlow:
    """Test suite for Flow datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Flow("flow")
        assert a.name == "flow"
        assert a.measurement_type == "flow"


class TestLevel:
    """Test suite for Level datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Level("level")
        assert a.name == "level"
        assert a.measurement_type == "level"


class TestCount:
    """Test suite for Count datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Count("count")
        assert a.name == "count"
        assert a.measurement_type == "count"


class TestVersion:
    """Test suite for Version datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Version("version")
        assert a.name == "version"
        assert a.measurement_type == "version"

    def test_from_heatpump(self):
        """Test cases for from_heatpump function"""

        assert Version("").from_heatpump(bytes([51, 46, 56, 56])) == "3.88"
        assert Version("").from_heatpump(bytes([51, 46, 56, 56, 00])) == "3.88"
        assert Version("").from_heatpump(bytes([00, 51, 46, 56, 56, 00])) == "3.88"
        assert Version("").from_heatpump(bytes([48])) == "0"


class TestIcon:
    """Test suite for Icon datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = Icon("icon")
        assert a.name == "icon"
        assert a.measurement_type == "icon"


class TestHeatingMode:
    """Test suite for HeatingMode datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = HeatingMode("heating_mode")
        assert a.name == "heating_mode"
        assert a.measurement_type == "selection"
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
        assert a.measurement_type == "selection"
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
        assert a.measurement_type == "selection"
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
        assert a.measurement_type == "selection"
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
        assert a.measurement_type == "selection"
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
        assert a.measurement_type == "selection"
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
        assert a.measurement_type == "selection"
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
        assert a.measurement_type == "selection"
        assert len(a.codes) == 68

    def test_options(self):
        """Test cases for options property"""

        a = HeatpumpCode("")
        assert len(a.options()) == 68
        assert a.options() == list(a.codes.values())


class TestBivalenceLevel:
    """Test suite for BivalenceLevel datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = BivalenceLevel("bivalence_level")
        assert a.name == "bivalence_level"
        assert a.measurement_type == "selection"
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
        assert a.measurement_type == "selection"
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
        assert a.measurement_type == "selection"
        assert len(a.codes) == 11

    def test_options(self):
        """Test cases for options property"""

        a = SwitchoffFile("")
        assert len(a.options()) == 11
        assert a.options() == list(a.codes.values())


class TestMainMenuStatusLine1:
    """Test suite for MainMenuStatusLine1 datatype"""

    def test_init(self):
        """Test cases for initialization"""

        a = MainMenuStatusLine1("main_menu_status_line1")
        assert a.name == "main_menu_status_line1"
        assert a.measurement_type == "selection"
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
        assert a.measurement_type == "selection"
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
        assert a.measurement_type == "selection"
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
        assert a.measurement_type == "selection"
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
        assert a.measurement_type is None
