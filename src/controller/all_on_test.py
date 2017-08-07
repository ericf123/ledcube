import cubestate
import serial
import numpy as np
cs = cubestate.CubeState(1, '/dev/cu.SLAB_USBtoUART')

leds = []
for x in range(0,4):
    for y in range(0,4):
        for z in range(0,4):
            leds.append((x,y,z))
cs.update(pos_list=leds)
input()
print(cs.send())
input()
