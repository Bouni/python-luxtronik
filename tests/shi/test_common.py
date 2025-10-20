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

    def test_prepare(self):
        telegram = LuxtronikSmartHomeReadTelegram(10, 3)

        # remove existing data
        telegram.data = [1, 2, 3]
        telegram.prepare()
        assert telegram.addr == 10
        assert telegram.count == 3
        assert telegram.data == []

    def test_set(self):
        telegram = LuxtronikSmartHomeReadTelegram(10, 3)

        # set valid data
        telegram.data = [5, 4, 3]
        assert telegram.addr == 10
        assert telegram.count == 3
        assert telegram.data == [5, 4, 3]

        # set invalid data (too less data)
        telegram.data = [2, 1]
        assert telegram.addr == 10
        assert telegram.count == 3
        assert telegram.data == None

class TestWriteTelegram:

    def test_init(self):
        # init with data
        telegram = LuxtronikSmartHomeWriteTelegram(10, [1, 2, 3])
        assert telegram.addr == 10
        assert telegram.count == 3
        assert telegram.data == [1, 2, 3]

        # init without data
        telegram = LuxtronikSmartHomeWriteTelegram(15, None)
        assert telegram.addr == 15
        assert telegram.count == 0
        assert telegram.data == []

    def test_set(self):
        telegram = LuxtronikSmartHomeWriteTelegram(10, [1, 2, 3])

        # set valid data
        telegram.data = [7, 6]
        assert telegram.addr == 10
        assert telegram.count == 2
        assert telegram.data == [7, 6]

        # set invalid data (no list)
        telegram.data = 4
        assert telegram.addr == 10
        assert telegram.count == 0
        assert telegram.data == []