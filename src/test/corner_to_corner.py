import cubestate
import serial
import numpy as np
from time import sleep
DELAY = .1
cs = cubestate.CubeState('/dev/cu.SLAB_USBtoUART', exp_time=DELAY) 

input("press enter to start")
leds = [(0,0,0)]
cs.update(pos_list=leds)
cs.send()


def append_if_bounds(led_list, led_coords):
    x,y,z = led_coords
    if (x >= 0 and x < 4) and (y >= 0 and y < 4) and (z >= 0 and z < 4) and (led_coords not in led_list):
        led_list.append(led_coords)
direction = 0
while True:
    for led in list(leds):
        x,y,z = led
        if (x == 3 and y == 3 and z == 3 and direction % 2 == 0):
            leds = [(3,3,3)]
            direction += 1
            break
        elif (x == 0 and y == 0 and z == 0 and direction % 2 == 1):
            leds = [(0,0,0)]
            direction += 1
            break
        append_if_bounds(leds, (x, y+1, z))
        append_if_bounds(leds, (x, y, z+1))
        append_if_bounds(leds, (x+1, y, z))
        append_if_bounds(leds, (x, y-1, z))
        append_if_bounds(leds, (x, y, z-1))
        append_if_bounds(leds, (x-1, y, z))
    cs.update(pos_list=leds)
    cs.send()
    sleep(DELAY)
