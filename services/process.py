import numpy as np

from utilities.utilities import utilitiesUveg 

class processUveg():

    def __init__(self,sk):
        self.sk = sk
        

    def variables(self):     
        Lbb29 = (utilitiesUveg.consA)/(np.power(utilitiesUveg.lonOnda29,5) * (np.exp(utilitiesUveg.consB/(utilitiesUveg.lonOnda29*self.sk))-1))
        Lbb31 = (utilitiesUveg.consA)/(np.power(utilitiesUveg.lonOnda31,5) * (np.exp(utilitiesUveg.consB/(utilitiesUveg.lonOnda31*self.sk))-1))
        Lbb32 = (utilitiesUveg.consA)/(np.power(utilitiesUveg.lonOnda32,5) * (np.exp(utilitiesUveg.consB/(utilitiesUveg.lonOnda32*self.sk))-1))
        return Lbb29, Lbb31, Lbb32
               

    
    
    
    
  
    