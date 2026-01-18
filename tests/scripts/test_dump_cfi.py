from luxtronik.scripts.dump_cfi import dump_all
from tests.fake import FakeLuxtronik


class TestDumpCfi:

    def test_dump_all(self):
        client = FakeLuxtronik()

        # It is sufficient if no exception occurs.
        dump_all(client)
