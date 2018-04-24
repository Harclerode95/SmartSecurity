#####################################################################
# SmartSecurity Embedded System Software                            #
# Team: SmartSecurity                                               #
# Tyler Harclerode, Brandon Lin, Zachary Davoli, Jonathan Griffin   #
# CET/CSC Senior Project 2017/2018                                  #
#####################################################################

# !/usr/bin/python          # Script in Python interpreter
import RPi.GPIO as GPIO     # For Raspberry Pi GPIO utilization
import time
import picamera             # Python camera library
import os                   # for sys.exit()

#  Import project specific files #
import LCD_Display          # Printing to LCD
import Matrix_Keypad        # Handing the keypad IO
import DHT11                # Temperature and humidity sensor
import PIR                  # Pyroelectric Infrared Motion Detector
import LEDs                 # LEDs for status and alert
import CO_Sensor            # Carbon Monoxide sensor
import alarm                # Alarm buzzer

#####################################################################

#  Class Instantiations  #
lcd = LCD_Display.AdafruitCharLCD()     # LCD
kp = Matrix_Keypad.Keypad()             # Keypad
pir = PIR.PIR()                         # Motion Detector
led = LEDs.LED()                        # Status/Alert LEDs
cam = picamera.Picamera()               # Video Camera
co = CO_Sensor.COSensor()               # Carbon Monoxide Sensor
alm = alarm.Alarm()                     # Alarm buzzer

# Constants #
NULL_PIN = [0,0,0,0]
DIGITS = [0,1,2,3,4,5,6,7,8,9]
DISABLED = "DISABLED"
ENABLED = "ENABLED"
FAHRENHEIT = "FAHRENHEIT"
CELSIUS = "CELSIUS"


def __main__():

    # Setup LEDs [turns on power LED too] #
    led.__init__()

    # Display Greeting #
    lcd.__init__()
    lcd.__message__("Welcome! \nPowering up...")
    print("Welcome! Powering up...")
    time.sleep(1)

    # Setup keypad for PIN entry #
    kp.__init__()

    # Check user activation #
    if __check_user_activation__():
        # If activated, have user enter PIN to verify #
        for attempts in range(1,6):                     # user has 5 attempts to input PIN
            pin = __get_pin__()
            if __test_pin__(pin):                       # break out if verified PIN
                break
            else:                                       # update user on remaining attempts
                lcd.__clear__()
                lcd.__message__("Incorrect PIN\n" + 5 - attempts + "tries left.")
                print("Incorrect PIN, please try again." + 5 - attempts + "attempts left.")
                # If user has tried 5 times and failed, have them enter a new PIN #
                if attempts == 5:
                    lcd.__clear__()
                    lcd.__message__("Max attempts.\nEnter new PIN.")
                    print("Max attempts reached. Enter a new PIN")
                    time.sleep(1)
                    pin = __new_user_pin__()
                    __write_pin_to_file__(pin)
                    break
                continue
    else:
        # No saved user PIN, set up the new user #
        pin = __new_user_pin__()
        __write_pin_to_file__(pin)

    # Let's set the user conditions up #
    security_state = __get_security_state__()           # security system enabled?
    if security_state == ENABLED:
        led.__turn_on_alarm_g_led__()                   # turn on enabled security LED

    time.sleep(1)

    if not __get_temp_scale_from_file__():              # user doesn't have previously saved temperature scale
        temp_scale = __get_temp_scale__()               # fahrenheit or celsius?
        __write_temp_scale_to_file__(temp_scale)        # store temperature scale
    elif FAHRENHEIT == __get_temp_scale_from_file__():  # fahrenheit already selected
        temp_scale = FAHRENHEIT
    elif CELSIUS == __get_temp_scale_from_file__():     # celsius already selected
        temp_scale = CELSIUS

    time.sleep(0.5)
    min_temp = __get_min_safe_temp__()                  # lowest acceptable temperature?
    time.sleep(1)
    max_temp = __get_max_safe_temp__()                  # highest acceptable temperature?
    time.sleep(1)
    min_hum = __get_min_safe_humidity__()               # lowest acceptable humidity?
    time.sleep(1)
    max_hum = __get_max_safe_temp__()                   # highest acceptable humidity?

    temperature, humidity = DHT11.read_sensor()
    if temperature > max_temp:
        print("Dangerously high temperature levels.")

    motion_detected = False  # make sure system doesn't immediately set alarm

    # Infinite loop for embedded system software #
    while True:

        # Check for motion detection
        if motion_detected:
            # Save camera snapshot #
            led.__turn_on_alarm_y_led__()               # yellow LED indicated detected motion
            # Get response from keypad
            # Get response from app

        if __check_for_power_off__():
            # Cleanup resources when done #
            __power_off__()


