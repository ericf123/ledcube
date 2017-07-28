import numpy as np
from time import time

def bitset(x, y, z):
    """x,y,z: integer in [0,3] (cube coordinate)
       Returns a 64bit int with the correct index bit set.
       For example, (3, 3, 3) is led 64 (index 63), (3,0,0) is led 49 (index 48)."""
    return 1 << 16*x + 4*y + z #this is really sexy

def pack_bitset(bits):
    """Packs bits into a padded array of 8 bytes for sending to Arduino over serial.
       Byte ordering is big endian, i.e. MSB is index 0."""
    packed = np.empty(8, dtype=np.uint8)
    for i in range(0,8):
        #current_byte is 8 ones shifted to match position in bitset 
        #anded with the bitset, and shifted right to be only 8 bits
        current_byte = (bits & 0xFF << 8*(7-i)) >> 8*(7-i)
        packed.itemset(i, current_byte)
    return packed

def test_all():
    for x  in range(0,4):
        for y in range(0,4):
            for z in range(0,4):
                #print("({:d}, {:d}, {:d}): {:s}".format(x,y,z,format(bitset(x,y,z), 'b').rjust(64, '0')))
                print(pack_bitset(bitset(x,y,z)))
test_all()
