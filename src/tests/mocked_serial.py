import logging
import unittest
from typing import Dict
from unittest.mock import Mock, patch

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
        "Serial.write": ("edwardsserial.serial_protocol.serial.Serial.write", Mock()),
    }
    # todo: maybe use this, since you can assign the patch
    #  function to class attributes and do not need to provide them as method arguments

    def setUp(self):
        self.mocks: Dict[Mock] = {}
        for key, patch_arg in self.patch_args.items():
            self.mocks[key] = patch(*patch_arg).start()
        self.addCleanup(patch.stopall)

    def check_return_value(self, method, serial_return_value, expected_return_value):
        self.mocks["read_until"].return_value = serial_return_value
        self.assertEqual(expected_return_value, method())
