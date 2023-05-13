# unit tests for string_utils.py

import unittest

from utils.string_utils import seconds_to_hms_str


class TestStringUtils(unittest.TestCase):
    """Unit tests for string_utils.py"""

    def test_seconds_to_hms_str(self):
        """Test seconds_to_hms_str"""
        self.assertEqual(seconds_to_hms_str(0), "")
        self.assertEqual(seconds_to_hms_str(1), "1s")
        self.assertEqual(seconds_to_hms_str(60), "1m")
        self.assertEqual(seconds_to_hms_str(3600), "1h")
        self.assertEqual(seconds_to_hms_str(3601), "1h 1s")
        self.assertEqual(seconds_to_hms_str(3660), "1h 1m")
        self.assertEqual(seconds_to_hms_str(3661), "1h 1m 1s")
        self.assertEqual(seconds_to_hms_str(36001), "10h 1s")
        self.assertEqual(seconds_to_hms_str(36060), "10h 1m")
        self.assertEqual(seconds_to_hms_str(36061), "10h 1m 1s")
        self.assertEqual(seconds_to_hms_str(36600), "10h 10m")
        self.assertEqual(seconds_to_hms_str(36601), "10h 10m 1s")

    def test_seconds_to_hms_str_bad_types(self):
        """Test seconds_to_hms_str with bad types"""
        with self.assertRaises(TypeError):
            seconds_to_hms_str("a")
        with self.assertRaises(TypeError):
            seconds_to_hms_str([1])
        with self.assertRaises(TypeError):
            seconds_to_hms_str((1, 2))
        with self.assertRaises(TypeError):
            seconds_to_hms_str({1: 2})
        with self.assertRaises(TypeError):
            seconds_to_hms_str({1, 2})
        with self.assertRaises(TypeError):
            seconds_to_hms_str(None)


if __name__ == "__main__":
    unittest.main()
