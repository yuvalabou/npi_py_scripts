"""LED Blink script using sys/class/gpio"""
import os
from time import sleep

# echo "203" >/sys/class/gpio/export
# os.system('echo "out" >/sys/class/gpio/gpio203/direction')
while True:
    os.system('echo "1" >/sys/class/gpio/gpio203/value')
    sleep(0.2)
    os.system('echo "0" >/sys/class/gpio/gpio203/value')
