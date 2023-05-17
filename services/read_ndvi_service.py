import netCDF4 as net

class ReadNdviService():

    def read_ndvi_file(path_files_nvdi, year, month):
        '''
        Resum: Function read ndvi file

        Params: (path_ndvi_file, month)

        Output: Matrix-> ndvi_lat, ndvi_lon, ndvi_data

        Call example: ndvi_lat, ndvi_lon, ndvi = read_ndvi_file('/path_Input/',  month)
        '''
        try:
            print('#'*20)
            print('Read files NDVI.................')
            path_ndvi = path_files_nvdi + year + '/' + month + '/'
            data      = net.Dataset(path_ndvi + 'out.nc','r')
            ndvi      = data.variables['ndvi'][:]
            ndvi_lat  = data.variables['lat'][:]
            ndvi_lon  = data.variables['lon'][:]
            print('NDVI files upload!!')
            print('#'*20)
            data.close()

            return ndvi_lat, ndvi_lon, ndvi

        except ValueError:
            print('Error load NDVI')  