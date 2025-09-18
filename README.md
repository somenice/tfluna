# Gemini Project Context: tfluna

## Project Overview

This project contains a single-file CircuitPython library (`tfluna.py`) for interfacing with the TFLuna LiDAR time-of-flight distance sensor.

The library supports communication with the sensor via both UART and I2C protocols. It provides a simple class-based interface to read distance, signal strength, and temperature data.

**Key Technologies:**
*   CircuitPython
*   Python

## Building and Running

This is a CircuitPython library and is not intended to be run as a standalone application on a desktop computer.

**To use this library:**

1.  Copy the `tfluna.py` file to the `lib` directory of your CircuitPython-compatible microcontroller.
2.  Instantiate the `TFLuna` class in your `code.py` or other main script, providing either a `busio.UART` or `busio.I2C` object.

**Example Usage:**

```python
import board
import busio
import tfluna
import time

# For I2C
# i2c = busio.I2C(board.SCL, board.SDA)
# sensor = tfluna.TFLuna(i2c=i2c)

# For UART
uart = busio.UART(board.TX, board.RX, baudrate=115200)
sensor = tfluna.TFLuna(uart=uart)

while True:
    sensor.read()
    print(f"Distance: {sensor.distance} cm")
    print(f"Signal Strength: {sensor.signal_strength}")
    print(f"Temperature: {sensor.temperature_c} C")
    time.sleep(0.1)
```

## Development Conventions

The project consists of a single library file. Development should follow standard CircuitPython coding conventions. The `TFLuna` class encapsulates all interaction with the sensor. To get new data, the `read()` method must be called, which then populates the `distance`, `signal_strength`, and `temperature_c` properties.

## Key Functions in `tfluna.py`

The `TFLuna` class contains the following key methods and properties:

*   `__init__(self, uart=None, i2c=None, address=0x10)`: Constructor to set up the sensor. You must provide either a `uart` or `i2c` object.
*   `read()`: Triggers a new reading from the sensor. This method must be called before accessing the data properties.
*   `distance` (property): Returns the most recent distance measurement in centimeters.
*   `signal_strength` (property): Returns the most recent signal strength measurement.
*   `temperature_c` (property): Returns the most recent temperature measurement in degrees Celsius.

### Measurement Control (I2C Only)
*   `set_mode(self, mode)`: Sets the operating mode to `'continuous'` or `'trigger'`.
*   `trigger_measurement(self)`: Triggers a single reading when in 'trigger' mode.
*   `set_frame_rate(self, fps)`: Sets the measurement frequency, from 1 to 250 Hz.

### Power and Device Management (I2C Only)
*   `enable_sensor()`: Enables the sensor to start measurements.
*   `disable_sensor()`: Disables the sensor to stop measurements.
*   `set_power_mode(self, mode)`: Sets the power mode to `'normal'` or `'low'`.
*   `save_settings()`: Saves the sensor's current configuration to non-volatile memory.
*   `reboot()`: Reboots the sensor.
*   `restore_defaults()`: Resets the sensor's settings to factory defaults.

## Reference

*   **TF-Luna Instruction Manual:** https://cdn.robotshop.com/media/b/ben/rb-ben-17/pdf/tf-luna-8m-lidar-distance-sensor-instructions-manual.pdf
