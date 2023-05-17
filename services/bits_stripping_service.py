import numpy as np

class BitsStrippingService():

    def __init__(self, value):
        self.value = value


    def bits_stripping(self): 
        bitmask=pow(2, 1 + 2)-1

        return np.right_shift(np.bitwise_and(self.value,bitmask), 1)