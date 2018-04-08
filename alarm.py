# !/usr/bin/python          # Script in Python interpreter
import RPi.GPIO as GPIO     # For Raspberry Pi GPIO utilization
from time import sleep


class Alarm:
    ALARM_PIN = 13  # Needs a valid pin

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)  # Numbers pins by physical location
        GPIO.setup(self.ALARM_PIN, GPIO.OUT)  # Set pin mode as output
        GPIO.output(self.ALARM_PIN, GPIO.HIGH)  # Set pin to high(+3.3V) to off the beep

    def __buzzer_loop__(self):
        # Buzz twice per second #
        while True:
            GPIO.output(self.ALARM_PIN, GPIO.LOW)
            sleep(0.5)
            GPIO.output(self.ALARM_PIN, GPIO.HIGH)
            sleep(0.5)

    def __kill_alarm__(self):
        GPIO.output(self.ALARM_PIN, GPIO.HIGH)  # beep off
        GPIO.cleanup()  # Release resource

