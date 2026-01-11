"""Test suite for parameters module"""

# pylint: disable=too-few-public-methods

from luxtronik import Calculations
from luxtronik.datatypes import Base


class TestCalculations:
    """Test suite for Calculations"""

    def test_init(self):
        """Test cases for initialization"""
        calculations = Calculations()
        assert calculations.name == "calculation"
        assert calculations.calculations == calculations._data

    def test_data(self):
        """Test cases for the data dictionary"""
        calculations = Calculations()
        data = calculations.calculations

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
