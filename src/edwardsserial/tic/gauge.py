from edwardsserial.serial_protocol import SerialProtocol


class Gauge(SerialProtocol):
    UNITS = {
        59: "Pa",
        66: "V",
        81: "%",
    }

    def __init__(self, port, object_id):
        super().__init__(port)
        self.object_id = object_id

    @property
    def pressure(self):
        value, unit, state = self._check_alert(self.object_id)
        unit = int(unit)
        if unit == 81:
            return int(value)
        return float(value)

    @property
    def unit(self):
        value, unit, state = self._check_alert(self.object_id)
        return self.UNITS.get(int(unit))

    @property
    def type(self):
        return

    @property
    def name(self):
        return

    @property
    def gas_type(self):
        return

    @property
    def ASG_range(self):
        return
