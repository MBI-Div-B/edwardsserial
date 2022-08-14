import logging

from edwardsserial.descriptors import SerialQuery
from edwardsserial.serial_protocol import SerialProtocol
from tests.mocked_serial import MockedBaseTest

log = logging.getLogger()


class _TestingSerialProtocol(SerialProtocol):
    serial_query = SerialQuery("V", 123, float)


class TestSerialQuery(MockedBaseTest.MockedSerial):
    def test_single_ret_val(self):
        self.mocks["read_until"].return_value = b"=V123 0.54\r"
        self.assertEqual(0.54, _TestingSerialProtocol(port="").serial_query)
        self.mocks["Serial.write"].assert_called_with(b"?V123\r")

    def test_multi_ret_val(self):
        self.mocks["read_until"].return_value = b"=V123 0.54;1.34\r"
        self.assertEqual([0.54, 1.34], _TestingSerialProtocol(port="").serial_query)
        self.mocks["Serial.write"].assert_called_with(b"?V123\r")
