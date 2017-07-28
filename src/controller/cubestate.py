import numpy as np
from expirationqueue import ExpirationQueue as eq
from time import time

class CubeState:
    def __init__(self, ext_time):
        """standard initializer
           ext_time is the time (in seconds) and LED should stay on after being turned on"""
        self.current = np.uint64(0) #current map of leds that are on - initialize to none on (treated as 64bit in)
        self.ext_queue = eq() 
        self.ext_time = ext_time
        self.last_sent = -1 #used to check if we should send data
        
    def bitset(self, x=None, y=None, z=None, pos_list=None):
        """x,y,z: integer in [0,3] (cube coordinate)
           Alternatively, one can pass a pos_list where each elem is tuple of form (x,y,z). 
           Returns a 64bit int with the correct index bit set.
           For example, (3, 3, 3) is led 64 (index 63), (3,0,0) is led 49 (index 48).
           NOTE: This method does no error checking except for -1 in a pos_list. Do error checking somewhere else.
           """
        if pos_list is not None:
            bset = 0
            for pos in pos_list:
                x = pos[0]
                y = pos[1]
                z = pos[2]
                if not (x == -1 or y == -1 or z == -1):
                    bset |= (1 << (16*x + 4*y + z))
            return bset
        else:
            #1 << index
            return 1 << 16*x + 4*y + z #just bask in the elegance

    def pack_bitset(self, bits):
        """Packs bits into a padded array of 8 bytes for sending to Arduino over serial.
           Byte ordering is big endian, i.e. MSB is index 0."""
        packed = np.empty(8, dtype=np.uint8)
        for i in range(0,8):
            #current_byte is 8 ones shifted to match position in bitset 
            #anded with the bitset, and shifted right to be only 8 bits
            current_byte = (bits & 0xFF << 8*(7-i)) >> 8*(7-i)
            packed.itemset(i, current_byte)
        return packed

    def update(self, x=None, y=None, z=None, pos_list=None):
        """Sets the current state to a bitset derived from x,y,z as cube coords.
           Does error checking and expiration handling around bitset()"""
        if pos_list is not None:
            new_state = self.bitset(pos_list=pos_list)
            self.current |= new_state
            self.ext_queue.push(~new_state, time() + self.ext_time)
        elif -1 not in [x,y,z]:#use -1 to set everything off
           new_state = self.bitset(x,y,z)
           self.current |= new_state #turn on new LED in addition to ones that are already on
           self.ext_queue.push(~new_state, time() + self.ext_time)
        self.current &= self.ext_queue.pop()#turn off the expired LEDs

    def send(self):
        """todo - implement this to send packed bitsets to the arduino"""
        if self.last_sent != self.current:#don't want to send any data unless state changes
            print(bin(self.current))
            self.last_sent = self.current

if __name__ == '__main__':
    cs = CubeState(1)
    #print(bin(cs.bitset(pos_list=[(3,3,3),(0,0,0),(1,0,0),(0,1,0),(0,0,0)])))
    cs.update(pos_list=[(3,3,3),(0,0,0),(1,0,0),(0,1,0),(0,0,0)])
    while True:
        cs.update(x=-1,y=-1,z=-1, pos_list=None)
        cs.send()
        if cs.current == 0:
            break

