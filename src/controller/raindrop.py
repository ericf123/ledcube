import cubestate
from random import randint
from time import sleep

def run(cs, delay):
    pattern = gen_random_top_z()
    while True:
        cs.update(coords=pattern)
        cs.send()
        pattern = shift_pattern_down(pattern)
        pattern.extend(gen_random_top_z())
        sleep(delay)

def gen_random_top_z():
    pattern = []
    for i in range(4):
        new_coord = (randint(0,3), randint(0,3), 3)
        while new_coord in pattern: 
            new_coord = (randint(0,3), randint(0,3), 3)
        pattern.append(new_coord)
    return pattern
        
def shift_pattern_down(pattern):
    shifted_pattern = []
    for coord in pattern:
        x,y,z = coord
        z -= 1
        if z >= 0:
            shifted_pattern.append((x,y,z))
    return shifted_pattern

if __name__ == '__main__':
    cs = cubestate.CubeState('/dev/cu.SLAB_USBtoUART', exp_time=-1)
    run(cs, .15)


