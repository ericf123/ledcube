import curses
import cubestate
from time import sleep
from random import choice

S_PER_FRAME = .03


#direction constants
DIR_POS_X = 0
DIR_NEG_X = 1
DIR_POS_Y = 2
DIR_NEG_Y = 3
DIR_POS_Z = 4
DIR_NEG_Z = 5

def init_curses():
    stdscr = curses.initscr()
    stdscr.nodelay(1)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)

    return stdscr

def close_curses(stdscr):
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()

class Snake:
    def __init__(self):
        self.__x = 0
        self.__y = 0
        self.__z = 0
        self.__direction = DIR_POS_X
        self.__current_frame = 0
        self.__cs = cubestate.CubeState('/dev/cu.SLAB_USBtoUART', exp_time=1)
#        self.__stdscr = init_curses()

    def play(self):
        while True:
            try:
                #c = self.__stdscr.getch()
                """keypress_directions = self.get_keypress_directions()
                if c == ord('w'):
                    self.__direction = keypress_directions[0]
                elif c == ord('a'):
                    self.__direction = keypress_directions[1]
                elif c == ord('s'):
                    self.__direction = keypress_directions[2]
                elif c == ord('d'):
                    self.__direction = keypress_directions[3]
                elif c == ord('q'):
                    break"""

                self.inc_current_direction()
                self.direction = choice(self.get_valid_directions())

                self.update_position()
                self.__cs.update(self.__x, self.__y, self.__z)
                self.__cs.send()

                """coord_string = "({0}, {1}, {2}), {3}\r".format(self.__x, self.__y, self.__z, self.__direction)
                self.__stdscr.addstr(1,0, coord_string)
                self.__stdscr.refresh()"""

                self.__current_frame += 1
                self.__current_frame %= 30
                sleep(S_PER_FRAME)
            
            except KeyboardInterrupt:
                break
            
        #close_curses(self.__stdscr)

    def update_position(self):
        clipped_x = self.clip(self.__x)
        clipped_y = self.clip(self.__y)
        clipped_z = self.clip(self.__z)
        if self.__x != clipped_x or self.__y != clipped_y or self.__z != clipped_z: #out of bounds
            self.__direction = choice(self.get_valid_directions())

        self.__x = clipped_x
        self.__y = clipped_y
        self.__z = clipped_z

    def inc_current_direction(self):
        if self.__direction == DIR_POS_X:
            self.__x += 1
        elif self.__direction == DIR_NEG_X:
            self.__x -= 1
        elif self.__direction == DIR_POS_Y:
            self.__y += 1
        elif self.__direction == DIR_NEG_Y:
            self.__y -= 1
        elif self.__direction == DIR_POS_Z:
            self.__z += 1
        else:
            self.__z -= 1


    def clip(self, val, lower=0, upper=3):
        if val > upper:
            return upper
        elif val < lower:
            return lower
        return val
 

    def get_keypress_directions(self):
        valid_directions = self.get_valid_directions()

        absolute_direction = self.__direction // 2 #basically x,y, or z without the pos or neg

        if absolute_direction == 0: #x
            w = self.ensure_validity(DIR_POS_Z, valid_directions)
            a = self.ensure_validity(DIR_POS_Y, valid_directions)
            s = self.ensure_validity(DIR_NEG_Z, valid_directions)
            d = self.ensure_validity(DIR_NEG_Y, valid_directions)
        elif absolute_direction == 1: #y
            w = self.ensure_validity(DIR_POS_Z, valid_directions)
            a = self.ensure_validity(DIR_POS_X, valid_directions)
            s = self.ensure_validity(DIR_NEG_Z, valid_directions)
            d = self.ensure_validity(DIR_NEG_X, valid_directions)
        else: #z
            w = self.ensure_validity(DIR_POS_Y, valid_directions)
            a = self.ensure_validity(DIR_POS_X, valid_directions)
            s = self.ensure_validity(DIR_NEG_Y, valid_directions)
            d = self.ensure_validity(DIR_NEG_X, valid_directions)

        return (w,a,s,d)
    
    def ensure_validity(self, direction, valid_directions):
        """return direction if it is in valid_directions, otherwise return current direction"""
        if direction in valid_directions:
            return direction
        else:
            return self.__direction

    def get_valid_directions(self):
        """Returns a list of all the possible next directions to go from the current position"""
        current_coord = [self.__x, self.__y, self.__z]
        directions = [[DIR_POS_X, DIR_NEG_X], [DIR_POS_Y, DIR_NEG_Y], [DIR_POS_Z, DIR_NEG_Z]]

        # // = integer division
        del directions[self.__direction // 2]#remove both the negative and positive current direction as options
        del current_coord[self.__direction // 2]#don't need to consider the current value of the our direction

        for i in range(2):#directions, current_coord will each have two elements after above step
            if current_coord[i] == 0:
                del directions[i][1]#directions[i][1] is the negative of the direciton corresponding to coord[i]
            elif current_coord[i] == 3:
                del directions[i][0]#similarly, direcitons[i][0] is the positive 

        #poor-man's ravel to create a 1D list rather than a list of tuples
        #numpy.ravel doesn't work on 2D arrays with different dimensions on the inside
        valid_directions = []
        for i in range(2):
            for j in range(len(directions[i])):
                valid_directions.append(directions[i][j])
            
        return valid_directions

if __name__ == '__main__':
    s = Snake()
    s.play()
