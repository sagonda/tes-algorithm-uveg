import numpy as np

class NewArrayService():

    def __init__(self, array, mask, dimension_original, data_type):
        self.array              = array
        self.mask               = mask
        self.dimension_original = dimension_original
        self.data_type          = data_type


    def new_array(self):
        new            = np.empty([self.dimension_original, 1354], dtype = self.data_type)
        new[:]         = 0
        new[self.mask] = self.array
        
        return new