def __check_user_activation__():

    # Attempt to read PIN from file #
    try:
        pin = __get_pin_from_file__()
        if pin == NULL_PIN:                     # no saved PIN means no active user
            return False                        # 0 means device not user activated
        else:
            return True                         # PIN must previously have been entered, so user activated
    except Exception as err:                    # catch any errors like IOError
        lcd.__clear__()
        lcd.__message__("Error.")
        time.sleep(1)
        print(err)
        return False                            # disable loop by just requesting new pin


def __get_pin__():

    # Instruct the user #
    lcd.__clear__()
    lcd.__message__("Enter your 4\ndigit PIN.")
    print("Enter your 4-digit PIN.")
    time.sleep(0.5)

    # Ensure a valid 4-digit PIN is entered #
    key_list = [0] * 4
    for i in key_list:
        valid_pin = False
        while not valid_pin:
            key = kp.__get_key__()                  # check pressed key
            time.sleep(0.1)
            if key in DIGITS:                       # is it numeric? (must be)
                if i == 0:
                    lcd.__message__("PIN: ")        # start displaying pin when first key pressed
                    print("PIN: ")
                key_list[i] = key                   # store in temporary key list for pin
                lcd.__message__(key)                # if it's a number, add to display as well
                print(key)
                valid_pin = True
            else:
                print("Non-numeric entry, try again.")

    time.sleep(1)                                   # give user time to read PIN
    return key_list


def __new_user_pin__():

    # Instruct the user #
    lcd.__clear__()
    lcd.__message__("Let's get your\n account setup!")
    print("Let's get your account setup!")
    time.sleep(1.5)

    # Repeat until we have a valid, confirmed PIN #
    confirmed = False
    while not confirmed:

        # Read new PIN from keypad
        new_pin = __get_pin__()

        # Prompt user to reenter PIN for confirmation #
        lcd.__clear__()
        lcd.__message__("Verify PIN")
        print("Please verify PIN.")

        # Confirm user PIN with reentry #
        test_pin = __get_pin__()
        for i in test_pin:
            if new_pin[i] == test_pin[i]:
                if i == 3:
                    confirmed = True
            else:
                time.sleep(0.5)             # make sure user has time to read entered PIN
                lcd.__clear__()
                lcd.__message__("Couldn't confirm\n try again")
                print("Could not confirm PIN, try again.")

    return new_pin


def __test_pin__(pin_t):
    # Compare entered PIN from read_keypad() to saved PIN
    pin_f = open('pincode.txt', 'r')
    test = list(pin_f.read(4))                  # check the PIN file

    if pin_t != test:
        lcd.__clear__()
        lcd.__message__("Invalid PIN \n Please try again.")
        print('Invalid PIN. Please try again')
        return False
    else:
        lcd.__clear__()
        lcd.__message__("Login successful")
        print("Login successful")
        return True


def __get_pin_from_file__():
    file_pin = [0] * 4
    try:
        pf = open('pin_code.txt', 'r')          # open the PIN file
        file_pin = list(pf.read(4))             # PIN always saved as only line
        pf.close()
    except Exception as err:
        lcd.__clear__()
        lcd.__message__("Error.")
        time.sleep(1)
        print(err)

    return file_pin


def __write_pin_to_file__(pin):
    try:
        pf = open('pincode.txt', 'w')
        pin = str(pin)
        pf.write(pin)
        pf.close()
    except Exception as err:
        print(err)


