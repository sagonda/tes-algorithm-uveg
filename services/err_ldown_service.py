import numpy as np

class err_ldown_services:
    def __init__(self, ldown29, ldown31, ldown32, z, dimension_modis_ravel):
        self.ldown29 = ldown29
        self.ldown31 = ldown31
        self.ldown32 = ldown32
        self.z = z
        self.dimension_modis_ravel = dimension_modis_ravel



    def ldown_error(self):

        err_ldown = np.zeros(
        shape=(3, self.dimension_modis_ravel), dtype=np.float64)
        c1_29 = 0.018690841
        c1_31 = 0.024681043
        c1_32 = 0.025080562
        c2_29 = -0.000014073
        c2_31 = 0.000003659
        c2_32 = 0.000001100
        c3_29 = 0.000002232
        c3_31 = 0.000001042
        c3_32 = 0.000000949
        c4_29 = -0.001359401
        c4_31 = -0.002232340
        c4_32 = -0.002368573
        c5_29 = 0.000000323
        c5_31 = -0.000000011
        c5_32 = 0.000000131
        c0_29 = -0.004099838
        c0_31 = 0.001119390
        c0_32 = 0.000240263

        b29 = c0_29 + c1_29*self.ldown29 + c2_29*self.z + c3_29 * \
            self.ldown29*self.z + c4_29*self.ldown29**2 + c5_29*self.z**2
        b31 = c0_31 + c1_31*self.ldown31 + c2_31*self.z + c3_31 * \
            self.ldown31*self.z + c4_31*self.ldown31**2 + c5_31*self.z**2
        b32 = c0_32 + c1_32*self.ldown32 + c2_32*self.z + c3_32 * \
            self.ldown32*self.z + c4_32*self.ldown32**2 + c5_32*self.z**2
        err_ldown[0, :] = b29
        err_ldown[1, :] = b31
        err_ldown[2, :] = b32

        return err_ldown