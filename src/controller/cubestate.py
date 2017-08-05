import numpy as np
from expirationqueue import ExpirationQueue as eq
from time import time
import serial
from sys import exit

class CubeState:
    def __init__(self, ext_time, serial_port, serial_baud=115200):
        """standard initializer
           ext_time is the time (in seconds) and LED should stay on after being turned on"""
        self.current = 0 #current map of leds that are on - initialize to none on (treated as 64bit in)
        self.ext_queue = eq() 
        self.ext_time = ext_time
        self.serial_port = serial_port #port to use to communicate with arduino
        self.serial_baud = serial_baud
        self.last_sent = -1 #used to check if we should send data

        #TODO - improve error handling
        #open serial connection
        try:
            self.serial = serial.Serial(port=self.serial_port, baudrate=self.serial_baud)
        except Exception:
            print("Error opening serial port. Bye.")
            exit(1) #sys.exit 
    def z_helper(self, z):
        """hacky way of making the thing work. I'm really sorry about this."""
        if z == 2:
            z = 3
        elif z == 3:
            z = 2
        return z

        
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
                z = self.z_helper(z)
                if not (x == -1 or y == -1 or z == -1):
                    bset |= (1 << (16*x + 4*z + y))
            return bset
        else:
            #1 << index
            z = self.z_helper(z)
            return 1 << 16*x + 4*z + y

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
        """Packs self.current into an array of 8 bytes and writes it to self.serial.
           Before sending, it checks to see if self.current has changed from the last time it 
           sent data to avoid flooding the Arduino with unneeded data.
           Returns byte array that was sent if it sends something, -1 if it sends nothing."""
        if self.last_sent != self.current:#don't want to send any data unless state changes
            self.last_sent = self.current
            to_send = np.flipud(self.pack_bitset(self.current))#we flip the array because numpy loads it into buffer in reverse order
            self.serial.write(to_send)
            return to_send
        return -1

if __name__ == '__main__':
    cs = CubeState(1, '/dev/ttyUSB1')
    cs.update(pos_list=[(0,0,0),(1, 0, 0),(2,0,0),(3,0,0)])
    print(cs.send())

