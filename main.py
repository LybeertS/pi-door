#!/usr/bin/env python3
import evdev
import pifacerelayplus
from evdev import ecodes
from time import sleep
import logging
#from zenlog import logging

#import ptvsd
#ptvsd.enable_attach("pidoor", address = ('pi-door.local', 3000))

# Enable the line of source code below only if you want the application to wait until the debugger has attached to it
#ptvsd.wait_for_attach()

logging.basicConfig(filename='events.log', format='[%(levelname)s]\t[%(asctime)s]\t%(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)

#Constants
KEY_PRESSED = 1
KEY_RELEASED = 0

#Variables
pressed = []
btns_num = [
    ecodes.KEY_KP0,
    ecodes.KEY_KP1,
    ecodes.KEY_KP2,
    ecodes.KEY_KP3,
    ecodes.KEY_KP4,
    ecodes.KEY_KP5,
    ecodes.KEY_KP6,
    ecodes.KEY_KP7,
    ecodes.KEY_KP8,
    ecodes.KEY_KP9
    ]
btns_alt = [
    ecodes.KEY_INSERT,
    ecodes.KEY_END,
    ecodes.KEY_DOWN,
    ecodes.KEY_PAGEDOWN,
    ecodes.KEY_LEFT,
    0,
    ecodes.KEY_RIGHT,
    ecodes.KEY_HOME,
    ecodes.KEY_UP,
    ecodes.KEY_PAGEUP
    ]

DELAY = 3.0
DELAY_PULSE = 0.25

def convertButtonsToString(buttons):
    numbers = ""
    for b in buttons:
        for i in range(0, len(btns_alt)):
            if (b == btns_num[i]) or (b == btns_alt[i]):
                numbers += str(i)
    return numbers

#OLD: replaced by key from file
#key = [1, 2, 7, 8]

#Get key from file and convert to ecodes
with open('key', 'r') as file:
    key_str = file.readline().strip()
    key = [int(i) for i in list(key_str)]
key_num = [btns_num[i] for i in key]
key_alt = [btns_alt[i] for i in key]

#Startup debug info
devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
for device in devices:
    print(device.fn, device.name, device.phys)

device = evdev.InputDevice('/dev/input/event0')
print(device)

relay = pifacerelayplus.PiFaceRelayPlus(pifacerelayplus.RELAY)

#Actual reading loop
print("Reading input")
for event in device.read_loop():
    if event.type == ecodes.EV_KEY and event.value == KEY_PRESSED:
        #print(evdev.categorize(event))
        if event.code in btns_num + btns_alt:
            #print("Number pressed")
            pressed.append(event.code)
        elif event.code == ecodes.KEY_KPENTER:
            if (pressed == key_num) or (pressed == key_alt):
                print("*** CODE OK, DOOR WILL OPEN ***")
                logging.info("*** Correct code entered: DOOR OPENING ***")
                relay.relays[0].set_high()
                sleep(DELAY_PULSE)
                relay.relays[0].set_low()
            else:
                pressed_str = convertButtonsToString(pressed)
                print("Wrong code entered: " + pressed_str)
                logging.info("Wrong code entered: %s", pressed_str)
            pressed.clear()
