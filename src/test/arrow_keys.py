import curses
import cubestate
from time import sleep

S_PER_FRAME = .1

current_frame = 0

#direction constants
DIR_POS_X = 1
DIR_POS_Y = 2
DIR_POS_Z = 3
DIR_NEG_X = -1
DIR_NEG_Y = -2
DIR_NEG_Z = -3

stdscr = curses.initscr()
stdscr.nodelay(1)
curses.noecho()
curses.cbreak()
stdscr.keypad(1)

x = 0
y = 0
z = 0
current_direction = DIR_POS_X

cs = cubestate.CubeState('/dev/cu.SLAB_USBtoUART', exp_time=-1)

def force_bounds(val):
    if val < 0:
        return 3
    else:
        return val % 4

def get_new_position(x,y,z):
    """current_position should be a tuple of (x,y,z)"""
    if current_direction == DIR_X and x > 3:
       y += 1 
       current_direction = DIR_POS_Y
    elif current_direction == DIR_NEG_X and x < 0:
        y -= 1
        current_direction = DIR_NEG_Y

    return (x,y,z)

def increment_current_direction():
    if current_direction == DIR_POS_X:
        x += 1
    elif current_direction == DIR_NEG_X:
        x -= 1
    elif current_direction == DIR_POS_Y:
        y += 1
    elif current_direction == DIR_NEG_Y:
        y -= 1
    elif current_direction == DIR_POS_Z:
        z += 1
    else:
        z -= 1

while True:
    try:
        c = stdscr.getch()
        if c > -1:
            if c == ord('w'):
                stdscr.addstr(0,0,"up\n")
                stdscr.refresh()
                z+=1
            elif c == ord('a'):
                stdscr.addstr(0,0,"left\n")
                stdscr.refresh()
                y += 1
            elif c == ord('s'):
                stdscr.addstr(0,0,"down\n")
                stdscr.refresh()
                z -= 1
            elif c == ord('d'):
                stdscr.addstr(0,0,"right\n")
                stdscr.refresh()
                y -= 1
            elif c == ord('q'):
                break
            else:
                stdscr.addstr(0,0,"\r")
                stdscr.refresh()
        if current_frame % 2 == 0:
            x += 1
            #increment_current_direction()

        sleep(S_PER_FRAME)

#        x,y,z = get_new_position(x,y,z)
        x = force_bounds(x)
        y = force_bounds(y)
        z = force_bounds(z)

        cs.update(x,y,z)
        cs.send()   
        current_frame += 1
        current_frame %= 30
        stdscr.refresh()

    except KeyboardInterrupt:
        break


curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()
    
