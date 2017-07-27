import numpy as np

def pack_bits(index_array):
    """generates 8 bytes representing 64 bools (1 per led). Lowest index is MSB"""
    out = np.zeros(64, dtype=np.uint8)
    for index in index_array:
        if (index >= out.size):
            return False
        out.itemset(index,True)
    return np.packbits(out)



