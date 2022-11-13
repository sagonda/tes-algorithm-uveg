import numpy as np

class FVC_services():
    def __init__(self, ndvi, e31, e32):
        self.ndvi = ndvi
        self.e31 = e31
        self.e32 = e32
        
    def FVC(self):
        
        try:
            FVC = np.empty(shape=(self.ndvi.shape))
            fvc_E31 = np.empty(shape=(self.ndvi.shape))
            fvc_E32 = np.empty(shape=(self.ndvi.shape))
            e31_ = np.empty(shape=(self.ndvi.shape))
            e32_ = np.empty(shape=(self.ndvi.shape))
            
            FVC[:] = ((self.ndvi[:] - 0.2) / np.float32(0.5 - 0.2))**2
            FVC[:] = np.where(FVC > 1, 1, FVC)
            FVC[:] = np.where(FVC < 0, np.nan, FVC)

            e31_[:] = self.e31[:]
            e32_[:] = self.e32[:]
            
            c_veg = np.where(self.ndvi >= 0.2)
            c_soil = np.where(self.ndvi < 0.2)
            
            e31_[c_veg] = 0.968 + 0.021 * FVC[c_veg]
            e32_[c_veg] = 0.974 + 0.015 * FVC[c_veg]
              
            return e31_, e32_
        except OSError as err:
              print("OS error: {0}".format(err))