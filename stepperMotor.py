#!/usr/bin/env python
import RPi.GPIO as GPIO
from time import sleep


class StepperMotor:
    IN1 = 32    # pin 32
    IN2 = 36    # pin 36
    IN3 = 38    # pin 38
    IN4 = 40    # pin 40

    def __set_step__(self,w1, w2, w3, w4):
        GPIO.output(self.IN1, w1)
        GPIO.output(self.IN2, w2)
        GPIO.output(self.IN3, w3)
        GPIO.output(self.IN4, w4)

    def __stop__(self):
        self.__set_step__(0, 0, 0, 0)

    def __forward__(self,delay, steps):
        for i in range(0, steps):
            self.__set_step__(1, 0, 0, 0)
            sleep(delay)
            self.__set_step__(0, 1, 0, 0)
            sleep(delay)
            self.__set_step__(0, 0, 1, 0)
            sleep(delay)
            self.__set_step__(0, 0, 0, 1)
            sleep(delay)

    def __backward__(self, delay, steps):
        for i in range(0, steps):
            self.__set_step__(0, 0, 0, 1)
            sleep(delay)
            self.__set_step__(0, 0, 1, 0)
            sleep(delay)
            self.__set_step__(0, 1, 0, 0)
            sleep(delay)
            self.__set_step__(1, 0, 0, 0)
            sleep(delay)

    def __setup__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
        GPIO.setup(self.IN1, GPIO.OUT)      # Set pin's mode as output
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)

    if __name__ == '__main__':     # Program start from here
        __setup__()
