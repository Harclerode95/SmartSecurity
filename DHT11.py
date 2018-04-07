#!/usr/bin/python
import RPi.GPIO as GPIO
from time import sleep


class DHT11:
    channel = 16

    def __init__(self):
        # Setup GPIO #
        GPIO.setmode(GPIO.BOARD)
        sleep(1)
        GPIO.setup(self.channel, GPIO.OUT)
        GPIO.output(self.channel, GPIO.LOW)
        sleep(0.02)
        GPIO.output(self.channel, GPIO.HIGH)
        GPIO.setup(self.channel, GPIO.IN)

    def __read_sensor__(self):


        # Grab the data #
        data = []
        j = 0
        while GPIO.input(self.channel) == GPIO.LOW:
            continue

        while GPIO.input(self.channel) == GPIO.HIGH:
            continue

        while j < 40:
            k = 0
            while GPIO.input(self.channel) == GPIO.LOW:
                continue

            while GPIO.input(self.channel) == GPIO.HIGH:
                k += 1
                if k > 100:
                    break

            if k < 8:
                data.append(0)
            else:
                data.append(1)

            j += 1

        # Copy lists from data into variables #
        humidity_bit = data[0:8]
        humidity_point_bit = data[8:16]
        temperature_bit = data[16:24]
        temperature_point_bit = data[24:32]
        check_bit = data[32:40]

        # Use these integer variables #
        humidity = 0
        humidity_point = 0
        temperature = 0
        temperature_point = 0
        check = 0

        # Set the used variables from bit lists #
        for i in range(8):
            humidity += humidity_bit[i] * 2 ** (7 - i)
            humidity_point += humidity_point_bit[i] * 2 ** (7 - i)
            temperature += temperature_bit[i] * 2 ** (7 - i)
            temperature_point += temperature_point_bit[i] * 2 ** (7 - i)
            check += check_bit[i] * 2 ** (7 - i)

        # Check for valid data #
        tmp = humidity + humidity_point + temperature + temperature_point

        if check == tmp:
            print("temperature : ", temperature, ", humidity : ", humidity)
        else:
            # Print values and error #
            print("wrong")
            print("temperature : ", temperature, ", humidity : ", humidity, " check : ", check, " tmp : ", tmp)

        return temperature, humidity
