import numpy as np
from expirationqueue import ExpirationQueue as eq
from time import time
from time import sleep
import serial
from sys import exit
import symbol

class CubeState:
    def __init__(self,  serial_port, serial_baud=115200, exp_time=-1):
        """standard initializer
           exp_time is the time (in seconds) and LED should stay on after being turned on"""
        self.current = 0 #current map of leds that are on - initialize to none on (treated as 64bit in)
        self.exp_queue = eq() 
        self.exp_time = exp_time
        self.serial_port = serial_port #port to use to communicate with arduino
        self.serial_baud = serial_baud
        self.last_sent = -1 #used to check if we should send data

        #TODO - improve error handling
        #open serial connection
        try:
            self.serial = serial.Serial(port=self.serial_port, baudrate=self.serial_baud, timeout=1)
        except Exception:
            print("Error opening serial port. Bye.")
            exit(1) #sys.exit 
       
    def bitset(self, x=None, y=None, z=None, coords=None):
        """x,y,z: integer in [0,3] (cube coordinate)
           Alternatively, one can pass a coords where each elem is tuple of form (x,y,z). 
           Returns a 64bit int with the correct index bit set.
           For example, (3, 3, 3) is led 64 (index 63), (3,0,0) is led 49 (index 48).
           NOTE: This method does no error checking except for -1 in a coords. Do error checking somewhere else.
           """
        if coords is not None:
            bset = 0
            for coord in coords:
                x = coord[0]
                y = coord[1]
                z = coord[2]
                if not (x == -1 or y == -1 or z == -1):
                    bset |= (1 << (16*x + 4*z + y))
            return bset
        else:
            #1 << index
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

    def update(self, x=None, y=None, z=None, coords=None):
        """Sets the current state to a bitset derived from x,y,z as cube coords.
           Does error checking and expiration handling around bitset()"""
        if self.exp_time >= 0:#negative expiration time means don't do automatic expiration
            if coords is not None:
                new_state = self.bitset(coords=coords)
            elif -1 not in [x,y,z]:#use -1 to set everything off
               new_state = self.bitset(x,y,z)

            self.current |= new_state
            self.exp_queue.push(~new_state, time() + self.exp_time)
            self.current &= self.exp_queue.pop()#turn off the expired LEDs
        else:
            if coords is not None:
                new_state = self.bitset(coords=coords)
            elif -1 not in [x,y,z]:#use -1 to set everything off
                new_state = self.bitset(x,y,z)
            else: 
                new_state = 0
            self.current = new_state

    def send(self):
        """Packs self.current into an array of 8 bytes and writes it to self.serial.
           Before sending, it checks to see if self.current has changed from the last time it 
           sent data to avoid flooding the Arduino with unneeded data.
           Returns byte array that was sent if it sends something, -1 if it sends nothing."""
        #if self.last_sent != self.current:#don't want to send any data unless state changes
            #self.last_sent = self.current
        to_send = np.flipud(self.pack_bitset(self.current)).tobytes()#we flip the array because numpy loads it into buffer in reverse order
        self.serial.write(to_send)
        return to_send
    #return -1

    def printf(self, string, delay, z_planes=[3]):#
        """convenient helper function to print strings"""
        for char in string:
            #flash off for a small amount of time for breaks between letters
            self.update(-1,-1,-1)
            self.send()
            sleep(delay*.5)

            #send new letter and wait a little
            self.update(coords=symbol.coords(char, z_planes))
            self.send()
            sleep(delay)
        #clear cube after print
        self.update(-1,-1,-1)
        self.send()

    """def printf(self, string, delay, z_planes=[0]):#
        convenient helper function to print strings
        char_in_z = np.array([" ", " ", " ", " "], dtype='U')
        for i in range(len(string) + 4):
            char_in_z = np.roll(char_in_z, 1)
            if i < len(string):
                char_in_z.itemset(0, string[i])
            else:
                char_in_z.itemset(0, " ")
            print(char_in_z)

            coords = []
            for j in range(len(char_in_z)):
                coords.extend(symbol.coords(char_in_z.item(j), z_planes=[j]))
            self.update(coords=coords)
            self.send()
            sleep(delay)
            """
    def marquee(self, string, delay):
        upcoming_chars = np.array([" ", " ", " "], dtype='U')
        for i in range(len(string) + 3):
            upcoming_chars = np.roll(upcoming_chars, 1)
            if i < len(string):
                upcoming_chars.itemset(0, string[i])
            else:
                upcoming_chars.itemset(0, " ")
            print(upcoming_chars)

            coords = symbol.coords(upcoming_chars[0], 2, 1, 0, 0)
            coords.extend(symbol.coords(upcoming_chars[1], 0, 1, 2, 3))
            coords.extend(symbol.coords(upcoming_chars[2], 2, 1, 0, 3))

            self.update(coords=coords)
            self.send()
            sleep(delay)
