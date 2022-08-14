import logging

from edwardsserial.descriptors import ValueRange
from edwardsserial.serial_protocol import SerialProtocol
from tests.mocked_serial import MockedBaseTest

log = logging.getLogger()


class _TestingSerialProtocol(SerialProtocol):
    value_range = ValueRange(2, 6, operation="S", object_id=123)


class TestSerialQuery(MockedBaseTest.MockedSerial):
    def test_value_in_range(self):
        self.mocks["read_until"].return_value = b"=S123 6\r"
        for value in (2, 4, 6):
            with self.subTest(value=value):
                _TestingSerialProtocol(port="").value_range = value
        self.mocks["Serial.write"].assert_called_with(f"!S123 {value}\r".encode())

    def test_value_out_of_range(self):
        for value in (1, 7):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    _TestingSerialProtocol(port="").value_range = value

    def test_float_value(self):
        for value in (1.9, 2.5, 6.1):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    _TestingSerialProtocol(port="").value_range = value
