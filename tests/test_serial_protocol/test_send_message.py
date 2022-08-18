import logging

from edwardsserial.serial_protocol import ErrorResponse, SerialProtocol
from edwardsserial.tic import TIC
from tests.mocked_serial import MockedBaseTest

log = logging.getLogger()
log.getChild("serial_protocol")
log.setLevel(logging.DEBUG)

# file_handler = logging.FileHandler(filedir / f"{__name__}.log", mode="w")

# logger.addHandler(file_handler)
log.addHandler(logging.StreamHandler())


class TestSendMessage(MockedBaseTest.MockedSerial):
    def test_no_serial_return_value(self):
        self.mocks["read_until"].return_value = b""
        with self.assertRaises(ConnectionError):
            SerialProtocol(port="COM3").send_message("?V", 913)
        self.mocks["Serial.write"].assert_called_with(b"?V913\r")

    def test_error_response(self):
        self.mocks["read_until"].return_value = b"*V913 1\r"
        with self.assertRaisesRegex(
            ErrorResponse,
            "Device responded with error code 1: Invalid command for object ID",
        ):
            SerialProtocol(port="COM3").send_message("?V", 913)
        self.mocks["Serial.write"].assert_called_with(b"?V913\r")

    def test_error_response_no_error(self):
        self.mocks["read_until"].return_value = b"*V913 0\r"
        SerialProtocol(port="COM3").send_message("?V", 913)
        self.mocks["Serial.write"].assert_called_with(b"?V913\r")

    def test_error_response_no_message(self):
        self.mocks["read_until"].return_value = b"*V913 10\r"
        with self.assertRaisesRegex(
            ErrorResponse,
            "Device responded with error code 10: None",
        ):
            SerialProtocol(port="COM3").send_message("?V", 913)
        self.mocks["Serial.write"].assert_called_with(b"?V913\r")

    def test_data_response(self):
        self.mocks[
            "read_until"
        ].return_value = b"=V913 0.34;59;state;alert ID;priority\r"
        expected_data = ["0.34", "59", "state", "alert ID", "priority"]
        data = SerialProtocol(port="COM3").send_message("?V", 913)
        self.assertEqual(data, expected_data)
        self.mocks["Serial.write"].assert_called_with(b"?V913\r")

    def test_data_response_single(self):
        self.mocks["read_until"].return_value = b"=V913 0.34\r"
        expected_data = ["0.34"]
        data = SerialProtocol(port="COM3").send_message("?V", 913)
        self.assertEqual(data, expected_data)
        self.mocks["Serial.write"].assert_called_with(b"?V913\r")
