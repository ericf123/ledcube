import cubestate
import serial
import numpy as np
cs = cubestate.CubeState(1, '/dev/ttyUSB1')

led_list = []
while True:
    x = int(input("x: "))
    y = int(input("y : "))
    z = int(input("z : "))
    led_list.append((x,y,z))
    cs.update(pos_list=led_list)
    print(cs.send())

