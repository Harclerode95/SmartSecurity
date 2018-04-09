#!/usr/bin/python
import RPi.GPIO as GPIO
from time import sleep


class AdafruitCharLCD:
    # Commands
    LCD_CLEARDISPLAY = 0x01
    LCD_RETURNHOME = 0x02
    LCD_ENTRYMODESET = 0x04
    LCD_DISPLAYCONTROL = 0x08
    LCD_CURSORSHIFT = 0x10
    LCD_FUNCTIONSET = 0x20
    LCD_SETCGRAMADDR = 0x40
    LCD_SETDDRAMADDR = 0x80

    # Flags for display entry mode
    LCD_ENTRYRIGHT = 0x00
    LCD_ENTRYLEFT = 0x02
    LCD_ENTRYSHIFTINCREMENT = 0x01
    LCD_ENTRYSHIFTDECREMENT = 0x00

    # Flags for display on/off control
    LCD_DISPLAYON = 0x04
    LCD_DISPLAYOFF = 0x00
    LCD_CURSORON = 0x02
    LCD_CURSOROFF = 0x00
    LCD_BLINKON = 0x01
    LCD_BLINKOFF = 0x00

    # Flags for display/cursor shift
    LCD_DISPLAYMOVE = 0x08
    LCD_CURSORMOVE = 0x00
    LCD_MOVERIGHT = 0x04
    LCD_MOVELEFT = 0x00

    # Flags for function set
    LCD_8BITMODE = 0x10
    LCD_4BITMODE = 0x00
    LCD_2LINE = 0x08
    LCD_1LINE = 0x00
    LCD_5x10DOTS = 0x04
    LCD_5x8DOTS = 0x00

    PIN_RS = 23
    PIN_E = 29
    PINS_DB = [31, 33, 35, 37]

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PIN_E, GPIO.OUT)
        GPIO.setup(self.PIN_RS, GPIO.OUT)

        for pin in self.PINS_DB:
            GPIO.setup(pin, GPIO.OUT)

        self.__write_4_bits__(0x33)  # initialization
        self.__write_4_bits__(0x32)  # initialization
        self.__write_4_bits__(0x28)  # 2 line 5x7 matrix
        self.__write_4_bits__(0x0C)  # turn cursor off 0x0E to enable cursor
        self.__write_4_bits__(0x06)  # shift cursor right

        self.displaycontrol = self.LCD_DISPLAYON | self.LCD_CURSOROFF | self.LCD_BLINKOFF

        self.displayfunction = self.LCD_4BITMODE | self.LCD_1LINE | self.LCD_5x8DOTS
        self.displayfunction |= self.LCD_2LINE

        """ Initialize to default text direction (for romance languages) """
        self.displaymode = self.LCD_ENTRYLEFT | self.LCD_ENTRYSHIFTDECREMENT
        self.__write_4_bits__(self.LCD_ENTRYMODESET | self.displaymode)  # set the entry mode

        self.__clear__()

    def __begin__(self, lines):
        if lines > 1:
            self.num_lines = lines
            self.displayfunction |= self.LCD_2LINE
            self.current_line = 0

    def __home__(self):
        self.__write_4_bits__(self.LCD_RETURNHOME)  # set cursor position to zero
        __delay_microseconds__(3000)  # this command takes a long time!

    def __clear__(self):
        self.__write_4_bits__(self.LCD_CLEARDISPLAY)  # command to clear display
        __delay_microseconds__(3000)  # 3000 microsecond sleep, clearing the display takes a long time

    def __set_cursor__(self, col, row):
        self.row_offsets = [0x00, 0x40, 0x14, 0x54]

        if row > self.num_lines:
            row = self.num_lines - 1  # we count rows starting w/0

        self.__write_4_bits__(self.LCD_SETDDRAMADDR | (col + self.row_offsets[row]))

    def __no_display__(self):
        """ Turn the display off (quickly) """
        self.displaycontrol &= ~self.LCD_DISPLAYON
        self.__write_4_bits__(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def __display__(self):
        """ Turn the display on (quickly) """
        self.displaycontrol |= self.LCD_DISPLAYON
        self.__write_4_bits__(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def __no_cursor__(self):
        """ Turns the underline cursor on/off """
        self.displaycontrol &= ~self.LCD_CURSORON
        self.__write_4_bits__(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def __cursor__(self):
        """ Cursor On """
        self.displaycontrol |= self.LCD_CURSORON
        self.__write_4_bits__(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def __no_blink__(self):
        """ Turn on and off the blinking cursor """
        self.displaycontrol &= ~self.LCD_BLINKON
        self.__write_4_bits__(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def __display_left__(self):
        """ These commands scroll the display without changing the RAM """
        self.__write_4_bits__(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVELEFT)

    def __scroll_display_right__(self):
        """ These commands scroll the display without changing the RAM """
        self.__write_4_bits__(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVERIGHT)

    def __left_to_right__(self):
        """ This is for text that flows Left to Right """
        self.displaymode |= self.LCD_ENTRYLEFT
        self.__write_4_bits__(self.LCD_ENTRYMODESET | self.displaymode)

    def __right_to_left__(self):
        """ This is for text that flows Right to Left """
        self.displaymode &= ~self.LCD_ENTRYLEFT
        self.__write_4_bits__(self.LCD_ENTRYMODESET | self.displaymode)

    def __autoscroll__(self):
        """ This will 'right justify' text from the cursor """
        self.displaymode |= self.LCD_ENTRYSHIFTINCREMENT
        self.__write_4_bits__(self.LCD_ENTRYMODESET | self.displaymode)

    def __no_autoscroll__(self):
        """ This will 'left justify' text from the cursor """
        self.displaymode &= ~self.LCD_ENTRYSHIFTINCREMENT
        self.__write_4_bits__(self.LCD_ENTRYMODESET | self.displaymode)

    def __write_4_bits__(self, bits, char_mode=False):
        """ Send command to LCD """
        __delay_microseconds__(1000)  # 1000 microsecond sleep
        bits = bin(bits)[2:].zfill(8)
        GPIO.output(self.PIN_RS, char_mode)

        for pin in self.PINS_DB:
            GPIO.output(pin, False)

        for i in range(4):
            if bits[i] == "1":
                GPIO.output(self.PINS_DB[::-1][i], True)

        self.__pulse_enable__()

        for pin in self.PINS_DB:
            GPIO.output(pin, False)

        for i in range(4, 8):
            if bits[i] == "1":
                GPIO.output(self.PINS_DB[::-1][i - 4], True)

        self.__pulse_enable__()

    def __pulse_enable__(self):
        GPIO.output(self.PIN_E, False)
        __delay_microseconds__(1)  # 1 microsecond pause - enable pulse must be > 450ns
        GPIO.output(self.PIN_E, True)
        __delay_microseconds__(1)  # 1 microsecond pause - enable pulse must be > 450ns
        GPIO.output(self.PIN_E, False)
        __delay_microseconds__(1)  # commands need > 37us to settle

    def message(self, text):
        """ Send string to LCD. Newline wraps to second line"""

        for char in text:
            if char == '\n':
                self.__write_4_bits__(0xC0)  # next line
            else:
                self.__write_4_bits__(ord(char), True)


def __delay_microseconds__(microseconds):
    seconds = microseconds / float(1000000)  # divide microseconds by 1 million for seconds
    sleep(seconds)

