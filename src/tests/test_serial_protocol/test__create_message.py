import unittest

from edwardsserial.serial_protocol import SerialProtocol


class TestCreateMessage(unittest.TestCase):
    def test_correct_command(self):
        expected_message = "!C912 1\r"
        actual_message = SerialProtocol._create_message("!C", 912, 1)
        self.assertEqual(actual_message, expected_message)

    def test_correct_query(self):
        expected_message = "?V912\r"
        actual_message = SerialProtocol._create_message("?V", 912)
        self.assertEqual(actual_message, expected_message)

    def test_data_in_query(self):
        with self.assertRaises(ValueError):
            SerialProtocol._create_message("?V", 912, 1)

    def test_wrong_operation(self):
        with self.assertRaises(ValueError):
            SerialProtocol._create_message("!V", 912, 1)
