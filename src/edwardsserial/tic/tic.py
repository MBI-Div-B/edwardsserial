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

    @property
    def gauge_values(self):
        answer = self.send_message("?V", 940)
        values = {
            int(gauge): float(value) for gauge, value in zip(answer[::2], answer[1::2])
        }
        return values
