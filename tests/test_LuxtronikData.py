"""Test suite for LuxtronikData"""

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
