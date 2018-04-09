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
stepper = stepperMotor.StepperMotor()      # Stepper Motor
pir = PIR.PIR()                         # Motion Detector
dht = DHT11.DHT11()                     # Temperature and humidity sensor
led = LEDs.LED()                        # Status/Alert LEDs


def __main__():

    # Activate power LED #
    led.__setup_pwr_led__()
    led.__turn_on_pwr_led__()

    # Setup LCD screen #
    lcd.__init__()

    # lcd.home()                        # do we need this? Find out during testing

    # Display Greeting #
    lcd_string = "Welcome... \nPowering up..."     # Welcome on top row, Powering on second
    lcd.message(lcd_string)
    print('Welcome! Powering up...')

    # Check user activation #
    kp.__init__()
    try:    # Retrieve saved PIN if present #
        pin = __get_pin_from_file__()
        while pin == [0, 0, 0, 0]:                  # no saved PIN means no active user
            pin = __new_user_pin__()                # go get new PIN
    except IOError as err:
        print(err)
    else:
        # Request user PIN when system activated #
        lcd_string = "Enter user PIN."
        lcd.message(lcd_string)
        print('Enter user PIN.')
        key_list = [0] * 4                          # used for testing inputted PIN

        for i in range(4):                         # 0,1,2,3
            key_list[i] = kp.__get_key__()
            time.sleep(0.2)

        pin = tuple(key_list)                       # copies list into PIN as immutable tuple
        __test_pin__(pin)                           # verifies matching PIN
        lcd_string = "Login successful"
        lcd.message(lcd_string)                     # confirm with user
        __write_pin_to_file__(pin)                  # write PIN to pin_file

    # Let's get the desired security state #
    lcd_string = 'Please enter \nsecurity state'
    lcd.message(lcd_string)
    print('Please use the keypad to enter the desired security state.')
    print('0 = inactive, 1 = active')  # 2 will mean triggered, 3 will mean alarmed
    security_state = __get_security_state__()

    # Set the boundary values (min/max temp,humidity, etc) in Fahrenheit
    lcd_string = 'Please enter \nmin. safe temp'
    lcd.message(lcd_string)
    print('Please enter minimum safe temperature')
    min_temp = __get_min_safe_temp__()

    # Maximum acceptable temperature #
    lcd_string = 'Please enter \nmax. safe temp'
    lcd.message(lcd_string)
    print('Please enter maximum safe temperature')
    max_temp = __get_max_safe_temp__()


    # Minimum acceptable humidity #
    lcd_string = 'Please enter \nmin humidity.'
    lcd.message(lcd_string)
    print('Please enter minimum safe humidity')
    min_hum = __get_min_safe_humidity__()

    # Maximum acceptable humidity #
    lcd_string = 'Please enter \nmax humidity'
    lcd.message(lcd_string)
    print('Please enter maximum safe humidity')
    max_hum = __get_max_safe_temp__()

    # Use interrupts from motion detection
    motion_detected = False                     # motion detected boolean for interrupt handling
    while not motion_detected:
        print('ok')

    # Cleanup resources when done #
    GPIO.cleanup()


#  Get new user PIN  #
def __new_user_pin__():
    lcd_string = "Let's get your\n account setup!"
    lcd.message(lcd_string)
    time.sleep(2)                       # wait 2 seconds
    lcd_string = "To begin, enter\n a 4-digit PIN."
    lcd.message(lcd_string)
    time.sleep(0.5)
    print('Enter a 4-digit PIN to begin.')

    new_pin = [0] * 4
    for i in range(4):                  # 0-3 for 4-digit PIN
        new_pin[i] = kp.__get_key__()
        time.sleep(0.1)                 # handle bounce

    lcd_string = "Verify PIN"
    lcd.message(lcd_string)
    print('Please verify PIN.')
    time.sleep(0.5)

    # Verify user PIN with reentry
    test_pin = [0] * 4
    for i in range(4):
        test_pin[i] = kp.__get_key__()
        time.sleep(0.1)                 # handle bounce

    # Confirm verified PIN #
    for i in range(4):
        if new_pin[i] == test_pin[i]:
            continue
        else:
            lcd_string = "Couldn't confirm\n try again"
            lcd.message(lcd_string)
            print('Could not confirm PIN, try again.')
            __new_user_pin__()

    return new_pin


# Test entered PIN against saved PIN in file #
def __test_pin__(pin_t):
    # Compare entered PIN from read_keypad() to saved PIN
    pin_flag = False
    attempts = 5                        # 5 tries max to avoid hacking
    pin_f = open('pincode.txt', 'r')
    test = pin_f.read()                 # check the PIN file

    if pin_t != test:
        attempts -= 1
        while attempts >= 0:
            print('Invalid PIN. Please try again, ', attempts, 'tries left.')
            lcd_string = "Invalid PIN \n Please try again."
            lcd.message(lcd_string)
    else:
        pin_flag = True                 # boolean for PIN confirmation

    return pin_flag


