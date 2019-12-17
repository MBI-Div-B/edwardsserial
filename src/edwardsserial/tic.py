import re

import serial

from edwardsserial.edwards_serial_protocol import EdwardsSerialProtocol


class TIC(EdwardsSerialProtocol):
    def __init__(self, port: str):
        self.port = port

    def __repr__(self):
        pass

    def read_pressure(self, gauge: int) -> float:
        pass
