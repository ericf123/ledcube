import cubestate
import serial
import numpy as np
from time import sleep
import alphanumeric
DELAY = .5
cs = cubestate.CubeState('/dev/cu.SLAB_USBtoUART', exp_time=-1) 
A_PATTERN = alphanumeric.A_COORDS

N_PATTERN = [(0,0), (1,0), (2,0), (3,0), (1,1), (2,2), (3,3), (0,3), (1,3), (2,3)]
O_PATTERN = [(0,0), (1,0), (2,0), (3,0), (3,1), (3,2), (3,3), (2,3), (1,3), (0,3), (0,2), (0,1)]

def send_letter(letter_2d):
    letter_3d = []
    for z in range(0,4):
        for i in range(len(letter_2d)):
            x,y = letter_2d[i]
            letter_3d.append((x,y,0))
            cs.update(pos_list=letter_3d)
        cs.send()
        sleep(DELAY)

input("press enter to start")
while True:
    send_letter(A_PATTERN)
    #sleep(DELAY)
    send_letter(A_PATTERN)
    #sleep(DELAY)
