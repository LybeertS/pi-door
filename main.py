#!/usr/bin/env python3
import evdev
from evdev import ecodes

#Constants
KEY_PRESSED = 1
KEY_RELEASED = 0

#Variables
pressed = []
keys_num = [
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
keys_alt = [
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
code = [1, 2, 7, 8]
code_num = [ecodes.KEY_KP1, ecodes.KEY_KP2, ecodes.KEY_KP7, ecodes.KEY_KP8]
code_alt= [ecodes.KEY_END, ecodes.KEY_DOWN, ecodes.KEY_HOME, ecodes.KEY_UP]

#Startup debug info
devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
for device in devices:
    print(device.fn, device.name, device.phys)

device = evdev.InputDevice('/dev/input/event0')
print(device)

#Actual reading loop
print("Reading input")
for event in device.read_loop():
    if event.type == ecodes.EV_KEY and event.value == KEY_PRESSED:
        #print(evdev.categorize(event))
        if event.code in keys_num + keys_alt:
            #print("Number pressed")
            pressed.append(event.code)
        elif event.code == ecodes.KEY_KPENTER:
            if (pressed == code_num) or (pressed == code_alt):
                print("*** CODE OK, DOOR WILL OPEN ***")
            else:
                print("Wrong code entered")
            pressed.clear()
