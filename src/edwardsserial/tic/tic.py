from edwardsserial.serial_protocol import SerialProtocol
from edwardsserial.tic.gauge import Gauge
from edwardsserial.tic.pump import BackingPump, TurboPump


class TIC(SerialProtocol):
    def __init__(self, port):
        super().__init__(port)
        self._turbo_pump = TurboPump(port)
        self._backing_pump = BackingPump(port)
        self._gauge1 = Gauge(port, 913)
        self._gauge2 = Gauge(port, 914)
        self._gauge3 = Gauge(port, 915)

    @property
    def turbo_pump(self):
        return self._turbo_pump

    @property
    def backing_pump(self):
        return self._backing_pump

    @property
    def gauge1(self):
        return self._gauge1

    @property
    def gauge2(self):
        return self._gauge2

    @property
    def gauge3(self):
        return self._gauge3

    def pressure(self, gauge_number: int) -> float:
        if gauge_number not in (1, 2, 3):
            raise ValueError("gauge_number must be in (1,2,3)")
        object_id = 912 + gauge_number
        return 1e-2 * float(self.send_message(operation="?V", object_id=object_id)[0])
