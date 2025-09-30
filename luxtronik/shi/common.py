
###############################################################################
# Smart home telegrams
###############################################################################

class LuxtronikSmartHomeReadTelegram:
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
        self.addr = addr
        self.count = count
        self.data = []


class LuxtronikSmartHomeWriteTelegram:
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
        self.addr = addr
        self.data = data if isinstance(data, list) else []
        self.count = len(self.data)