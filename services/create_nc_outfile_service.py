import netCDF4 as net
import numpy as np

class create_nc_outfile_services():

    def __init__(self, path_output, year, month, day, date_modis, dimension_original,\
                          latitud, longitud, Ts, e, mask_original_modis, toma,  errTs, err_e29, err_e31, err_e32, z):
        self.path_output = path_output
        self.year = year
        self.month = month
        self.day= day
        self.date_modis = date_modis
        self.dimension_original = dimension_original
        self.latitud = latitud
        self.longitud = longitud
        self.Ts = Ts 
        self.e = e
        self.mask_original_modis = mask_original_modis
        self.toma = toma
        self.errTs = errTs
        self.err_e29 = err_e29
        self.err_e31 = err_e31
        self.err_e32 = err_e32
        self.z = z
        
    def create_nc_outfile(self):
        
        try:
           
            ###### Create *nc out file  
            mask1_ = self.mask_original_modis
            path = str(self.path_output)                      
            out_nc = net.Dataset(path+self.year+'/'+self.month+'/'+self.day+'/'+'TES_'+self.year+self.month+self.day+'_'+self.date_modis+'_'+self.toma+'.nc',mode='w',format='NETCDF4')                              
    
            
            ####### Create dimesions 
            x = out_nc.createDimension('x', self.dimension_original)
            y = out_nc.createDimension('y', 1354)
            time_ = out_nc.createDimension('time', None)   
            
            ##### Add atributes file
            out_nc.title = 'Emissivity  and Land Surface Temperature Map v.1'
            out_nc.summary = 'This data set contains the map of temperatures (LST) and emissivities of the earths surface, derived from MODIS, ERA5 products and calculated from the TES algorithm.'
            out_nc.type = 'LST_TES_MAP_1KM'
            out_nc.id = ''
            out_nc.project = 'Land Surface Temperature ESACCI'
            out_nc.reference = ''
            out_nc.institution = 'GLOBAL CHANGE UNIT IMAGE PROCESSING LABORATORY UNIVERSITY OF VALENCIA'
            out_nc.contact = 'daniel.salinas@uv.es'
            out_nc.comment = ''
                  
            lat = out_nc.createVariable('lat', np.int32, ('x', 'y'), zlib=True)
            lat.units = 'degrees_north'
            lat.long_name = 'latitude*10000'
            
            lon = out_nc.createVariable('lon', np.int32, ('x','y'), zlib=True)
            lon.units = 'degrees_east'
            lon.long_name = 'longitude*10000'
            
            time_ = out_nc.createVariable('time',np.uint16, ('time',), zlib=True)
            time_.units = 'hours since 1800-01-01'
            time_.long_name = 'time'
            
            lst = out_nc.createVariable('UVEG_LST', np.uint16,('x','y'), zlib=True)
            lst.units = 'Kelvin K'
            lst._Offset = '0.0'
            lst._Scale = '0.02'
            lst.standar_name = 'UVEG Land Surface Temperature TES Algorithm'
            
            e29 = out_nc.createVariable('UVEG_e29', np.uint8,('x','y'), zlib=True)
            e29.units = 'N/A'
            e29._Offset = '0.49'
            e29._Scale = '0.002'
            
            e31 = out_nc.createVariable('UVEG_e31', np.uint8,('x','y'), zlib=True)
            e31.units = 'N/A'
            e31._Offset = '0.49'
            e31._Scale = '0.002'
            
            e32 = out_nc.createVariable('UVEG_e32',np.uint8,('x','y'), zlib=True)
            e32.units = 'N/A'
            e32._Offset = '0.49'
            e32._Scale = '0.002'
            
            lst_error = out_nc.createVariable('UVEG_LST_error', np.uint8,('x','y'), zlib=True)
            lst_error.units = 'Kelvin K'
            lst_error._Offset = '0.0'
            lst_error._Scale = '0.04'
            
            e29_error = out_nc.createVariable('UVEG_e29_error', np.uint16,('x','y'), zlib=True)
            e29_error.units = 'N/A'
            e29_error._Offset = '0.0'
            e29_error._Scale = '0.0001'
            
            e31_error = out_nc.createVariable('UVEG_e31_error', np.uint16,('x','y'), zlib=True)
            e31_error.units = 'N/A'
            e31_error._Offset = '0.0'
            e31_error._Scale = '0.0001'
            
            e32_error = out_nc.createVariable('UVEG_e32_error',np.uint16,('x','y'), zlib=True)
            e32_error.units = 'N/A'
            e32_error._Offset = '0.0'
            e32_error._Scale = '0.0001'
            
            z_ = out_nc.createVariable('View_angle',np.uint8,('x','y'), zlib=True)
            z_.units = 'Degree*100'
            z_._Offset = '0.0'
            z_._Scale = '0.5'

            # write data                       
            lat[:] = self.latitud
            lon[:] = self.longitud
            lst[:] = UvegProcess.new_array(self.Ts, mask1_, self.dimension_original, data_type=np.uint16)
            e29[:] = UvegProcess.new_array(self.e[0,:], mask1_, self.dimension_original, data_type=np.uint8)
            e31[:] = UvegProcess.new_array(self.e[1,:], mask1_, self.dimension_original, data_type=np.uint8)
            e32[:] = UvegProcess.new_array(self.e[2,:], mask1_, self.dimension_original, data_type=np.uint8)
            lst_error[:] = UvegProcess.new_array(self.errTs, mask1_, self.dimension_original, data_type=np.uint8)
            e29_error[:] = UvegProcess.new_array(self.err_e29, mask1_, self.dimension_original, data_type=np.uint16)
            e31_error[:] = UvegProcess.new_array(self.err_e31, mask1_, self.dimension_original, data_type=np.uint16)
            e32_error[:] = UvegProcess.new_array(self.err_e32, mask1_, self.dimension_original, data_type=np.uint16)
            z_[:] = UvegProcess.new_array(self.z, mask1_, self.dimension_original, data_type=np.uint8)
            
            print('The image has been saved correctly!!!')
    
            out_nc.close() 
        except OSError as err:
            print("OS error: {0}".format(err))