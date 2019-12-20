from edwardsserial.serial_protocol import SerialProtocol
from edwardsserial.tic.gauge import Gauge
from edwardsserial.tic.pump import BackingPump, TurboPump


class TIC(SerialProtocol):
    def __init__(self, port):
        super().__init__(port)
        self.turbo_pump = TurboPump(port)
        self.backing_pump = BackingPump(port)

    def pressure(self, gauge_number: int) -> float:
        if gauge_number not in (1, 2, 3):
            raise ValueError("gauge_number must be in (1,2,3)")
        object_id = 912 + gauge_number
        return 1e-2 * float(self.send_message(operation="?V", object_id=object_id)[0])
