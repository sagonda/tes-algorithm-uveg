import numpy as np

class PackedValueService():

    def __init__(self, input_matrix, add_offset, scale_factor, data_type):
        self.input_matrix = input_matrix
        self.add_offset   = add_offset
        self.scale_factor = scale_factor
        self.data_type    = data_type


    def packed_value(self):
        if self.input_matrix.ndim == 2:
            result = np.empty((self.input_matrix.shape[0],self.input_matrix.shape[1]), dtype = self.data_type)
        elif self.input_matrix.ndim == 1:
            result = np.empty(self.input_matrix.shape[0], dtype = self.data_type)
        result[:] = (self.input_matrix - self.add_offset) / self.scale_factor

        return result