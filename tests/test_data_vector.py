"""Test suite for data_vector module"""

# pylint: disable=too-few-public-methods,invalid-name,too-many-lines

import pytest

from luxtronik.data_vector import DataVector
from luxtronik.datatypes import Base


class ObsoleteDataVector(DataVector):

    name = "Obsolete"

    _obsolete = {
        "baz": "foo"
    }

    def __init__(self):
        super().__init__()
        self._data = {
            0: Base(["foo", "bar"]),
        }


class TestDataVector:
    """Test suite for DataVector"""

    @pytest.mark.parametrize("name, exception_expected", [
        ("foo", False),
        ("bar", True),
        ("baz", True),
        ("qux", False),
    ])
    def test_obsolete(self, name, exception_expected):
        """Test cases for initialization"""
        obsolete = ObsoleteDataVector()
        try:
            obsolete.get(name)
            assert not exception_expected
        except KeyError:
            assert exception_expected