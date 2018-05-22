import os.path
import unittest
from unittest.mock import patch

from ddt import data, ddt, file_data, unpack

import functions


@ddt
class ForwardGeocoding(unittest.TestCase):

    @file_data(os.path.join("data", "data_003", "test_amount_data.json"))
    def test_amount(self, count, name):
        self.assertTrue(functions.compare_amount(count, name))

    @file_data(os.path.join("data", "data_003", "test_coord_data.json"))
    def test_coord(self, name, lat, lon):
        self.assertEqual(functions.get_coord(name), (float(lat), float(lon)))
        self.assertTrue(functions.check_coordinates(name, lat, lon))

    @file_data(os.path.join("data", "data_003", "test_same_data.json"))
    def test_same_result(self, name1, name2):
        self.assertEqual(functions.get_info(name1), functions.get_info(name2))


@ddt
class ReverseGeocoding(unittest.TestCase):

    @file_data(os.path.join("data", "data_003", "small_reverse_data.json"))
    def test_result(self, place_id, lat, lon, category, type, addresstype, display_name, address):
        self.assertEqual(str(display_name), functions.get_display_name(lat, lon))


if __name__ == '__main__':
    unittest.main()
