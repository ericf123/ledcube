import cubestate
import serial
import numpy as np
cs = cubestate.CubeState('/dev/cu.SLAB_USBtoUART', exp_time=1)

while True:
    x = int(input("x: "))
    y = int(input("y: "))
    z = int(input("z: "))
    cs.update(x,y,z)
    print(cs.send())
