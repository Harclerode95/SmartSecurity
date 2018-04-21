#####################################################################
# SmartSecurity Core Python Program                                 #
# Team: SmartSecurity                                               #
# Tyler Harclerode, Brandon Lin, Zachary Davoli, Jonathan Griffin   #
# CET/CSC Senior Project 2017/2018                                  #
#####################################################################

# !/usr/bin/python           # Script in Python interpreter
import RPi.GPIO as GPIO     # For Raspberry Pi GPIO utilization
import time
from picamera import PiCamera

#  Import project specific files #
import LCD_Display           # Printing to LCD
import MatrixKeypad         # Handing the keypad IO
import DHT11                # Temperature and humidity sensor
import PIR                  # Pyroelectric Infrared Motion Detector
import LEDs                 # LEDs for status and alert
import Alarm                # Alarm (buzzer/LED)
import CO_Sensor            # Carbon Monoxide detection
####################################################################
#  Class Instantiations  #

kp = MatrixKeypad.keypad()              # Keypad
pir = PIR.PIR()                         # Motion Detector
#dht = DHT11.DHT11Sensor()                # Temperature and humidity sensor
led = LEDs.LED()                        # Status/Alert LEDs
#alarm = Alarm.Alarm()                   # Alarm (buzzer)
co = CO_Sensor.COSensor()               # Carbon Monoxide Sensor
lcd = LCD_Display.AdafruitCharLCD()


def main():

    #camera = PiCamera()

    #camera.start_preview()
    #sleep(10)
    #camera.stop_preview()
    
    DHT11.read_sensor() # works, just needs averaging to handle occassional misreading

    #__pir_test__()      # "functional" 

    #keypad_test()       # works fine

    #led_test()          # works

    #__lcd_test__()

    #lcd.message('LCD TEST')

    #time.sleep(1)

    #GPIO.cleanup(21)

    #__co_test__()

    #__alarm_test__()

    GPIO.cleanup()

    print("end main")


# Cleanup resources #
#def __destroy__():
    #GPIO.cleanup()


def __co_test__():
    print('CO test')
    co.__init__()
    print('CO test end')


def led_test():
    print('LED test')
    led.__setup_pwr_led__()
    led.__setup_network_led__()
    led.__setup_alarm_g_led__()
    led.__setup_alarm_y_led__()
    led.__setup_alarm_r_led__()
    for i in range(3):
        led.__turn_on_pwr_led__()
        led.__turn_on_network_led__()
        led.__turn_on_alarm_g_led__()
        led.__turn_on_alarm_y_led__()
        led.__turn_on_alarm_r_led__()
    print('LED test end')


def __lcd_test__():
    print('LCD test')
    lcd.__init__()
    lcd.__clear__()
    lcd.message('TEST')
    time.sleep(0.5)

    lcd.__clear__()
    lcd.message('TEST2')
    time.sleep(0.5)

    
    print('LCD test end')

def __alarm_test__():
    print('Alarm test')
    alarm.__init__()
    alarm.__buzzer_loop__()
    alarm.__kill_alarm__()
    print('Alarm test end')


def keypad_test():
    print('Keypad test: Press key')
    #kp.__init__()
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
 

main()
