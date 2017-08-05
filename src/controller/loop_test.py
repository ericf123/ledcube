import cubestate
import serial
import numpy as np
from time import sleep
DELAY = .25
cs = cubestate.CubeState(DELAY, '/dev/ttyUSB0')

while True:
    for z in range(0, 4):
        leds = []
        for x in range(0,4):
            for y in range(0,4):
                leds.append((x,y,z))
        cs.update(pos_list=leds)
        cs.send()
        sleep(DELAY)
        
