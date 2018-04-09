#!/usr/bin/python
import RPi.GPIO as GPIO
from time import sleep


class DHT11Sensor:

    channel = 16        # Pin 16
    total_temp = 0      # Totaled summed temperature readings to be averaged
    total_humidity = 0  # Totaled summed humidity readings to be averaged
    valid_count = 0     # Number of valid readings for averaging (check == temp)

    def __init__(self):

        # Setup GPIO #
        GPIO.setmode(GPIO.BOARD)
        sleep(1)
        GPIO.setup(self.channel, GPIO.OUT)
        GPIO.output(self.channel, GPIO.LOW)
        sleep(0.02)
        GPIO.output(self.channel, GPIO.HIGH)
        GPIO.setup(self.channel, GPIO.IN)
        print('End of DHT init')

    def __read_sensor__(self):
        print('Starting sensor reading')
        # Data will be 40 segment (bit) list #
        data = []
        j = 0

        # Average verified data from 5 attempts #
        #for attempts in range(5):

            # Break through no matter what #
        while GPIO.input(self.channel) == GPIO.LOW:
            continue
        while GPIO.input(self.channel) == GPIO.HIGH:
            continue

        # Fill list based on high/low signals #
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
                print('Sensor is working')

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
                #self.valid_count += 1
                #self.total_temp += temperature
                #self.total_humidity += humidity
                print("temperature : ", temperature, ", humidity : ", humidity)
            else:
                # Print values and error #
                print("wrong")
                print("temperature : ", temperature, ", humidity : ", humidity, " check : ", check, " tmp : ", tmp)

        # Make sure at least one reading was valid #
        #if self.valid_count == 0:
            #self.__read_sensor__()  # If not, try again

        # Get the average verified values for accuracy #
        #temperature = self.total_temp / self.valid_count
        #humidity = self.total_humidity / self.valid_count

        return temperature, humidity
