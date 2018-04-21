import RPi.GPIO as GPIO
from RPLCD import CharLCD
import time
GPIO.setwarnings(False)
lcd = CharLCD(numbering_mode = GPIO.BOARD, cols = 16, rows = 2, pin_rs = 23, pin_e = 29, pins_data = [31,33,35,37])
'''
lcd.cols = 16
lcd.rows = 2
lcd.pin_rs = 23
lcd.pin_e = 29
lcd.pins_data = [31,33,35,37]
'''
lcd.write_string(u'test1')
time.sleep(1)
lcd.clear()
lcd.write_string(u'test2')
time.sleep(2)
#numbering_mode = GPIO.BOARD, cols = 16, rows = 2, pin_rs = 23, pin_e = 29, pins_data = [31,33,35,37]
