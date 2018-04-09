# the sensor has to be connected to pin 1 for power, pin 6 for ground
# and pin 7 for signal(board numbering!).
 
import time, sys
import RPi.GPIO as GPIO


class COSensor:
    CO_PIN = 40     # Needs valid pin

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.CO_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.CO_PIN, GPIO.RISING)
        GPIO.add_event_callback(self.CO_PIN, action)

    def __action__(self, pin):              # Parameters?
        print('Sensor detected action!')
        return

    try:
        while True:
            print('alive')
            time.sleep(0.5)
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit()
