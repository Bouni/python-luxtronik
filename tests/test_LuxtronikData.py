"""Test suite for LuxtronikData"""

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
