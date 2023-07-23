"""Test suite for parameters module"""

# pylint: disable=too-few-public-methods

from luxtronik.calculations import Calculations


class TestCalculations:
    """Test suite for Calculations"""

    def test_init(self):
        """Test cases for initialization"""
        calculations = Calculations()
        assert calculations.name == "Calculation"
