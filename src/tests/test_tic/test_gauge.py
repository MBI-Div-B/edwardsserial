import logging

from edwardsserial.tic import TIC
from tests.mocked_serial import MockedSerial

log = logging.getLogger()
log.getChild("serial_protocol")
# log.setLevel(logging.DEBUG)

# file_handler = logging.FileHandler(filedir / f"{__name__}.log", mode="w")

# logger.addHandler(file_handler)
log.addHandler(logging.StreamHandler())


class TestGauge(MockedSerial):
    def test_on(self):
        pass

    def test_off(self):
        pass

    def test_zero(self):
        pass

    def test_calibrate(self):
        pass

    def test_degas(self):
        pass

    def test_new_id(self):
        pass


class TestFilter(MockedSerial):
    controller = TIC("")

    def test_get_filter(self):
        calls = {b"=S913 7;0;1\r": True, b"=S913 7;0;0\r": False}
        for key, value in calls.items():
            with self.subTest(serial_return_value=key, expected_return_value=value):
                self.check_return_value(
                    method=lambda: self.controller.gauge1.filter,
                    serial_return_value=key,
                    expected_return_value=value,
                )

    def test_set_filter(self):
        self.check_return_value(
            method=lambda: self.controller.gauge1.filter,
            serial_return_value=b"=S913 7;0;1\r",
            expected_return_value=True,
        )
