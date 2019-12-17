import unittest

from edwardsserial.tic import TIC


class TestSerialProtocolMessage(unittest.TestCase):
    def test_correct_message(self):
        expected_message = "!C912 1\r"
        actual_message = TIC._serial_protocol_message("!C", 912, 1)
        self.assertEqual(actual_message, expected_message)

    def test_data_in_query(self):
        with self.assertRaises(ValueError):
            TIC._serial_protocol_message("?V", 912, 1)

    def test_wrong_operation(self):
        with self.assertRaises(ValueError):
            TIC._serial_protocol_message("!V", 912, 1)
