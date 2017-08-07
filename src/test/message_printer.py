import cubestate

cs = cubestate.CubeState('/dev/cu.SLAB_USBtoUART', exp_time=-1)
input("press enter to start")
while True:
    cs.printf(input("enter message: "), .25, z_planes=[3])
