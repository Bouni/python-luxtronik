from luxtronik.scripts.watch_shi import dump_all
from luxtronik.shi import LuxtronikSmartHomeData
from tests.fake import FakeShiInterface, FakeScreen


class TestWatchShi:

    def test_dump_all(self):
        client = FakeShiInterface.for_script_test()
        changes = {}
        prev_data = LuxtronikSmartHomeData()
        this_data = LuxtronikSmartHomeData()
        screen = FakeScreen()

        # It is sufficient if no exception occurs.
        dump_all(screen, client, changes, prev_data, this_data)
