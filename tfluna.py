import struct
import time

__version__ = "0.1.0"
__repo__ = "https://github.com/your_github/tf_luna"

class TFLuna:
    def __init__(self, uart=None, i2c=None, address=0x10):
        if uart and i2c:
            raise ValueError("Use only one: UART or I2C.")
        self._uart = uart
        self._i2c = i2c
        self._address = address
        self._buffer = bytearray(9) if uart else bytearray(2)
        self._dist = None
        self._amp = None
        self._temp_raw = None

    def _read_uart_frame(self):
        while True:
            self._uart.readinto(self._buffer, end=1)
            if self._buffer[0] == 0x59:
                self._uart.readinto(self._buffer, start=1)
                if self._buffer[1] == 0x59:
                    break
        dist = self._buffer[2] | (self._buffer[3] << 8)
        amp = self._buffer[4] | (self._buffer[5] << 8)
        temp_raw = self._buffer[6] | (self._buffer[7] << 8)
        checksum = sum(self._buffer[0:8]) & 0xFF
        if checksum != self._buffer[8]:
            raise RuntimeError("Checksum mismatch")
        return dist, amp, temp_raw

    def _read_word(self, reg):
        result = bytearray(2)
        self._i2c.writeto(self._address, bytes([reg]))
        self._i2c.readfrom_into(self._address, result)
        return result[0] | (result[1] << 8)

    def _write_word(self, reg, value):
        data = bytes([reg, value & 0xFF, (value >> 8) & 0xFF])
        self._i2c.writeto(self._address, data)

    def _read_i2c(self):
        dist = self._read_word(0x00)
        amp = self._read_word(0x02)
        temp_raw = self._read_word(0x04)
        return dist, amp, temp_raw

    def read(self):
        """
        Reads distance, signal strength, and temperature from the sensor.
        The values can then be accessed via the distance, signal_strength,
        and temperature_c properties.
        """
        if self._uart:
            self._dist, self._amp, self._temp_raw = self._read_uart_frame()
        elif self._i2c:
            self._dist, self._amp, self._temp_raw = self._read_i2c()
        else:
            raise RuntimeError("No interface initialized")

    @property
    def distance(self):
        """
        The most recent distance measurement in centimeters.
        Returns None if no measurement has been taken.
        """
        return self._dist

    @property
    def signal_strength(self):
        """
        The most recent signal strength measurement.
        Returns None if no measurement has been taken.
        """
        return self._amp

    @property
    def temperature_c(self):
        """
        The most recent temperature measurement in degrees Celsius.
        Returns None if no measurement has been taken.
        """
        if self._temp_raw is None:
            return None
        return self._temp_raw / 8.0 - 256

    def set_mode(self, mode):
        """
        Set the operating mode of the sensor.
        :param str mode: 'continuous' or 'trigger'
        """
        if self._i2c is None:
            raise RuntimeError("set_mode is only available in I2C mode.")
        if mode == 'continuous':
            self._write_word(0x23, 0x00)
        elif mode == 'trigger':
            self._write_word(0x23, 0x01)
        else:
            raise ValueError("Mode must be 'continuous' or 'trigger'")

    def trigger_measurement(self):
        """
        Triggers a single measurement when in trigger mode.
        """
        if self._i2c is None:
            raise RuntimeError("trigger_measurement is only available in I2C mode.")
        self._write_word(0x24, 0x01)

    def set_frame_rate(self, fps):
        """
        Set the frame rate (measurement frequency) of the sensor.
        :param int fps: The desired frame rate (1-250 Hz).
        """
        if self._i2c is None:
            raise RuntimeError("set_frame_rate is only available in I2C mode.")
        if not 1 <= fps <= 250:
            raise ValueError("Frame rate must be between 1 and 250 Hz.")
        self._write_word(0x26, fps)

    def enable_sensor(self):
        """
        Enables the sensor to start measurements (I2C only).
        """
        if self._i2c is None:
            raise RuntimeError("enable_sensor is only available in I2C mode.")
        self._write_word(0x25, 0x00)

    def disable_sensor(self):
        """
        Disables the sensor to stop measurements (I2C only).
        """
        if self._i2c is None:
            raise RuntimeError("disable_sensor is only available in I2C mode.")
        self._write_word(0x25, 0x01)

    def set_power_mode(self, mode):
        """
        Set the power mode of the sensor.
        :param str mode: 'normal' or 'low' for low power
        """
        if self._i2c is None:
            raise RuntimeError("set_power_mode is only available in I2C mode.")
        if mode == 'normal':
            self._write_word(0x28, 0x00)
        elif mode == 'low':
            self._write_word(0x28, 0x01)
        else:
            raise ValueError("Power mode must be 'normal' or 'low'")

    def restore_defaults(self):
        """
        Restores the sensor's settings to factory defaults (I2C only).
        """
        if self._i2c is None:
            raise RuntimeError("restore_defaults is only available in I2C mode.")
        self._write_word(0x29, 0x01)

    def save_settings(self):
        self._write_word(0x20, 0x01)

    def reboot(self):
        self._write_word(0x21, 0x02)