from unittest import TestCase

from machinescatchers import MachinesCatcher


class MachinesCrawlerTest(TestCase):
    def test_get_unknown_platform_machines(self):
        with self.assertRaises(KeyError):
            MachinesCatcher("foobar")
