import cubestate
import raindrop
import corner
import vision

PRINTER = 1
VISION = 2
CORNER_PATTERN = 3
RAINDROP_PATTERN = 4
QUIT = 5

cs = cubestate.CubeState('/dev/ttyUSB0', exp_time=-1)

def loop():
    while True:
        choice = menu()

        if choice == PRINTER:
            while True:
                try:
                    cs.printf(input("enter string (^C to quit): "), .4)
                except KeyboardInterrupt:
                    break
        elif choice == VISION:
            vision.run(cs, .03)

        elif choice == CORNER_PATTERN:
            try:
                corner.run(cs)
            except KeyboardInterrupt:
                pass
        elif choice == RAINDROP_PATTERN:
            try:
                raindrop.run(cs, .2)
            except KeyboardInterrupt:
                pass
        else:
            break
    cs.update(-1,-1,-1)
    cs.send()
    print("bye")

def menu():
    user_input = -1
    while user_input not in [PRINTER, VISION, CORNER_PATTERN, RAINDROP_PATTERN, QUIT]:
        show_menu_options()
        try:
            user_input = int(input("Make your selection (1/2/3/4/5):"))
        except:
            print("Please enter either 1, 2, 3, 4, or 5.")
            user_input = -1
    return user_input

def show_menu_options():
    print("\n----Cube Menu-----")
    print("1) Message Printer")
    print("2) CV Controlled")
    print("3) Corner Pattern")
    print("4) Raindrop Pattern")
    print("5) Quit")



loop()
