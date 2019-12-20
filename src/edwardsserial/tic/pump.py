from abc import ABC, abstractmethod
from warnings import warn

from edwardsserial.serial_protocol import AlertID, SerialProtocol


class Pump(SerialProtocol, ABC):
    PUMP_ID: int
    SPEED_ID: int
    POWER_ID: int

    # @property
    # @classmethod
    # @abstractmethod
    # def PUMP_ID(cls):
    #     return NotImplementedError
    #
    # def print_constant(self):
    #     print(type(self).CONSTANT)

    def on(self):
        self.send_message("!C", self.PUMP_ID, 1)

    def off(self):
        self.send_message("!C", self.PUMP_ID, 0)

    @property
    def state(self):
        value, alert_id, priority = self.send_message("?V", self.PUMP_ID)
        if alert_id:
            warn(AlertID(alert_id))
        return value

    @property
    def speed(self):
        value, alert_id, priority = self.send_message("?V", self.SPEED_ID)
        if alert_id:
            warn(AlertID(alert_id))
        return value

    @property
    def power(self):
        value, alert_id, priority = self.send_message("?V", self.POWER_ID)
        if alert_id:
            warn(AlertID(alert_id))
        return value

    @property
    def type(self):
        return self.send_message("?S", self.PUMP_ID, 3)


class TurboPump(Pump):
    PUMP_ID = 904
    SPEED_ID = 905
    POWER_ID = 906
    NORMAL_ID = 907
    STANDBY_ID = 908
    CYCLE_ID = 909

    @property
    def normal(self):
        value, alert_id, priority = self.send_message("?V", self.NORMAL_ID)
        if alert_id:
            warn(AlertID(alert_id))
        if value == "0":
            return False
        if value == "4":
            return True
        raise ValueError(f"Got state={value}. Expected 0 or 4.")

    @property
    def standby(self):
        value, alert_id, priority = self.send_message("?V", self.STANDBY_ID)
        if alert_id:
            warn(AlertID(alert_id))
        if value == "0":
            return False
        if value == "4":
            return True
        raise ValueError(f"Got state={value}. Expected 0 or 4.")

    @standby.setter
    def standby(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("Value must be of type bool.")
        self.send_message("?C", self.STANDBY_ID, int(value))

    @property
    def cycle_time(self):
        value, state, alert_id, priority = self.send_message("?V", self.STANDBY_ID)
        if alert_id:
            warn(AlertID(alert_id))
        return value

    @property
    def delay(self):
        return self.send_message("?S", self.STANDBY_ID, 21)

    @delay.setter
    def delay(self, value: int):
        if value not in range(0, 100):
            raise ValueError("Must be between 0 and 99")
        self.send_message("!S", self.STANDBY_ID, "21;{value}")


class BackingPump(Pump):
    PUMP_ID = 910
    SPEED_ID = 911
    POWER_ID = 912

    @property
    def sequence_options(self):
        pass
