import cubestate
import serial
import numpy as np
from random import randint
from time import sleep
DELAY = .1
cs = cubestate.CubeState(DELAY, '/dev/cu.SLAB_USBtoUART')


while True:
    num_drops = 10
    drop_coords = []
    for i in range(0, num_drops):
        x = randint(0, 3)
        y = randint(0, 3)
        drop_coords.append((x,y))

    for z in range(0, 4):
            led_list =[(drop_coords[i][0], drop_coords[i][1], 3-z) for i in range(0, num_drops)]
            cs.update(pos_list=led_list)
            cs.send();
            sleep(DELAY)


