from luxtronik.scripts.dump_shi import dump_all
from tests.fake import FakeShiInterface


class TestDumpShi:

    def test_dump_all(self):
        client = FakeShiInterface.for_script_test()

        # It is sufficient if no exception occurs.
        dump_all(client)
