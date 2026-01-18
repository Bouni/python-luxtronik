from luxtronik.shi.common import LuxtronikSmartHomeReadTelegram


class FakeModbus:
    telegram_list = []
    result = True

    def __init__(self, host="", port="", timeout=0):
        self._connected = False
        self._blocking = False

    def _get_data(self, addr, count):
        return [addr - 10000 + i for i in range(count)]

    def read_inputs(self, addr, count):
        return self._get_data(addr, count) if self.result else None

    def send(self, telegrams):
        if not isinstance(telegrams, list):
            telegrams = [telegrams]
        FakeModbus.telegram_list = telegrams

        for t in telegrams:
            if isinstance(t, LuxtronikSmartHomeReadTelegram):
                t.data = self._get_data(t.addr, t.count)
        return self.result