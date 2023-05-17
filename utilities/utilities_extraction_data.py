import netCDF4 as net
import numpy   as np
from scipy     import spatial

class UtilitiesExtractionData():

    def extract_mask_land(path_Input):
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
            nc_fileT = net.Dataset(path_input+year+'/'+month+'/'+day+'/'+file_data+year+month+day+hours[hours_list]+'.t.nc','r')
            nc_fileQ = net.Dataset(path_input+year+'/'+month+'/'+day+'/'+file_data+year+month+day+hours[hours_list]+'.q.nc','r')
            print('PATH NC FILES:',path_input +year+'/'+month+'/'+day+'/' + file_data+year+month+day+hours[hours_list]+'.t.nc')

            temp   = nc_fileT.variables['t'][:,[15, 45, 58, 66, 72, 77, 81, 85, 88, 91, 94, 97, 99, 102 ,104, 106 ,110, 112 ,114, 116, 118, 121, 124, 129,136],:,:] # shape (1 , 137, 721, 1440) temperature variable in kelvin
            t      = np.reshape(temp,(25,721,1440))
            t      = np.where(mask_sea_land_era5==1,t,-999)
            lat_Nc = nc_fileT.variables['latitude'][:]  #shape (721), grados norte (90 , -90)
            hum_E  = nc_fileQ.variables['q'][:,[15, 45, 58, 66, 72, 77, 81, 85, 88, 91, 94, 97, 99, 102 ,104, 106 ,110, 112 ,114, 116, 118, 121, 124, 129,136],:,:] #(1 , 137, 721, 1440) k*k ^-1
            q      = np.reshape(hum_E,(25,721,1440))
            q      = np.where(mask_sea_land_era5==1,q,-999)
            lon    = np.arange(0,180,0.25)
            lon_   = np.arange(-180,0,0.25)
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
            data_Myd03 = [net.Dataset(files) for files in f_Myd03_hours[hours_list]]
            num_files_myd03 = len(data_Myd03)
            name_files_myd03 = f_Myd03_hours[hours_list]
            height = [i.variables['Height'][:] for i in data_Myd03]                 
            lat_Myd03 = [i.variables['Latitude'][:] for i in data_Myd03]
            lon_Myd03 = [i.variables['Longitude'][:] for i in data_Myd03]
            zsat = [i.variables['SensorZenith'][:] for i in data_Myd03]
            mask_sea_land_modis = [i.variables['Land/SeaMask'][:] for i in data_Myd03]

            return height, lat_Myd03, lon_Myd03, zsat, mask_sea_land_modis, name_files_myd03, num_files_myd03, data_Myd03

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
        try:

            ymax, ymin, xmin, xmax = np.max(lat_Modis), np.min(lat_Modis), np.min(lon_Modis), np.max(lon_Modis)          
            bound_x = np.logical_and(ndvi_lon > xmin, ndvi_lon < xmax)
            bound_y = np.logical_and(ndvi_lat > ymin, ndvi_lat < ymax)
            box = np.logical_and(bound_x, bound_y)
 
            if (box[0].size > 0) & (box[1].size > 0):

                tree_ndvi = spatial.cKDTree(np.c_[ndvi_lat[box], ndvi_lon[box]], compact_nodes=False, copy_data=False, balanced_tree=False)
                _, index_ndvi = tree_ndvi.query(np.stack((lat_Modis,lon_Modis), axis=-1), k=1)
                ndvi_d = ndvi[box].ravel()[index_ndvi]

            elif bool(box[0].any()) == False:
                ndvi_vacia = np.empty([lat_Modis.shape[0]])
                ndvi_vacia[:] = np.nan
                ndvi_d = ndvi_vacia

            return ndvi_d.ravel()

        except ValueError:
            print("Error extract ndvi clip")
        

    def extract_vars2m_era5(path_input, year, month, day, mask_sea_land_era5, hours, hours_list, file_data):
        ''' 
        Resum: Function extract vars 2m temperature, skin temperature, dew point, pressure 2m

        Params: files (t_2m, skin_T, d_2m, msl, mask_sea_land)

        Output Matrix-> t2m, skt, d2m, msl1, level

        Call example: t2m, skt, d2m, msl1, level = extract_vars2m_era5(t_2m, skin_T, d_2m, msl, mask_sea_land)
        '''
        try:
            skin_T = net.Dataset(path_input+year+'/'+month+'/'+day+'/'+file_data+year+month+day+hours[hours_list]+'.skt.nc','r')
            t_2m   = net.Dataset(path_input+year+'/'+month+'/'+day+'/'+file_data+year+month+day+hours[hours_list]+'.2t.nc','r')
            d_2m   = net.Dataset(path_input+year+'/'+month+'/'+day+'/'+file_data+year+month+day+hours[hours_list]+'.2d.nc','r')
            msl    = net.Dataset(path_input+year+'/'+month+'/'+day+'/'+file_data+year+month+day+hours[hours_list]+'.msl.nc','r')

            t2m  = t_2m.variables['t2m'][:]
            skt  = skin_T.variables['skt'][:]
            d2m  = d_2m.variables['d2m'][:]
            msl1 = msl.variables['msl'][:]   #shape (1 ,721 , 1440) Pa

            t2m  = np.where(mask_sea_land_era5==1, t2m, -999)
            skt  = np.where(mask_sea_land_era5==1, skt, -999)
            d2m  = np.where(mask_sea_land_era5==1, d2m, -999)
            msl1 = np.where(mask_sea_land_era5==1, msl1, -999)
            print(path_input+year+'/'+month+'/'+day+'/'+file_data+year+month+day+hours[hours_list]+'.skt.nc','r')

            ''' Pressure levels, 137 pressure levels according to U.S. Standard Atmosphere, 1976 (hpa) '''
            level = np.array([0.0200,0.0310,0.0467,0.0683,0.0975,0.1361,0.1861,0.2499,0.3299,0.4288,0.5496,0.6952,0.8690,1.074,1.314,1.593,1.913,2.280,2.695,3.164,3.690,4.276,4.926,5.644,6.433,7.297,8.240,9.263,10.372,11.569,12.856,14.238,15.716,17.295,18.975,20.761,22.654,24.658,26.774,29.004,31.351,33.817,36.405,39.115,41.949,44.908,47.992,51.199,54.530,57.983,61.561,65.270,69.119,73.119,77.281,81.618,86.145,90.877,95.828,101.005,106.415,112.068,117.971,124.134,130.564,137.270,144.262,151.549,159.140,167.045,175.273,183.834,192.739,201.997,211.619,221.615,231.995,242.772,253.955,265.556,277.585,290.055,302.976,316.361,330.220,344.566,359.411,374.767,390.645,407.058,424.019,441.540,459.632,478.310,497.585,517.420,537.720,558.343,579.193,600.167,621.162,642.076,662.808,683.262,703.347,722.980,742.086,760.600,778.466,795.640,812.085,827.776,842.696,856.838,870.200,882.791,894.622,905.712,916.082,925.757,934.767,943.140,950.908,958.104,964.758,970.905,976.574,981.797,986.604,991.023,995.082,998.808,1002.225,1005.356,1008.224,1010.849,1013.250],dtype=float)
            level = level[[15, 45, 58, 66, 72, 77, 81, 85, 88, 91, 94, 97, 99, 102 ,104, 106 ,110, 112 ,114, 116, 118, 121, 124, 129,136]]


            skin_T.close()
            t_2m.close()
            d_2m.close()
            msl.close()

            return t2m, skt, d2m, msl1, level

        except ValueError:
            print("Error read multiple files 2m ERA-5")


    def extract_index_modis_and_era(lat_Nc, lon_Nc, lat_Modis, lon_Modis, mask_sea_land_era5):
        ''' 
        Resum: This function extracts a snippet of Era5 global data from an image Modis

        Params: (lat_Nc, lon_Nc, lat_Modis, lon_Modis, mask_land_modis)

        Output: Matrix-> index_Era, lat, lon

        Call example: index_Era, lat, lon = extract_index_modis_and_era(lat_Nc, lon_Nc, lat_Modis, lon_Modis, mask_land_modis)
        '''
        try:
            lon, lat = np.meshgrid(lon_Nc, lat_Nc)
            lon      = np.where(mask_sea_land_era5==1,lon,-999)
            lat      = np.where(mask_sea_land_era5==1,lat,-999)
            points   = np.dstack((lat_Modis,lon_Modis))

            tree = spatial.cKDTree(np.c_[lat.ravel(), lon.ravel()], compact_nodes=False, copy_data=False, balanced_tree=False)
            _, index_Era = tree.query(points, k=1, n_jobs=3)

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
        h = h[mask_land_modis      ]

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
        e = 6.112*np.exp((17.67*(d2_m - 273.15))/((d2_m - 273.15)+243.5))
        q2 = (0.622*e)/(p-(0.378*e))
        q2 = q2.ravel()

        return np.round(t_2m,5), np.round(sk_t,5), np.round(p,5), np.round(q2,5)