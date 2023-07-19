"""Test suite for parameters module"""

# pylint: disable=too-few-public-methods,invalid-name,protected-access

from luxtronik.parameters import Parameters


class TestParameters:
    """Test suite for Parameters"""

    def test_init(self):
        """Test cases for initialization"""
        parameters = Parameters()
        assert parameters.safe
        assert len(parameters.queue) == 0

        parameters = Parameters(False)
        assert not parameters.safe
        assert len(parameters.queue) == 0

    def test_get(self):
        """Test cases for get"""
        parameters = Parameters()
        s = "ID_Transfert_LuxNet"
        assert parameters.get(0).name == s
        assert parameters.get("0").name == s
        assert parameters.get(s).name == s

    def test__lookup(self):
        """Test cases for _lookup"""
        parameters = Parameters()
        s = "ID_Transfert_LuxNet"
        assert parameters._lookup(0).name == s
        assert parameters._lookup("0").name == s
        assert parameters._lookup(s).name == s

        p0 = parameters._lookup(0)
        assert parameters._lookup(0, True) == (0, p0)
        assert parameters._lookup("0", True) == (0, p0)
        assert parameters._lookup(s, True) == (0, p0)

        s = "ID_BarFoo"
        assert parameters._lookup(s, True)[0] is None

    def test_parse(self):
        """Test cases for _parse"""
        parameters = Parameters()

        n = 2000
        t = [0] * (n + 1)
        parameters.parse(t)

        p = parameters.get(n)

        assert p.name == f"Unknown_Parameter_{n}"
