import re

import serial


class TIC:

    OPERATIONS = ("!C", "!S", "?S", "?V")
    COMMAND = re.compile("![CS]\d{1,5}(.+;?)+\r", flags=re.ASCII)
    QUERY = re.compile("\?[SV]\d{1,5}\r]", flags=re.ASCII)
    MESSAGE = re.compile(f"{COMMAND}|{QUERY}")

    RESPONSE = re.compile("")

    def __init__(self, port: str):
        self.port = port

    def __repr__(self):
        pass

    def _serial_protocol_message(self, operation, object_id, data):
        data = data or ""
        message = f"{operation}{object_id} {data}\r"
        if not self.MESSAGE.match(message):
            raise ValueError(
                f"Serial message '{message}' does not have the correct format of {self.MESSAGE}"
            )
        return message

    def _send_message(self, operation, object_id, data):
        with serial.Serial(self.port, timeout=1, baudrate=9600) as ser:
            message = f"{operation}{object_id}"
            ser.write(b"?V913\r")
            answer = ser.read_until(b"\r").decode()
        pressure = 1e-2 * float(re.split("[ ;]", answer.rstrip())[1])
        return pressure

    def read_pressure(self, gauge: int) -> float:
        pass
