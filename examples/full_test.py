# SPDX-FileCopyrightText: 2024 somenice
#
# SPDX-License-Identifier: MIT

import time
import board
import busio
import tfluna

# This example requires an I2C connection, as trigger mode and power modes are I2C-only features.
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = tfluna.TFLuna(i2c=i2c)

print("TFLuna full_test")
print("-----------------")

# Set the sensor to trigger mode
try:
    print("Setting sensor to trigger mode...")
    sensor.set_mode('trigger')
    print("Mode set successfully.")
except RuntimeError as e:
    print(f"Could not set mode: {e}")
    print("This example must be run in I2C mode.")
    # Stop the script if we can't set the mode
    while True:
        pass

# --- Trigger Mode Demonstration ---
print("\n--- Trigger Mode Demo ---")
for i in range(5):
    try:
        print(f"Triggering measurement {i+1}/5...")
        sensor.trigger_measurement()
        # There's no explicit data-ready signal, so we'll just wait a moment
        # for the sensor to perform the measurement before reading.
        # The time required may vary based on the sensor's internal processing.
        time.sleep(0.1)
        sensor.read()

        dist = sensor.distance
        amp = sensor.signal_strength
        temp = sensor.temperature_c

        print(f"  Distance: {dist if dist is not None else 'N/A'} cm")
        print(f"  Signal:   {amp if amp is not None else 'N/A'}")
        print(f"  Temp:     {temp if temp is not None else 'N/A'} C")

    except RuntimeError as e:
        print(f"Error during measurement: {e}")

    time.sleep(1) # Wait 1 second between triggered readings

# --- Sleep/Power Mode Demonstration ---
print("\n--- Low Power Mode Demo ---")
try:
    print("Enabling low power mode for 5 seconds...")
    sensor.set_power_mode('low')
    time.sleep(5)
    print("Returning to normal power mode...")
    sensor.set_power_mode('normal')
    # It may take a moment for the sensor to wake up fully
    time.sleep(0.5)
    print("Sensor is back in normal power mode.")

except RuntimeError as e:
    print(f"Could not set power mode: {e}")

print("\nTest complete.")
