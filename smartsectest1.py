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
import LCD_Display           # Printing to LCD
import MatrixKeypad         # Handing the keypad IO
import DHT11                # Temperature and humidity sensor
import PIR                  # Pyroelectric Infrared Motion Detector
import LEDs                 # LEDs for status and alert
import Alarm                # Alarm (buzzer/LED)
#import CO_Sensor            # Carbon Monoxide detection

#####################################################################
#dht = DHT11.DHT11Sensor()
#  Class Instantiations  #
lcd = LCD_Display.AdafruitCharLCD()     # LCD
#kp = MatrixKeypad.Keypad()              # Keypad
#pir = PIR.PIR()                         # Motion Detector
   # dht = DHT11.DHT11()                     # Temperature and humidity sensor
#led = LEDs.LED()                        # Status/Alert LEDs
#alarm = Alarm.Alarm()                   # Alarm (buzzer)
#co = CO_Sensor.COSensor()               # Carbon Monoxide Sensor
def main():

    

    #dht_test()

    #__pir_test__()

    __lcd_test__()

    #keypad_test()

    #led_test()

    #__co_test__()

    #__alarm_test__()


    #__destroy__()

    print("end main")


# Cleanup resources #
def __destroy__():
    GPIO.cleanup()


"""
def __co_test__():
    print('CO test')
    co.__init__()
    print('CO test end')


def led_test():
    print('LED test')
    led.__setup_pwr_led__()
    for i in range(3):
        led.__turn_on_pwr_led__()
    print('LED test end')
"""

def __lcd_test__():
    print('LCD test')
    lcd.__init__()
    lcd.message('TEST')
    time.sleep(5)
    print('LCD test end')

"""
def __alarm_test__():
    print('Alarm test')
    alarm.__init__()
    alarm.__buzzer_loop__()
    alarm.__kill_alarm__()
    print('Alarm test end')
"""
'''
def keypad_test():
    print('Keypad test: Press key')
    kp.__init__()
    pressed_key = kp.__get_key__()
    print(pressed_key)
    kp.exit()
    print('Keypad test end')


def dht_test():
    print('DHT11 TEST:')
    #dht.__init__()
    dht.__read_sensor__()
    print('DHT test end')
  

def __pir_test__():
    print('PIR test')
    pir.__init__()
    pir.pir_test()
    print('PIR test end')
''' 

main()
