"""Test suite for LuxtronikData"""

import pytest
from luxtronik import LuxtronikData, Parameters, Calculations, Visibilities


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
        ("calc", 241, ["HUP_PWM", "Circulation_Pump", "Unknown_Calculation_241"]),
        ("visi", 182, ["ID_Visi_Heizung_Zeitschaltprogramm", "ID_Visi_Heizung_Zeitschlaltprogramm", "Unknown_Visibility_182"]),
        ("visi", 326, ["Unknown_Visibility_326"]),
    ])
    def test_downward_compatibility(self, vector, index, names):
        """Test data access with outdated names"""

        a = LuxtronikData()

        match vector:
            case "para":
                vector = a.parameters
            case "calc":
                vector = a.calculations
            case _:
                vector = a.visibilities

        entry = vector.get(index)
        for name in names:
            e = vector.get(name)
            assert e == entry
            assert e.name == names[0]
            assert e.get_supported_names() == names
        

