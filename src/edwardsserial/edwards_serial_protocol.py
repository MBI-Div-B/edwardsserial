import re

import serial


class EdwardsSerialProtocol:
    BAUDRATE = 9600
    OPERATIONS = ("!C", "!S", "?S", "?V")
    COMMAND = re.compile(r"![CS]\d{1,5}(.+;?)+\r", flags=re.ASCII)
    QUERY = re.compile(r"\?[SV]\d{1,5}\r]", flags=re.ASCII)
    MESSAGE = re.compile(f"{COMMAND.pattern}|{QUERY.pattern}")

    RESPONSE = re.compile("")

    def __init__(self, port: str):
        self.port = port

    def __repr__(self):
        pass

    @classmethod
    def _serial_protocol_message(self, operation, object_id, data):
        data = data or ""
        message = f"{operation}{object_id} {data}\r"
        if not self.MESSAGE.match(message):
            raise ValueError(
                f"Serial message '{message}' does not have the correct format of {self.MESSAGE}."
            )
        return message

    def _send_message(self, operation, object_id, data):
        with serial.Serial(self.port, timeout=1, baudrate=self.BAUDRATE) as ser:
            message = self._serial_protocol_message(operation, object_id, data)
            ser.write(message)
            answer = self.RESPONSE.match(ser.read_until(b"\r"))
        if not answer:
            raise ConnectionError("No serial connection to device.")
        return data
