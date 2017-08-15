import cubestate
import raindrop
import corner

PRINTER = 1
CORNER_PATTERN = 2
RAINDROP_PATTERN = 3

cs = cubestate.CubeState('/dev/cu.SLAB_USBtoUART', exp_time=-1)

def loop():
    while True:
        choice = menu()

        if choice == PRINTER:
            while True:
                try:
                    cs.printf(input("enter string (^C to quit): "), .4)
                except KeyboardInterrupt:
                    break
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
    while user_input not in [1,2,3,4]:
        show_menu_options()
        try:
            user_input = int(input("Make your selection (1/2/3/4):"))
        except:
            print("Please enter either 1, 2, 3 or 4.")
            user_input = -1
    return user_input

def show_menu_options():
    print("----Cube Menu-----")
    print("1) Message Printer")
    print("2) Corner Pattern")
    print("3) Raindrop Pattern")
    print("4) Quit")



loop()
