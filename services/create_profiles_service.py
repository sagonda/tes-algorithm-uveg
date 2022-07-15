import numpy as np

class create_profiles_services():

    def __init__(self, dimension_modis, altura, latitud, longitud, h_, p2m, t2, q2m, sk, level, temp_era, year, month, day):
        self.dimension_modis = dimension_modis
        self.altura = altura
        self.latitud = latitud
        self.longitud = longitud
        self.h_ = h_
        self.p2m = p2m
        self.t2 = t2
        self.q2m = q2m
        self.sk = sk
        self.level = level
        self.temp_era = temp_era
        self.year = year
        self.month = month
        self.day = day
    def create_profiles(self):
        ''' 
        Resum: Function to create RTTOV input profiles
        
        Params: (dimension_modis, z, latitud, longitud, h_, p2m, t2, q2m, sk, level, temp_era, date_era5, date_modis)
        
        Output: Matrix-> datetimes, angles, surftype, surfgeom, s2m, skin, simplecloud, clwscheme, \
            icecloud, zeeman, p, t
        
        Call example: datetimes, angles, surftype, surfgeom, s2m, skin, simplecloud, clwscheme, Icecloud, \
            zeeman, p, t = create_profiles(dimension_modis, z, latitud, longitud, h_, p2m, t2, q2m, sk, level, temp_era)
        '''

        try:

            datetimes = np.empty((self.dimension_modis,6), order='F', dtype=np.int32)
            datetimes[:,:] = np.array([int(self.year),int(self.month),int(self.day),0,0,0])
            datetimes = datetimes.transpose()
            
            angles = np.empty((self.altura.shape[0],4), order='F', dtype=np.float32)
            angles[:,0] = self.altura
            angles = angles.transpose()
            
            surftype = np.empty((self.dimension_modis,2), order='F', dtype=np.int32)
            surftype[:,0] = 0
            surftype[:,1] = 0
            surftype = surftype.transpose()
            
            surfgeom = np.empty((self.dimension_modis,3), order='F', dtype=np.float64)
            surfgeom[:,0] = self.latitud
            surfgeom[:,1] = self.longitud
            surfgeom[:,2] = (self.h_/1000)
            surfgeom = surfgeom.transpose()
            
            s2m = np.empty((self.dimension_modis,6), order='F', dtype=np.float64)
            s2m[:,0] = self.p2m
            s2m[:,1] = self.t2
            s2m[:,2] = self.q2m
            s2m[:,3:] = 0
            s2m = s2m.transpose()
            
            skin = np.empty((self.dimension_modis, 10), order='F', dtype=np.float64)
            skin[:,0] = self.sk
            skin[:,1:] = 0
            skin = skin.transpose()
            
            simplecloud = np.empty((self.dimension_modis,2), order='F', dtype=np.float64)
            simplecloud[:,0] = 500
            simplecloud[:,1] = 0
            simplecloud = simplecloud.transpose()
            
            clwscheme = np.empty((self.dimension_modis), order='F', dtype=np.int32)
            clwscheme[:] = 0
            clwscheme = clwscheme.transpose()
            
            icecloud= np.empty((self.dimension_modis,2), order='F', dtype=np.int32)
            icecloud[:,0] = 0
            icecloud[:,1] = 0
            icecloud = icecloud.transpose()
            
            zeeman = np.empty((self.dimension_modis,2), order='F', dtype=np.float64)
            zeeman = zeeman.transpose()
            
            p = np.empty((self.dimension_modis, 25), order='F', dtype=np.float64)
            p[:,:] = self.level
            p = p.transpose()
            
            t = np.empty((25, self.dimension_modis), order='F', dtype=np.float64)
            t[:,:] = self.temp_era
            
            return datetimes, angles, surftype, surfgeom, s2m, skin, simplecloud, clwscheme, icecloud, zeeman, p, t

        except OSError as err:
            print("OS error: {0}".format(err))