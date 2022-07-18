import netCDF4 as net
import numpy as np
from scipy import spatial
from pyhdf.SD import SD, SDC
from rttov_wrapper_f2py import *
from operator import itemgetter


class utilitiesUveg():

    consA = np.float64(119110000.0)
    consB = np.float64(14388.0)
    lonOnda29 = np.float64(8.55)
    lonOnda31 = np.float64(11.015)
    lonOnda32 = np.float64(12.02)
    nOnda29 = np.float64(1173.263)
    nOnda31 = np.float64(908.273)
    nOnda32 = np.float64(831.523)
    emissivity = 0.98
    lo = [8.535, 11.015, 12.041]

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

   

    
    def extract_mask_land( path_Input):
        ''' 
        Resum: Function extract global mask sea/land era5 files
        
        Params: (path_Input)
        
        Output mask-> mask index sea/land
        
        Call example: mask_sea_land_era5 = extract_mask_land(path_Input)
        '''
        try:
            sea_land = net.Dataset(path_Input+'ecmwf-era5_oper_an_sfc_200001010000.lsm.inv.nc')
            lsm = sea_land.variables['lsm'][0,:,:]
            mask_sea_land_era5 = np.where(lsm==1,lsm,-999)
            
            # print("Era5 mask sea/land successfully upload!!!")
            # print('#################################################')
            sea_land.close()
            
            return mask_sea_land_era5
        
        except OSError as err:
            print("OS error: {0}".format(err))


    def extract_vars_era5(path_input, year, month, day, mask_sea_land_era5, hours, hours_list, file_data):
        ''' 
        Resum: Function extract vars  Temperature and Relative Humidity
        
        Params: (nc_fileT, nc_fileQ, mask_sea_land)
        
        Output Matrix-> t, q, lat_Nc, lon_Nc
        
        Call example: t, q, lat_Nc, lon_Nc = extract_vars_era5(nc_fileT, nc_fileQ, mask_sea_land)
        '''
        try:
            #====== Añadimos la ruta donde se ecuentra los perfiles netCDF4 descargado de CEDA

            nc_fileT = net.Dataset(path_input+year+'/'+month+'/'+day+'/'+file_data+year+month+day+hours[hours_list]+'.t.nc','r')
            nc_fileQ = net.Dataset(path_input+year+'/'+month+'/'+day+'/'+file_data+year+month+day+hours[hours_list]+'.q.nc','r')
            print(path_input +year+'/'+month+'/'+day+'/' + file_data+year+month+day+hours[hours_list]+'.t.nc')

            #=====Humedad especifica perfil .nc CEDA
            temp = nc_fileT.variables['t'][:,[15, 45, 58, 66, 72, 77, 81, 85, 88, 91, 94, 97, 99, 102 ,104, 106 ,110, 112 ,114, 116, 118, 121, 124, 129,136],:,:] # shape (1 , 137, 721, 1440) temperature variable in kelvin
            t = np.reshape(temp,(25,721,1440))
            t = np.where(mask_sea_land_era5==1,t,-999)
        
            lat_Nc = nc_fileT.variables['latitude'][:]  # shape (721), grados norte (90 , -90)

            #=====Humedad especifica perfil .nc CEDA
            hum_E = nc_fileQ.variables['q'][:,[15, 45, 58, 66, 72, 77, 81, 85, 88, 91, 94, 97, 99, 102 ,104, 106 ,110, 112 ,114, 116, 118, 121, 124, 129,136],:,:] #(1 , 137, 721, 1440) k*k ^-1
            q = np.reshape(hum_E,(25,721,1440))
            q = np.where(mask_sea_land_era5==1,q,-999)
            
            lon = np.arange(0,180,0.25)
            lon_ = np.arange(-180,0,0.25)
            lon_Nc = np.append(lon,lon_)

            nc_fileT.close()
            nc_fileQ.close()
            return t, q, lat_Nc, lon_Nc
        
        except ValueError:
            print("Error in the path of the ERA-5 files")


    def extract_vars_myd03(f_Myd03_hours, hours_list):
        ''' 
        Resum: Function extract vars  height, lat, lon, zsat, mask sea/land product myd03
        
        Params: (data_Myd03)
        
        Output Matrix-> height, lat_Myd03, lon_Myd03, zsat, mask_sea_land_modis
        
        Call example: height, lat_Myd03, lon_Myd03, zsat, mask_sea_land_modis = extract_vars_myd03(data_Myd03)
        '''
        try:
            # data_Myd03 = net.Dataset(file_Myd03)
            # height = data_Myd03.variables['Height'][:]  
            # lat_Myd03 = data_Myd03.variables['Latitude'][:] 
            # lon_Myd03 = data_Myd03.variables['Longitude'][:] 
            # zsat = data_Myd03.variables['SensorZenith'][:] 
            # mask_sea_land_modis = data_Myd03.variables['Land/SeaMask'][:] 
            data_Myd03 = [net.Dataset(files) for files in f_Myd03_hours[hours_list]]
            
            rep = len(data_Myd03)
            name = f_Myd03_hours[hours_list]
    
            height = [i.variables['Height'][:] for i in data_Myd03]                 
            lat_Myd03 = [i.variables['Latitude'][:] for i in data_Myd03]
            lon_Myd03 = [i.variables['Longitude'][:] for i in data_Myd03]
            zsat = [i.variables['SensorZenith'][:] for i in data_Myd03]
            mask_sea_land_modis = [i.variables['Land/SeaMask'][:] for i in data_Myd03]
            
            # data_Myd03.close()
            # data_Myd03.close()
            
            return height, lat_Myd03, lon_Myd03, zsat, mask_sea_land_modis, name, rep, data_Myd03
        
        except ValueError:
            print("Error in the path of the Myd03 files")
    

    def extract_index_image(lat_Modis, lon_Modis, mask_sea_land_modis, dimension):
        ''' 
        Resum: This function stores the dimensions of the original 2d matrix, 
               and is used to reconstruct a flattened matrix to a 2d matrix
        
        Params: (lat_Modis, lon_Modis, mask_modis, dimension)
        
        Output: Matrix-> lat_Modis, lon_Modis and mask -> mask_land_modis, mask_original_modis
        
        Call example: lat_Modis, lon_Modis, mask_land_modis, mask_original_modis = extract_index_image(lat_Modis, lon_Modis, mask_sea_land_modis, dimension)
        '''
        try: 

            mask_ = mask_sea_land_modis
            mask1 = mask_
            mask_land_modis = ((mask1.ravel() >=1) & (mask1.ravel() <=2))
            
            mask1_ = np.where((mask1 >=1) & (mask1 <=2))
            mask2_ = np.ravel_multi_index(mask1_, (dimension, 1354), mode=('clip'))
            mask_original_modis = mask1.ravel()[mask2_]

            lat_Modis = lat_Modis.ravel()
            lon_Modis = lon_Modis.ravel()
            
            lat_Modis = lat_Modis[mask_land_modis]
            lon_Modis = lon_Modis[mask_land_modis]     
            
            return lat_Modis, lon_Modis, mask_land_modis, mask1_
          
        except ValueError:
            print("Error extract original mask")


    def extract_ndvi(lat_Modis, lon_Modis, ndvi_lat, ndvi_lon, ndvi):
        ''' 
        Resum: This function extracts a clipping of the NDVI matrix based on the input modis image
        
        Params: (lat_Modis, lon_Modis, ndvi_lat, ndvi_lon, ndvi)
        
        Output: Matrix-> clip_ndvi
        
        Call example: clip_ndvi = extract_ndvi(lat_Modis, lon_Modis, ndvi_lat, ndvi_lon, ndvi)
        '''
        
        #print('Interpolate NDVI....................')
        #print('....................................')
        #print('ndvi_lat_min, ndvi_lat_max',np.min(ndvi_lat), np.max(ndvi_lat))
        #print('ndvi_lon_min, ndvi_lon_max',np.min(ndvi_lon), np.max(ndvi_lon))
        #print('lat_lon_Modis',np.max(lat_Modis), np.min(lat_Modis), np.min(lon_Modis), np.max(lon_Modis))
        try:  
            
            ymax, ymin, xmin, xmax = np.max(lat_Modis), np.min(lat_Modis), np.min(lon_Modis), np.max(lon_Modis)          
            bound_x = np.logical_and(ndvi_lon > xmin, ndvi_lon < xmax)
            bound_y = np.logical_and(ndvi_lat > ymin, ndvi_lat < ymax)
            box = np.logical_and(bound_x, bound_y)
 
            if (box[0].size > 0) & (box[1].size > 0):
                
                tree_ndvi = spatial.cKDTree(np.c_[ndvi_lat[box], ndvi_lon[box]], compact_nodes=False, copy_data=False, balanced_tree=False)
                distance_points_ndvi, index_ndvi = tree_ndvi.query(np.stack((lat_Modis,lon_Modis), axis=-1), k=1)
                ndvi_d = ndvi[box].ravel()[index_ndvi]

            elif bool(box[0].any()) == False:
                ndvi_vacia = np.empty([lat_Modis.shape[0]])
                ndvi_vacia[:] = np.nan
                ndvi_d = ndvi_vacia

            return ndvi_d.ravel()
        
        except ValueError:
          print("Error extract ndvi clip")

    def extract_vars2m_era5(cls, path_input, year, month, day, mask_sea_land_era5, hours, hours_list, file_data):
        ''' 
        Resum: Function extract vars 2m temperature, skin temperature, dew point, pressure 2m
        
        Params: files (t_2m, skin_T, d_2m, msl, mask_sea_land)
        
        Output Matrix-> t2m, skt, d2m, msl1, level
        
        Call example: t2m, skt, d2m, msl1, level = extract_vars2m_era5(t_2m, skin_T, d_2m, msl, mask_sea_land)
        '''
        try:
            
            #===== Añadimos la ruta de los archivos ERA5 descargados de CEDA, a 2m
            skin_T = net.Dataset(path_input+year+'/'+month+'/'+day+'/'+file_data+year+month+day+hours[hours_list]+'.skt.nc','r')
            t_2m = net.Dataset(path_input+year+'/'+month+'/'+day+'/'+file_data+year+month+day+hours[hours_list]+'.2t.nc','r')
            d_2m = net.Dataset(path_input+year+'/'+month+'/'+day+'/'+file_data+year+month+day+hours[hours_list]+'.2d.nc','r')
            msl = net.Dataset(path_input+year+'/'+month+'/'+day+'/'+file_data+year+month+day+hours[hours_list]+'.msl.nc','r')
        
            #=====Temperatura a 2m extraida del perfil .nc a 2m CEDA, shape (1 ,721 , 1440)
            t2m = t_2m.variables['t2m'][:]   # shape (1 ,721 , 1440) Kelvin
            skt = skin_T.variables['skt'][:] # shape (1 ,721 , 1440) Kelvin
            d2m = d_2m.variables['d2m'][:]   # shape (1 ,721 , 1440) Kelvin
            msl1 = msl.variables['msl'][:]   # shape (1 ,721 , 1440) Pa
            
            t2m = np.where(mask_sea_land_era5==1,t2m,-999)
            skt = np.where(mask_sea_land_era5==1,skt,-999)
            d2m = np.where(mask_sea_land_era5==1,d2m,-999)
            msl1 = np.where(mask_sea_land_era5==1,msl1,-999)
            print(path_input+year+'/'+month+'/'+day+'/'+file_data+year+month+day+hours[hours_list]+'.skt.nc','r')

            #===== Pressure levels, 137 pressure levels according to U.S. Standard Atmosphere, 1976 (hpa)
            level = np.array([0.0200,0.0310,0.0467,0.0683,0.0975,0.1361,0.1861,0.2499,0.3299,0.4288,0.5496,0.6952,0.8690,1.074,1.314,1.593,1.913,2.280,2.695,3.164,3.690,4.276,4.926,5.644,6.433,7.297,8.240,9.263,10.372,11.569,12.856,14.238,15.716,17.295,18.975,20.761,22.654,24.658,26.774,29.004,31.351,33.817,36.405,39.115,41.949,44.908,47.992,51.199,54.530,57.983,61.561,65.270,69.119,73.119,77.281,81.618,86.145,90.877,95.828,101.005,106.415,112.068,117.971,124.134,130.564,137.270,144.262,151.549,159.140,167.045,175.273,183.834,192.739,201.997,211.619,221.615,231.995,242.772,253.955,265.556,277.585,290.055,302.976,316.361,330.220,344.566,359.411,374.767,390.645,407.058,424.019,441.540,459.632,478.310,497.585,517.420,537.720,558.343,579.193,600.167,621.162,642.076,662.808,683.262,703.347,722.980,742.086,760.600,778.466,795.640,812.085,827.776,842.696,856.838,870.200,882.791,894.622,905.712,916.082,925.757,934.767,943.140,950.908,958.104,964.758,970.905,976.574,981.797,986.604,991.023,995.082,998.808,1002.225,1005.356,1008.224,1010.849,1013.250],dtype=float)
            level = level[[15, 45, 58, 66, 72, 77, 81, 85, 88, 91, 94, 97, 99, 102 ,104, 106 ,110, 112 ,114, 116, 118, 121, 124, 129,136]]
        
    
            skin_T.close()
            t_2m.close()
            d_2m.close()
            msl.close()
            
            return t2m, skt, d2m, msl1, level
              
        except ValueError:
            print("Error read multiple files 2m ERA-5")

            
    def match_myd03_myd021_myd35(f_Myd03 , f_Myd02, f_Myd35):
        ''' 
        Resum: Function match files Myd03, Myd021km and Myd35 
        
        Params: (list_myd03 , list_myd021, list_myd35)
        
        Output list-> matching elements myd03, myd021km and myd35
        
        Call example: list_myd03, list_myd021, list_myd35 = match_myd03_myd021_myd35(list_myd03 , list_myd021, list_myd35)
         '''
       
        try:  
            
            list_name_file_myd03 = [i.split('.')[-5:-3] for i in f_Myd03]
            list_name_file_myd02 = [j.split('.')[-5:-3] for j in f_Myd02]  
    
            list_name_file_myd03 = [''.join(list_name_file_myd03[i]) for i in range(len(list_name_file_myd03))]
            list_name_file_myd02 = [''.join(list_name_file_myd02[i]) for i in range(len(list_name_file_myd02))]
            
            list_name_file_myd03 = [i[1:] for i in list_name_file_myd03]
            list_name_file_myd02 = [i[1:] for i in list_name_file_myd02]
            
            #print('Have found',len(list_name_file_myd03),'MYD03 MODIS PRODUCT')
            #print('Have found',len(list_name_file_myd02),'MYD021KM MODIS PRODUCT')
            #print('##################################################')
           
            try:
                
                matrix_name_file_myd03 = np.array(list_name_file_myd03)
                matrix_name_file_myd02 = np.array(list_name_file_myd02)
                
                match_files_index_myd03 = np.intersect1d(matrix_name_file_myd03, matrix_name_file_myd02,  return_indices=True)
                index_03 = list(match_files_index_myd03[1])
                
                match03 = (list(itemgetter(*index_03)(f_Myd03)))
                f_Myd03 = match03 #devulve lista de rutas  de archivos matcheados
                #print(f_Myd03)
                #print('MYD03 in MYD021KM',len(f_Myd03),'Matching elements have been found')
            
    
                matrix_name_file_myd03 = np.array(list_name_file_myd03)
                matrix_name_file_myd02 = np.array(list_name_file_myd02)
                
                match_files_index_myd02 = np.intersect1d(matrix_name_file_myd02, matrix_name_file_myd03,  return_indices=True)
                index_02 = list(match_files_index_myd02[1])
                
                match02 = (list(itemgetter(*index_02)(f_Myd02)))
                f_Myd02 = match02 #devulve lista de rutas  de archivos matcheados
                #print(f_Myd02)
                
                # file_myd03 = [i.split('.')[-5:-3] for i in f_Myd03]
                # file_myd03 = [''.join(file_myd03[i]) for i in range(len(file_myd03))]
                # file_myd03 = [i[1:] for i in file_myd03]
                # file_myd03 = np.array(file_myd03) # devulve un string con fecha, año, semana, dia
                #print(file_myd03)
            except OSError as err:
                print("OS error: {0}".format(err))
                
            
            if len(f_Myd03) >= len(f_Myd35):
    
                option3 = 3                
                file_myd03 = [i.split('.')[-5:-3] for i in f_Myd03]
                file_myd35 = [j.split('.')[-5:-3] for j in f_Myd35]
                               
                file_myd03 = [''.join(file_myd03[i]) for i in range(len(file_myd03))]
                file_myd35 = [''.join(file_myd35[i]) for i in range(len(file_myd35))]
                
                file_myd03 = [i[1:] for i in file_myd03]
                file_myd35 = [i[1:] for i in file_myd35]
       
                file_myd03 = np.array(file_myd03)
                file_myd35 = np.array(file_myd35)
                
                match_files_index_myd03 = np.intersect1d(file_myd03, file_myd35, return_indices=True)
                index_03_files = list(match_files_index_myd03[1])
                
                match_myd03_files = (list(itemgetter(*index_03_files)(f_Myd03)))
                         
                f_Myd03 = match_myd03_files
                f_Myd35 = f_Myd35
                f_Myd02 = f_Myd02                
    
            if len(f_Myd35) >= len(f_Myd03):
    
                option4 = 4
                file_myd03 = [i.split('.')[-5:-3] for i in f_Myd03]
                file_myd35 = [j.split('.')[-5:-3] for j in f_Myd35]
                
                
                file_myd03 = [''.join(file_myd03[i]) for i in range(len(file_myd03))]
                file_myd35 = [''.join(file_myd35[i]) for i in range(len(file_myd35))]
                
                file_myd35 = [i[1:] for i in file_myd35]
                file_myd03 = [i[1:] for i in file_myd03]
        
                file_myd03 = np.array(file_myd03)
                file_myd35 = np.array(file_myd35)
                
                match_files_index_myd35 = np.intersect1d(file_myd35, file_myd03, return_indices=True)
                index_21 = list(match_files_index_myd35[1])
                
                match_myd35 = (list(itemgetter(*index_21)(f_Myd35)))
            
                f_Myd03 = f_Myd03
                f_Myd35 = match_myd35
                f_Myd02 = f_Myd02
                
                file_myd03 = [i.split('.')[-5:-3] for i in f_Myd03]
                file_myd02 = [j.split('.')[-5:-3] for j in f_Myd02]
                file_myd35 = [j.split('.')[-5:-3] for j in f_Myd35]
                               
                file_myd03 = [''.join(file_myd03[i]) for i in range(len(file_myd03))]
                file_myd02 = [''.join(file_myd02[i]) for i in range(len(file_myd02))]
                file_myd35 = [''.join(file_myd35[i]) for i in range(len(file_myd35))]
                
                file_myd03 = [i[1:] for i in file_myd03]
                file_myd02 = [i[1:] for i in file_myd02]
                file_myd35 = [i[1:] for i in file_myd35]                 
            
            if len(f_Myd02) >= len(f_Myd35):
    
                option5 = 5
                file_myd02 = [i.split('.')[-5:-3] for i in f_Myd02]
                file_myd35 = [j.split('.')[-5:-3] for j in f_Myd35]
                               
                file_myd02 = [''.join(file_myd02[i]) for i in range(len(file_myd02))]
                file_myd35 = [''.join(file_myd35[i]) for i in range(len(file_myd35))]
                
                file_myd02 = [i[1:] for i in file_myd02]
                file_myd35 = [i[1:] for i in file_myd35]
        
                file_myd02 = np.array(file_myd02)
                file_myd35 = np.array(file_myd35)
                
                match_files_index_myd02 = np.intersect1d(file_myd02, file_myd35, return_indices=True)
                index_02_files = list(match_files_index_myd02[1])
                
                match_myd02_files = (list(itemgetter(*index_02_files)(f_Myd02)))
            
                f_Myd02 = match_myd02_files
                f_Myd35 = f_Myd35
                f_Myd03 = f_Myd03

            print('Files MYD03: ',len(f_Myd03))
            print('Files myd35: ',len(f_Myd35))
            print('Files MYD02: ',len(f_Myd02))
            return f_Myd03, f_Myd02, f_Myd35
            
        except OSError as err:
            print("OS error: {0}".format(err))


    def extract_ndvi(lat_Modis, lon_Modis, ndvi_lat, ndvi_lon, ndvi):
        ''' 
        Resum: This function extracts a clipping of the NDVI matrix based on the input modis image
        
        Params: (lat_Modis, lon_Modis, ndvi_lat, ndvi_lon, ndvi)
        
        Output: Matrix-> clip_ndvi
        
        Call example: clip_ndvi = extract_ndvi(lat_Modis, lon_Modis, ndvi_lat, ndvi_lon, ndvi)
        '''
        
        #print('Interpolate NDVI....................')
        #print('....................................')
        #print('ndvi_lat_min, ndvi_lat_max',np.min(ndvi_lat), np.max(ndvi_lat))
        #print('ndvi_lon_min, ndvi_lon_max',np.min(ndvi_lon), np.max(ndvi_lon))
        #print('lat_lon_Modis',np.max(lat_Modis), np.min(lat_Modis), np.min(lon_Modis), np.max(lon_Modis))
        try:  
            
            ymax, ymin, xmin, xmax = np.max(lat_Modis), np.min(lat_Modis), np.min(lon_Modis), np.max(lon_Modis)          
            bound_x = np.logical_and(ndvi_lon > xmin, ndvi_lon < xmax)
            bound_y = np.logical_and(ndvi_lat > ymin, ndvi_lat < ymax)
            box = np.logical_and(bound_x, bound_y)
 
            if (box[0].size > 0) & (box[1].size > 0):
                
                tree_ndvi = spatial.cKDTree(np.c_[ndvi_lat[box], ndvi_lon[box]], compact_nodes=False, copy_data=False, balanced_tree=False)
                distance_points_ndvi, index_ndvi = tree_ndvi.query(np.stack((lat_Modis,lon_Modis), axis=-1), k=1)
                ndvi_d = ndvi[box].ravel()[index_ndvi]

            elif bool(box[0].any()) == False:
                ndvi_vacia = np.empty([lat_Modis.shape[0]])
                ndvi_vacia[:] = np.nan
                ndvi_d = ndvi_vacia

            return ndvi_d.ravel()
        
        except ValueError:
          print("Error extract ndvi clip")


    def extract_index_modis_and_era(lat_Nc, lon_Nc, lat_Modis, lon_Modis, mask_sea_land_era5):
        ''' 
        Resum: This function extracts a snippet of Era5 global data from an image Modis
        
        Params: (lat_Nc, lon_Nc, lat_Modis, lon_Modis, mask_land_modis)
        
        Output: Matrix-> index_Era, lat, lon
        
        Call example: index_Era, lat, lon = extract_index_modis_and_era(lat_Nc, lon_Nc, lat_Modis, lon_Modis, mask_land_modis)
        '''
        try:
            lon, lat = np.meshgrid(lon_Nc, lat_Nc)
            lon = np.where(mask_sea_land_era5==1,lon,-999)
            lat = np.where(mask_sea_land_era5==1,lat,-999)
            points = np.dstack((lat_Modis,lon_Modis))
    
            tree = spatial.cKDTree(np.c_[lat.ravel(), lon.ravel()], compact_nodes=False, copy_data=False, balanced_tree=False)
            distance_points_, index_Era = tree.query(points, k=1, n_jobs=3)
        
            lat = lat.ravel()[index_Era]
            lon = lon.ravel()[index_Era]
            lat = lat.ravel()
            lon = lon.ravel()
        
            return index_Era, lat, lon
        except ValueError:
            print("Error extract era5 clip")


    def extract_height(height, mask_land_modis, cloud_mask_flag):
      height = np.where(cloud_mask_flag==0, 0, height)
      h = height.ravel()
      h = h[mask_land_modis]
      return h


    def extract_zenith(zenith, mask_land_modis, cloud_mask_flag):
      zenith = np.where(cloud_mask_flag==0, 0, zenith)
      z = zenith.ravel()
      z = z[mask_land_modis]
      return z


    def extract_temperature(temp_era, index_Era):
        n = len(temp_era[0,:,0])
        m = len(temp_era[0,0,:])
        m_n = m * n
        t = np.reshape(temp_era,(25,m_n))
        t = t[:,index_Era]
        t = np.reshape(t,(25,len(index_Era[0,:])))
        return np.round(t,5)


    def extract_humidity(hum_E, index_Era):
        n = len(hum_E[0,:,0])
        m = len(hum_E[0,0,:])
        m_n = m * n
        he = np.reshape(hum_E,(25,m_n))
        he = he[:,index_Era]
        he = np.reshape(he,(25,len(index_Era[0,:])))
        #he = 28.9644/18.01528*1e6*he
        return np.round(he,8)


    def extract_param_2m(t_2m, sk_t, d2_m, ms_l1, index_Era, h_):
        t_2m = t_2m.ravel()
        sk_t = sk_t.ravel()
        d2_m = d2_m.ravel()
        ms_l1 = ms_l1.ravel()
    
        t_2m = t_2m[index_Era]
        sk_t = sk_t[index_Era]
        d2_m = d2_m[index_Era]
        ms_l1 = ms_l1[index_Era]
        t_2m = t_2m.ravel()
        sk_t = sk_t.ravel()
    
        p = ((ms_l1)*np.exp((-9.80665 * 0.0289644*( (h_ + 2)- 0))/(8.3144598*t_2m)))/100 # Pressure in Hpa
        p = p.ravel()
        #q2 = ((622*6.113*np.exp((5423 * (d2_m - 273.15))/(d2_m * 273.15)))/p)/1000 # Calculate Especific humidity in 
        #q2 = 100*(np.exp((17.625*(d2_m_- 273.15))/(243.04+(d2_m_- 273.15)))/np.exp((17.625*(t2_-273.15))/(243.04+(t2_-273.15)))) # Calculate Relative humidity in %
        #q2 = 28.9644/18.01528*1e6*q2
        e = 6.112*np.exp((17.67*(d2_m - 273.15))/((d2_m - 273.15)+243.5))
        q2 = (0.622*e)/(p-(0.378*e))
        #q2 = 28.9644/18.01528*1e6*q2
        q2 = q2.ravel()
        return np.round(t_2m,5), np.round(sk_t,5), np.round(p,5), np.round(q2,5)


    def chance_units(consA, consB, bt, radtotal, radup, raddown, tautotal, emissivity, nOnda29, nOnda31, nOnda32, lonOnda29, lonOnda31, \
                          lonOnda32, Lbb29, Lbb31, Lbb32):
        try:
            # Cambio de unidades radiancia total
            rt29 = (((radtotal[0,:] * nOnda29)/lonOnda29)/1000)
            rt31 = (((radtotal[1,:] * nOnda31)/lonOnda31)/1000)
            rt32 = (((radtotal[2,:] * nOnda32)/lonOnda32)/1000)
            #print('Total radiance:',rt29,rt31,rt32)
           
            # Cambio de unidades radiancia upwelling
            lUp29 = (((radup[0,:] * nOnda29)/lonOnda29)/1000)
            lUp31 = (((radup[1,:] * nOnda31)/lonOnda31)/1000)
            lUp32 = (((radup[2,:] * nOnda32)/lonOnda32)/1000)
            #print('Lup RTTOV:', lUp29,lUp31,lUp32)
           
           
            Ldown_29 = ((rt29 - lUp29)/(1-emissivity)/tautotal[0,:])
            Ldown_31 = ((rt31 - lUp31)/(1-emissivity)/tautotal[1,:])
            Ldown_32 = ((rt32 - lUp32)/(1-emissivity)/tautotal[2,:])
            #print('Ldown Ecuación:',Ldown_29, Ldown_31, Ldown_32)
           
            # Brigtnees Temperature (K) to radiances
            l29 = (consA) / ((lonOnda29**5)*(np.exp(consB/(bt[0,:]*lonOnda29))-1))
            l31 = (consA) / ((lonOnda31**5)*(np.exp(consB/(bt[1,:]*lonOnda31))-1))
            l32 = (consA) / ((lonOnda32**5)*(np.exp(consB/(bt[2,:]*lonOnda32))-1))
          
           
            # Calculo B(T) ECWF
            blonT29 = emissivity * Lbb29 + (1 - emissivity) * Ldown_29
            blonT31 = emissivity * Lbb31 + (1 - emissivity) * Ldown_31
            blonT32 = emissivity * Lbb32 + (1 - emissivity) * Ldown_32
            #print('B(T):',blonT29, blonT31, blonT32)
           
            Lup_29 = l29 - blonT29 * tautotal[0,:]
            Lup_31 = l31 - blonT31 * tautotal[1,:]
            Lup_32 = l32 - blonT32 * tautotal[2,:]        
            #print('Lup Ecuación:',Lup_29, Lup_31, Lup_32)
           
            Ldown_29 = ((rt29 - lUp29)/(1-emissivity)/tautotal[0,:])#*1.5
            Ldown_31 = ((rt31 - lUp31)/(1-emissivity)/tautotal[1,:])#*1.5
            Ldown_32 = ((rt32 - lUp32)/(1-emissivity)/tautotal[2,:])#*1.5
            #print('Ldown Ecuación:',Ldown_29, Ldown_31, Ldown_32)
           
            return Lup_29, Lup_31, Lup_32, Ldown_29, Ldown_31, Ldown_32
        except OSError as err:
            print("OS error: {0}".format(err))

    def write_csv_files(path ,file, year, month):  
        try:
           # open the file in the write mode
           with open(path + year + month +'.csv', 'a', newline='') as f:
               writer = csv.writer(f)
               writer.writerow([file])
           print('file added to the general file!!!')
        except OSError as err:
            print("OS error: {0}".format(err))