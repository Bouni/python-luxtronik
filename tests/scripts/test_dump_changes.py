from luxtronik.scripts.dump_changes import dump_all
from luxtronik import LuxtronikData
from tests.fake import FakeSocketInterface, FakeScreen


class TestDumpChanges:

    def test_dump_all(self):
        client = FakeSocketInterface("host", 0)
        changes = {}
        prev_data = LuxtronikData()
        this_data = LuxtronikData()
        screen = FakeScreen()

        # It is sufficient if no exception occurs.
        dump_all(screen, client, changes, prev_data, this_data)
