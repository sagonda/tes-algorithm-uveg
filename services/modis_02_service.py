import netCDF4 as net
import numpy as np
 
class modis_02_Services():

    def __init__(self, f_Myd02_hours, hours_list, i_modis, cloud_mask_flag, dimension_original):
        self.f_Myd02_hours = f_Myd02_hours
        self.hours_list = hours_list
        self.i_modis = i_modis
        self.cloud_mask_flag = cloud_mask_flag
        self.dimension_original = dimension_original
    def modis_02(self):
        ''' 
        Resum: Function extract vars product myd021km
        
        Params: (f_Myd02, mask2)
        
        Output Matrix-> radiance, image_rad
        
        Call example: radiance, image_rad = modis_02(f_Myd02, mask2)
        '''
        try: 
            #*****Product MYD021KM
            myd02 = [net.Dataset(files) for files in self.f_Myd02_hours[self.hours_list]]
            
            # lat = myd02.variables['Latitude'][:]
            # lon = myd02.variables['Longitude'][:] 
            image_rad = [i.variables['EV_1KM_Emissive'] for i in myd02]
            gain = [i.variables['EV_1KM_Emissive'].radiance_scales for i in myd02]
            offset = [i.variables['EV_1KM_Emissive'].radiance_offsets for i in myd02]
            # image_ref1 = [i.variables['EV_1KM_RefSB'][:] for i in myd02]
            # gain1 = [i.variables['EV_1KM_RefSB'].radiance_scales for i in myd02]
            # offset1 = [i.variables['EV_1KM_RefSB'].radiance_offsets for i in myd02] 
            # hueco = [i.variables['EV_1KM_RefSB']._FillValue for i in myd02] 
            
            n = image_rad[self.i_modis][0,:,0].shape[0]
            m = image_rad[self.i_modis][0,0,:].shape[0]
            m_n = m * n

            radiance = np.empty(shape=(3,self.dimension_original,1354))
            radiance[0,:,:] = gain[self.i_modis][8] * (image_rad[self.i_modis][8,:,:] - offset[self.i_modis][8] )  
            radiance[1,:,:] = gain[self.i_modis][10] * (image_rad[self.i_modis][10,:,:] - offset[self.i_modis][10] )  
            radiance[2,:,:] = gain[self.i_modis][11] * (image_rad[self.i_modis][11,:,:] - offset[self.i_modis][11] )  
            
            radiance = np.where(self.cloud_mask_flag==0, 0, radiance)
            radiance = np.reshape(radiance.ravel(),(3,m_n))
            myd02[self.i_modis].close()

            return radiance, image_rad[:]
        except:
            
            print("Error in the path of the MODIS files")