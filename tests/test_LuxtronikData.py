"""Test suite for LuxtronikData"""

import pytest

from luxtronik import (
    LuxtronikData,
    LuxtronikAllData,
    Parameters,
    Calculations,
    Visibilities
)
from luxtronik.shi import (
    Inputs,
    Holdings
)


class TestLuxtronikData:
    """Test suite for LuxtronikData datatype"""

    def test_init(self):
        """Test cases for __init__"""

        a = LuxtronikData()
        assert a.parameters.safe

        b = LuxtronikData(safe=False)
        assert not b.parameters.safe

        para = Parameters()
        c = LuxtronikData(para)
        assert c.parameters == para
        assert a.parameters != para

        calc = Calculations()
        visi = Visibilities()
        d = LuxtronikData(calculations=calc, visibilities=visi)
        assert d.calculations == calc
        assert d.visibilities == visi
        assert c.calculations != calc
        assert c.visibilities != visi

    def test_get_firmware_version(self):
        """Test cases for get_firmware_version()"""

        a = LuxtronikData()
        for i in range(81, 91):
            a.calculations.get(i).raw = 0
        assert a.get_firmware_version() == ""

        a.calculations.get(81).raw = ord("V")
        assert a.get_firmware_version() == "V"

        a.calculations.get(82).raw = ord("3")
        assert a.get_firmware_version() == "V3"

        a.calculations.get(83).raw = ord(".")
        assert a.get_firmware_version() == "V3."

        a.calculations.get(84).raw = ord("1")
        assert a.get_firmware_version() == "V3.1"

        # Test of downward compatibility with outdated entry name
        assert a.calculations.get("ID_WEB_SoftStand").value == "V3.1"


    @pytest.mark.parametrize("vector, index, names", [
        ("para", 1106, ["ID_Einst_SilenceTimer_13", "Unknown_Parameter_1106"]),
        ("para", 1109, ["ID_Einst_SilenceTimer_16", "Unknown_Parameter_1109"]),
        ("calc", 232, ["Vapourisation_Temperature", "Unknown_Calculation_232"]),
        ("calc", 241, ["HUP_PWM", "Circulation_Pump"]),
        ("visi", 182, ["ID_Visi_Heizung_Zeitschaltprogramm", "ID_Visi_Heizung_Zeitschlaltprogramm"]),
        ("visi", 326, ["Unknown_Visibility_326"]),
    ])
    def test_obsolete(self, vector, index, names):
        """Test data access with outdated names"""

        data = LuxtronikData()

        if vector == "para":
            vector = data.parameters
        elif vector == "calc":
            vector = data.calculations
        elif vector == "visi":
            vector = data.visibilities

        field_i = vector.get(index)
        for idx, name in enumerate(names):
            try:
                # field should be found for index 0
                field_n = vector.get(name)
                assert idx == 0
                assert field_n == field_i
                assert field_n.name == names[0]
                assert field_n._names == names
            except Exception:
                # KeyError should be thrown for all other indices
                assert idx > 0


class TestLuxtronikAllData:
    """Test suite for LuxtronikAllData datatype"""

    def test_init(self):
        """Test cases for __init__"""

        a = LuxtronikAllData()
        assert a.parameters.safe

        b = LuxtronikAllData(safe=False)
        assert not b.parameters.safe

        para = Parameters()
        hold = Holdings()
        c = LuxtronikAllData(para, holdings=hold)
        assert c.parameters == para
        assert c.holdings == hold
        assert a.parameters != para
        assert a.holdings != hold

        calc = Calculations()
        visi = Visibilities()
        inpu = Inputs()
        d = LuxtronikAllData(calculations=calc, visibilities=visi, inputs=inpu)
        assert d.calculations == calc
        assert d.visibilities == visi
        assert d.inputs == inpu
        assert c.calculations != calc
        assert c.visibilities != visi
        assert c.inputs != inpu
