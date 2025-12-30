"""
Commonly used methods and classes throughout
the Luxtronik smart home interface (SHI) module.
"""

import logging

LOGGER = logging.getLogger("Luxtronik.SmartHomeInterface")

###############################################################################
# Version methods
###############################################################################

def parse_version(version):
    """
    Parse a version string into a tuple with exactly 4 integers.
    The individual numbers correspond to `major.minor.patch.build`.
    A given tuple of integers is expanded or reduced to 4 integers.

    Examples:
        "1"         -> (1, 0, 0, 0)
        "2.1"       -> (2, 1, 0, 0)
        "3.2.1"     -> (3, 2, 1, 0)
        "1.2.3.4"   -> (1, 2, 3, 4)
        "1.2.3.4.5" -> (1, 2, 3, 4)   # extra parts are ignored
        "a.b"       -> None

    Args:
        version (str | tuple[int, ...]): Version string or version as tuple.

    Returns:
        tuple[int, int, int, int] | None: Parsed version tuple, or None if invalid.
    """
    if isinstance(version, tuple) and all(type(p) is int for p in version):
        return (version + (0, 0, 0, 0))[:4]
    elif isinstance(version, str):
        parts = version.strip().split(".")
        if not parts or any(not p.isdigit() for p in parts):
            return None
        nums = [int(p) for p in parts]
        nums = (nums + [0, 0, 0, 0])[:4]
        return tuple(nums)
    else:
        return None


def version_in_range(version, since=None, until=None):
    """
    Check whether a version is within the specified range of `[since..until]`.
    If an argument is None, the corresponding check is skipped.

    Args:
        version (tuple[int, ...] | None): The version to check.
            If None, returns True.
        since (tuple[int, ...] | None): Lower bound (inclusive).
            If None, no lower bound is applied.
        until (tuple[int, ...] | None): Upper bound (inclusive).
            If None, no upper bound is applied.

    Returns:
        bool: True if version is within the range, False otherwise.
    """
    if version is None:
        return True
    if since is not None and version < since:
        return False
    if until is not None and version > until:
        return False
    return True

###############################################################################
# Smart home telegrams
###############################################################################

class LuxtronikSmartHomeTelegram:
    """
    Base class for luxtronik read and write telegrams
    """

    @property
    def addr(self):
        return self._addr

    @property
    def count(self):
        return self._count

    @property
    def data(self):
        return self._data

    def prepare(self):
        pass

###############################################################################
# Smart home read telegrams
###############################################################################

class LuxtronikSmartHomeReadTelegram(LuxtronikSmartHomeTelegram):
    """
    Represents a single smart home data field(s) read operation.

    A telegram encapsulates both the request parameters (`addr`, `count`)
    and the response data (`data`). It is primarily used to support
    list-based read operations.
    """

    def __init__(self, addr, count):
        """
        Initialize a read telegram.

        Args:
            addr (int): Starting register address to read from.
            count (int): Number of 16-bit registers to read.
        """
        self._addr = addr
        self._count = count
        self._data = []

    @LuxtronikSmartHomeTelegram.data.setter
    def data(self, value):
        self._data = value if isinstance(value, list) \
            and len(value) == self._count else None

    def prepare(self):
        "Prepare the telegram for a (repeat) read operation"
        self._data = []

class LuxtronikSmartHomeReadHoldingsTelegram(LuxtronikSmartHomeReadTelegram):
    pass

class LuxtronikSmartHomeReadInputsTelegram(LuxtronikSmartHomeReadTelegram):
    pass

###############################################################################
# Smart home write telegrams
###############################################################################

class LuxtronikSmartHomeWriteTelegram(LuxtronikSmartHomeTelegram):
    """
    Represents a smart home data field(s) write operation.

    A write telegram encapsulates the request parameters (`addr`, `count`)
    and the payload (`data`). It is primarily used to support list-based
    write operations.
    """

    def __init__(self, addr, data):
        """
        Initialize a write telegram.

        Args:
            addr (int): Starting register address to write to.
            data (list[int]): Values to be written. If None or not a list,
                the telegram will be initialized with an empty payload.
        """
        self._addr = addr
        self._count = 0
        self._data = []
        self.data = data

    @LuxtronikSmartHomeTelegram.data.setter
    def data(self, value):
        self._data = value if isinstance(value, list) else []
        self._count = len(self._data)

class LuxtronikSmartHomeWriteHoldingsTelegram(LuxtronikSmartHomeWriteTelegram):
    pass

###############################################################################
# Set of all usable telegrams
###############################################################################

LuxtronikSmartHomeTelegrams = {
    LuxtronikSmartHomeReadHoldingsTelegram,
    LuxtronikSmartHomeReadInputsTelegram,
    LuxtronikSmartHomeWriteHoldingsTelegram,
}
