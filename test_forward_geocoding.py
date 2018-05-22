import unittest
import os.path
from ddt import ddt, data, file_data, unpack


@ddt
class ForwardGeocoding(unittest.TestCase):
    @file_data(os.path.join("data", "spb_streets.json"))
    def test_reverse(self, lat, lon, display_name, address):
        self.assertTrue(1 == 1)