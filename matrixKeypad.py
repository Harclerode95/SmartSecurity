#!/usr/bin/env python
import RPi.GPIO as GPIO
import time


class Keypad:
    # CONSTANTS
    KEYPAD = [
        [1, 2, 3, "A"],
        [4, 5, 6, "B"],
        [7, 8, 9, "C"],
        ["*", 0, "#", "D"]
    ]

    ROW = [11, 12, 13, 15]
    COLUMN = [16, 18, 22, 7]

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        # Set all columns as output low
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.OUT)
            GPIO.output(self.COLUMN[j], GPIO.LOW)

        # Set all rows as input
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def __get_key__(self):
        # Scan rows for pushed key/button
        # A valid key press should set "rowVal"  between 0 and 3.
        row_val = -1
        for i in range(len(self.ROW)):
            tmp_read = GPIO.input(self.ROW[i])
            if tmp_read == 0:
                row_val = i

        # If rowVal is not 0 through 3 then no button was pressed and we can exit
        if row_val < 0 or row_val > 3:
            self.exit()
            return

        # Convert columns to input
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # Switch the i-th row found from scan to output
        GPIO.setup(self.ROW[row_val], GPIO.OUT)
        GPIO.output(self.ROW[row_val], GPIO.HIGH)

        # Scan columns for still-pushed key/button
        # A valid key press should set "colVal"  between 0 and 2.
        col_val = -1
        for j in range(len(self.COLUMN)):
            tmp_read = GPIO.input(self.COLUMN[j])
            if tmp_read == 1:
                col_val = j

        # if colVal is not 0 thru 2 then no button was pressed and we can exit
        if col_val < 0 or col_val > 3:
            self.exit()
            return

        # Return the value of the key pressed
        self.exit()
        return self.KEYPAD[row_val][col_val]

    def exit(self):
        # Reinitialize all rows and columns as input at exit
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)


if __name__ == '__main__':
    # Initialize the keypad class
    kp = Keypad()
    # Loop while waiting for a keypress
    while True:
        digit = None
        while not digit:
            digit = kp.__get_key__()
            # Print the result
        print(digit)
        time.sleep(0.5)