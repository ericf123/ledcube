import serial
import cubestate
import numpy as np
s = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)
cs = cubestate.CubeState(1)

while True:
    x = int(input("x: "))
    y = int(input("y: "))
    z = int(input("z: "))
    cs.update(x,y,z)
    to_send = cs.send()
    if to_send is not None:
        print(to_send)
        s.write(to_send)
    cs.update(-1,-1,-1)
