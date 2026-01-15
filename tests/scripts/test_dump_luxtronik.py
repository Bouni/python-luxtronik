from luxtronik.scripts.dump_luxtronik import dump_all
from tests.fake import FakeLuxtronik


class TestDumpLuxtronik:

    def test_dump_all(self):
        client = FakeLuxtronik()

        # It is sufficient if no exception occurs.
        dump_all(client)
