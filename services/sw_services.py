import numpy as np
 
class sw_services():

    def __init__(self, lo, radiance, dimension, e_29_original, e31_fvc, e32_fvc, ldown, R, trans, Ts, aux = False, aux1 = False):
       self.lo = lo
       self.radiance = radiance
       self.dimension = dimension
       self.e_29_original = e_29_original
       self.e31_fvc = e31_fvc
       self.e32_fvc = e32_fvc
       self.ldown = ldown
       self.R = R
       self.trans = trans
       self.Ts = Ts
       self.aux = aux
       self.aux1 = aux1
    
    def sw(self):
        
        try:
            e_recal = np.empty(shape=(3,self.dimension),dtype = np.float64)
            BT_recal = np.empty(shape=(3,self.dimension),dtype = np.float64)
            rad_recal = np.empty(shape=(3,self.dimension),dtype = np.float64)
            T31 = np.empty(shape=(self.dimension),dtype = np.float64)
            T32 = np.empty(shape=(self.dimension),dtype = np.float64)
            Tsw = np.empty(shape=(self.dimension),dtype = np.float64)
            
            if self.aux:
                #radiance = np.where( radiance > 1, radiance, np.nan)
    
                a0=-0.004
                a1=2.625
                a2=0.424
                a3=41.4
                a4=0.04
                a5=-201
                a6=26.6
    
                ww=-68.80969804*self.trans[0,:]+38.35444487*self.trans[0,:]**2+53.74448404*self.trans[1,:]-40.96607658*self.trans[2,:]+18.44174348
    
                #**********************Split Window************************
                T31[:] = (14387.7/np.float64(self.lo[1]))*((np.log(((1.19104e8)/np.float64(((self.lo[1]**5)*self.radiance[1,:])))+1))**(-1))
                T32[:] = (14387.7/np.float64(self.lo[2]))*((np.log(((1.19104e8)/np.float64(((self.lo[2]**5)*self.radiance[2,:])))+1))**(-1))
    
                Tsw[:] = a0+T31+a1*(T31-T32)+a2*(T31-T32)**2+(a3+a4*ww)*(1-(self.e31_fvc+self.e32_fvc)/np.float(2))+(a5+a6*ww)*(self.e31_fvc-self.e32_fvc)
               
                c_camb = np.where(np.abs(Tsw - self.Ts) > 1.5)
    
                self.Ts[c_camb] = Tsw[c_camb]#Donde la diferencia de LST sea > a 1.5 Ts = TSW  
                
            if self.aux1:
            
                BT_recal[:,:] = [1.19104e8/np.float64(self.lo[i]**5*(np.exp(14387.9/np.float64(self.lo[i]*self.Ts))-1)) for i in range(3)]
                e_recal[:,:] = [self.R[i,:]/np.float64(BT_recal[i,:]) for i in range(3)]
                rad_recal[:,:] = [e_recal[i,:]*np.float64(BT_recal[i,:])+((1-e_recal[i,:])*self.ldown[i,:]) for i in range(3)] # guardar radiancia anterior
    
            return rad_recal
        
        except OSError as err:
            print("OS error: {0}".format(err))