def __get_security_state__():

    # Instruct the user #
    lcd.__clear__()
    lcd.__message__("Press 1 for\nactive security.")
    time.sleep(1)
    lcd.__clear__()
    lcd.__message__("Press 0 for\ninactive.")
    print("Please use the keypad to enter the desired security state.")
    print("0 = inactive, 1 = active\nYou entered: ", end = '')           # 2 will mean triggered, 3 will mean alarmed

    # User enters state through keypad #
    state_key = kp.__get_key__()
    print(state_key)

    # Only 0 or 1 are accepted answers
    if state_key == 0:
        print("Security: DISABLED")
        lcd.__clear__()
        lcd.__message__("Security\n" + DISABLED)
        return DISABLED
    elif state_key == 1:
        print("Security: ENABLED")
        lcd.__clear__()
        lcd.__message__("Security\n" + ENABLED)
        return ENABLED
    else:                                       # repeat until valid entry
        lcd.__clear__()
        lcd.__message__("0 or 1 only.")
        print("Enter only a 0 or 1.")
        time.sleep(1)
        __get_security_state__()


def __get_temp_scale__():

    # Instruct user #
    lcd.__clear__()
    lcd.__message__("Select desired\ntemp. scale.")
    print("Select desired\ntemp. scale.")
    time.sleep(1.2)
    lcd.__clear__()
    lcd.__message__("A: Fahrenheit\nB: Celsius")
    print("A: Fahrenheit\nB: Celsius")

    # User enters desired temperature scale from keypad #
    scale = kp.__get_key__()
    while scale not in ('A', 'B'):          # repeat until valid entry
        print("Invalid entry. Please enter in A for Fahrenheit, or B for Celsius")
        scale = kp.__get_key__()

    # Save to file and return #
    if scale == 'A':
        print("Temperature will be in Fahrenheit.")
        lcd.__clear__()
        lcd.__message__("Temperature now\nFahrenheit.")
        __write_temp_scale_to_file__(FAHRENHEIT)
        return FAHRENHEIT
    elif scale == 'B':
        print("Temperature will be in Celsius.")
        lcd.__clear__()
        lcd.__message__("Temperature now\nCelsius.")
        __write_temp_scale_to_file__(CELSIUS)
        return CELSIUS


def __get_temp_scale_from_file__():
    tcf = open('temp_scale.txt','r')
    t_scale = tcf.read(1)               # read first character to tell scale
    if t_scale == 'E':                  # temp_scale txt file must be holding "EMPTY"
        tcf.close()
        return False
    elif t_scale == 'F':                # fahrenheit is stored as temperature scale
        tcf.close()
        return FAHRENHEIT
    elif t_scale == 'C':                # celsius is stored as temperature scale
        tcf.close()
        return CELSIUS
    else:
        tcf.close()
        return False                    # if nothing useful found, we don't have saved temperature scale


def __write_temp_scale_to_file__(tmp_scale):

    try:
        tcf = open('temp_scale.txt', 'w')
        tcf.write(tmp_scale)
        tcf.close()
        return True
    except Exception as err:
        print(err)


def __get_min_safe_temp__():

    # Instruct user #
    lcd.__clear__()
    lcd.__message__("Please enter \nmin. safe temp.")
    print('Please enter minimum safe temperature.')

    # Grab tens value #
    key_is_numeric = False
    tens = 0
    while not key_is_numeric:
        num_key = kp.__get_key__()          # check pressed key
        time.sleep(0.1)
        if num_key in DIGITS:               # is it numeric? (must be)
            tens = num_key
            lcd.__clear__()
            lcd.__message__("Min safe temp:\n" + num_key)  # if it's a number, add to display
            print("Minimum safe temperature: " + num_key, end = '')
            key_is_numeric = True
        else:
            print("Non-numeric entry, try again.")

    # Grab ones value #
    key_is_numeric = False
    ones = 0
    while not key_is_numeric:
        num_key = kp.__get_key__()  # check pressed key
        time.sleep(0.1)
        if num_key in DIGITS:  # is it numeric? (must be)
            ones = num_key
            lcd.__clear__()
            lcd.__message__(num_key)  # if it's a number, add to display
            print(num_key)
            key_is_numeric = True
        else:
            print("Non-numeric entry, try again.")

    min_safe_temp = tens * 10 + ones
    print("Minimum safe temperature set to: " + min_safe_temp)
    return min_safe_temp


