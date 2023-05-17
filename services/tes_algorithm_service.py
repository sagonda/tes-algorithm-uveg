import numpy as np
 
class TesAlgorithmService():

    def __init__(self, lo, lup, ldown, trans, radiance, z=False, aux=False, recal=False):
        self.lo       = lo
        self.lup      = lup
        self.ldown    = ldown
        self.trans    = trans
        self.radiance = radiance
        self.z        = z
        self.aux      = aux
        self.recal    = recal

    def tes_modis(self):
        try:
            c1 = 0.998449
            c2 = -0.654215
            c3 = 0.735536 
            K1 = [2631.58, 735.84, 471.25] 
            K2 = [1686.18, 1306.72, 1195.27]            

            radiance  = np.where( self.radiance > 1, self.radiance, np.nan)
            dimension = self.lup.shape[1]

            e      = np.empty(shape=(3,dimension),dtype = np.float64)
            R      = np.empty(shape=(3,dimension),dtype = np.float64)
            BT     = np.empty(shape=(3,dimension),dtype = np.float64)
            beta   = np.empty(shape=(3,dimension),dtype = np.float64)
            rad    = np.empty(shape=(3,dimension),dtype = np.float64)
            T      = np.empty(shape=(3,dimension),dtype = np.float64)
            Ts     = np.empty(shape=(1,dimension),dtype = np.float64)
            e[:,:] = 0.97

            if self.aux:
                rad[:,:] = [((radiance[i,:] - self.lup[i,:]) / self.trans[i,:]) for i in range(3)]
            else:
                rad[:,:] = radiance

            for tes in range(8):
                R[:,:] = [(rad[i,:] - (1-e[i,:]) * self.ldown[i,:]) for i in range(3)]
                T[:,:] = [(14387.7/self.lo[i]) * ((np.log(((1.19104e8 *e[i,:])/( (self.lo[i]**5) * R[i,:])) + 1)) **(-1)) for i in range(3)]
                #T[:,:] = [K2[i]/np.log((K1[i]*e[i,:])/R[i,:]+1) for i in range(3)]
                Ts[:] = np.max(T[:,:],axis=0)
                BT[:,:] = [1.19104e8 / (self.lo[i]**5 * (np.exp(14387.9/(self.lo[i]*Ts[0,:]))-1)) for i in range(3)]
                #BT[:,:] = [K1[i]/(np.exp(K2[i]/Ts[0,:])-1) for i in range(3)]
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
            #T[:,:] = [K2[i]/np.log((K1[i]*e[i,:])/R[i,:]+1) for i in range(3)] 
            T[:,:] = [(14387.7/self.lo[i]) * ((np.log(((1.19104e8 *e[i,:])/( (self.lo[i]**5) * R[i,:])) + 1)) **(-1)) for i in range(3)]
            Ts[:,:] = np.max(T[:,:],axis=0)
            #BT[:,:] = [K1[i]/(np.exp(K2[i]/Ts[0,:])-1) for i in range(3)]
            BT[:,:] = [1.19104e8 / (self.lo[i]**5 * (np.exp(14387.9/(self.lo[i]*Ts[0,:]))-1)) for i in range(3)]
            e[:,:] = [R[i,:]/BT[i,:] for i in range(3)]# Solo modificar la banda 29

            if self.recal:
                print('Recalculando banda 31 y 32')
                e[1:,:] = [R[i,:]/BT[i,:] for i in range(1,3)]

            ''' Error rad '''
            erad = np.empty(shape=(3,dimension),dtype = np.float64)
            eq1 = np.empty(shape=(3,dimension),dtype = np.float64)
            eq2 = np.empty(shape=(3,dimension),dtype = np.float64)

            d1_1 = [0.016117854,0.028460421,0.026695870]
            d2_1 = [-0.017482940,-0.028220773,-0.028131707]
            d3_1 = [0.000049389,0.000043778,0.000021690]
            d4_1 = [-0.000000219,0.000000063,0.000000126]
            d5_1 = [-0.000056240,-0.000053979,-0.000030838]
            d6_1 = [0.000726560,0.000216716,0.001238195]

            f1_1 = [0.019000886,0.024789637,0.030145755]
            f2_1 = [-0.001376105,-0.002572940,-0.003234448]
            f3_1 = [0.000014232,-0.000063260,0.000004645]
            f4_1 = [-0.000000329,0.000001213,0.000000452]
            f5_1 = [0.000001726,0.000018007,0.000004733]
            f6_1 = [0.001851194,0.001218762,0.001042131]

            eq1[:,:]  = [d1_1[i]*self.trans[i,:]+d2_1[i]*self.trans[i,:]**2+d3_1[i]*self.z[:]+d4_1[i]*self.z[:]**2+d5_1[i]*self.trans[i,:]*self.z[:]+d6_1[i] for i in range(3)]
            eq2[:,:]  = [f1_1[i]*self.lup[i,:]+f2_1[i]*self.lup[i,:]**2+f3_1[i]*self.z[:]+f4_1[i]*self.z[:]**2+f5_1[i]*self.lup[i,:]*self.z[:]+f6_1[i] for i in range(3)]
            erad[:,:] = [(((0.003*radiance[i,:]/self.trans[i,:])**2+(eq2[i,:]/self.trans[i,:])**2+(eq1[i,:]*((radiance[i,:]-self.lup[i,:]))/(self.trans[i,:]**2))**2)**0.5) for i in range(3)]

            return Ts.ravel(), e, BT, rad, R, erad

        except OSError as err:
            print("OS error: {0}".format(err))