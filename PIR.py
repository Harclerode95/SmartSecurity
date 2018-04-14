#!/usr/bin/python
import RPi.GPIO as GPIO     # For Raspberry Pi GPIO utilization
from time import sleep


class PIR:
    PIR_PIN = 17  # pin11
    motion_flag = False

    def __init__(self):
        GPIO.setmode(GPIO.BCM)                # Numbers GPIOs by physical location
        GPIO.setup(self.PIR_PIN, GPIO.IN)   # Set BtnPin's mode as input

    def pir_test(self):
        for i in range(8):
            if GPIO.input(self.PIR_PIN) == GPIO.LOW:
                print('...Movement not detected!', i)
                break
            else:
                print('Movement detected!...', i)
                self.motion_flag = True
                break

        print(self.motion_flag)
        return self.motion_flag
