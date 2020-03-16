import logging
import unittest
from functools import partial
from typing import Dict
from unittest.mock import Mock, patch

from edwardsserial.tic import TIC

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


# class PatchMeta(type):
#     """A metaclass to patch all inherited classes."""
#
#     patch_args: List[Tuple[str, Any]] = []
#
#     def __init__(cls, *args, **kwargs):
#         super(PatchMeta, cls).__init__(*args, **kwargs)
#         for patch_arg in cls.patch_args:
#             log.debug(patch_arg)
#             patch(*patch_arg)(cls)
class MockedBaseTest:
    class MockedSerial(unittest.TestCase):
        """
        BaseClass that mocks the serial connection of the serial protocol.
        Each test_ method inside the derived TestClass will get an additional argument 'mock_read_until'.
        """

        patch_args = {
            "read_until": (
                "edwardsserial.serial_protocol.serial.Serial.read_until",
                Mock(),
            ),
            "Serial.open": ("edwardsserial.serial_protocol.serial.Serial.open", Mock()),
            "Serial.write": (
                "edwardsserial.serial_protocol.serial.Serial.write",
                Mock(),
            ),
        }

        def setUp(self):
            self.mocks: Dict[Mock] = {}
            for key, patch_arg in self.patch_args.items():
                self.mocks[key] = patch(*patch_arg).start()
            self.addCleanup(patch.stopall)

    class MockedGauge(MockedSerial):
        attribute: str
        controller = TIC("")
        get_values: dict
        set_values: dict
        wrong_set_values: list

        @classmethod
        def setUpClass(cls):
            cls.get_method = partial(
                cls.controller.gauge1.__getattribute__, cls.attribute
            )
            cls.set_method = partial(cls.controller.gauge1.__setattr__, cls.attribute)

        def test_get_values(self):
            for serial_return, get_value in self.get_values.items():
                with self.subTest(get_value=get_value, serial_return=serial_return):
                    self.mocks["read_until"].return_value = serial_return
                    self.assertEqual(get_value, self.get_method())

        def test_set_values(self):
            for set_value, serial_command in self.set_values.items():
                with self.subTest(set_value=set_value, serial_command=serial_command):
                    self.set_method(set_value)
                    self.mocks["Serial.write"].assert_called_with(serial_command)

        def test_wrong_input_error_raised(self):
            for set_value in self.wrong_set_values:
                with self.subTest(set_value=set_value):
                    with self.assertRaises(ValueError):
                        self.set_method(set_value)
