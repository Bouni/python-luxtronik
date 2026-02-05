"""Test suite for parameters module"""

# pylint: disable=too-few-public-methods,invalid-name,protected-access

from luxtronik import Parameters
from luxtronik.datatypes import Base


class TestParameters:
    """Test suite for Parameters"""

    def test_init(self):
        """Test cases for initialization"""
        parameters = Parameters()
        assert parameters.name == "parameter"
        assert parameters.parameters == parameters._data
        assert parameters.safe

        parameters = Parameters(False)
        assert not parameters.safe

    def test_data(self):
        """Test cases for the data dictionary"""
        parameters = Parameters()
        data = parameters.parameters

        # The Value must be a fields
        # The key can be an index
        assert isinstance(data[0], Base)
        for k in data:
            assert isinstance(k, int)
        for v in data.values():
            assert isinstance(v, Base)
        for k, v in data.items():
            assert isinstance(k, int)
            assert isinstance(v, Base)

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
        assert parameters["BarFoo"] is None

        # Set something which was previously (v0.3.14) not allowed to be set
        parameters.set("ID_Transfert_LuxNet", 1)
        assert parameters["ID_Transfert_LuxNet"].raw == 1
        assert parameters["ID_Transfert_LuxNet"].write_pending

        # Set something which is allowed to be set
        parameters.set("ID_Einst_WK_akt", 2)
        assert parameters["ID_Einst_WK_akt"].raw == 20
        assert parameters["ID_Einst_WK_akt"].write_pending

        parameters = Parameters(safe=False)

        # Set something which was previously (v0.3.14) not allowed to be set, but we are brave.
        parameters.set("ID_Transfert_LuxNet", 4)
        assert parameters["ID_Transfert_LuxNet"].raw == 4
        assert parameters["ID_Transfert_LuxNet"].write_pending
