"""Test suite for parameters module"""

# pylint: disable=too-few-public-methods,invalid-name,protected-access

from luxtronik.parameters import Parameters


class TestParameters:
    """Test suite for Parameters"""

    def test_init(self):
        """Test cases for initialization"""
        parameters = Parameters()
        assert parameters.name == "Parameter"
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

        # Look for a name which does not exist
        s = "ID_BarFoo"
        assert parameters._lookup(s, True)[0] is None

        # Look for something which is not an int and not a string
        j = 0.0
        assert parameters._lookup(j) is None

    def test_parse(self):
        """Test cases for _parse"""
        parameters = Parameters()

        n = 2000
        t = [0] * (n + 1)
        parameters.parse(t)

        p = parameters.get(n)

        assert p.name == f"Unknown_Parameter_{n}"

    def test___iter__(self):
        """Test cases for __iter__"""
        parameters = Parameters()

        for i, p in parameters:
            if i == 0:
                assert p.name == "ID_Transfert_LuxNet"
            elif i == 1:
                assert p.name == "ID_Einst_WK_akt"
            else:
                break

    def test_set(self):
        """Test cases for set"""
        parameters = Parameters()

        # Set something which does not exist
        parameters.set("BarFoo", 0)
        assert len(parameters.queue) == 0

        # Set something which is not allowed to be set
        parameters.set("ID_Transfert_LuxNet", 0)
        assert len(parameters.queue) == 0

        # Set something which is allowed to be set
        parameters.set("ID_Einst_WK_akt", 0)
        assert len(parameters.queue) == 1

        parameters = Parameters(safe=False)

        # Set something which is not allowed to be set, but we are brave.
        parameters.set("ID_Transfert_LuxNet", 0)
        assert len(parameters.queue) == 1
