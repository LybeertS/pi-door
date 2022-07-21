#!/usr/bin/env python
import RPi.GPIO as GPIO
import keypad_matrix_io
import user_reader
import pifacerelayplus
import logging
from time import sleep

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

#Get users
reader = user_reader.UserReader('users')

#with open('key', 'r') as file:
#    key_str = file.readline().strip()
#    key = [int(i) for i in list(key_str)]

def convert_pressed_to_key(pressed):
    key = ""
    for b in pressed:
        key += str(b)
    return key

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
        pressed_key = convert_pressed_to_key(pressed)
        user = reader.get_user_with_key(pressed_key)
        if user:
            attempts = 0
            if reader.check_user_time_valid(user):
                info = "*** Correct code entered for user \"{}\": DOOR OPENING ***".format(user["name"])
                print(info)
                logging.info(info)
                relay.relays[0].set_high()
                sleep(DELAY_PULSE)
                relay.relays[0].set_low()
            else:
                info = "Correct code entered for user \"{}\", but invalid time".format(user["name"])
                print(info)
                logging.info(info)
        else:
            info = "Invalid code entered: " + str(pressed_key)
            print(info)
            logging.info(info)
            attempts += 1
            if attempts >= 5:
                text = "--- 5 invalid codes entered, waiting for 60s ---"
                print(text)
                logging.info(text)
                sleep(60)
                attempts = 0
        pressed.clear()
