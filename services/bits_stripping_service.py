import numpy as np

class bits_stripping_services():
    def __init__(self, bit_start, bit_count, value):
        self.bit_start = bit_start
        self.bit_count = bit_count
        self.value = value
        
    def bits_stripping(self): 
        bitmask=pow(2, self.bit_start+self.bit_count)-1
        return np.right_shift(np.bitwise_and(self.value,bitmask), self.bit_start)