def __get_max_safe_temp__():

    # Instruct user #
    lcd.__clear__()
    lcd.__message__("Please enter \nmax. safe temp.")
    print('Please enter maximum safe temperature.')

    # Grab tens value #
    key_is_numeric = False
    tens = 0
    while not key_is_numeric:
        num_key = kp.__get_key__()  # check pressed key
        time.sleep(0.1)
        if num_key in DIGITS:  # is it numeric? (must be)
            tens = num_key
            lcd.__clear__()
            lcd.__message__("Max safe temp:\n" + num_key)  # if it's a number, add to display
            print("Maximum safe temperature: " + num_key, end = '')
            key_is_numeric = True
        else:
            print("Non-numeric entry, try again.")

    # Grab ones value #
    key_is_numeric = False
    ones = 0
    while not key_is_numeric:
        num_key = kp.__get_key__()  # check pressed key
        time.sleep(0.1)
        if num_key in DIGITS:  # is it numeric? (must be)
            ones = num_key
            lcd.__clear__()
            lcd.__message__(num_key)  # if it's a number, add to display
            print(num_key)
            key_is_numeric = True
        else:
            print("Non-numeric entry, try again.")

    max_safe_temp = tens * 10 + ones
    print("Maximum safe temperature set to: " + max_safe_temp)
    return max_safe_temp


def __get_min_safe_humidity__():

    # Instruct user #
    lcd.__clear__()
    lcd.__message__("Please enter \nmin. safe hum.")
    print('Please enter minimum safe humidity.')

    # Grab tens value #
    key_is_numeric = False
    tens = 0
    while not key_is_numeric:
        num_key = kp.__get_key__()  # check pressed key
        time.sleep(0.1)
        if num_key in DIGITS:  # is it numeric? (must be)
            tens = num_key
            lcd.__clear__()
            lcd.__message__("Min safe hum.:\n" + num_key)  # if it's a number, add to display
            print("Minimum safe humidity: " + num_key, end = '')
            key_is_numeric = True
        else:
            print("Non-numeric entry, try again.")

    # Grab ones value #
    key_is_numeric = False
    ones = 0
    while not key_is_numeric:
        num_key = kp.__get_key__()  # check pressed key
        time.sleep(0.1)
        if num_key in DIGITS:  # is it numeric? (must be)
            ones = num_key
            lcd.__clear__()
            lcd.__message__(num_key)  # if it's a number, add to display
            print(num_key)
            key_is_numeric = True
        else:
            print("Non-numeric entry, try again.")

    min_safe_hum = tens * 10 + ones
    return min_safe_hum


def __get_max_safe_humidity__():

    # Instruct user #
    lcd.__clear__()
    lcd.__message__("Please enter \nmax. safe hum.")
    print('Please enter maximum safe humidity.')

    # Grab tens value #
    key_is_numeric = False
    tens = 0
    while not key_is_numeric:
        num_key = kp.__get_key__()  # check pressed key
        time.sleep(0.1)
        if num_key in DIGITS:  # is it numeric? (must be)
            tens = num_key
            lcd.__clear__()
            lcd.__message__("Max safe hum.:\n" + num_key)  # if it's a number, add to display
            print("Maximum safe humidity: " + num_key, end = '')
            key_is_numeric = True
        else:
            print("Non-numeric entry, try again.")

    # Grab ones value #
    key_is_numeric = False
    ones = 0
    while not key_is_numeric:
        num_key = kp.__get_key__()  # check pressed key
        time.sleep(0.1)
        if num_key in DIGITS:  # is it numeric? (must be)
            ones = num_key
            lcd.__clear__()
            lcd.__message__(num_key)  # if it's a number, add to display
            print(num_key)
            key_is_numeric = True
        else:
            print("Non-numeric entry, try again.")

    max_safe_hum = tens * 10 + ones
    return max_safe_hum


def __check_for_power_off__():

    # User holds star key for 3 seconds #
    power_key = ['*', '*', '*']
    for i in power_key:
        if not power_key[i] == kp.__get_key__():    # if at any time they aren't holding '*', don't turn off
            return False
        else:
            if i == 2:                              # are we at 3 seconds?
                return True                         # if so, safely turn off device
            time.sleep(1)                           # otherwise continue scanning


def __power_off__():

    # Clean up the GPIO resources #
    GPIO.cleanup()

    # Handle what else needs done #


    # System exit
    sys.exit()