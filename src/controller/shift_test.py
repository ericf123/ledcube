import cubestate
import serial
import numpy as np
from time import sleep
cs = cubestate.CubeState(1, '/dev/ttyUSB1')

leds = []

for x in range(0,4):
    for y in range(0, 4):
        for z in range(0, 4):
            leds.append((x,y,z))
while True:
    cs.update(pos_list=leds)
    print(cs.send())
    input()
