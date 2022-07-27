import netCDF4 as net
import numpy as np
import glob
from operator import itemgetter
import traceback



class readerUveg():
    def __init__(self, year, month, day, path_files_nvdi, path_files_Myd03, path_files_Myd021, path_files_Myd35, path_files_CSV):
        self.year = year
        self.month = month
        self.day = day
        self.path_files_nvdi=path_files_nvdi
        self.path_files_Myd03 = path_files_Myd03
        self.path_files_Myd021 = path_files_Myd021
        self.path_files_Myd35 = path_files_Myd35
        self.path_files_CSV = path_files_CSV
    @classmethod
    def read_ndvi_file(cls,year, month, path_files_nvdi):
        '''
        Resum: Function read ndvi file
        
        Params: (path_ndvi_file, month)
        
        Output: Matrix-> ndvi_lat, ndvi_lon, ndvi_data
        
        Call example: ndvi_lat, ndvi_lon, ndvi = read_ndvi_file('/path_Input/',  month)
        
        '''
        
        try:
            print('#'*20)
            print('Read files NDVI.................')
            
            # Read files
            path_ndvi = path_files_nvdi + year + '/' + month + '/'
            data = net.Dataset(path_ndvi + 'out.nc','r')
            
            # Read variables
            # print(data.variables.keys())
            ndvi = data.variables['ndvi'][:]
            # print(ndvi.shape)
            #red = data.variables['red'][:]
            ndvi_lat = data.variables['lat'][:]
            ndvi_lon = data.variables['lon'][:]
            
            print('NDVI files upload!!')
            print('#'*20)
            data.close()
            return ndvi_lat, ndvi_lon, ndvi
            
        except ValueError:
            print('Error load NDVI')  

    #Linea 82 - 104

    def read_myd03_files(self):
        '''
        Resum: Function read MODIS Myd03 file
        
        Params: (path_Myd03_files, year, month, day)
        
        Output: list-> files myd03
        
        Call example: list_myd03_files = read_myd03_files('/path_Input/',  year, month, day)
        
        '''
        try:
            print('#################################################')
            print('Read files Myd03.................')
            path_modis_myd03 =  self.path_files_Myd03 + self.year + '/' + self.month + '/' + self.day + '/'
            f_Myd03 = sorted(glob.glob( path_modis_myd03 + "/*.hdf"))
            
            print('Myd03 files upload!!')
            print('#################################################')
            return f_Myd03
        
        except ValueError:
            print('Error load MYD03')   
        

    def read_myd021_files(self):
        ''' 
        Resum: Function read M0DIS Myd021km files
        
        Params: (path_Myd021_files, year, month, day)
        
        Output list-> files Myd021km
        
        Call example: list_myd021_files = read_myd021_files('/path_Input/',  year, month, day)
        '''
        try:
            print('#################################################')
            print('Read files Myd021km.................')
            #====== READ HDF5 FILES MODIS MYD021KM
            path_modis02 = self.path_files_Myd021 + self.year + '/' + self.month + '/' + self.day + '/'
            f_Myd02 = sorted(glob.glob( path_modis02 + "/*.hdf"))
            
            print("MYD021KM files have been successfully uploaded!!!")
            print('#################################################')
            return f_Myd02
    
        except ValueError:
            print('Error load MYD021KM')


    def read_myd35_files(self):
        ''' 
        Resum: Function read M0DIS myd35km files
        
        Params: (path_myd35_files, year, month, day)
        
        Output list-> files myd35
        
        Call example: list_myd35_files = read_myd35_files('/path_Input/',  year, month, day)
        '''
        try:
            print('#################################################')
            print('Read files myd35km.................')
            #====== READ HDF5 FILES MODIS myd35KM
            path_modis35 = self.path_files_Myd35 + self.year + '/' + self.month + '/' + self.day + '/'
            f_Myd35 = sorted(glob.glob( path_modis35 + "/*.hdf"))
            
            print("myd35KM files have been successfully uploaded!!!")
            print('#################################################')
            return f_Myd35
    
        except ValueError:
            print('Error load myd35')


    @staticmethod
    def match_myd03_myd021_myd35(f_Myd03, f_Myd02, f_Myd35):
        ''' 
        Resum: Function match files Myd03, Myd021km and Myd35 
        
        Params: (list_myd03 , list_myd021, list_myd35)
        
        Output list-> matching elements myd03, myd021km and myd35
        
        Call example: list_myd03, list_myd021, list_myd35 = match_myd03_myd021_myd35(list_myd03 , list_myd021, list_myd35)
         '''
        # f_Myd03 = self.read_myd03_files()
        # f_Myd02 = self.read_myd021_files()
        # file_myd35 = self.read_myd35_files()
        
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
            except Exception:
                print(traceback.format_exc())
                
            
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

            print(f_Myd03, f_Myd02,f_Myd35)

            return f_Myd03, f_Myd02, f_Myd35
            
        except Exception:
            print(traceback.format_exc())


    


    
    def read_match_files(self,f_Myd03, f_Myd02, f_Myd35):
        ''' 
        Resum: 
        
        Params: 
        
        Output list files-> 
        
        Call example: 
        '''
         
        try:
            cero_hour = ['0000', '0005', '0010', '0015', '0020', '0025', '0030']        
                    
            one_hour = ['0035', '0040', '0045', '0050', '0055', '0100', '0105', '0110', '0115', '0120', '0125', '0130']
            
            two_hour =  ['0135', '0140', '0145', '0150', '0155', '0200', '0205', '0210', '0215', '0220', '0225', '0230']
            
            tree_hour = ['0235', '0240', '0245', '0250', '0255', '0300', '0305', '0310', '0315', '0320', '0325', '0330']
            
            four_hour = ['0335', '0340', '0345', '0350', '0355', '0400', '0405', '0410', '0415', '0420', '0425', '0430']
            
            five_hour = ['0435', '0440', '0445', '0450', '0455', '0500', '0505', '0510', '0515', '0520', '0525', '0530']
            
            six_hour =  ['0535', '0540', '0545', '0550', '0555', '0600', '0605', '0610', '0615', '0620', '0625', '0630']
            
            seven_hour = ['0635', '0640', '0645', '0650', '0655', '0700', '0705', '0710', '0715', '0720', '0725', '0730']
            
            eight_hour = ['0735', '0740', '0745', '0750', '0755', '0800', '0805', '0810', '0815', '0820', '0825', '0830']
            
            nine_hour = ['0835', '0840', '0845', '0850', '0855', '0900', '0905', '0910', '0915', '0920', '0925', '0930']
            
            ten_hour = ['0935', '0940', '0945', '0950', '0955', '1000', '1005', '1010', '1015', '1020', '1025', '1030']
            
            eleven_hour = ['1035', '1040', '1045', '1050', '1055', '1100', '1105', '1110', '1115', '1120', '1125', '1130']
            
            twelve_hour = ['1135', '1140', '1145', '1150', '1155', '1200', '1205', '1210', '1215', '1220', '1225', '1230']
            
            thirteen_hour = ['1235', '1240', '1245', '1250', '1255', '1300', '1305', '1310', '1315', '1320', '1325', '1330']
            
            fourteen_hour = ['1335', '1340', '1345', '1350', '1355', '1400', '1405', '1410', '1415', '1420', '1425', '1430']
    
            fifteen_hour = ['1435', '1440', '1445', '1450', '1455', '1500', '1505', '1510', '1515', '1520', '1525', '1530']
            
            sixteen_hour = ['1535', '1540', '1545', '1550', '1555', '1600', '1605', '1610', '1615', '1620', '1625', '1630']
            
            seventeen_hour = ['1635', '1640', '1645', '1650', '1655', '1700', '1705', '1710', '1715', '1720', '1725', '1730']
            
            eighteen_hour = ['1735', '1740', '1745', '1750', '1755', '1800', '1805', '1810', '1815', '1820', '1825', '1830']
            
            nineteen_hour = ['1835', '1840', '1845', '1850', '1855', '1900', '1905', '1910', '1915', '1920', '1925', '1930']
            
            twenty_hour = ['1935', '1940', '1945', '1950', '1955', '2000', '2005', '2010', '2015', '2020', '2025', '2030']
            
            twenty_one_hour = ['2035', '2040', '2045','2050', '2055', '2100', '2105', '2110', '2115', '2120', '2125', '2130']
            
            twenty_two_hour = ['2135', '2140', '2145', '2150', '2155', '2200', '2205', '2210', '2215', '2220', '2225', '2230']
            
            twenty_three_hour = ['2235', '2240', '2245', '2250', '2255', '2300', '2305', '2310', '2315', '2320', '2325', '2330',
                                '2335', '2340', '2345', '2350', '2355']
            
            list_total_myd03 = [i.split('.')[2] for i in f_Myd03] #devulve lista de horas
            list_total_myd02 = [j.split('.')[2] for j in f_Myd02]
            list_total_myd35 = [i.split('.')[2] for i in f_Myd35]
            
            
            cero = [index for index, item in enumerate(list_total_myd03) if item in cero_hour]  
            one = [index for index, item in enumerate(list_total_myd03) if item in one_hour]           
            two = [index for index, item in enumerate(list_total_myd03) if item in two_hour]
            three = [index for index, item in enumerate(list_total_myd03) if item in tree_hour]
            four = [index for index, item in enumerate(list_total_myd03) if item in four_hour]
            five = [index for index, item in enumerate(list_total_myd03) if item in five_hour]
            six = [index for index, item in enumerate(list_total_myd03) if item in six_hour]
            seven = [index for index, item in enumerate(list_total_myd03) if item in seven_hour]
            eight = [index for index, item in enumerate(list_total_myd03) if item in eight_hour]
            nine = [index for index, item in enumerate(list_total_myd03) if item in nine_hour]
            ten = [index for index, item in enumerate(list_total_myd03) if item in ten_hour]
            eleven = [index for index, item in enumerate(list_total_myd03) if item in eleven_hour]
            twelve = [index for index, item in enumerate(list_total_myd03) if item in twelve_hour]
            thirteen = [index for index, item in enumerate(list_total_myd03) if item in thirteen_hour]
            fourteen = [index for index, item in enumerate(list_total_myd03) if item in fourteen_hour]
            fifteen = [index for index, item in enumerate(list_total_myd03) if item in fifteen_hour]
            sixteen = [index for index, item in enumerate(list_total_myd03) if item in sixteen_hour]
            seventeen = [index for index, item in enumerate(list_total_myd03) if item in seventeen_hour]
            eighteen = [index for index, item in enumerate(list_total_myd03) if item in eighteen_hour]
            nineteen = [index for index, item in enumerate(list_total_myd03) if item in nineteen_hour]
            twenty = [index for index, item in enumerate(list_total_myd03) if item in twenty_hour]
            twenty_one = [index for index, item in enumerate(list_total_myd03) if item in twenty_one_hour]
            twenty_two = [index for index, item in enumerate(list_total_myd03) if item in twenty_two_hour]
            twenty_three = [index for index, item in enumerate(list_total_myd03) if item in twenty_three_hour]
            # print(cero)
            # print(np.array(self.read_myd03_files())) 
            #f_Myd03
            
            cero_Myd03 = list(np.array(f_Myd03)[cero])
            one_Myd03 = list(np.array(f_Myd03)[one])
            two_Myd03 = list(np.array(f_Myd03)[two])
            three_Myd03 = list(np.array(f_Myd03)[three])
            four_Myd03 = list(np.array(f_Myd03)[four])
            five_Myd03 = list(np.array(f_Myd03)[five])
            six_Myd03 = list(np.array(f_Myd03)[six])
            seven_Myd03 = list(np.array(f_Myd03)[seven])
            eight_Myd03 = list(np.array(f_Myd03)[eight])
            nine_Myd03 = list(np.array(f_Myd03)[nine])
            ten_Myd03 = list(np.array(f_Myd03)[ten])
            eleven_Myd03 = list(np.array(f_Myd03)[eleven])
            twelve_Myd03 = list(np.array(f_Myd03)[twelve])
            thirteen_Myd03 = list(np.array(f_Myd03)[thirteen])
            fourteen_Myd03 = list(np.array(f_Myd03)[fourteen])
            fifteen_Myd03 = list(np.array(f_Myd03)[fifteen])
            sixteen_Myd03 = list(np.array(f_Myd03)[sixteen])
            seventeen_Myd03 = list(np.array(f_Myd03)[seventeen])
            eighteen_Myd03 = list(np.array(f_Myd03)[eighteen])
            nineteen_Myd03 = list(np.array(f_Myd03)[nineteen])
            twenty_Myd03 = list(np.array(f_Myd03)[twenty])
            twenty_one_Myd03 = list(np.array(f_Myd03)[twenty_one])
            twenty_two_Myd03 = list(np.array(f_Myd03)[twenty_two])
            twenty_three_Myd03 = list(np.array(f_Myd03)[twenty_three])
            f_Myd03_hours = [cero_Myd03, one_Myd03, two_Myd03, three_Myd03, four_Myd03, five_Myd03, six_Myd03, seven_Myd03
                            , eight_Myd03, nine_Myd03, ten_Myd03, eleven_Myd03, twelve_Myd03, thirteen_Myd03,
                            fourteen_Myd03, fifteen_Myd03, sixteen_Myd03, seventeen_Myd03, eighteen_Myd03, 
                            nineteen_Myd03, twenty_Myd03, twenty_one_Myd03, twenty_two_Myd03, twenty_three_Myd03]
            # devulve lista de listas por horas
            #, f_Myd02
           
            cero_Myd02 = list(np.array(f_Myd02)[cero])
            one_Myd02 = list(np.array(f_Myd02)[one])
            two_Myd02 = list(np.array(f_Myd02)[two])
            three_Myd02 = list(np.array(f_Myd02)[three])
            four_Myd02 = list(np.array(f_Myd02)[four])
            five_Myd02 = list(np.array(f_Myd02)[five])
            six_Myd02 = list(np.array(f_Myd02)[six])
            seven_Myd02 = list(np.array(f_Myd02)[seven])
            eight_Myd02 = list(np.array(f_Myd02)[eight])
            nine_Myd02 = list(np.array(f_Myd02)[nine])
            ten_Myd02 = list(np.array(f_Myd02)[ten])
            eleven_Myd02 = list(np.array(f_Myd02)[eleven])
            twelve_Myd02 = list(np.array(f_Myd02)[twelve])
            thirteen_Myd02 = list(np.array(f_Myd02)[thirteen])
            fourteen_Myd02 = list(np.array(f_Myd02)[fourteen])
            fifteen_Myd02 = list(np.array(f_Myd02)[fifteen])
            sixteen_Myd02 = list(np.array(f_Myd02)[sixteen])
            seventeen_Myd02 = list(np.array(f_Myd02)[seventeen])
            eighteen_Myd02 = list(np.array(f_Myd02)[eighteen])
            nineteen_Myd02 = list(np.array(f_Myd02)[nineteen])
            twenty_Myd02 = list(np.array(f_Myd02)[twenty])
            twenty_one_Myd02 = list(np.array(f_Myd02)[twenty_one])
            twenty_two_Myd02 = list(np.array(f_Myd02)[twenty_two])
            twenty_three_Myd02 = list(np.array(f_Myd02)[twenty_three])
            f_Myd02_hours = [cero_Myd02, one_Myd02, two_Myd02, three_Myd02, four_Myd02, five_Myd02, six_Myd02, seven_Myd02
                , eight_Myd02, nine_Myd02, ten_Myd02, eleven_Myd02, twelve_Myd02, thirteen_Myd02,
                fourteen_Myd02, fifteen_Myd02, sixteen_Myd02, seventeen_Myd02, eighteen_Myd02, 
                nineteen_Myd02, twenty_Myd02, twenty_one_Myd02, twenty_two_Myd02, twenty_three_Myd02]
            
            #f_Myd35
            cero_Myd35 = list(np.array(f_Myd35)[cero])
            one_Myd35 = list(np.array(f_Myd35)[one])
            two_Myd35 = list(np.array(f_Myd35)[two])
            three_Myd35 = list(np.array(f_Myd35)[three])
            four_Myd35 = list(np.array(f_Myd35)[four])
            five_Myd35 = list(np.array(f_Myd35)[five])
            six_Myd35 = list(np.array(f_Myd35)[six])
            seven_Myd35 = list(np.array(f_Myd35)[seven])
            eight_Myd35 = list(np.array(f_Myd35)[eight])
            nine_Myd35 = list(np.array(f_Myd35)[nine])
            ten_Myd35 = list(np.array(f_Myd35)[ten])
            eleven_Myd35 = list(np.array(f_Myd35)[eleven])
            twelve_Myd35 = list(np.array(f_Myd35)[twelve])
            thirteen_Myd35 = list(np.array(f_Myd35)[thirteen])
            fourteen_Myd35 = list(np.array(f_Myd35)[fourteen])
            fifteen_Myd35 = list(np.array(f_Myd35)[fifteen])
            sixteen_Myd35 = list(np.array(f_Myd35)[sixteen])
            seventeen_Myd35 = list(np.array(f_Myd35)[seventeen])
            eighteen_Myd35 = list(np.array(f_Myd35)[eighteen])
            nineteen_Myd35 = list(np.array(f_Myd35)[nineteen])
            twenty_Myd35 = list(np.array(f_Myd35)[twenty])
            twenty_one_Myd35 = list(np.array(f_Myd35)[twenty_one])
            twenty_two_Myd35 = list(np.array(f_Myd35)[twenty_two])
            twenty_three_Myd35 = list(np.array(f_Myd35)[twenty_three])
            f_Myd35_hours = [cero_Myd35, one_Myd35, two_Myd35, three_Myd35, four_Myd35, five_Myd35, six_Myd35, seven_Myd35
                , eight_Myd35, nine_Myd35, ten_Myd35, eleven_Myd35, twelve_Myd35, thirteen_Myd35,
                fourteen_Myd35, fifteen_Myd35, sixteen_Myd35, seventeen_Myd35, eighteen_Myd35, 
                nineteen_Myd35, twenty_Myd35, twenty_one_Myd35, twenty_two_Myd35, twenty_three_Myd35]
            
    
            hours = ['0000','0100','0200','0300','0400','0500','0600','0700','0800','0900','1000','1100','1200',
                    '1300','1400','1500','1600','1700','1800','1900','2000','2100','2200','2300']
            
            return hours, f_Myd03_hours, f_Myd02_hours, f_Myd35_hours
            # return  f_Myd03, f_Myd02, file_myd03
            # print('MYD021KM in MYD03',len(f_Myd02),'Matching elements have been found')
                    
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


    @classmethod
    def read_csv_files(cls, path, year, month):  
        try:
           # open the file in the write mode
           with open(path + year + month +'.csv', 'r') as f:
               line = f.readlines()
               line = line[-1]
               day = line[10:12]
               hour = line[13:17]
               
           return day, hour               
           
        except OSError as err:
            print("OS error: {0}".format(err))