#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created: 2020
version: v1.1
Content: Library process RTTOV

@author: DANIEL SALINAS GONZALEZ
         UCG (UNIT GLOBAL CHANGE)
         IPL (Image Processing Laboratory)
"""

# Importamos las librerias
from services import bits_stripping_service
from services import call_rttov_service
from services import cloud_mas_service
from services import create_nc_outfile_service
from services import create_profiles_service
from services import FCV_service
from services import modis_02_service
from services import new_array_service
from services import packed_value_service
from services import process
from services.reader import readerUveg
from services import recl_e_service
from services import sw_services
from services import tes_modis_service
from services import unpacked_value_service
from utilities import *


import netCDF4 as net
import numpy as np
from scipy import spatial
import glob
from rttov_wrapper_f2py import *
from operator import itemgetter
from datetime import datetime
from datetime import timedelta
import re
import time
import os
import warnings
import time
from calendar import monthrange
import sys
import gc

from run_processv3 import UvegProcess as rt

warnings.filterwarnings("ignore")
os.environ['HDF5_DISABLE_VERSION_CHECK']='2'

year = sys.argv[1]
month = sys.argv[2]
# year = '2016'
# month = '08'
INIT = 1
output_path_images_uveg ='/gws/nopw/j04/esacci_lst/UV/output_uveg/'
input_path_images_ndvi = '/gws/nopw/j04/esacci_lst/UV/data/ndvi/'
input_path_images_collection61 = '/neodc/modis/data/MYD03/collection61/'
input_path_images_MYD021KM = '/neodc/modis/data/MYD021KM/collection61/'
input_path_images_MYD35_L2 =  '/neodc/modis/data/MYD35_L2/collection61/'
input_path_images_invariants = '/badc/ecmwf-era5/data/invariants/'
input_path_images_ecmwfera5_an_ml = '/badc/ecmwf-era5/data/oper/an_ml/'
input_path_images_ecmwfera5_an_sfc = '/badc/ecmwf-era5/data/oper/an_sfc/'
input_path_images_ecmwfera51_an_ml = '/badc/ecmwf-era51/data/oper/an_ml/'
input_path_images_ecmwfera51_an_sfc = '/badc/ecmwf-era51/data/oper/an_sfc/'
input_path_images_rtcoef_rttov12 = '/gws/nopw/j04/esacci_lst/UV/software/rttov12/rtcoef_rttov12/'


try:
    
    if os.path.isfile(output_path_images_uveg+year+'/'+month+'/'+year+month+'.csv'):
        print('Existe el archivo de rutas')
        INIT , hour = rt.read_csv_files(output_path_images_uveg+year+'/'+month+'/', year, month)
    else:
        hour = '0000'
        print('No existe archivo de rutas')
    
except Exception as e: 
    print(e)

print('Process year:',year,'month:', month)
num_days = monthrange(int(year), int(month))[1]
print('INIT:',INIT)

for day_ in range(int(INIT), num_days+1):
    try:
        day = str(day_).zfill(2)
        print('day:',day)

        if not os.path.exists(output_path_images_uveg+year+'/'+month+'/'+day+'/'):
            os.makedirs(output_path_images_uveg+year+'/'+month+'/'+day+'/')
        
        #----------Read NDVI----------
        ndvi_lat, ndvi_lon, ndvi = readerUveg.read_ndvi_file(input_path_images_ndvi, year, month)
        
        #***********init time********
        start_time = time.time()
        
        #----------Read MYD03 files------
        lista_files_Myd03 = readerUveg.read_myd03_files(input_path_images_collection61,  year, month, day)
        
        #---------Read Myd021km files....
        lista_files_Myd02 = readerUveg.read_myd021_files(input_path_images_MYD021KM,  year, month, day)
        
        #---------Read Myd35 files....
        lista_files_Myd35 = rt.read_myd021_files(input_path_images_MYD35_L2,  year, month, day)
        
        #---------Match files------------
        f_Myd03, f_Myd02, f_Myd35 = rt.match_myd03_myd021_myd35(lista_files_Myd03 , lista_files_Myd02, lista_files_Myd35)
        
        #---------Match files------------
        hours, f_Myd03_hours, f_Myd02_hours, f_Myd35_hours = rt.read_match_files(f_Myd03, f_Myd02, f_Myd35)
        #print(hours, f_Myd03_hours, f_Myd02_hours, f_Myd35_hours)
        
        mask_sea_land_era5 = rt.extract_mask_land(input_path_images_invariants)
        print('Se van a procesar: ', len(f_Myd03), 'imagenes!!')
        INIT_HOURS = hours.index(hour)
        print('INIT_HOURS:',INIT_HOURS)
        print('len_hours:', len(hours))
        
        for hours_list in range(INIT_HOURS, len(hours)): 
            try:     
                cloud_Masks = rt.cloud_mask(f_Myd35_hours, hours_list)
                height, lat_Myd03, lon_Myd03, zsat, mask_sea_land_modis, name, rep, data_Myd03 = rt.extract_vars_myd03(f_Myd03_hours, hours_list)
                if os.path.exists(input_path_images_ecmwfera5_an_ml+year+'/'+month+'/'+day+'/'):
                    file_data = 'ecmwf-era5_oper_an_ml_'
                    temp_era, hum_E, lat_Nc, lon_Nc = rt.extract_vars_era5(input_path_images_ecmwfera5_an_ml, year, month, day, mask_sea_land_era5, hours, hours_list, file_data)
                else:
                    file_data = 'ecmwf-era51_oper_an_ml_'
                    temp_era, hum_E, lat_Nc, lon_Nc = rt.extract_vars_era5(input_path_images_ecmwfera51_an_ml, year, month, day, mask_sea_land_era5, hours, hours_list, file_data)
                
                if os.path.exists(input_path_images_ecmwfera5_an_sfc+year+'/'+month+'/'+day+'/'):
                    file_data_ = 'ecmwf-era5_oper_an_sfc_'
                    t2m, skt, d2m, msl1, level = rt.extract_vars2m_era5(input_path_images_ecmwfera5_an_sfc,year, month, day, mask_sea_land_era5, hours, hours_list, file_data_)
                    
                else:
                    file_data_ = 'ecmwf-era51_oper_an_sfc_'
                    t2m, skt, d2m, msl1, level = rt.extract_vars2m_era5(input_path_images_ecmwfera51_an_sfc,year, month, day, mask_sea_land_era5, hours, hours_list, file_data_)

            except Exception as e: 
                print(e)
            
            for i_modis in range(rep):
                try:
                    import time
                    #***********init time********
                    start_time_0 = time.time()

                    date_modis = name[i_modis].split('/')
                    date_modis = date_modis[-1].split('.')
                    date_modis = date_modis[-4]
                    print('time image:', date_modis, ' for the day ', day)
                    a = data_Myd03[i_modis].__dict__
                    b = a['CoreMetadata.0']
                    c = b.split()
                    toma = c[68].split('"')[1]
                    print('TOMA:', toma)
                    
                    if os.path.isfile(output_path_images_uveg+year+'/'+month+'/'+day+'/'+'TES_'+year+month+day+'_'+str(date_modis)+'_'+str(toma)+'.nc'):
                        print('Existe el archivo')
                        continue
                    else:
                        print('Archivo no procesado, procesando!!')     

                    h_03 = height[i_modis]
                    s_Z = zsat[i_modis]
                    cloud_mask = cloud_Masks[i_modis]
                    cloud_mask_flag = rt.bits_stripping(1,2,cloud_mask[0,:,:])
                    dimension = h_03.shape[0]
                    dimension_original = dimension
                    latitud = lat_Myd03[i_modis]
                    longitud = lon_Myd03[i_modis]

                    lat_Modis, lon_Modis, mask_land_modis, mask_original_modis = rt.extract_index_image(lat_Myd03[i_modis], lon_Myd03[i_modis], mask_sea_land_modis[i_modis], dimension)

                    ndvi_d = rt.extract_ndvi(lat_Modis, lon_Modis, ndvi_lat, ndvi_lon, ndvi)
                    
                    if ndvi_d.size > 0:
                        print('Process with NDVI')
                    else:
                        continue

                    index_Era, lat, lon = rt.extract_index_modis_and_era(lat_Nc, lon_Nc, lat_Modis, lon_Modis, mask_sea_land_era5)
                    
                    date_era5 = year+month+day
                    
                    h_ = rt.extract_height(h_03, mask_land_modis, cloud_mask_flag)
                    print('Pixeles a procesar:', h_.shape)

                    z = rt.extract_zenith(s_Z, mask_land_modis, cloud_mask_flag)
                    t_ = rt.extract_temperature(temp_era, index_Era)
                    he = rt.extract_humidity(hum_E, index_Era)
                    t2, sk, p2m, q2m = rt.extract_param_2m(t2m, skt, d2m, msl1, index_Era, h_)
                    dimension_modis_ravel = z.shape[0]
                   
                    datetimes, angles, surftype, surfgeom, s2m, skin, simplecloud, clwscheme, icecloud, \
                                            zeeman, p, t = rt.create_profiles(dimension_modis_ravel, \
                                                            z, lat_Modis, lon_Modis, h_, p2m, t2, q2m,  \
                                                            sk, level, t_, year, month, day)
                    path_nc_file = output_path_images_uveg
                    nc_file = net.Dataset(path_nc_file+year+'/'+month+'/'+day+'/'+'TES_'+year+month+day+'_'+date_modis+'_'+toma+'.nc',mode='w',format='NETCDF4')
                    nc_file.close()
                    print('Se ha creado el archivo temporal:', path_nc_file+year+'/'+month+'/'+day+'/'+'TES_'+year+month+day+'_'+date_modis+'_'+toma+'.nc')
                    bt, radtotal, radup, raddown, tautotal  = rt.call_rttov(input_path_images_rtcoef_rttov12, datetimes, angles, \
                                                            surfgeom, surftype, s2m, skin, simplecloud, clwscheme, \
                                                                icecloud, zeeman, p, t, he)
                    
                    consA, consB, lonOnda29, lonOnda31, lonOnda32, nOnda29, nOnda31, nOnda32, Lbb29,\
                                                        Lbb31, Lbb32, emissivity, lo = rt.variables(sk)
                
                    Lup_29, Lup_31, Lup_32, Ldown_29, Ldown_31, Ldown_32 = rt.chance_units(consA, consB, bt, radtotal,\
                                        radup, raddown, tautotal, emissivity,  nOnda29, nOnda31, nOnda32,\
                                            lonOnda29, lonOnda31, lonOnda32, Lbb29, Lbb31, Lbb32)
                    
                    lup = np.array((Lup_29, Lup_31, Lup_32),dtype = np.float64) 
                    ldown = np.array((Ldown_29,Ldown_31, Ldown_32),dtype = np.float64) 
                    trans = tautotal
                
                    radiance, image_rad = rt.modis_02(f_Myd02_hours, hours_list, i_modis, cloud_mask_flag, dimension_original) 
                    radiance = radiance[:,mask_land_modis]
                    
                    ###########TES UVEG###################
                    Ts, e, BT, rad, R, erad = rt.tes_modis(lo, lup, ldown, trans, radiance, z=z.ravel(), aux = True, recal=False)
                    e_original = np.zeros(shape=(3,dimension_modis_ravel),dtype = np.float64)
                    e_original[:,:] = e[:,:]
                    e_mod = rt.recl_e(e, dimension_modis_ravel)
                    e31_fvc, e32_fvc = rt.FVC(ndvi_d.ravel(), e_mod[1,:], e_mod[2,:])
                    
                    #*****************Errors***************
                    radiance1 = np.empty(shape=(3,dimension_modis_ravel),dtype = np.float64)
                    radiance2 = np.empty(shape=(3,dimension_modis_ravel),dtype = np.float64)
                    errTs = np.empty(shape=(dimension_modis_ravel),dtype = np.float64)
                    err_e29 = np.empty(shape=(dimension_modis_ravel),dtype = np.float64)
                    err_e31 = np.empty(shape=(dimension_modis_ravel),dtype = np.float64)
                    err_e32 = np.empty(shape=(dimension_modis_ravel),dtype = np.float64)
            
                    radiance1[:,:] = rad[:,:] + erad[:,:]
                    radiance2[:,:] = rad[:,:] - erad[:,:]
                    
                    def ldown_error(ldown29, ldown31, ldown32, z, dimension_modis_ravel):
                        
                        err_ldown = np.zeros(shape=(3,dimension_modis_ravel),dtype = np.float64)
                        c1_29 = 0.018690841; c1_31 = 0.024681043; c1_32 = 0.025080562
                        c2_29 = -0.000014073; c2_31 = 0.000003659; c2_32 = 0.000001100
                        c3_29 = 0.000002232; c3_31 = 0.000001042; c3_32 = 0.000000949
                        c4_29 = -0.001359401; c4_31 = -0.002232340; c4_32 = -0.002368573
                        c5_29 = 0.000000323; c5_31 = -0.000000011; c5_32 = 0.000000131
                        c0_29 = -0.004099838; c0_31 = 0.001119390; c0_32 = 0.000240263
                        
                        b29 = c0_29 + c1_29*ldown29 + c2_29*z + c3_29*ldown29*z + c4_29*ldown29**2 + c5_29*z**2
                        b31 = c0_31 + c1_31*ldown31 + c2_31*z + c3_31*ldown31*z + c4_31*ldown31**2 + c5_31*z**2
                        b32 = c0_32 + c1_32*ldown32 + c2_32*z + c3_32*ldown32*z + c4_32*ldown32**2 + c5_32*z**2
                        err_ldown[0,:] = b29
                        err_ldown[1,:] = b31
                        err_ldown[2,:] = b32
                        
                        return err_ldown
                    
                    err_ldown = ldown_error(ldown[0,:], ldown[1,:], ldown[2,:], z.ravel(), dimension_modis_ravel)
                    
                    ldown1 = np.empty(shape=(3, dimension_modis_ravel),dtype = np.float64)
                    ldown2 = np.empty(shape=(3, dimension_modis_ravel),dtype = np.float64)
                    
                    ldown1[:,:] = ldown + err_ldown
                    ldown2[:,:] = ldown - err_ldown
                    
                    ###########TES UVEG###################
                    Ts1, e1, rad1, BT1,  R1, erad1 = rt.tes_modis(lo, lup, ldown1, trans, radiance1, z=z.ravel(), aux=False, recal=False)
                    Ts2, e2, rad2, BT2,  R2, erad2 = rt.tes_modis(lo, lup, ldown2, trans, radiance2, z=z.ravel(), aux=False, recal=False)
            
                    e1_mod = rt.recl_e(e1, dimension_modis_ravel)
                    e2_mod = rt.recl_e(e2, dimension_modis_ravel)
            
                    e1_31_fvc, e1_32_fvc = rt.FVC(ndvi_d.ravel(), e1_mod[1,:], e1_mod[2,:])
                    e2_31_fvc, e2_32_fvc = rt.FVC(ndvi_d.ravel(), e2_mod[1,:], e2_mod[2,:])
            
                    rad_recal_e1 = rt.sw(lo, radiance1, dimension_modis_ravel, e1[0,:], e1_31_fvc, e1_32_fvc, ldown1, R1, trans, Ts1, aux = False, aux1 = True)
                    rad_recal_e2 = rt.sw(lo, radiance2, dimension_modis_ravel, e2[0,:], e2_31_fvc, e2_32_fvc, ldown2, R2, trans, Ts2, aux = False, aux1 = True)
                    ###########TES UVEG###################
                    Ts1_, e1_, rad1_, BT1_,  R1_, erad1_ = rt.tes_modis(lo, lup, ldown1, trans, rad_recal_e1, z=z.ravel(), aux=False, recal=False)
                    Ts2_, e2_, rad2_, BT2_,  R2_, erad2_ = rt.tes_modis(lo, lup, ldown2, trans, rad_recal_e2, z=z.ravel(), aux=False, recal=False)
            
                    errTs[:] = np.abs((Ts1_-Ts2_)/2)
                    err_e29[:] = np.abs((e1_[0,:]-e2_[0,:])/2)
                    err_e31[:] = np.abs((e1_[1,:]-e2_[1,:])/2)
                    err_e32[:] = np.abs((e1_[2,:]-e2_[2,:])/2)
                    
                    e_29_original = e_original[0,:]
                    
                    #******Split Window*****
                    rad_recal = rt.sw(lo, radiance, dimension_modis_ravel, e_29_original, e31_fvc, e32_fvc, ldown, R, trans, Ts, aux = True, aux1 = True)
                    ###########TES UVEG###################
                    Ts_1, e_1, BT_, rad_1, R_1, erad_1 = rt.tes_modis(lo, lup, ldown, trans, rad_recal, z=z.ravel(), aux=False, recal=True)
                    Ts_1 = np.round(Ts_1, 2)
                    Ts_1_int = rt.packed_value(Ts_1, 0.0, 0.02, data_type=np.uint16)

                    e_1 = np.round(e_1, 3)
                    e_1_int = rt.packed_value(e_1, 0.49, 0.002, data_type=np.uint8)
                    
                    errTs = np.round(errTs, 2)
                    errTs_int = rt.packed_value(errTs, 0.0, 0.04, data_type=np.uint8)                    
                    
                    err_e29 = np.round(err_e29, 4)
                    err_e29_int = rt.packed_value(err_e29, 0.0, 0.0001, data_type=np.uint16)
                    
                    err_e31 = np.round(err_e31, 4)
                    err_e31_int = rt.packed_value(err_e31, 0.0, 0.0001, data_type=np.uint16)
                    
                    err_e32 = np.round(err_e32, 4)
                    err_e32_int = rt.packed_value(err_e32, 0.0, 0.0001, data_type=np.uint16)
                    
                    z = np.round(z, 2)
                    z_int = rt.packed_value(z, 0.0, 0.5, data_type=np.uint8)

                    latitud_int = (latitud*10000).astype(np.int32)
                    longitud_int = (longitud*10000).astype(np.int32)
                    if os.path.exists(path_nc_file+year+'/'+month+'/'+day+'/'+'TES_'+year+month+day+'_'+date_modis+'_'+toma+'.nc'):
                        os.remove(path_nc_file+year+'/'+month+'/'+day+'/'+'TES_'+year+month+day+'_'+date_modis+'_'+toma+'.nc')
                        print('Archivo borrado')
                    else:
                        print('No se ha borrado el archivo')
                    rt.create_nc_outfile(output_path_images_uveg, year, month, day, date_modis, dimension_original,\
                                    latitud_int, longitud_int, Ts_1_int, e_1_int, mask_original_modis, toma,  errTs_int, err_e29_int, err_e31_int, err_e32_int, z_int)
                    
                    rt.write_csv_files(output_path_images_uveg+year+'/'+month+'/', 'TES_'+year+month+day+'_'+date_modis+'_'+toma+'.nc', year, month)
                    
                    elapsed_time_0 = time.time() - start_time_0
                    print(' Time process file: ',elapsed_time_0)
                    
                    del t2, sk, p2m, q2m, index_Era, h_
                    del datetimes, angles, surftype, surfgeom, s2m, skin, simplecloud, clwscheme, icecloud, \
                                            zeeman, p, t, dimension_modis_ravel, \
                                                            z, lat_Modis, lon_Modis, t_, date_era5, date_modis
                    del bt, radtotal, radup, raddown, tautotal
                    del consA, consB, lonOnda29, lonOnda31, lonOnda32, nOnda29, nOnda31, nOnda32, Lbb29,\
                                                        Lbb31, Lbb32, emissivity, lo
                    del Lup_29, Lup_31, Lup_32, Ldown_29, Ldown_31, Ldown_32
                    del lup, ldown, trans, radiance
                    del radiance1
                    del ldown2, radiance2
                    del e1_31_fvc, e1_32_fvc
                    del e2_31_fvc, e2_32_fvc
                    del rad_recal_e1, rad_recal_e2
                    del Ts1_, e1_, rad1_, BT1_,  R1_, erad1_
                    del rad_recal, Ts_1, e_1, BT_, rad_1, R_1, erad_1, Ts2_, e2_, rad2_, BT2_,  R2_, erad2_
                    del latitud, longitud, Ts_1_int, e_1_int, errTs_int, err_e29_int, err_e31_int, err_e32_int, z_int
                    del a, b, c, e, e1, e1_mod, e2, e2_mod, e31_fvc, e32_fvc, e_29_original, e_mod, e_original, erad, erad1, erad2, err_e29
                    del err_e31, err_e32, err_ldown, errTs, h_03, he, image_rad, lat, ldown1, lon
                    del mask_land_modis, mask_original_modis, ndvi_d, R, R1, R2
                    del rad, rad1, rad2, s_Z, Ts, Ts1, Ts2
                    gc.collect()

                #except:
                     #continue
                except Exception as e: 
                    print(e)
            del temp_era, hum_E, lat_Nc, lon_Nc, t2m, skt, d2m, msl1, level
            gc.collect()
        elapsed_time = time.time() - start_time
        print(' Time read files: ',elapsed_time)
        hour = '0000'
        
    # except:
    #     continue
    except Exception as e: 
        print(e)
        
del ndvi, ndvi_lat, ndvi_lon, mask_sea_land_era5, start_time, elapsed_time, f_Myd02, hours, f_Myd03_hours, f_Myd02_hours
del year, month, day, num_days
gc.collect() 

globals().clear()

            
    
