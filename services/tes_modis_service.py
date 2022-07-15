import numpy as np
 
class tes_modis_services():

    def __init__(self, lo, lup, ldown, trans, radiance, z=False, aux=False, recal=False):
        self.lo = lo
        self.lup = lup
        self.ldown = ldown
        self.trans = trans
        self.radiance = radiance
        self.z = z
        self.aux = aux
        self.recal = recal


    def tes_modis(self):
        # Algorith TES
        try:
            
            self.radiance = np.where( self.radiance > 1, self.radiance, np.nan)
            dimension = self.lup.shape[1]
            # Create variables 
            e = np.empty(shape=(3,dimension),dtype = np.float64)
            R = np.empty(shape=(3,dimension),dtype = np.float64)
            BT = np.empty(shape=(3,dimension),dtype = np.float64)
            beta = np.empty(shape=(3,dimension),dtype = np.float64)
            rad = np.empty(shape=(3,dimension),dtype = np.float64)
            T = np.empty(shape=(3,dimension),dtype = np.float64)
            Ts = np.empty(shape=(1,dimension),dtype = np.float64)
            e[:,:] = 0.97 

            if self.aux:
                rad[:,:] = [((self.radiance[i,:] - self.lup[i,:]) / self.trans[i,:]) for i in range(3)]
                
            else:
                rad[:,:] = self.radiance
                
            for tes in range(8):
                R[:,:] = [(rad[i,:] - (1-e[i,:]) * self.ldown[i,:]) for i in range(3)]
                #T[:,:] = [K2[i]/np.log(K1[i]/R[i,:]+1) for i in range(3)] 
                T[:,:] = [(14387.7/self.lo[i]) * ((np.log(((1.19104e8 *e[i,:])/( (self.lo[i]**5) * R[i,:])) + 1)) **(-1)) for i in range(3)]

                Ts[:,:] = np.max(T[:,:],axis=0)
                #BT[:,:] = [K1[i]/(np.exp(K2[i]/Ts[0,:])-1) for i in range(3)]
                BT[:,:] = [1.19104e8 / (self.lo[i]**5 * (np.exp(14387.9/(self.lo[i]*Ts[0,:]))-1)) for i in range(3)]

                e[:,:] = [R[i,:]/BT[i,:] for i in range(3)]
            emedia = np.empty(shape=(dimension),dtype = np.float64)
            emedia = (e[0,:] + e[1,:] + e[2,:])/np.float64(3) 
            maximo = np.empty(shape=(dimension),dtype = np.float64)
            minimo = np.empty(shape=(dimension),dtype = np.float64)
            maximo[:] = 0.0
            minimo[:] = 10.0
           
            beta[:,:] = [e[i,:]/emedia for i in range(3)]
            maximo[:] = np.max(beta[:,:], axis=0) 
            minimo[:] = np.min(beta[:,:], axis=0) 
        
            MMD = maximo-minimo              
            emin = c1+c2*(MMD**c3)
            e[:,:] = [beta[i,:]*(emin/minimo) for i in range(3)]
        
            R[:,:] = [rad[i,:] - (1-e[i,:])*self.ldown[i,:] for i in range(3)]
            #T[:,:] = [K2[i]/np.log(K1[i]/R[i,:]+1) for i in range(3)] 
            T[:,:] = [ (14387.7/self.lo[i])*np.log(((1.19104e8*e[i,:])/(self.lo[i]**5*R[i,:]))+1)**(-1) for i in range(3)]
            Ts[:,:] = np.max(T[:,:],axis=0)
            #BT[:,:] = [K1[i]/(np.exp(K2[i]/Ts[0,:])-1) for i in range(3)]
            BT[:,:] = [1.19104e8/(self.lo[i]**5 * (np.exp(14387.9/(self.lo[i]*Ts[0,:]))-1)) for i in range(3)]
            e[:,:] = [R[i,:]/BT[i,:] for i in range(3)]
            
            if self.recal:
                print('Recalculando banda 31 y 32')
                e[1:,:] = [R[i,:]/BT[i,:] for i in range(1,3)]

            #***Error rad ****
            erad = np.empty(shape=(3,dimension),dtype = np.float64)
            eq1 = np.empty(shape=(3,dimension),dtype = np.float64)
            eq2 = np.empty(shape=(3,dimension),dtype = np.float64)
            
            
            
            eq1[:,:] = [d1_1[i]*self.trans[i,:]+d2_1[i]*self.trans[i,:]**2+d3_1[i]*self.z[:]+d4_1[i]*self.z[:]**2+d5_1[i]*self.trans[i,:]*self.z[:]+d6_1[i] for i in range(3)]
            eq2[:,:] = [f1_1[i]*self.lup[i,:]+f2_1[i]*self.lup[i,:]**2+f3_1[i]*self.z[:]+f4_1[i]*self.z[:]**2+f5_1[i]*self.lup[i,:]*self.z[:]+f6_1[i] for i in range(3)]
            erad[:,:]=[(((0.003*self.radiance[i,:]/self.trans[i,:])**2+(eq2[i,:]/self.trans[i,:])**2+(eq1[i,:]*((self.radiance[i,:]-self.lup[i,:]))/(self.trans[i,:]**2))**2)**0.5) for i in range(3)]
           
            return Ts.ravel(), e, BT, rad, R, erad

        except OSError as err:
            print("OS error: {0}".format(err))