import time, sys
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

class COSensor:
    CO_PIN = 21     
    CO_FLAG = False

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.CO_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.CO_PIN, GPIO.RISING)
        GPIO.add_event_callback(self.CO_PIN, self.__action__)
        print('Carbon Monoxide sensor initialized')

    def __action__(self, pin):              # Parameters?
        print('Sensor detected action!')
        self.CO_FLAG = True
        return

