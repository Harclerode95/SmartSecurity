#####################################################################
# SmartSecurity Core Python Program                                 #
# Team: SmartSecurity                                               #
# Tyler Harclerode, Brandon Lin, Zachary Davoli, Jonathan Griffin   #
# CET/CSC Senior Project 2017/2018                                  #
#####################################################################

# !/usr/bin/python           # Script in Python interpreter
import RPi.GPIO as GPIO     # For Raspberry Pi GPIO utilization
import time

#  Import project specific files #
import lcdDisplay           # Printing to LCD
import stepperMotor         # Controlling the stepper motor
import matrixKeypad         # Handing the keypad IO
import DHT11                # Temperature and humidity sensor
import PIR                  # Pyroelectric Infrared Motion Detector
import LEDs                 # LEDs for status and alert

#####################################################################
#  Class Instantiations  #
lcd = lcdDisplay.AdafruitCharLCD()      # LCD
kp = matrixKeypad.Keypad()              # Keypad
stpr = stepperMotor.StepperMotor()      # Stepper Motor
pir = PIR.PIR()                         # Motion Detector
dht = DHT11.DHT11()                     # Temperature and humidity sensor
led = LEDs.LED()                        # Status/Alert LEDs


def __dht_test__():
    print('DHT11 TEST:')

    dht.__init__()

    dht.__read_sensor__()


def __pir_test__():
    pir.__init__()

    pir.pir_test()


# Cleanup resources #
def __destroy__():
    GPIO.cleanup()


def __main__():
    __dht_test__()

    __destroy__()

    __pir_test_()



__main__()