# Retrieve saved user PIN from file #
def __get_pin_from_file__():
    pin = [0] * 4
    pf = open('pin_code.txt', 'r')
    try:
        for i in range(4):
            digit = pf.readline()
            digit.rstrip('\n')
            pin[i] = digit
    except Exception as err:
        print(err)

    return pin


# Write the user PIN to file #
def __write_pin_to_file__(pin):
    pf = open('pincode.txt', 'w')
    for i in range(4):
        pf.write(pin[i] + '\n')


# Retrieve desired security state from user #
def __get_security_state__():
    security_state = kp.__get_key__()
    # Only 0 or 1 are accepted answers
    if security_state == 0:
        return security_state
    elif security_state == 1:
        return security_state
    else:
        __get_security_state__()


# Retrieve the user specified minimum safe temperature #
def __get_min_safe_temp__():
    min_safe_temp = 0
    tens = 0
    ones = 0

    # Grab tens value #
    tmp = kp.__get_key__()
    if 0 <= tmp <=9:        # only accept 0-9
        tens = tmp
        time.sleep(0.3)     # handle bounce
    else:
        lcd_string = "Please only \nenter digits 0-9"
        lcd.message(lcd_string)
        print('Make sure you only enter number inputs 0-9')
        __get_min_safe_temp__()

    # Grab ones value #
    tmp = kp.__get_key__()
    if 0 <= tmp <= 9:  # only accept 0-9
        ones = tmp
        time.sleep(0.3)
    else:
        lcd_string = "Please only \nenter digits 0-9"
        lcd.message(lcd_string)
        print('Make sure you only enter number inputs 0-9')
        __get_min_safe_temp__()

    min_st = tens * 10
    min_safe_temp = min_st + ones

    return min_safe_temp


def __get_max_safe_temp__():
    max_safe_temp = 0
    tens = 0
    ones = 0

    # Grab tens value #
    tmp = kp.__get_key__()
    if 0 <= tmp <= 9:  # only accept 0-9
        tens = tmp
        time.sleep(0.3)  # handle bounce
    else:
        lcd_string = "Please only \nenter digits 0-9"
        lcd.message(lcd_string)
        print('Make sure you only enter number inputs 0-9')
        __get_max_safe_temp__()

    # Grab ones value #
    tmp = kp.__get_key__()
    if 0 <= tmp <= 9:  # only accept 0-9
        ones = tmp
        time.sleep(0.3)
    else:
        lcd_string = "Please only \nenter digits 0-9"
        lcd.message(lcd_string)
        print('Make sure you only enter number inputs 0-9')
        __get_max_safe_temp__()

    max_st = tens * 10
    max_safe_temp = max_st + ones

    return max_safe_temp


def __get_min_safe_humidity__():
    min_safe_hum = 0
    tens = 0
    ones = 0

    # Grab tens value #
    tmp = kp.__get_key__()
    if 0 <= tmp <= 9:  # only accept 0-9
        tens = tmp
        time.sleep(0.3)  # handle bounce
    else:
        lcd_string = "Please only \nenter digits 0-9"
        lcd.message(lcd_string)
        print('Make sure you only enter number inputs 0-9')
        __get_min_safe_humidity__()

    # Grab ones value #
    tmp = kp.__get_key__()
    if 0 <= tmp <= 9:  # only accept 0-9
        ones = tmp
        time.sleep(0.3)
    else:
        lcd_string = "Please only \nenter digits 0-9"
        lcd.message(lcd_string)
        print('Make sure you only enter number inputs 0-9')
        __get_min_safe_humidity__()

    min_sh = tens * 10
    min_safe_hum = min_sh + ones
    return min_safe_hum


def __get_max_safe_humidity__():
    max_safe_hum = 0
    tens = 0
    ones = 0

    # Grab tens value #
    tmp = kp.__get_key__()
    if 0 <= tmp <= 9:  # only accept 0-9
        tens = tmp
        time.sleep(0.3)  # handle bounce
    else:
        lcd_string = "Please only \nenter digits 0-9"
        lcd.message(lcd_string)
        print('Make sure you only enter number inputs 0-9')
        __get_max_safe_humidity__()

    # Grab ones value #
    tmp = kp.__get_key__()
    if 0 <= tmp <= 9:  # only accept 0-9
        ones = tmp
        time.sleep(0.3)
    else:
        lcd_string = "Please only \nenter digits 0-9"
        lcd.message(lcd_string)
        print('Make sure you only enter number inputs 0-9')
        __get_max_safe_humidity__()

    max_sh = tens * 10
    max_safe_hum = max_sh + ones
    return max_safe_hum


# Cleanup resources #
def __destroy__():
    GPIO.cleanup()

