import unittest
from unittest.mock import Mock, patch

from edwardsserial.tic import TIC

mock_write = Mock()


@patch("edwardsserial.serial_protocol.serial.Serial.write", mock_write)
@patch("edwardsserial.serial_protocol.serial.Serial.open", Mock())
class TestPressure(unittest.TestCase):
    @patch("edwardsserial.serial_protocol.serial.Serial.read_until")
    def test_float(self, mock_read_until):
        mock_read_until.return_value = "=V913 12.3;59\r"
        expected_result = 0.123
        self.assertAlmostEqual(TIC("/dev/ttyS0").pressure(1), expected_result)

    @unittest.skip("not implemented")
    @patch("edwardsserial.serial_protocol.serial.Serial.read_until")
    def test_voltage(self, mock_read_until):
        mock_read_until.return_value = "=V913 12.3;59\r"
        expected_result = 0.123
        self.assertAlmostEqual(TIC("/dev/ttyS0").pressure(1), expected_result)

    @unittest.skip("not implemented")
    @patch("edwardsserial.serial_protocol.serial.Serial.read_until")
    def test_percent(self, mock_read_until):
        mock_read_until.return_value = "=V913 89;81\r"
        expected_result = 89
        self.assertAlmostEqual(TIC("/dev/ttyS0").pressure(1), expected_result)

    @patch(
        "edwardsserial.serial_protocol.serial.Serial.read_until",
        Mock(return_value="=V913 81\r"),
    )
    def test_correct_call(self):
        TIC("/dev/ttyS0").pressure(1)
        mock_write.assert_called_with("?V913\r")
