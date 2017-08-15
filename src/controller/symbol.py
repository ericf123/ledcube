"""
A helper module for easy display of letters, numbers, and some special characters.
All letters are expecting the origin to be in the bottom right corner
relative to the viewer.
The below constants are lists of cube coordinates in 2d (x,y).
The z value gets added later depending on the plane in which they
should be displayed. See coords().
"""
A_COORDS = [(0,0), (1,0), (2,0), (3,1), (3,2), (2,3), (1,3), (0,3), (1,1), (1,2)]
B_COORDS = [(3,3), (2,3), (1,3), (0,3), (2,2), (0,2), (2,1), (0,1), (1,0)]
C_COORDS = [(2,3), (1,3), (3,2), (0,2), (3,1), (0,1), (3,0), (0,0)]
D_COORDS = [(1,3), (2,2), (0,2), (2,1), (0,1), (3,0), (2,0), (1,0), (0,0)]
E_COORDS = [(2,3), (1,3), (3,2), (2,2), (0,2), (3,1), (2,1), (0,1), (2,0), (0,0)]
F_COORDS = [(3,3), (2,3), (1,3), (0,3), (3,2), (1,2), (3,1), (1,1), (3,0), (1,0)]
G_COORDS = [(2,3), (1,3), (3,2), (1,2), (0,2), (3,1), (1,1), (0,1), (3,0), (1,0), (0,0)]
#G_COORDS = [(3,3), (2,3), (0,3), (3,2), (2,2), (0,2), (3,1), (2,1), (0,1), (3,0), (2,0), (1,0), (0,0)]
H_COORDS = [(3,3), (2,3), (1,3), (0,3), (2,2), (1,2), (2,1), (1,1), (3,0), (2,0), (1,0), (0,0)]
I_COORDS = [(3,3), (0,3), (3,2), (2,2), (1,2), (0,2), (3,1), (2,1), (1,1), (0,1), (3,0), (0,0)]
J_COORDS = [(0,3), (1,2), (0,2), (3,1), (2,1), (1,1), (0,1), (3,0), (2,0), (1,0)]
K_COORDS = [(3,3), (2,3), (1,3), (0,3), (2,2), (1,2), (3,1), (0,1)]
L_COORDS = [(3,3), (2,3), (1,3), (0,3), (0,2), (0,1), (0,0)]
M_COORDS = [(3,3), (2,3), (1,3), (0,3), (2,2), (2,1), (3,0), (2,0), (1,0), (0,0)]
N_COORDS = [(0,0), (1,0), (2,0), (3,0), (1,1), (2,2), (3,3), (0,3), (1,3), (2,3)]
O_COORDS = [(2,3), (1,3), (3,2), (0,2), (3,1), (0,1), (2,0), (1,0)]
P_COORDS = [(3,3), (2,3), (1,3), (0,3), (3,2), (1,2), (3,1), (1,1), (2,0)]
Q_COORDS = [(3,3), (2,3), (1,3), (3,2), (1,2), (3,1), (2,1), (1,1), (0,0)]
R_COORDS = [(1,3), (0,3), (2,2), (2,1)]
S_COORDS = [(0,3), (3,2), (2,2), (0,2), (3,1), (1,1), (0,1), (3,0)]
T_COORDS = [(3,3), (3,2), (2,2), (1,2), (0,2), (3,1), (2,1), (1,1), (0,1), (3,0)]
U_COORDS = [(3,3), (2,3), (1,3), (0,2), (0,1), (3,0), (2,0), (1,0)] 
V_COORDS = [(2,3), (0,2), (2,1)]
W_COORDS = [(3,3), (2,3), (1,3), (0,3), (1,2), (1,1), (3,0), (2,0), (1,0), (0,0)]
X_COORDS = [(3,3), (0,3), (2,2), (1,2), (2,1), (1,1,), (3,0), (0,0)]
Y_COORDS = [(3,3), (2,3), (1,2), (0,2), (1,1), (0,1), (3,0), (2,0)]
Z_COORDS = [(3,3), (0,3), (3,2), (1,2), (0,2), (3,1), (2,1), (0,1), (3,0), (0,0)]
ZERO_COORDS = [(3,3), (2,3), (1,3), (0,3), (3,2), (0,2), (3,1), (0,1), (3,0), (2,0), (1,0), (0,0)]
ONE_COORDS = [(2,3), (0,3), (3,2), (0,2), (3,1), (2,1), (1,1), (0,1), (0,0)]
TWO_COORDS = [(2,3), (0,3), (3,2), (0,2), (3,1), (1,1), (0,1), (2,0), (0,0)]
#THREE_COORDS = [(3,3), (2,3), (1,3), (0,3), (3,2), (2,2), (1,2), (0,2), (3,1), (2,1), (1,1), (0,1)]
THREE_COORDS = [(3,3), (2,2), (1,1)]
FOUR_COORDS = [(3,3), (2,3), (1,3), (1,2), (3,1), (2,1), (1,1), (0,1)]
FIVE_COORDS = [(3,3), (2,3), (0,3), (3,2), (1,2), (0,2), (3,1), (1,1), (0,1), (3,0), (1,0), (0,0)]
SIX_COORDS = [(3,3), (2,3), (1,3), (0,3), (3,2), (1,2), (0,2), (3,1), (1,1), (0,1), (3,0), (1,0), (0,0)]
SEVEN_COORDS = [(3,3), (0,3), (3,2), (1,2), (3,1), (2,1), (3,0)]
EIGHT_COORDS = [(2,3), (0,3), (3,2), (1,2), (2,1), (0,1)]
NINE_COORDS = [(3,3), (2,3), (3,2), (2,2), (3,1), (2,1), (3,0), (2,0), (1,0), (0,0)]
EXCLAMATION_COORDS = [(3,2), (2,2), (0,2), (3,1), (2,1), (0,1)]
COLON_COORDS = [(2,2), (0,2), (2,1), (0,1)]
OPEN_PAREN_COORDS = [(2,2), (1,2), (3,1), (0,1)]
CLOSE_PAREN_COORDS = [(3,2), (0,2), (2,1), (1,1)]
SINGLE_QUOTE_COORDS = [(3,2), (2,2)]

