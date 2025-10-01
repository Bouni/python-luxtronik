from luxtronik.shi.common import (
    LuxtronikSmartHomeReadTelegram,
    LuxtronikSmartHomeWriteTelegram,
)

###############################################################################
# Tests
###############################################################################

class TestReadTelegram:

    def test_init(self):
        telegram = LuxtronikSmartHomeReadTelegram(10, 20)
        assert telegram.addr == 10
        assert telegram.count == 20
        assert telegram.data == []

class TestWriteTelegram:

    def test_init(self):
        telegram = LuxtronikSmartHomeWriteTelegram(10, [1, 2, 3])
        assert telegram.addr == 10
        assert telegram.count == 3
        assert telegram.data == [1, 2, 3]

        telegram = LuxtronikSmartHomeWriteTelegram(15, None)
        assert telegram.addr == 15
        assert telegram.count == 0
        assert telegram.data == []
