import re

import serial

from edwardsserial.serial_protocol import SerialProtocol


class TIC(SerialProtocol):
    def __init__(self, port: str):
        self.port = port

    def __repr__(self):
        pass

    def read_pressure(self, gauge: int) -> float:
        pass
