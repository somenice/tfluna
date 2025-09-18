# SPDX-FileCopyrightText: 2024 somenice
#
# SPDX-License-Identifier: MIT

import time
import board
import busio
import tfluna

# -- I2C Example --
# i2c = board.I2C()  # uses board.SCL and board.SDA
# # i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
# sensor = tfluna.TFLuna(i2c=i2c)

# -- UART Example --
# For most boards, you can use the default UART pins
uart = busio.UART(board.TX, board.RX, baudrate=115200)
sensor = tfluna.TFLuna(uart=uart)


print("TFLuna simpletest")
print("--------------------")

while True:
    sensor.read()
    distance_cm = sensor.distance
    if distance_cm is not None:
        print(f"Distance: {distance_cm} cm")
    else:
        print("Distance not available")
    time.sleep(0.1) # Adjust sleep time based on sensor frame rate
