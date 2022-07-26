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

# Importamos las libreriasP

from nbformat import read
from services.call_rttov_service import call_rttov_services
from services.cloud_mas_service import cloud_mask_services
from services.bits_stripping_service import bits_stripping_services
from services.create_nc_outfile_service import create_nc_outfile_services
from services.create_profiles_service import create_profiles_services
from services.FCV_service import FCV_services
from services.modis_02_service import modis_02_Services
from services.new_array_service import new_array_services
from services.packed_value_service import packed_value_services
from services.process import processUveg
from services.reader import readerUveg
from services.recl_e_service import recl_services
from services.sw_services import sw_services
from services.tes_modis_service import tes_modis_services
from services.unpacked_value_service import unpacked_value_services
from services.err_ldown_service import err_ldown_services
from utilities.utilities import utilitiesUveg

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
import traceback
from utilities.utilities import utilitiesUveg 


warnings.filterwarnings("ignore")
os.environ['HDF5_DISABLE_VERSION_CHECK'] = '2'

# year = sys.argv[1]
# month = sys.argv[2]
year = '2016'
month = '08'
INIT = 4
# output_path_images_uveg ='/gws/nopw/j04/esacci_lst/UV/output_uveg/'
# input_path_images_ndvi = '/gws/nopw/j04/esacci_lst/UV/data/ndvi/'
# input_path_images_collection61 = '/neodc/modis/data/MYD03/collection61/'
# input_path_images_MYD021KM = '/neodc/modis/data/MYD021KM/collection61/'
# input_path_images_MYD35_L2 =  '/neodc/modis/data/MYD35_L2/collection61/'
# input_path_images_invariants = '/badc/ecmwf-era5/data/invariants/'
# input_path_images_ecmwfera5_an_ml = '/badc/ecmwf-era5/data/oper/an_ml/'
# input_path_images_ecmwfera5_an_sfc = '/badc/ecmwf-era5/data/oper/an_sfc/'
# input_path_images_ecmwfera51_an_ml = '/badc/ecmwf-era51/data/oper/an_ml/'
# input_path_images_ecmwfera51_an_sfc = '/badc/ecmwf-era51/data/oper/an_sfc/'
# input_path_images_rtcoef_rttov12 = '/gws/nopw/j04/esacci_lst/UV/software/rttov12/rtcoef_rttov12/'


output_path_images_uveg = '/home/sagonda/Documentos/archive/output_recal'
input_path_images_ndvi = '/home/sagonda/Documentos/archive/NDVI/'
input_path_images_collection61 = '/home/sagonda/Documentos/archive/myd03/'
input_path_images_MYD021KM = '/home/sagonda/Documentos/archive/myd021/'
input_path_images_MYD35_L2 = '/home/sagonda/Documentos/archive/myd35/'
input_path_images_invariants = '/home/sagonda/Documentos/archive/invariants/'
input_path_images_ecmwfera5_an_ml = '/home/sagonda/Documentos/archive/an_ml/'
input_path_images_ecmwfera5_an_sfc = '/home/sagonda/Documentos/archive/an_sfc/'
input_path_images_ecmwfera51_an_ml = '/home/sagonda/Documentos/archive/an_ml'
input_path_images_ecmwfera51_an_sfc = '/home/sagonda/Documentos/archive/an_sfc/'
input_path_images_rtcoef_rttov12 = '/usr/local/rttov12/rtcoef_rttov12/'


try:

    if os.path.isfile(output_path_images_uveg+year+'/'+month+'/'+year+month+'.csv'):
        print('Existe el archivo de rutas')
        INIT, hour = readerUveg.read_csv_files(
            output_path_images_uveg+year+'/'+month+'/', year, month)
    else:
        hour = '0100'
        print('No existe archivo de rutas')

except Exception as e: 
    print(e)



print('Process year:', year, 'month:', month)
num_days = monthrange(int(year), int(month))[1]
print('INIT:', INIT)

