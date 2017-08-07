import cubestate

cs = cubestate.CubeState('/dev/cu.SLAB_USBtoUART', exp_time=-1)
input()
while True:
    cs.printf("hello world", .5, z_planes=[3])
