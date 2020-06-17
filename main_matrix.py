#!/usr/bin/env python3
import RPi.GPIO as GPIO
import keypad_matrix_io
import pifacerelayplus
from time import sleep
import logging

#import ptvsd
#ptvsd.enable_attach("pidoor", address = ('pi-door.local', 3000))

# Enable the line of source code below only if you want the application to wait until the debugger has attached to it
#ptvsd.wait_for_attach()

GPIO.setwarnings(False)

logging.basicConfig(filename='events_matrix.log', format='[%(levelname)s]\t[%(asctime)s]\t%(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)

#Constants
DELAY_KEYPRESS = 0.1
DELAY_PULSE = 0.25

#Variables
pressed = []
attempts = 0

#OLD: replaced by key from file
#key = [1, 2, 7, 8]

#Get key from file 
with open('key', 'r') as file:
    key_str = file.readline().strip()
    key = [int(i) for i in list(key_str)]

def convertDigitsToString(buttons):
    numbers = ""
    for b in buttons:
        numbers += str(b)
    return numbers

kp = keypad_matrix_io.keypad()

relay = pifacerelayplus.PiFaceRelayPlus(pifacerelayplus.RELAY)

#Actual reading loop
print("Reading input")
while True:
    digit = kp.waitForKeyPress()
    sleep(DELAY_KEYPRESS)
    if digit != "#":
        #print("Number pressed")
        pressed.append(digit)
    else:
        if (pressed == key):
            info = "*** Correct code entered: DOOR OPENING ***"
            print(info)
            logging.info(info)
            relay.relays[0].set_high()
            sleep(DELAY_PULSE)
            relay.relays[0].set_low()
            attempts = 0
        else:
            pressed_str = convertDigitsToString(pressed)
            info = "Wrong code entered: " + str(pressed_str)
            print(info)
            logging.info(info)
            attempts += 1
            if attempts >= 5:
                text = "--- 5 wrong code entered, waiting for 5s ---"
                print(text)
                logging.info(text)
                sleep(5)
                attempts = 0
        pressed.clear()
