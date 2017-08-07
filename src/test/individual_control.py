import cubestate
import serial
import numpy as np
cs = cubestate.CubeState(1, '/dev/cu.SLAB_USBtoUART')

while True:
    x = int(input("x: "))
    y = int(input("y: "))
    z = int(input("z: "))
    cs.update(x,y,z)
    print(cs.send())
