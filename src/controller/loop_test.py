import cubestate
import serial
import numpy as np
from time import sleep
DELAY = .01
cs = cubestate.CubeState(16*DELAY, '/dev/cu.SLAB_USBtoUART')

while True:
    for z in range(0, 4):
        for x in range(0,4):
            for y in range(0,4):
                cs.update(x,y,z)
                cs.send()
                sleep(DELAY)
        