SYMBOLS = "abcdefghijklmnopqrstuvwxyz0123456789!:()'" #valid symbols
#indexes are same as above string, used to look up pattern for symbol
SYMBOL_COORDS_LIST = [A_COORDS, B_COORDS, C_COORDS, D_COORDS, E_COORDS, F_COORDS, G_COORDS, H_COORDS,
                      I_COORDS, J_COORDS, K_COORDS, L_COORDS, M_COORDS, N_COORDS, O_COORDS, P_COORDS, 
                      Q_COORDS, R_COORDS, S_COORDS, T_COORDS, U_COORDS, V_COORDS, W_COORDS, X_COORDS, 
                      Y_COORDS, Z_COORDS, ZERO_COORDS, ONE_COORDS, TWO_COORDS, THREE_COORDS, FOUR_COORDS,
                      FIVE_COORDS, SIX_COORDS, SEVEN_COORDS, EIGHT_COORDS, NINE_COORDS, EXCLAMATION_COORDS,
                      COLON_COORDS, OPEN_PAREN_COORDS, CLOSE_PAREN_COORDS, SINGLE_QUOTE_COORDS] 

def coords(symbol, z_planes=[0]):
    symbol = symbol.lower() #we only have one case
    index = SYMBOLS.find(symbol) #lookup pattern
    
    if index < 0:#invalid symbol
        if symbol != " ":
            print("Can't display symbol '{0}'".format(symbol))
        return [(-1,-1,-1)]

    symbol_coords_2d = SYMBOL_COORDS_LIST[index]
    symbol_coords_3d = []
    for z in z_planes:#add all the requested z's
        for i in range(len(symbol_coords_2d)):
            x,y = symbol_coords_2d[i]
            symbol_coords_3d.append((x,y,z))
    return symbol_coords_3d

"""def coords(symbol, trans_x=0, trans_y=1, trans_z=2, orig_z=0):
    #does no error checking on x,y,z 
    symbol = symbol.lower() #we only have one case
    index = SYMBOLS.find(symbol) #lookup pattern
    
    if index < 0:#invalid symbol
        if symbol != " ":
            print("Can't display symbol '{0}'".format(symbol))
        return [(-1,-1,-1)]

    symbol_coords_2d = SYMBOL_COORDS_LIST[index]
    symbol_coords_3d = []
    for i in range(len(symbol_coords_2d)):
            x,y = symbol_coords_2d[i]
            coord = (x,y,orig_z)
            translated_coord = (coord[trans_x], coord[trans_y], coord[trans_z])
            symbol_coords_3d.append(translated_coord)
    return symbol_coords_3d"""
