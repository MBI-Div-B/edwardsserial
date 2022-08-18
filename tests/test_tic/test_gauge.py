import logging

from edwardsserial.serial_protocol import AlertID
from edwardsserial.tic import TIC
from tests.mocked_serial import MockedBaseTest

log = logging.getLogger()
log.getChild("serial_protocol")
# log.setLevel(logging.DEBUG)

# file_handler = logging.FileHandler(filedir / f"{__name__}.log", mode="w")

# logger.addHandler(file_handler)
log.addHandler(logging.StreamHandler())


class TestGauge(MockedBaseTest.MockedSerial):
    def setUp(self):
        super().setUp()
        self.gauge = TIC("").gauge1

    def test_state(self):
        self.mocks["read_until"].return_value = b"=V913 0.34;59;11;0;0\r"
        self.assertEqual("11: On", self.gauge.state)
        self.mocks["Serial.write"].assert_called_with(b"?V913\r")

    def test_unit(self):
        serial_returns = {
            b"=V913 0.34;59;11;0;0\r": "Pa",
            b"=V913 0.34;66;11;0;0\r": "V",
            b"=V913 0.34;81;11;0;0\r": "%",
        }
        for serial_return, return_value in serial_returns.items():
            self.mocks["read_until"].return_value = serial_return
            self.assertEqual(return_value, self.gauge.unit)
            self.mocks["Serial.write"].assert_called_with(b"?V913\r")

    def test_type(self):
        serial_returns = {
            b"=S913 5;0\r": "0: Unknown Device",
            b"=S913 5;15\r": "15: WRG",
            b"=S913 5;25\r": "25: ASG",
        }
        for serial_return, return_value in serial_returns.items():
            self.mocks["read_until"].return_value = serial_return
            self.assertEqual(return_value, self.gauge.type)
            self.mocks["Serial.write"].assert_called_with(b"?S913 5\r")

    def test_on(self):
        self.mocks["read_until"].return_value = b"*C913 0\r"
        self.gauge.on()
        self.mocks["Serial.write"].assert_called_with(b"!C913 1\r")

    def test_off(self):
        self.mocks["read_until"].return_value = b"*C913 0\r"
        self.gauge.off()
        self.mocks["Serial.write"].assert_called_with(b"!C913 0\r")

    def test_zero(self):
        self.mocks["read_until"].return_value = b"*C913 0\r"
        self.gauge.zero()
        self.mocks["Serial.write"].assert_called_with(b"!C913 3\r")

    def test_calibrate(self):
        self.mocks["read_until"].return_value = b"*C913 0\r"
        self.gauge.calibrate()
        self.mocks["Serial.write"].assert_called_with(b"!C913 4\r")

    def test_degas(self):
        self.mocks["read_until"].return_value = b"*C913 0\r"
        self.gauge.degas()
        self.mocks["Serial.write"].assert_called_with(b"!C913 5\r")

    def test_new_id(self):
        self.mocks["read_until"].return_value = b"*C913 0\r"
        self.gauge.new_id()
        self.mocks["Serial.write"].assert_called_with(b"!C913 2\r")


class TestPressure(MockedBaseTest.MockedGauge):
    attribute = "pressure"
    get_values = {
        b"=V913 0.34;59;11;0;0\r": 0.34,
        b"=V913 0.001;59;11;0;0\r": 1e-3,
        b"=V913 90;81;11;0;0\r": 90,
        b"=V913 5.9;66;11;0;0\r": 5.9,
    }
    set_values: dict = {}
    wrong_set_values: list = []

    def test_gauge_disconnected(self):
        self.mocks["read_until"].return_value = b"=V913 990000000;59;2;9;0\r"
        with self.assertWarns(AlertID):
            self.assertIs(self.controller.gauge1.pressure, None)

    def test_gauge_never_conncted(self):
        self.mocks["read_until"].return_value = b"=V913 990000000;59;0;0;0\r"
        self.assertIs(self.controller.gauge1.pressure, None)

    def test_gauge_calibrating(self):
        self.mocks["read_until"].return_value = b"=V913 990000000;59;8;0;0\r"
        self.assertEqual(9.9e8, self.controller.gauge1.pressure)


class TestName(MockedBaseTest.MockedGauge):
    attribute = "name"
    get_values = {b"=S913 68;NAME\r": "NAME"}
    set_values = {
        "NAME": b"!S913 68;NAME\r",
        "NAM": b"!S913 68;NAM\r",
        "4": b"!S913 68;4\r",
    }
    wrong_set_values = ["name", "name1"]


class TestGasType(MockedBaseTest.MockedGauge):
    attribute = "gas_type"
    get_values = {b"=S913 7;0;0\r": "0: Nitrogen", b"=S913 7;1;0\r": "1: Helium"}
    set_values = {0: b"!S913 7;0;0\r", 3: b"!S913 7;3;0\r"}
    wrong_set_values = ["True", "False", 7, 8]


class TestFilter(MockedBaseTest.MockedGauge):
    attribute = "filter"
    get_values = {b"=S913 7;0;1\r": True, b"=S913 7;0;0\r": False}
    set_values = {False: b"!S913 7;0;0\r", True: b"!S913 7;0;1\r"}
    wrong_set_values = ["True", "False", 0, 1]


class TestASGRange(MockedBaseTest.MockedGauge):
    attribute = "ASG_range"
    get_values = {b"=S913 6;0\r": "0: 1000 mbar", b"=S913 6;1\r": "1: 2000 mbar"}
    set_values = {0: b"!S913 6;0\r", 1: b"!S913 6;1\r"}
    wrong_set_values = ["True", "False"]
