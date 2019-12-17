import unittest
from unittest.mock import Mock, patch

from edwardsserial.serial_protocol import ErrorResponse, SerialProtocol


@patch("edwardsserial.serial_protocol.serial.Serial.open", Mock())
@patch("edwardsserial.serial_protocol.serial.Serial.write", Mock())
class TestSendMessage(unittest.TestCase):
    @patch("edwardsserial.serial_protocol.serial.Serial.read_until")
    def test_no_serial_return_value(self, mock_read_until):
        mock_read_until.return_value = ""
        with self.assertRaises(ConnectionError):
            SerialProtocol(port="COM3").send_message("?V", 913)

    @patch("edwardsserial.serial_protocol.serial.Serial.read_until")
    def test_error_response(self, mock_read_until):
        mock_read_until.return_value = "*V913 1\r"
        with self.assertRaisesRegex(
            ErrorResponse,
            "Device responded with error code 1: Invalid command for object ID",
        ):
            SerialProtocol(port="COM3").send_message("?V", 913)

    @patch("edwardsserial.serial_protocol.serial.Serial.read_until")
    def test_data_response(self, mock_read_until):
        mock_read_until.return_value = "=V913 0.34;59;state;alert ID;priority\r"
        expected_data = ["0.34", "59", "state", "alert ID", "priority"]
        data = SerialProtocol(port="COM3").send_message("?V", 913)
        self.assertEqual(data, expected_data)
