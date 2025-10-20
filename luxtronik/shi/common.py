"""
Commonly used methods and classes throughout
the Luxtronik Smart Home Interface (SHI) module.
"""

import logging

LOGGER = logging.getLogger("Luxtronik.SmartHomeInterface")


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
