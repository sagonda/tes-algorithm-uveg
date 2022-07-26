class unpacked_value_services():

    def __init__(self, packed_value, add_offset, scale_factor):
        self.packed_value = packed_value
        self.add_offset = add_offset
        self.scale_factor = scale_factor
    def unpacked_value(self):
        return (self.packed_value * self.scale_factor) + self.add_offset