for day_ in range(int(INIT), 5):  # num_days+1):
   
    try:
        day = str(day_).zfill(2)
        print('day:', day)
     

        if not os.path.exists(output_path_images_uveg+year+'/'+month+'/'+day+'/'):
            os.makedirs(output_path_images_uveg+year+'/'+month+'/'+day+'/')

        reader = readerUveg(year, month, day, input_path_images_ndvi, input_path_images_collection61,
                            input_path_images_MYD021KM, input_path_images_MYD35_L2, output_path_images_uveg)

        # ----------Read NDVI----------
        ndvi_lat, ndvi_lon, ndvi = reader.read_ndvi_file()

        # ***********init time********
        start_time = time.time()
    
        # ----------Read MYD03 files------
        lista_files_Myd03 = reader.read_myd03_files()

        # ---------Read Myd021km files....
        lista_files_Myd02 = reader.read_myd021_files()

        # ---------Read Myd35 files....
        lista_files_Myd35 = reader.read_myd35_files()

        # ---------Match files------------
        f_Myd03, f_Myd02, f_Myd35 = reader.match_myd03_myd021_myd35(
            lista_files_Myd03, lista_files_Myd02, lista_files_Myd35)

        # ---------Match files------------
        hours, f_Myd03_hours, f_Myd02_hours, f_Myd35_hours = reader.read_match_files(f_Myd03, f_Myd02, f_Myd35)
        #print(hours, f_Myd03_hours, f_Myd02_hours, f_Myd35_hours)
        
        mask_sea_land_era5 = utilitiesUveg.extract_mask_land(
            input_path_images_invariants)
        print('Se van a procesar: ', len(f_Myd03), 'imagenes!!')
        INIT_HOURS = hours.index(hour)
        print('INIT_HOURS:', INIT_HOURS)
        print('len_hours:', len(hours))


        for hours_list in range(INIT_HOURS, 2):#len(hours)):

            cloud = cloud_mask_services(f_Myd35_hours, hours_list)

            try:
                cloud_Masks = cloud.cloud_mask()
                height, lat_Myd03, lon_Myd03, zsat, mask_sea_land_modis, name, rep, data_Myd03 = utilitiesUveg.extract_vars_myd03(
                    f_Myd03_hours, hours_list)
                if os.path.exists(input_path_images_ecmwfera5_an_ml+year+'/'+month+'/'+day+'/'):
                    file_data = 'ecmwf-era5_oper_an_ml_'
                    temp_era, hum_E, lat_Nc, lon_Nc = utilitiesUveg.extract_vars_era5(
                        input_path_images_ecmwfera5_an_ml, year, month, day, mask_sea_land_era5, hours, hours_list, file_data)
                else:
                    file_data = 'ecmwf-era51_oper_an_ml_'
                    temp_era, hum_E, lat_Nc, lon_Nc = utilitiesUveg.extract_vars_era5(
                        input_path_images_ecmwfera51_an_ml, year, month, day, mask_sea_land_era5, hours, hours_list, file_data)

                if os.path.exists(input_path_images_ecmwfera5_an_sfc+year+'/'+month+'/'+day+'/'):
                    file_data_ = 'ecmwf-era5_oper_an_sfc_'
                    t2m, skt, d2m, msl1, level = utilitiesUveg.extract_vars2m_era5(
                        input_path_images_ecmwfera5_an_sfc, year, month, day, mask_sea_land_era5, hours, hours_list, file_data_)

                else:
                    file_data_ = 'ecmwf-era51_oper_an_sfc_'
                    t2m, skt, d2m, msl1, level = utilitiesUveg.extract_vars2m_era5(
                        input_path_images_ecmwfera51_an_sfc, year, month, day, mask_sea_land_era5, hours, hours_list, file_data_)

            except Exception as e: 
                print(e)

            print("ok")

            for i_modis in range(rep):
                try:
                    import time
                    # ***********init time********
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

                    # if os.path.isfile(output_path_images_uveg+year+'/'+month+'/'+day+'/'+'TES_'+year+month+day+'_'+str(date_modis)+'_'+str(toma)+'.nc'):
                    #     print('Existe el archivo')
                    #     continue
                    # else:
                    #     print('Archivo no procesado, procesando!!')

                    

                    h_03 = height[i_modis]
                    s_Z = zsat[i_modis]
                    cloud_mask = cloud_Masks[i_modis]
                    cloud_mask_flag = bits_stripping_services(1, 2, cloud_mask[0, :, :]).bits_stripping()
                    dimension = h_03.shape[0]
                    dimension_original = dimension
                    latitud = lat_Myd03[i_modis]
                    longitud = lon_Myd03[i_modis]

                    lat_Modis, lon_Modis, mask_land_modis, mask_original_modis = utilitiesUveg.extract_index_image(
                        lat_Myd03[i_modis], lon_Myd03[i_modis], mask_sea_land_modis[i_modis], dimension)

                    ndvi_d = utilitiesUveg.extract_ndvi(
                        lat_Modis, lon_Modis, ndvi_lat, ndvi_lon, ndvi)

                    if ndvi_d.size > 0:
                        print('Process with NDVI')
                    else:
                        continue

                    index_Era, lat, lon = utilitiesUveg.extract_index_modis_and_era(
                        lat_Nc, lon_Nc, lat_Modis, lon_Modis, mask_sea_land_era5)

                    date_era5 = year+month+day

                    h_ = utilitiesUveg.extract_height(
                        h_03, mask_land_modis, cloud_mask_flag)
                    print('Pixeles a procesar:', h_.shape)

                    z = utilitiesUveg.extract_zenith(
                        s_Z, mask_land_modis, cloud_mask_flag)
                    t_ = utilitiesUveg.extract_temperature(temp_era, index_Era)
                    he = utilitiesUveg.extract_humidity(hum_E, index_Era)
                    t2, sk, p2m, q2m = utilitiesUveg.extract_param_2m(
                        t2m, skt, d2m, msl1, index_Era, h_)
                    dimension_modis_ravel = z.shape[0]

                    cps = create_profiles_services(dimension_modis_ravel, z, lat_Modis, lon_Modis, h_, p2m, t2, q2m, sk, level, t_, year, month, day)

                    datetimes, angles, surftype, surfgeom, s2m, skin, simplecloud, clwscheme, icecloud, \
                        zeeman, p, t = cps.create_profiles()
                    path_nc_file = output_path_images_uveg
                    nc_file = net.Dataset(path_nc_file+year+'/'+month+'/'+day+'/'+'TES_' +
                                          year+month+day+'_'+date_modis+'_'+toma+'.nc', mode='w', format='NETCDF4')
                    nc_file.close()
                    
                    
                    print('Se ha creado el archivo temporal:', path_nc_file+year+'/' +
                          month+'/'+day+'/'+'TES_'+year+month+day+'_'+date_modis+'_'+toma+'.nc')
                    bt, radtotal, radup, raddown, tautotal = call_rttov_services(input_path_images_rtcoef_rttov12, datetimes, angles, surfgeom, surftype, s2m, skin, simplecloud, clwscheme, icecloud, zeeman, p, t, he).call_rttov()

                    Lbb29, Lbb31, Lbb32 = processUveg(sk).variables()


                    Lup_29, Lup_31, Lup_32, Ldown_29, Ldown_31, Ldown_32 = utilitiesUveg.chance_units(utilitiesUveg.consA, utilitiesUveg.consB, bt, radtotal, radup, raddown, tautotal, utilitiesUveg.emissivity,  utilitiesUveg.nOnda29, utilitiesUveg.nOnda31, utilitiesUveg.nOnda32, utilitiesUveg.lonOnda29, utilitiesUveg.lonOnda31, utilitiesUveg.lonOnda32, Lbb29, Lbb31, Lbb32)


                    lup = np.array((Lup_29, Lup_31, Lup_32), dtype=np.float64)
                    ldown = np.array(
                        (Ldown_29, Ldown_31, Ldown_32), dtype=np.float64)
                    trans = tautotal

                    radiance, image_rad = modis_02_Services(f_Myd02_hours, hours_list, i_modis, cloud_mask_flag, dimension_original).modis_02()
                        
                    radiance = radiance[:, mask_land_modis]

                    ###########TES UVEG###################
                    Ts, e, BT, rad, R, erad = tes_modis_services(utilitiesUveg.lo, lup, ldown, trans, radiance, z=z.ravel(), aux=True, recal=False).tes_modis()
                        
                    #e_original = np.zeros(shape=(3, dimension_modis_ravel), dtype=np.float64)
                    e_original = utilitiesUveg.create_array_bidimentional(3,dimension_modis_ravel)
                    
                    e_original[:, :] = e[:, :]
                    e_mod = recl_services(e, dimension_modis_ravel).recl_e()
                    e31_fvc, e32_fvc = FCV_services(ndvi_d.ravel(), e_mod[1, :], e_mod[2, :]).FVC()

                    # *****************Errors***************
                    #radiance1 = np.empty(shape=(3, dimension_modis_ravel), dtype=np.float64)
                    radiance1 = utilitiesUveg.create_array_bidimentional(3,dimension_modis_ravel)

                    #radiance2 = np.empty(shape=(3, dimension_modis_ravel), dtype=np.float64)
                    radiance2 = utilitiesUveg.create_array_bidimentional(3,dimension_modis_ravel)

                    #errTs = np.empty(shape=(dimension_modis_ravel), dtype=np.float64)
                    errTs = utilitiesUveg.create_array_unidimentional(dimension_modis_ravel)

                    #err_e29 = np.empty(shape=(dimension_modis_ravel), dtype=np.float64)
                    err_e29 = utilitiesUveg.create_array_unidimentional(dimension_modis_ravel)
                    
                    #err_e31 = np.empty(shape=(dimension_modis_ravel), dtype=np.float64)
                    err_e31 = utilitiesUveg.create_array_unidimentional(dimension_modis_ravel)

                    #err_e32 = np.empty(shape=(dimension_modis_ravel), dtype=np.float64)
                    err_e32 = utilitiesUveg.create_array_unidimentional(dimension_modis_ravel)

                    radiance1[:, :] = rad[:, :] + erad[:, :]
                    radiance2[:, :] = rad[:, :] - erad[:, :]


                    err_ldown = err_ldown_services(ldown[0, :], ldown[1, :], ldown[2, :], z.ravel(), dimension_modis_ravel).ldown_error()

                    #ldown1 = np.empty(shape=(3, dimension_modis_ravel), dtype=np.float64)
                    ldown1 = utilitiesUveg.create_array_bidimentional(3,dimension_modis_ravel)

                    #ldown2 = np.empty(shape=(3, dimension_modis_ravel), dtype=np.float64)
                    ldown2 = utilitiesUveg.create_array_bidimentional(3,dimension_modis_ravel)

                    ldown1[:, :] = ldown + err_ldown
                    ldown2[:, :] = ldown - err_ldown

                    ###########TES UVEG###################

                    print("Estos son los errores")
                    
                    Ts1, e1, rad1, BT1,  R1, erad1 = tes_modis_services(utilitiesUveg.lo, lup, ldown1, trans, radiance1, z=z.ravel(), aux=False, recal=False).tes_modis()
                        
                    Ts2, e2, rad2, BT2,  R2, erad2 = tes_modis_services(utilitiesUveg.lo, lup, ldown2, trans, radiance2, z=z.ravel(), aux=False, recal=False).tes_modis()
                        

                    e1_mod = recl_services(e1, dimension_modis_ravel).recl_e()
                    e2_mod = recl_services(e2, dimension_modis_ravel).recl_e()

                    e1_31_fvc, e1_32_fvc = FCV_services(ndvi_d.ravel(), e1_mod[1, :], e1_mod[2, :]).FVC()
                    e2_31_fvc, e2_32_fvc = FCV_services(ndvi_d.ravel(), e2_mod[1, :], e2_mod[2, :]).FVC()

                    rad_recal_e1 = sw_services(
                        utilitiesUveg.lo, radiance1, dimension_modis_ravel, e1[0, :], e1_31_fvc, e1_32_fvc, ldown1, R1, trans, Ts1, aux=False, aux1=True).sw()
                    rad_recal_e2 = sw_services(
                        utilitiesUveg.lo, radiance2, dimension_modis_ravel, e2[0, :], e2_31_fvc, e2_32_fvc, ldown2, R2, trans, Ts2, aux=False, aux1=True).sw()
                    ###########TES UVEG###################
                    Ts1_, e1_, rad1_, BT1_,  R1_, erad1_ = tes_modis_services(utilitiesUveg.lo, lup, ldown1, trans, rad_recal_e1, z=z.ravel(), aux=False, recal=False).tes_modis()
                    Ts2_, e2_, rad2_, BT2_,  R2_, erad2_ = tes_modis_services(utilitiesUveg.lo, lup, ldown2, trans, rad_recal_e2, z=z.ravel(), aux=False, recal=False).tes_modis()


                    #print(Ts1_, e1_, rad1_, BT1_,  R1_, erad1_)

                    #print(Ts2_, e2_, rad2_, BT2_,  R2_, erad2_)
                    
                    errTs[:] = np.abs((Ts1_-Ts2_)/2)
                    err_e29[:] = np.abs((e1_[0, :]-e2_[0, :])/2)
                    err_e31[:] = np.abs((e1_[1, :]-e2_[1, :])/2)
                    err_e32[:] = np.abs((e1_[2, :]-e2_[2, :])/2)

                    e_29_original = e_original[0, :]

                    # ******Split Window*****
                    rad_recal = sw_services(utilitiesUveg.lo, radiance, dimension_modis_ravel, e_29_original, e31_fvc, e32_fvc, ldown, R, trans, Ts, aux=True, aux1=True).sw()
                    ###########TES UVEG###################
                    Ts_1, e_1, BT_, rad_1, R_1, erad_1 = tes_modis_services(utilitiesUveg.lo, lup, ldown, trans, rad_recal, z=z.ravel(), aux=False, recal=True).tes_modis()
                    Ts_1 = np.round(Ts_1, 2)
                    Ts_1_int = packed_value_services(Ts_1, 0.0, 0.02, data_type=np.uint16).packed_value()

                    e_1 = np.round(e_1, 3)
                    e_1_int = packed_value_services(e_1, 0.49, 0.002, data_type=np.uint8).packed_value()

                    errTs = np.round(errTs, 2)
                    errTs_int = packed_value_services(errTs, 0.0, 0.04, data_type=np.uint8).packed_value()

                    err_e29 = np.round(err_e29, 4)
                    err_e29_int = packed_value_services(err_e29, 0.0, 0.0001, data_type=np.uint16).packed_value()

                    err_e31 = np.round(err_e31, 4)
                    err_e31_int = packed_value_services(err_e31, 0.0, 0.0001, data_type=np.uint16).packed_value()

                    err_e32 = np.round(err_e32, 4)
                    err_e32_int = packed_value_services(err_e32, 0.0, 0.0001, data_type=np.uint16).packed_value()
                        

                    z = np.round(z, 2)
                    z_int = packed_value_services(z, 0.0, 0.5, data_type=np.uint8).packed_value()
                        

                    latitud_int = (latitud*10000).astype(np.int32)
                    longitud_int = (longitud*10000).astype(np.int32)
                    if os.path.exists(path_nc_file+year+'/'+month+'/'+day+'/'+'TES_'+year+month+day+'_'+date_modis+'_'+toma+'.nc'):
                        os.remove(path_nc_file+year+'/'+month+'/'+day+'/' +
                                  'TES_'+year+month+day+'_'+date_modis+'_'+toma+'.nc')
                        print('Archivo borrado')
                    else:
                        print('No se ha borrado el archivo')
                    
                    print(latitud_int, longitud_int, Ts_1_int, e_1_int, mask_original_modis, toma,  errTs_int, err_e29_int, err_e31_int, err_e32_int, z_int)
                    create_nc_outfile_services(output_path_images_uveg, year, month, day, date_modis, dimension_original,latitud_int, longitud_int, Ts_1_int, e_1_int, mask_original_modis, toma,  errTs_int, err_e29_int, err_e31_int, err_e32_int, z_int).create_nc_outfile()
                                                                 

                    utilitiesUveg.write_csv_files(
                        output_path_images_uveg+year+'/'+month+'/', 'TES_'+year+month+day+'_'+date_modis+'_'+toma+'.nc', year, month)

                    elapsed_time_0 = time.time() - start_time_0
                    print(' Time process file: ', elapsed_time_0)

                    del t2, sk, p2m, q2m, index_Era, h_
                    del datetimes, angles, surftype, surfgeom, s2m, skin, simplecloud, clwscheme, icecloud, \
                        zeeman, p, t, dimension_modis_ravel, \
                        z, lat_Modis, lon_Modis, t_, date_era5, date_modis
                    del bt, radtotal, radup, raddown, tautotal
                    del Lbb29,\
                        Lbb31, Lbb32
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

                # except:
                    # continue
                except Exception as e: 
                    print(e)
            
            gc.collect()
        elapsed_time = time.time() - start_time
        print(' Time read files: ', elapsed_time)
        hour = '0000'

    # except:
    #     continue
    except Exception as e: 
        print(e)


gc.collect()

globals().clear()
