import pytest

from luxtronik.common import (
    parse_version,
    version_in_range
)

###############################################################################
# Tests
###############################################################################

class TestVersion:

    @pytest.mark.parametrize(
        "string, version",
        [
            ("1",           (1, 0, 0, 0)),
            ("2.1",         (2, 1, 0, 0)),
            ("3.2.1",       (3, 2, 1, 0)),
            ("1.2.3.4",     (1, 2, 3, 4)),
            ("1.2.3.4.5",   (1, 2, 3, 4)),
            ("a.b",         None),
            ("hello",       None),
            ("foo.bar",     None),
            ("1_2",         None),
            ("3 4",         None),
            (None,          None),
            ((1, 0, 0, 4),  (1, 0, 0, 4)),
            ((2, 1, 3),     (2, 1, 3, 0)),
            ((3, 2),        (3, 2, 0, 0)),
            ((5,),          (5, 0, 0, 0)),
            ((),            (0, 0, 0, 0)),
            ((3, "foo", 2), None),
        ]
    )
    def test_parse(self, string, version):
        parsed = parse_version(string)
        assert parsed == version

    @pytest.mark.parametrize(
        "version, since, until, in_range",
        [
            (None,   None,   None,         True),
            ((1, 2), None,   None,         True),
            (None,   (5, 4), (2, 1),       True),
            ((2, 4), (1, 3), None,         True),
            ((2, 4), (5, 1), None,         False),
            ((2, 4), None,   (2, 3, 9),    False),
            ((2, 4), None,   (2, 4, 0, 1), True),
            ((5, 6), (5, 6), (5, 6),       True),
            ((5, 6), (5, 7), (5, 6),       False),
            ((5, 6), (5, 6), (5, 5),       False),
            ((3, 7), (2, 8), (4, 6),       True),
        ]
    )
    def test_in_range(self, version, since, until, in_range):
        result = version_in_range(version, since, until)
        assert result == in_range