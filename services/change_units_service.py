import numpy as np
from utilities.utilities import Utilities

class ChangeUnitsService():

    def __init__(self,sk):
        self.sk = sk


    def variables(self):     
        Lbb29 = (Utilities.consA)/(np.power(Utilities.lonOnda29,5) * (np.exp(Utilities.consB/(Utilities.lonOnda29*self.sk))-1))
        Lbb31 = (Utilities.consA)/(np.power(Utilities.lonOnda31,5) * (np.exp(Utilities.consB/(Utilities.lonOnda31*self.sk))-1))
        Lbb32 = (Utilities.consA)/(np.power(Utilities.lonOnda32,5) * (np.exp(Utilities.consB/(Utilities.lonOnda32*self.sk))-1))
        
        return Lbb29, Lbb31, Lbb32