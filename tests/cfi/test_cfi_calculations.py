"""Test suite for parameters module"""

# pylint: disable=too-few-public-methods

from luxtronik import Calculations


class TestCalculations:
    """Test suite for Calculations"""

    def test_init(self):
        """Test cases for initialization"""
        calculations = Calculations()
        assert calculations.name == "calculation"
        assert calculations.calculations == calculations._data
