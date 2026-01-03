"""Test suite for parameters module"""

# pylint: disable=too-few-public-methods

from luxtronik.visibilities import Visibilities


class TestVisibilities:
    """Test suite for Visibilities"""

    def test_init(self):
        """Test cases for initialization"""
        visibilities = Visibilities()
        assert visibilities.name == "Visibility"
        assert visibilities.visibilities == visibilities._data
