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
import time
import os
import warnings
import time
import sys
import gc
import traceback

import netCDF4 as net
import numpy   as np

from calendar import monthrange

from services.call_rttov_service        import CallRttovService
from services.cloud_mask_service        import CloudMaskService
from services.bits_stripping_service    import BitsStrippingService
from services.create_nc_outfile_service import CreateNcOutfileService
from services.create_profiles_service   import CreateProfilesService
from services.fvc_service               import FvcService
from services.modis_02_service          import Modis02Service
from services.matching_files_service    import MatchingFilesService
from services.recal_lse_service         import RecalLseService
from services.sw_service                import SwService
from services.tes_algorithm_service     import TesAlgorithmService
from services.err_ldown_service         import ErrLdownService
from services.change_units_service      import ChangeUnitsService
from services.read_ndvi_service         import ReadNdviService

from utilities.utilities                 import Utilities
from utilities.utilities_extraction_data import UtilitiesExtractionData               

warnings.filterwarnings("ignore")
os.environ['HDF5_DISABLE_VERSION_CHECK'] = '2'

class GenerateImagesProcess():

    def __init__(self, year, month):
        self.year  = year
        self.month = month

    check_server    = str(input('Run local(0) or production (1): '))
    check_satellite = str(input('Satellite products to be processed: Aqua/MYD (0) OR Terra/MOD (1): '))

    if check_satellite == '0':
        if check_server == '1':
            print('RUN IN PRODUCTION SERVER')
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

        if check_server == '0':
            print('RUN IN LOCAL SERVER')
            output_path_images_uveg = '/home/sagonda/Documentos/MYD/output/'
            input_path_images_ndvi = '/home/sagonda/Documentos/MYD/NDVI/'
            input_path_images_collection61 = '/home/sagonda/Documentos/MYD/myd03/'
            input_path_images_MYD021KM = '/home/sagonda/Documentos/MYD/myd021/'
            input_path_images_MYD35_L2 = '/home/sagonda/Documentos/MYD/myd35/'
            input_path_images_invariants = '/home/sagonda/Documentos/MYD/invariants/'
            input_path_images_ecmwfera5_an_ml = '/home/sagonda/Documentos/MYD/an_ml/'
            input_path_images_ecmwfera5_an_sfc = '/home/sagonda/Documentos/MYD/an_sfc/'
            input_path_images_ecmwfera51_an_ml = '/home/sagonda/Documentos/MYD/an_ml'
            input_path_images_ecmwfera51_an_sfc = '/home/sagonda/Documentos/MYD/an_sfc/'
            input_path_images_rtcoef_rttov12 = '/usr/local/rttov12/rtcoef_rttov12/'

    if check_satellite == '1':
        if check_server == '1':
            print('RUN IN PRODUCTION SERVER')
            output_path_images_uveg ='/gws/nopw/j04/esacci_lst/UV/output_uveg_terra/'
            input_path_images_ndvi = '/gws/nopw/j04/esacci_lst/UV/data/ndvi/'
            input_path_images_collection61 = '/neodc/modis/data/MOD03/collection61/'
            input_path_images_MOD021KM = '/neodc/modis/data/MOD021KM/collection61/'
            input_path_images_MOD35_L2 =  '/neodc/modis/data/MOD35_L2/collection61/'
            input_path_images_invariants = '/badc/ecmwf-era5/data/invariants/'
            input_path_images_ecmwfera5_an_ml = '/badc/ecmwf-era5/data/oper/an_ml/'
            input_path_images_ecmwfera5_an_sfc = '/badc/ecmwf-era5/data/oper/an_sfc/'
            input_path_images_ecmwfera51_an_ml = '/badc/ecmwf-era51/data/oper/an_ml/'
            input_path_images_ecmwfera51_an_sfc = '/badc/ecmwf-era51/data/oper/an_sfc/'
            input_path_images_rtcoef_rttov12 = '/gws/nopw/j04/esacci_lst/UV/software/rttov12/rtcoef_rttov12/'
        
        if check_server == '0':
            print('RUN IN LOCAL SERVER')
            output_path_images_uveg = '/home/sagonda/Documentos/MOD/output/'
            input_path_images_ndvi = '/home/sagonda/Documentos/MOD/NDVI/'
            input_path_images_collection61 = '/home/sagonda/Documentos/MOD/myd03/'
            input_path_images_MYD021KM = '/home/sagonda/Documentos/MOD/myd021/'
            input_path_images_MYD35_L2 = '/home/sagonda/Documentos/MOD/myd35/'
            input_path_images_invariants = '/home/sagonda/Documentos/MOD/invariants/'
            input_path_images_ecmwfera5_an_ml = '/home/sagonda/Documentos/MOD/an_ml/'
            input_path_images_ecmwfera5_an_sfc = '/home/sagonda/Documentos/MOD/an_sfc/'
            input_path_images_ecmwfera51_an_ml = '/home/sagonda/Documentos/MOD/an_ml'
            input_path_images_ecmwfera51_an_sfc = '/home/sagonda/Documentos/MOD/an_sfc/'
            input_path_images_rtcoef_rttov12 = '/usr/local/rttov12/rtcoef_rttov12/'


    def _check_hour_file(self):
        try:
            if os.path.isfile(self.output_path_images_uveg + self.year + '/' + self.month + '/' + self.year + self.month + '.csv'):
                print('Routes file exists!!!')
                day_init, hour = MatchingFilesService.read_csv_files(self.output_path_images_uveg + self.year + '/' + self.month + '/', self.year, self.month)
                return day_init, hour
            else:
                print('Not found routes files!!!')
                return 1, '0000'

        except Exception as e:
            print(e)


    def _num_days_to_process(self):
        return monthrange(int(self.year), int(self.month))[1]


    def _check_exists_path_images(self, day):
        if not os.path.exists(self.output_path_images_uveg + self.year + '/' + self.month + '/' + day + '/'):
            os.makedirs(self.output_path_images_uveg + self.year + '/' + self.month + '/' + day +'/')


    def _check_and_extract_data_an_ml(self, day, mask_sea_land_era5, hours, hours_list):
        if os.path.exists(self.input_path_images_ecmwfera5_an_ml + self.year + '/' + self.month + '/' + day + '/'):
            file_data = 'ecmwf-era5_oper_an_ml_'
            temp_era, hum_E, lat_Nc, lon_Nc = UtilitiesExtractionData.extract_vars_era5(
                self.input_path_images_ecmwfera5_an_ml, self.year, self.month, day, mask_sea_land_era5, hours, hours_list, file_data)
            return temp_era, hum_E, lat_Nc, lon_Nc
        else:
            file_data = 'ecmwf-era51_oper_an_ml_'
            temp_era, hum_E, lat_Nc, lon_Nc = UtilitiesExtractionData.extract_vars_era5(
                self.input_path_images_ecmwfera51_an_ml, self.year, self.month, day, mask_sea_land_era5, hours, hours_list, file_data)
            return temp_era, hum_E, lat_Nc, lon_Nc

    
    def _check_and_extract_data_an_sfc(self, day, mask_sea_land_era5, hours, hours_list):
        if os.path.exists(self.input_path_images_ecmwfera5_an_sfc + self.year + '/' + self.month + '/' + day + '/'):
            file_data_ = 'ecmwf-era5_oper_an_sfc_'
            t2m, skt, d2m, msl1, level = UtilitiesExtractionData.extract_vars2m_era5(
                self.input_path_images_ecmwfera5_an_sfc, self.year, self.month, day, mask_sea_land_era5, hours, hours_list, file_data_)
            return t2m, skt, d2m, msl1, level
        else:
            file_data_ = 'ecmwf-era51_oper_an_sfc_'
            t2m, skt, d2m, msl1, level = UtilitiesExtractionData.extract_vars2m_era5(
                self.input_path_images_ecmwfera51_an_sfc, self.year, self.month, day, mask_sea_land_era5, hours, hours_list, file_data_)
            return t2m, skt, d2m, msl1, level


    def _date_modis(self, i_modis, name_files_myd03, day):
        date_modis = name_files_myd03[i_modis].split('/')
        date_modis = date_modis[-1].split('.')
        date_modis = date_modis[-4]
        return f"{date_modis}"


    def _capture(self, data_Myd03, i_modis):
        metadata_myd03 = data_Myd03[i_modis].__dict__['CoreMetadata.0'].split()
        if '"Day"' in metadata_myd03:
            capture_date = 'Day'
        elif '"Night"' in metadata_myd03:
            capture_date = 'Night'
        elif '"Both"' in metadata_myd03:
            capture_date = 'Both'
        return capture_date


    def _process_images(self):
        ndvi_lat, ndvi_lon, ndvi = ReadNdviService.read_ndvi_file(self.input_path_images_ndvi, self.year, self.month)
        day_init, hour = self._check_hour_file()
        

        for day in range(int(day_init), self._num_days_to_process()+1):
            try:
                day = str(day).zfill(2)
                self._check_exists_path_images(day)

                reader = MatchingFilesService(self.year, self.month, day, self.input_path_images_collection61,
                                    self.input_path_images_MYD021KM, self.input_path_images_MYD35_L2, self.output_path_images_uveg)

                ''' Read MODIS products '''
                lista_files_Myd03 = reader.read_myd03_files()
                lista_files_Myd02 = reader.read_myd021_files()
                lista_files_Myd35 = reader.read_myd35_files()

                ''' Matching files '''
                f_Myd03, f_Myd02, f_Myd35 = reader.match_myd03_myd021_myd35(lista_files_Myd03, lista_files_Myd02, lista_files_Myd35)
                hours, f_Myd03_hours, f_Myd02_hours, f_Myd35_hours = reader.read_match_files(f_Myd03, f_Myd02, f_Myd35)

                mask_sea_land_era5 = UtilitiesExtractionData.extract_mask_land(self.input_path_images_invariants)
                print('Images to process: ', len(f_Myd03))
                INIT_HOURS = hours.index(hour)
                print('Init hours:', INIT_HOURS)
                print('Len hours:', len(hours))


                for hours_list in range(INIT_HOURS, len(hours)):
                    try:
                        cloud_Masks = CloudMaskService(f_Myd35_hours, hours_list).cloud_mask()
                        height, lat_Myd03, lon_Myd03, zsat, mask_sea_land_modis, name_files_myd03, num_files_myd03, data_Myd03 = UtilitiesExtractionData.extract_vars_myd03(f_Myd03_hours, hours_list)
                        temp_era, hum_E, lat_Nc, lon_Nc = self._check_and_extract_data_an_ml(day, mask_sea_land_era5, hours, hours_list)
                        t2m, skt, d2m, msl1, level = self._check_and_extract_data_an_sfc(day, mask_sea_land_era5, hours, hours_list)
                    except Exception:
                            print(traceback.format_exc())

                    for i_modis in range(num_files_myd03):
                        try:
                            #***********init time********
                            start_time = time.time()
                            if os.path.isfile(self.output_path_images_uveg + self.year + '/' + self.month + '/' + day + '/' + 'TES_' +
                                               self.year + self.month + day + '_' + str(self._date_modis(i_modis, name_files_myd03, day)) 
                                               + '_' + str(self._capture(data_Myd03, i_modis)) + '.nc'):
                                print('Existe el archivo')
                                continue
                            else:
                                print('Archivo no procesado, procesando!!')
 

                            h_03 = height[i_modis]
                            s_Z = zsat[i_modis]
                            cloud_mask = cloud_Masks[i_modis]
                            cloud_mask_flag = BitsStrippingService(cloud_mask[0, :, :]).bits_stripping()
                            dimension = h_03.shape[0]
                            dimension_original = dimension
                            latitud = lat_Myd03[i_modis]
                            longitud = lon_Myd03[i_modis]

                            lat_Modis, lon_Modis, mask_land_modis, mask_original_modis = UtilitiesExtractionData.extract_index_image(
                                lat_Myd03[i_modis], lon_Myd03[i_modis], mask_sea_land_modis[i_modis], dimension)

                            ndvi_d = UtilitiesExtractionData.extract_ndvi(
                                lat_Modis, lon_Modis, ndvi_lat, ndvi_lon, ndvi)

                            if ndvi_d.size > 0:
                                print('Process with NDVI')
                            else:
                                continue

                            index_Era, lat, lon = UtilitiesExtractionData.extract_index_modis_and_era(
                                lat_Nc, lon_Nc, lat_Modis, lon_Modis, mask_sea_land_era5)

                            date_era5 = self.year + self.month + day

                            h_ = UtilitiesExtractionData.extract_height(
                                h_03, mask_land_modis, cloud_mask_flag)
                            print('Pixeles a procesar:', h_.shape)

                            z = UtilitiesExtractionData.extract_zenith(
                                s_Z, mask_land_modis, cloud_mask_flag)
                            t_ = UtilitiesExtractionData.extract_temperature(
                                temp_era, index_Era)
                            he = UtilitiesExtractionData.extract_humidity(
                                hum_E, index_Era)
                            t2, sk, p2m, q2m = UtilitiesExtractionData.extract_param_2m(
                                t2m, skt, d2m, msl1, index_Era, h_)
                            dimension_modis_ravel = z.shape[0]

                            datetimes, angles, surftype, surfgeom, s2m, skin, simplecloud, clwscheme, icecloud, \
                                zeeman, p, t = CreateProfilesService(
                                    dimension_modis_ravel, z, lat_Modis, lon_Modis, h_, p2m, t2, q2m, sk, level, t_, self.year, self.month, day).create_profiles()

                            nc_file = net.Dataset(self.output_path_images_uveg + self.year + '/' + self.month + '/' + day + '/' + 'TES_' +
                                                self.year + self.month + day + '_' + self._date_modis(i_modis, name_files_myd03, day) + '_' 
                                                + self._capture(data_Myd03, i_modis) + '.nc', mode='w', format='NETCDF4')
                            nc_file.close()

                            print('Se ha creado el archivo temporal:', self.output_path_images_uveg+year+'/' +
                                self.month+'/'+day+'/'+'TES_'+self.year+self.month+day+'_'+self._date_modis(i_modis, name_files_myd03, day)+
                                '_'+self._capture(data_Myd03, i_modis)+'.nc')
                            bt, radtotal, radup, raddown, tautotal = CallRttovService(
                                self.input_path_images_rtcoef_rttov12, datetimes, angles, surfgeom, surftype, s2m, skin, simplecloud, clwscheme, icecloud, zeeman, p, t, he).call_rttov()

                            Lbb29, Lbb31, Lbb32 = ChangeUnitsService(sk).variables()

                            Lup_29, Lup_31, Lup_32, Ldown_29, Ldown_31, Ldown_32 = Utilities.chance_units(Utilities.consA, Utilities.consB, bt, radtotal, radup, raddown, tautotal, Utilities.emissivity,
                                                                                                            Utilities.nOnda29, Utilities.nOnda31, Utilities.nOnda32, Utilities.lonOnda29, Utilities.lonOnda31, Utilities.lonOnda32, Lbb29, Lbb31, Lbb32)

                            lup = np.array((Lup_29, Lup_31, Lup_32), dtype=np.float64)
                            ldown = np.array( (Ldown_29, Ldown_31, Ldown_32), dtype=np.float64)
                            trans = tautotal

                            radiance, image_rad = Modis02Service(f_Myd02_hours, hours_list, i_modis, cloud_mask_flag, dimension_original).modis_02()

                            radiance = radiance[:,mask_land_modis]

                            ###########TES UVEG###################
                            Ts, e, BT, rad, R, erad = TesAlgorithmService(Utilities.lo, lup, ldown, trans, radiance, z=z.ravel(), aux=True, recal=False).tes_modis()

                            e_original = Utilities.create_array_bidimentional(3, dimension_modis_ravel)

                            e_original[:,:] = e[:,:]
                            e_mod = RecalLseService(e, dimension_modis_ravel).recl_e()
                            e31_fvc, e32_fvc = FvcService(
                                ndvi_d.ravel(), e_mod[1,:], e_mod[2,:]).FVC()

                            # *****************Errors***************
                            radiance1 = Utilities.create_array_bidimentional(3, dimension_modis_ravel)

                            radiance2 = Utilities.create_array_bidimentional(3, dimension_modis_ravel)

                            errTs = Utilities.create_array_unidimentional(dimension_modis_ravel)

                            err_e29 = Utilities.create_array_unidimentional(dimension_modis_ravel)

                            err_e31 = Utilities.create_array_unidimentional(dimension_modis_ravel)

                            err_e32 = Utilities.create_array_unidimentional(dimension_modis_ravel)

                            radiance1[:,:] = rad[:,:] + erad[:,:]
                            radiance2[:,:] = rad[:,:] - erad[:,:]

                            err_ldown = ErrLdownService(ldown[0,:], ldown[1,:], ldown[2,:], z.ravel(
                            ), dimension_modis_ravel).ldown_error()

                            ldown1 = Utilities.create_array_bidimentional(
                                3, dimension_modis_ravel)

                            ldown2 = Utilities.create_array_bidimentional(
                                3, dimension_modis_ravel)

                            ldown1[:,:] = ldown + err_ldown
                            ldown2[:,:] = ldown - err_ldown

                            ###########TES UVEG###################
                            Ts1, e1, rad1, BT1,  R1, erad1 = TesAlgorithmService(
                                Utilities.lo, lup, ldown1, trans, radiance1, z=z.ravel(), aux=False, recal=False).tes_modis()

                            Ts2, e2, rad2, BT2,  R2, erad2 = TesAlgorithmService(
                                Utilities.lo, lup, ldown2, trans, radiance2, z=z.ravel(), aux=False, recal=False).tes_modis()

                            e1_mod = RecalLseService(e1, dimension_modis_ravel).recl_e()
                            e2_mod = RecalLseService(e2, dimension_modis_ravel).recl_e()

                            e1_31_fvc, e1_32_fvc = FvcService(
                                ndvi_d.ravel(), e1_mod[1,:], e1_mod[2,:]).FVC()
                            e2_31_fvc, e2_32_fvc = FvcService(
                                ndvi_d.ravel(), e2_mod[1,:], e2_mod[2,:]).FVC()

                            rad_recal_e1 = SwService(
                                Utilities.lo, radiance1, dimension_modis_ravel, e1[0,:], e1_31_fvc, e1_32_fvc, ldown1, R1, trans, Ts1, aux=False, aux1=True).sw()
                            rad_recal_e2 = SwService(
                                Utilities.lo, radiance2, dimension_modis_ravel, e2[0,:], e2_31_fvc, e2_32_fvc, ldown2, R2, trans, Ts2, aux=False, aux1=True).sw()
                            ###########TES UVEG###################
                            Ts1_, e1_, rad1_, BT1_,  R1_, erad1_ = TesAlgorithmService(
                                Utilities.lo, lup, ldown1, trans, rad_recal_e1, z=z.ravel(), aux=False, recal=False).tes_modis()
                            Ts2_, e2_, rad2_, BT2_,  R2_, erad2_ = TesAlgorithmService(
                                Utilities.lo, lup, ldown2, trans, rad_recal_e2, z=z.ravel(), aux=False, recal=False).tes_modis()

                            errTs[:] = np.abs((Ts1_-Ts2_)/2)
                            err_e29[:] = np.abs((e1_[0,:]-e2_[0,:])/2)
                            err_e31[:] = np.abs((e1_[1,:]-e2_[1,:])/2)
                            err_e32[:] = np.abs((e1_[2,:]-e2_[2,:])/2)

                            e_29_original = e_original[0,:]

                            # ******Split Window*****
                            rad_recal = SwService(Utilities.lo, radiance, dimension_modis_ravel,
                                                    e_29_original, e31_fvc, e32_fvc, ldown, R, trans, Ts, aux=True, aux1=True).sw()
                            ###########TES UVEG###################
                            Ts_1, e_1, BT_, rad_1, R_1, erad_1 = TesAlgorithmService(
                                Utilities.lo, lup, ldown, trans, rad_recal, z=z.ravel(), aux=False, recal=True).tes_modis()
                            Ts_1 = np.round(Ts_1, 2)
                            Ts_1_int = Utilities.packed_value(
                                Ts_1, 0.0, 0.02, data_type=np.uint16)

                            e_1 = np.round(e_1, 3)
                            e_1_int = Utilities.packed_value(
                                e_1, 0.49, 0.002, data_type=np.uint8)

                            errTs = np.round(errTs, 2)
                            errTs_int = Utilities.packed_value(
                                errTs, 0.0, 0.04, data_type=np.uint8)

                            err_e29 = np.round(err_e29, 4)
                            err_e29_int = Utilities.packed_value(
                                err_e29, 0.0, 0.0001, data_type=np.uint16)

                            err_e31 = np.round(err_e31, 4)
                            err_e31_int = Utilities.packed_value(
                                err_e31, 0.0, 0.0001, data_type=np.uint16)

                            err_e32 = np.round(err_e32, 4)
                            err_e32_int = Utilities.packed_value(
                                err_e32, 0.0, 0.0001, data_type=np.uint16)

                            z = np.round(z, 2)
                            z_int = Utilities.packed_value(
                                z, 0.0, 0.5, data_type=np.uint8)

                            latitud_int = (latitud*10000).astype(np.int32)
                            longitud_int = (longitud*10000).astype(np.int32)
                            if os.path.exists(self.output_path_images_uveg+self.year+'/'+self.month+'/'+day+'/'+'TES_'+self.year+self.month+
                                              day+'_'+self._date_modis(i_modis, name_files_myd03, day)+'_'+self._capture(data_Myd03, i_modis)+'.nc'):
                                os.remove(self.output_path_images_uveg+self.year+'/'+month+'/'+day+'/' +
                                        'TES_'+self.year+self.month+day+'_'+self._date_modis(i_modis, name_files_myd03, day)+'_'+self._capture(data_Myd03, 
                                                                                                                                    i_modis)+'.nc')
                                print('Archivo borrado')
                            else:
                                print('No se ha borrado el archivo')

                            CreateNcOutfileService(self.output_path_images_uveg, self.year, self.month, day, self._date_modis(i_modis, name_files_myd03, day), 
                                                   dimension_original, latitud_int, longitud_int, Ts_1_int, e_1_int, mask_original_modis, 
                                                   self._capture(data_Myd03, i_modis),  errTs_int, err_e29_int, err_e31_int, err_e32_int, z_int).create_nc_outfile()

                            Utilities.write_csv_files(
                                self.output_path_images_uveg+self.year+'/'+self.month+'/', 'TES_'+self.year+self.month+day+'_'+self._date_modis(i_modis, name_files_myd03, day)
                                +'_'+self._capture(data_Myd03, i_modis)+'.nc', self.year, self.month)

                            elapsed_time = time.time() - start_time
                            print(' Time process file: ', elapsed_time)

                            del t2, sk, p2m, q2m, index_Era, h_
                            del datetimes, angles, surftype, surfgeom, s2m, skin, simplecloud, clwscheme, icecloud, \
                                zeeman, p, t, dimension_modis_ravel, \
                                z, lat_Modis, lon_Modis, t_, date_era5
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
                            del e, e1, e1_mod, e2, e2_mod, e31_fvc, e32_fvc, e_29_original, e_mod, e_original, erad, erad1, erad2, err_e29
                            del err_e31, err_e32, err_ldown, errTs, h_03, he, image_rad, lat, ldown1, lon
                            del mask_land_modis, mask_original_modis, ndvi_d, R, R1, R2
                            del rad, rad1, rad2, s_Z, Ts, Ts1, Ts2
                            gc.collect()

                        except:
                            continue
                    gc.collect()
                elapsed_time = time.time() - start_time
                print(' Time read files: ', elapsed_time)
                hour = '0000'

            except:
                continue
        gc.collect()

        globals().clear()

if __name__ == '__main__':
    year = sys.argv[1]
    month = sys.argv[2]
    GenerateImagesProcess(year, month)._process_images()