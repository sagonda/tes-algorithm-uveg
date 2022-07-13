import netCDF4 as net
import numpy as np
from scipy import spatial
import glob
from pyhdf.SD import SD, SDC
from rttov_wrapper_f2py import *
from operator import itemgetter
from datetime import datetime
from datetime import timedelta
import csv
import re
import time
import os
import warnings

warnings.filterwarnings("ignore")
os.environ['HDF5_DISABLE_VERSION_CHECK']='2'

c1 = 0.998449
c2 = -0.654215
c3 = 0.735536 
K1 = [2631.58, 735.84, 471.25] 
K2 = [1686.18, 1306.72, 1195.27]

#***0.03  value ***
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

class processUveg():

    def __init__(self):
        A=1

    


    


    def tes_modis(self, lo, lup, ldown, trans, radiance, z=False, aux=False, recal=False):
        # Algorith TES
        try:
            
            radiance = np.where( radiance > 1, radiance, np.nan)
            dimension = lup.shape[1]
            # Create variables 
            e = np.empty(shape=(3,dimension),dtype = np.float64)
            R = np.empty(shape=(3,dimension),dtype = np.float64)
            BT = np.empty(shape=(3,dimension),dtype = np.float64)
            beta = np.empty(shape=(3,dimension),dtype = np.float64)
            rad = np.empty(shape=(3,dimension),dtype = np.float64)
            T = np.empty(shape=(3,dimension),dtype = np.float64)
            Ts = np.empty(shape=(1,dimension),dtype = np.float64)
            e[:,:] = 0.97 

            if aux:
                rad[:,:] = [((radiance[i,:] - lup[i,:]) / trans[i,:]) for i in range(3)]
                
            else:
                rad[:,:] = radiance
                
            for tes in range(8):
                R[:,:] = [(rad[i,:] - (1-e[i,:]) * ldown[i,:]) for i in range(3)]
                #T[:,:] = [K2[i]/np.log(K1[i]/R[i,:]+1) for i in range(3)] 
                T[:,:] = [(14387.7/lo[i]) * ((np.log(((1.19104e8 *e[i,:])/( (lo[i]**5) * R[i,:])) + 1)) **(-1)) for i in range(3)]

                Ts[:,:] = np.max(T[:,:],axis=0)
                #BT[:,:] = [K1[i]/(np.exp(K2[i]/Ts[0,:])-1) for i in range(3)]
                BT[:,:] = [1.19104e8 / (lo[i]**5 * (np.exp(14387.9/(lo[i]*Ts[0,:]))-1)) for i in range(3)]

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
        
            R[:,:] = [rad[i,:] - (1-e[i,:])*ldown[i,:] for i in range(3)]
            #T[:,:] = [K2[i]/np.log(K1[i]/R[i,:]+1) for i in range(3)] 
            T[:,:] = [ (14387.7/lo[i])*np.log(((1.19104e8*e[i,:])/(lo[i]**5*R[i,:]))+1)**(-1) for i in range(3)]
            Ts[:,:] = np.max(T[:,:],axis=0)
            #BT[:,:] = [K1[i]/(np.exp(K2[i]/Ts[0,:])-1) for i in range(3)]
            BT[:,:] = [1.19104e8/(lo[i]**5 * (np.exp(14387.9/(lo[i]*Ts[0,:]))-1)) for i in range(3)]
            e[:,:] = [R[i,:]/BT[i,:] for i in range(3)]
            
            if recal:
                print('Recalculando banda 31 y 32')
                e[1:,:] = [R[i,:]/BT[i,:] for i in range(1,3)]

            #***Error rad ****
            erad = np.empty(shape=(3,dimension),dtype = np.float64)
            eq1 = np.empty(shape=(3,dimension),dtype = np.float64)
            eq2 = np.empty(shape=(3,dimension),dtype = np.float64)
            
            
            
            eq1[:,:] = [d1_1[i]*trans[i,:]+d2_1[i]*trans[i,:]**2+d3_1[i]*z[:]+d4_1[i]*z[:]**2+d5_1[i]*trans[i,:]*z[:]+d6_1[i] for i in range(3)]
            eq2[:,:] = [f1_1[i]*lup[i,:]+f2_1[i]*lup[i,:]**2+f3_1[i]*z[:]+f4_1[i]*z[:]**2+f5_1[i]*lup[i,:]*z[:]+f6_1[i] for i in range(3)]
            erad[:,:]=[(((0.003*radiance[i,:]/trans[i,:])**2+(eq2[i,:]/trans[i,:])**2+(eq1[i,:]*((radiance[i,:]-lup[i,:]))/(trans[i,:]**2))**2)**0.5) for i in range(3)]
           
            return Ts.ravel(), e, BT, rad, R, erad

        except OSError as err:
            print("OS error: {0}".format(err))


    def variables(self, sk):    
    
        # Constantes planck
        consA = np.float64(119110000.0)
        consB = np.float64(14388.0)
        lonOnda29 = np.float64(8.55)
        lonOnda31 = np.float64(11.015)
        lonOnda32 = np.float64(12.02)
        nOnda29 = np.float64(1173.263)
        nOnda31 = np.float64(908.273)
        nOnda32 = np.float64(831.523)
       
        # Variables globales
        Lbb29 = (consA)/(np.power(lonOnda29,5) * (np.exp(consB/(lonOnda29*sk))-1))
        Lbb31 = (consA)/(np.power(lonOnda31,5) * (np.exp(consB/(lonOnda31*sk))-1))
        Lbb32 = (consA)/(np.power(lonOnda32,5) * (np.exp(consB/(lonOnda32*sk))-1))
    
        emissivity = 0.98
        lo = [8.535, 11.015, 12.041]
    
        return consA, consB, lonOnda29, lonOnda31, lonOnda32 ,nOnda29, nOnda31, nOnda32, Lbb29, Lbb31, Lbb32, emissivity, lo
    
      
    def recl_e(self, emiss, dimension):
        
        mask_e = np.where(emiss > 0.992)
        e_max = emiss[mask_e]
        dif = e_max - 0.992
        e_ori_dif = emiss[:,mask_e] - dif
        e_mod = np.zeros(shape=(3,dimension),dtype = np.float64)
        e_mod = emiss
        e_mod[:,mask_e] = e_ori_dif
        
        return e_mod
    
    def FVC(self, ndvi, e31, e32):
        
        try:
            FVC = np.empty(shape=(ndvi.shape))
            fvc_E31 = np.empty(shape=(ndvi.shape))
            fvc_E32 = np.empty(shape=(ndvi.shape))
            e31_ = np.empty(shape=(ndvi.shape))
            e32_ = np.empty(shape=(ndvi.shape))
            
            FVC[:] = ((ndvi[:] - 0.2) / np.float32(0.5 - 0.2))**2
            FVC[:] = np.where(FVC > 1, 1, FVC)
            FVC[:] = np.where(FVC < 0, np.nan, FVC)

            e31_[:] = e31[:]
            e32_[:] = e32[:]
            
            c_veg = np.where(ndvi >= 0.2)
            c_soil = np.where(ndvi < 0.2)
            
            e31_[c_veg] = 0.968 + 0.021 * FVC[c_veg]
            e32_[c_veg] = 0.974 + 0.015 * FVC[c_veg]
              
            return e31_, e32_
        except OSError as err:
              print("OS error: {0}".format(err))
    
   
    def sw(self, lo, radiance, dimension, e_29_original, e31_fvc, e32_fvc, ldown, R, trans, Ts, aux = False, aux1 = False):
        
        try:
            e_recal = np.empty(shape=(3,dimension),dtype = np.float64)
            BT_recal = np.empty(shape=(3,dimension),dtype = np.float64)
            rad_recal = np.empty(shape=(3,dimension),dtype = np.float64)
            T31 = np.empty(shape=(dimension),dtype = np.float64)
            T32 = np.empty(shape=(dimension),dtype = np.float64)
            Tsw = np.empty(shape=(dimension),dtype = np.float64)
            
            if aux:
                #radiance = np.where( radiance > 1, radiance, np.nan)
    
                a0=-0.004
                a1=2.625
                a2=0.424
                a3=41.4
                a4=0.04
                a5=-201
                a6=26.6
    
                ww=-68.80969804*trans[0,:]+38.35444487*trans[0,:]**2+53.74448404*trans[1,:]-40.96607658*trans[2,:]+18.44174348
    
                #**********************Split Window************************
                T31[:] = (14387.7/np.float64(lo[1]))*((np.log(((1.19104e8)/np.float64(((lo[1]**5)*radiance[1,:])))+1))**(-1))
                T32[:] = (14387.7/np.float64(lo[2]))*((np.log(((1.19104e8)/np.float64(((lo[2]**5)*radiance[2,:])))+1))**(-1))
    
                Tsw[:] = a0+T31+a1*(T31-T32)+a2*(T31-T32)**2+(a3+a4*ww)*(1-(e31_fvc+e32_fvc)/np.float(2))+(a5+a6*ww)*(e31_fvc-e32_fvc)
               
                c_camb = np.where(np.abs(Tsw - Ts) > 1.5)
    
                Ts[c_camb] = Tsw[c_camb]#Donde la diferencia de LST sea > a 1.5 Ts = TSW  
                
            if aux1:
            
                BT_recal[:,:] = [1.19104e8/np.float64(lo[i]**5*(np.exp(14387.9/np.float64(lo[i]*Ts))-1)) for i in range(3)]
                e_recal[:,:] = [R[i,:]/np.float64(BT_recal[i,:]) for i in range(3)]
                rad_recal[:,:] = [e_recal[i,:]*np.float64(BT_recal[i,:])+((1-e_recal[i,:])*ldown[i,:]) for i in range(3)] # guardar radiancia anterior
    
            return rad_recal
        
        except OSError as err:
            print("OS error: {0}".format(err))
    
    
                

    def new_array(self, array, mask, dimension_original, data_type):
        new = np.empty([dimension_original, 1354], dtype = data_type)
        new[:] = 0
        new[mask] = array
        
        return new
    

    def create_nc_outfile(self, path_output, year, month, day, date_modis, dimension_original,\
                          latitud, longitud, Ts, e, mask_original_modis, toma,  errTs, err_e29, err_e31, err_e32, z):
        
        try:
           
            ###### Create *nc out file  
            mask1_ = mask_original_modis
            path = str(path_output)                      
            out_nc = net.Dataset(path+year+'/'+month+'/'+day+'/'+'TES_'+year+month+day+'_'+date_modis+'_'+toma+'.nc',mode='w',format='NETCDF4')                              
    
            
            ####### Create dimesions 
            x = out_nc.createDimension('x', dimension_original)
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
            lat[:] = latitud
            lon[:] = longitud
            lst[:] = UvegProcess.new_array(Ts, mask1_, dimension_original, data_type=np.uint16)
            e29[:] = UvegProcess.new_array(e[0,:], mask1_, dimension_original, data_type=np.uint8)
            e31[:] = UvegProcess.new_array(e[1,:], mask1_, dimension_original, data_type=np.uint8)
            e32[:] = UvegProcess.new_array(e[2,:], mask1_, dimension_original, data_type=np.uint8)
            lst_error[:] = UvegProcess.new_array(errTs, mask1_, dimension_original, data_type=np.uint8)
            e29_error[:] = UvegProcess.new_array(err_e29, mask1_, dimension_original, data_type=np.uint16)
            e31_error[:] = UvegProcess.new_array(err_e31, mask1_, dimension_original, data_type=np.uint16)
            e32_error[:] = UvegProcess.new_array(err_e32, mask1_, dimension_original, data_type=np.uint16)
            z_[:] = UvegProcess.new_array(z, mask1_, dimension_original, data_type=np.uint8)
            
            print('The image has been saved correctly!!!')
    
            out_nc.close() 
        except OSError as err:
            print("OS error: {0}".format(err))
    
    
    def packed_value(self, input_matrix, add_offset, scale_factor, data_type):
        if input_matrix.ndim == 2:
            result = np.empty((input_matrix.shape[0],input_matrix.shape[1]), dtype = data_type)
        elif input_matrix.ndim == 1:
            result = np.empty(input_matrix.shape[0], dtype = data_type)
        result[:] = (input_matrix - add_offset) / scale_factor
        return result
    
  
    def unpacked_value(self, packed_value, add_offset, scale_factor):
        return (packed_value * scale_factor) + add_offset