from edwardsserial.descriptors import SerialQuery, ValueRange
from edwardsserial.serial_protocol import SerialProtocol


# make this as a descriptor that calls the owners pump start methods if available,
# since TIC does not forward some commands
# lrlunin: in case if you do not have a tic controller you still can communicate directly with the pump
# therefore this class was extended to cover the whole functionality
class nEXT(SerialProtocol):
    STATUS_BITS = {
        0: "Fail status condition active",
        1: "Below stopped speed",
        2: "Above normal speed",
        3: "Vent valve energised",
        4: "Start command active",
        6: "Serial enable active",
        7: "Above 50% rotational speed",
        8: "Exclusive control mode selection",
        9: "Exclusive control mode selection",
        10: "Controller internal software mismatch",
        11: "Controller failed internal configuration",
        12: "Timer expired",
        13: "Overspeed or Overcurrent trip activated",
        14: "Thermistor error",
        15: "Serial enable become inactivate following a serial Start command",
    }

    timer = ValueRange(start=1, end=30, operation="S", object_id=854)
    power_limit = ValueRange(start=50, end=200, operation="S", object_id=855)
    normal_speed = ValueRange(start=50, end=100, operation="S", object_id=856)
    standby_speed = ValueRange(start=55, end=100, operation="S", object_id=857)

    PIC_software_version = SerialQuery("S", 868, data_type=str)

    controller_run_time = SerialQuery("V", 882, data_type=int)
    pump_run_time = SerialQuery("V", 883, data_type=int)
    cycles = SerialQuery("V", 884, data_type=int)
    bearing_run_time = SerialQuery("V", 885, data_type=int)
    oil_cartridge_run_time = SerialQuery("V", 886, data_type=int)

    def restore_factory_settings(self):
        self.send_message("!S", 867, 1)

    def start(self):
        self.send_message("!C", 852, 1)

    def stop(self):
        self.send_message("!C", 852, 0)

    def get_speed_and_state(self):
        raw_speed, raw_state = self.send_message("?V", 852)
        return int(raw_speed), int(raw_state, 16)

    def get_link(self):
        return [0.1 * int(raw_data) for raw_data in self.send_message("?V", 860)]

    def get_temps(self):
        return [int(raw_data) for raw_data in self.send_message("?V", 859)]
    
    @property
    def state(self):
        # 8 single hex -> 32 bitds (only 16 first are in use, 16-31 - reserved)
        state_bits = int(self.send_message("?V", 852)[1], 16)
        return state_bits

    @property
    def link_voltage(self):
        """Measured link voltage in V"""
        ret_val = 0.1 * int(self.send_message("?V", 860)[0])
        return ret_val

    @property
    def link_current(self):
        """Measured link current in A"""
        ret_val = 0.1 * int(self.send_message("?V", 860)[1])
        return ret_val

    @property
    def link_power(self):
        """Measured link power in W"""
        ret_val = 0.1 * int(self.send_message("?V", 860)[2])
        return ret_val

    @property
    def motor_temperature(self):
        """Motor temperature in \u00B0C"""
        ret_val = int(self.send_message("?V", 859)[0])
        return ret_val

    @property
    def speed(self):
        return int(self.send_message("?V", 852)[0])

    @property
    def controller_temperature(self):
        """Controller temperature in \u00B0C"""
        ret_val = int(self.send_message("?V", 859)[1])
        return ret_val
