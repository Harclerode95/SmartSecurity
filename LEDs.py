#!/usr/bin/python
import RPi.GPIO as GPIO
from time import sleep

class LED:
    PWR_LED = 7
    NETWORK_LED = 4
    ALARM_LED_G = 14
    ALARM_LED_Y = 15
    ALARM_LED_R = 18

    def __setup_pwr_led__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PWR_LED, GPIO.OUT)
        GPIO.output(self.PWR_LED, GPIO.HIGH)        # Set pin to high (3.3v) to power off LED

    def __turn_on_pwr_led__(self):
        print('Turning power led on')
        GPIO.output(self.PWR_LED, GPIO.HIGH)
        sleep(3)
        GPIO.output(self.PWR_LED, GPIO.LOW)
        sleep(0.5)

    def __setup_network_led__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.NETWORK_LED, GPIO.OUT)
        GPIO.output(self.NETWORK_LED, GPIO.HIGH)    # Set pin to high (3.3v) to power off LED

    def __turn_on_network_led__(self):
        GPIO.output(self.NETWORK_LED, GPIO.LOW)

    def __setup__alarm_g_led__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.ALARM_LED_G, GPIO.OUT)
        GPIO.output(self.ALARM_LED_G, GPIO.HIGH)    # Set pin to high (3.3v) to power off LED

    def __turn_on_alarm_g_led__(self):
        GPIO.output(self.ALARM_LED_G, GPIO.LOW)

    def __setup_alarm_y_led__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.ALARM_LED_Y, GPIO.OUT)
        GPIO.output(self.ALARM_LED_Y, GPIO.HIGH)    # Set pin to high (3.3v) to power off LED

    def __turn_on_alarm_y_led__(self):
        GPIO.output(self.ALARM_LED_Y, GPIO.LOW)

    def __setup_alarm_r_led__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.ALARM_LED_R, GPIO.OUT)
        GPIO.output(self.ALARM_LED_R, GPIO.HIGH)    # Set pin to high (3.3v) to power off LED

    def __turn_on_alarm_r_led__(self):
        GPIO.output(self.ALARM_LED_R, GPIO.LOW)


if __name__ == '__main__':
    led = LED()
    led.__setup_pwr_led__()
    led.__setup_network_led__()
    led.__setup__alarm_g_led__()
    led.__setup_alarm_y_led__()
    led.__setup_alarm_r_led__()
