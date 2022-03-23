from unittest import TestCase

from machinescrawlers import MachinesCrawler


class MachinesCrawlerTest(TestCase):
    def test_get_unknown_platform_machines(self):
        with self.assertRaises(KeyError):
            MachinesCrawler("foobar")
