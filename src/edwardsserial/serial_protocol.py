import re

import serial


class ErrorResponse(Exception):

    ERROR_CODES = {
        1: "Invalid command for object ID",
        2: "Invalid query/command",
        3: "Missing parameter",
        4: "Parameter out of range",
        5: "Invalid command in current state - e.g. serial command to start or stop when in parallel control mode",
        6: "Data checksum error",
        7: "EEPROM read or write error",
        8: "Operation took too long",
        9: "Invalid config ID",
    }

    def __init__(self, error_code):
        message = f"Device responded with error code {error_code}: {self.ERROR_CODES.get(int(error_code))}"
        super().__init__(message)


class SerialProtocol:
    BAUDRATE = 9600
    COMMAND = re.compile(r"![CS]\d{1,5} (.+;?)+\r", flags=re.ASCII)
    QUERY = re.compile(r"\?[SV]\d{1,5}\r", flags=re.ASCII)
    MESSAGE = re.compile(f"{COMMAND.pattern}|{QUERY.pattern}")

    ERROR_RESPONSE = re.compile(
        r"\*[CSV]\d{1,5} (?P<error_code>\d{1,2})\r", flags=re.ASCII
    )
    DATA_RESPONSE = re.compile(r"=[SV]\d{1,5} (?P<data>.+;?)+\r", flags=re.ASCII)
    RESPONSE = re.compile(f"{ERROR_RESPONSE.pattern}|{DATA_RESPONSE.pattern}")

    def __init__(self, port: str):
        self.port = port

    @classmethod
    def _create_message(cls, operation: str, object_id: int, data=None) -> str:
        data = f" {data}" if data else ""
        message = f"{operation}{object_id}{data}\r"
        if not cls.MESSAGE.match(message):
            raise ValueError(
                f"Serial message {message.encode('unicode-escape')!r} does not have the correct format of {cls.MESSAGE}."
            )
        return message

    def send_message(self, operation, object_id, data=None):
        with serial.Serial(self.port, timeout=1, baudrate=self.BAUDRATE) as ser:
            message = self._create_message(operation, object_id, data=data)
            ser.write(message)
            response = ser.read_until("\r")
            print(f"response={response}")
            response = self.RESPONSE.match(response)
        if not response:
            raise ConnectionError("No serial connection to device.")
        groups = response.groupdict()
        if groups.get("error_code"):
            raise ErrorResponse(error_code=groups.get("error_code"))
        return groups.get("data").split(";")
