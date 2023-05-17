import numpy as np

class RecalLseService():

    def __init__(self, emiss, dimension):
        self.emiss     = emiss
        self.dimension = dimension

    def recl_e(self):
        mask_e          = np.where(self.emiss > 0.992)
        e_max           = self.emiss[mask_e]
        dif             = e_max - 0.992
        e_ori_dif       = self.emiss[:,mask_e] - dif
        e_mod           = np.zeros(shape=(3,self.dimension),dtype = np.float64)
        e_mod           = self.emiss
        e_mod[:,mask_e] = e_ori_dif

        return e_mod