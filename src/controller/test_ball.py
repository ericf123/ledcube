import cubestate
import serial
import numpy as np
from random import randint
from time import sleep
DELAY = .01
cs = cubestate.CubeState(DELAY, '/dev/cu.SLAB_USBtoUART')

runs = 0
while True:
    if (runs % 4 == 0):
        x = randint(0,3)
        y = randint(0,3)
        z = 3 

    cs.update(x,y,z)
    cs.send()

    x += 1
    y += 1 
    z += 1

    x = x % 4
    y = y % 4
    z = z % 4
    sleep(DELAY)
    runs += 1
