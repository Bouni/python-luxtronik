"""Test suite for parameters module"""

# pylint: disable=too-few-public-methods

from luxtronik import Calculations
from luxtronik.datatypes import Base
from luxtronik.definitions import LuxtronikDefinition


class TestCalculations:
    """Test suite for Calculations"""

    def test_init(self):
        """Test cases for initialization"""
        calculations = Calculations()
        assert calculations.name == "calculation"
        assert calculations.data == calculations._data

    def test_data(self):
        """Test cases for the data dictionary"""
        calculations = Calculations()
        data = calculations.data

        # The Value must be a fields
        # The key can be an index
        assert isinstance(data[0], Base)
        for d in data:
            assert isinstance(d, LuxtronikDefinition)
        for v in data.values():
            assert isinstance(v, Base)
        for d, v in data.items():
            assert isinstance(d, LuxtronikDefinition)
            assert isinstance(v, Base)
