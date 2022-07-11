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

class UvegProcess:
    
    #********************************************************************
    # 1. Functions read files product MODIS AQUA - TERRA and ERA5 profiles
    
    @classmethod
    def read_ndvi_file(cls, path_Input, year, month):
        '''
        Resum: Function read ndvi file
        
        Params: (path_ndvi_file, month)
        
        Output: Matrix-> ndvi_lat, ndvi_lon, ndvi_data
        
        Call example: ndvi_lat, ndvi_lon, ndvi = read_ndvi_file('/path_Input/',  month)
        
        '''
        
        try:
            print('#################################################')
            print('Read files NDVI.................')
            
            # Read files
            path_ndvi = path_Input + year + '/' + month + '/'
            data = net.Dataset(path_ndvi + 'out.nc','r')
            
            # Read variables
            # print(data.variables.keys())
            ndvi = data.variables['ndvi'][:]
            # print(ndvi.shape)
            #red = data.variables['red'][:]
            ndvi_lat = data.variables['lat'][:]
            ndvi_lon = data.variables['lon'][:]
            
            print('NDVI files upload!!')
            print('#################################################')
            data.close()
            return ndvi_lat, ndvi_lon, ndvi
            
        except ValueError:
            print('Error load NDVI')  
            
    @classmethod
    def read_myd03_files(cls, path_Input, year, month, day):
        '''
        Resum: Function read MODIS Myd03 file
        
        Params: (path_Myd03_files, year, month, day)
        
        Output: list-> files myd03
        
        Call example: list_myd03_files = read_myd03_files('/path_Input/',  year, month, day)
        
        '''
        try:
            print('#################################################')
            print('Read files Myd03.................')
            path_modis_myd03 =  path_Input + year + '/' + month + '/' + day + '/'
            f_Myd03 = sorted(glob.glob( path_modis_myd03 + "/*.hdf"))
            
            print('Myd03 files upload!!')
            print('#################################################')
            return f_Myd03
        
        except ValueError:
            print('Error load MYD03')   
            
    @classmethod        
    def read_myd021_files(cls, path_Input, year, month, day):
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
            path_modis02 = path_Input + year + '/' + month + '/' + day + '/'
            f_Myd02 = sorted(glob.glob( path_modis02 + "/*.hdf"))
            
            print("MYD021KM files have been successfully uploaded!!!")
            print('#################################################')
            return f_Myd02
    
        except ValueError:
            print('Error load MYD021KM')
            
    @classmethod        
    def read_myd35_files(cls, path_Input, year, month, day):
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
            path_modis35 = path_Input + year + '/' + month + '/' + day + '/'
            f_Myd35 = sorted(glob.glob( path_modis35 + "/*.hdf"))
            
            print("myd35KM files have been successfully uploaded!!!")
            print('#################################################')
            return f_Myd35
    
        except ValueError:
            print('Error load myd35')
            
    @classmethod
    def match_myd03_myd021_myd35(cls, f_Myd03 , f_Myd02, f_Myd35):
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
                
                
                
    def read_match_files(f_Myd03, f_Myd02, f_Myd35):
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
            
    @classmethod
    def cloud_mask(cls, f_Myd35_hours, hours_list):
        
        data_Myd35 = [SD(files, SDC.READ) for files in f_Myd35_hours[hours_list]]
        sds_obj = [file.select('Cloud_Mask') for file in data_Myd35]
        data = [sds_obj[i].get() for i in range(len(sds_obj))]
        maskVals = [data[i][:,:,:] for i in range(len(data))]
        return maskVals
    
    @classmethod
    def bits_stripping(cls, bit_start,bit_count,value):
        
        bitmask=pow(2,bit_start+bit_count)-1
        return np.right_shift(np.bitwise_and(value,bitmask),bit_start)

# status_flag = bits_stripping(0,1,maskVals[0,:,:]) 
# day_flag = bits_stripping(3,1,maskVals[0,:,:]) 
# cloud_mask_flag = bits_stripping(1,2,maskVals[0,:,:])
            
    
    # def read_era5_files(path_Input, var_name, year, month, day):
    #     ''' 
    #     Resum: Function read Era5 files
        
    #     Params: (path_Input, var_name, year, month, day, to proces)
        
    #     Output list-> var and files 
        
    #     Call example: nc_fileT, file_T = read_era5_files(path_Input, 't', year, month, day)
    #     '''
    #     # print('#################################################')
    #     # print('Read files Era5.................')
        
    #     file_atm = sorted(glob.glob( path_Input+year+'/'+month+'/'+day+"/*"+var_name+".nc"))
        
    #     var_atm = [re.split("\W+|_",i) for i in file_atm]
    #     var_atm = [i[-3] for i in var_atm]
        
    #     # print("Era5 files have been successfully uploaded!!!")
    #     # print('#################################################')
    #     return var_atm, file_atm
    
    # def extract_file_match(var_atm_list, match_var, var_original):
    #     ''' 
    #     Resum: Function to extract matching files
        
    #     Params: (var_atm_list, match_var, var_original)
        
    #     Output list-> match variable 
        
    #     Call example: nc_fileT, file_T = read_era5_files(path_Input, 't', year, month, day)
    #     '''
    #     try:
    #         var_atm_matrix = np.array(var_atm_list)
    #         var_atm_match = np.array(match_var)
           
    #         match_files_index = np.intersect1d(var_atm_matrix, var_atm_match,  return_indices=True)
    #         index_match = list(match_files_index[1])
    #         match_var = (list(itemgetter(*index_match)(var_original)))
            
    #         # print("Era5 files have been successfully match!!!")
    #         # print('#################################################')
    #         return match_var
    #     except OSError as err:
    #             print("OS error: {0}".format(err))
 
    
    
    
    @classmethod
    def extract_mask_land(cls, path_Input):
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
    
    #********************************************************************
    
    #********************************************************************
    # 2. Functions extract data variables files MODIS and ERA5
    @classmethod
    def extract_vars_era5(cls, path_input, year, month, day, mask_sea_land_era5, hours, hours_list, file_data):
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

    @classmethod        
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
            
    @classmethod        
    def extract_vars_myd03(cls, f_Myd03_hours, hours_list):
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
            
    # def modis_21(file_Myd21):
    #     ''' 
    #     Resum: Function extract vars LST&E myd21, lat, lon
        
    #     Params: (file myd21)
        
    #     Output Matrix-> temp21, lat21, lon21, em29, em31, em32
        
    #     Call example: temp21, lat21, lon21, em29, em31, em32 = modis_21(f_Myd21)
    #     '''
        
    #     try:
    #         #====== READ HDF5 MODIS MYD03
    #         myd21 = net.Dataset(file_Myd21)
    #         lat21 = myd21.variables['Latitude'][:] 
    #         lon21 = myd21.variables['Longitude'][:] 
    #         image_temp21 = myd21.variables['LST'][:] 
    #         range21 = myd21.variables['LST'].valid_range 
    #         gain21= myd21.variables['LST']._Scale 
    #         offset21 = myd21.variables['LST']._Offset 
           
    #         print("MYD21 files have been successfully uploaded!!!")
     
    #         #******Emissivity***************************
    #         emis29 = myd21.variables['Emis_29'][:] 
    #         range_29 = myd21.variables['Emis_29'].valid_range 
    #         gain_29 = myd21.variables['Emis_29']._Scale 
    #         offset_29 = myd21.variables['Emis_29']._Offset 
    #         emis31 = myd21.variables['Emis_31'][:] 
    #         emis32 = myd21.variables['Emis_32'][:]  
     
    #         # #******LST Land Surface Temperature*********
    #         temp21 = (image_temp21*gain21) + offset21            
    #         em29 = (emis29*gain_29) + offset_29
    #         em31 = (emis31*gain_29) + offset_29
    #         em32 = (emis32*gain_29) + offset_29
       
    #         myd21.close()
               
    #         return temp21.ravel(), lat21, lon21, em29.ravel(), em31.ravel(), em32.ravel()
    #     except:
            
    #         print("Error in the path of the MODIS files")
    @classmethod        
    def modis_02(cls, f_Myd02_hours, hours_list, i_modis, cloud_mask_flag, dimension_original):
        ''' 
        Resum: Function extract vars product myd021km
        
        Params: (f_Myd02, mask2)
        
        Output Matrix-> radiance, image_rad
        
        Call example: radiance, image_rad = modis_02(f_Myd02, mask2)
        '''
        try: 
            #*****Product MYD021KM
            myd02 = [net.Dataset(files) for files in f_Myd02_hours[hours_list]]
            
            # lat = myd02.variables['Latitude'][:]
            # lon = myd02.variables['Longitude'][:] 
            image_rad = [i.variables['EV_1KM_Emissive'] for i in myd02]
            gain = [i.variables['EV_1KM_Emissive'].radiance_scales for i in myd02]
            offset = [i.variables['EV_1KM_Emissive'].radiance_offsets for i in myd02]
            # image_ref1 = [i.variables['EV_1KM_RefSB'][:] for i in myd02]
            # gain1 = [i.variables['EV_1KM_RefSB'].radiance_scales for i in myd02]
            # offset1 = [i.variables['EV_1KM_RefSB'].radiance_offsets for i in myd02] 
            # hueco = [i.variables['EV_1KM_RefSB']._FillValue for i in myd02] 
            
            n = image_rad[i_modis][0,:,0].shape[0]
            m = image_rad[i_modis][0,0,:].shape[0]
            m_n = m * n
   
            radiance = np.empty(shape=(3,dimension_original,1354))
            radiance[0,:,:] = gain[i_modis][8] * (image_rad[i_modis][8,:,:] - offset[i_modis][8] )  
            radiance[1,:,:] = gain[i_modis][10] * (image_rad[i_modis][10,:,:] - offset[i_modis][10] )  
            radiance[2,:,:] = gain[i_modis][11] * (image_rad[i_modis][11,:,:] - offset[i_modis][11] )  
            
            radiance = np.where(cloud_mask_flag==0, 0, radiance)
            radiance = np.reshape(radiance.ravel(),(3,m_n))
            myd02[i_modis].close()

            return radiance, image_rad[:]
        except:
            
            print("Error in the path of the MODIS files")
            
    
    
    #********************************************************************
    # 2.1. Function for extracting the indices of the original matrix to reconstruct it again.
    @classmethod
    def extract_index_image(cls, lat_Modis, lon_Modis, mask_sea_land_modis, dimension):
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
    
    #********************************************************************
    
    #********************************************************************
    # 3. Functions to perform a trimming on global data from a Modis image     
    @classmethod      
    def extract_ndvi(cls, lat_Modis, lon_Modis, ndvi_lat, ndvi_lon, ndvi):
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
    def extract_index_modis_and_era(cls, lat_Nc, lon_Nc, lat_Modis, lon_Modis, mask_sea_land_era5):
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
          
          
    #********************************************************************
    
    #********************************************************************
    # 4. Function to mask Era5 global variables and function to create RTTOV input profiles.
    @classmethod
    def extract_height(cls, height, mask_land_modis, cloud_mask_flag):
      height = np.where(cloud_mask_flag==0, 0, height)
      h = height.ravel()
      h = h[mask_land_modis]
      return h

    @classmethod
    def extract_zenith(cls, zenith, mask_land_modis, cloud_mask_flag):
      zenith = np.where(cloud_mask_flag==0, 0, zenith)
      z = zenith.ravel()
      z = z[mask_land_modis]
      return z

    @classmethod
    def extract_temperature(cls, temp_era, index_Era):
        n = len(temp_era[0,:,0])
        m = len(temp_era[0,0,:])
        m_n = m * n
        t = np.reshape(temp_era,(25,m_n))
        t = t[:,index_Era]
        t = np.reshape(t,(25,len(index_Era[0,:])))
        return np.round(t,5)

    @classmethod
    def extract_humidity(cls, hum_E, index_Era):
        n = len(hum_E[0,:,0])
        m = len(hum_E[0,0,:])
        m_n = m * n
        he = np.reshape(hum_E,(25,m_n))
        he = he[:,index_Era]
        he = np.reshape(he,(25,len(index_Era[0,:])))
        #he = 28.9644/18.01528*1e6*he
        return np.round(he,8)

    @classmethod
    def extract_param_2m(cls, t_2m, sk_t, d2_m, ms_l1, index_Era, h_):
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

    @classmethod
    def create_profiles(cls, dimension_modis, z, latitud, longitud, h_, p2m, t2, q2m, sk, level, temp_era, year, month, day):
        ''' 
        Resum: Function to create RTTOV input profiles
        
        Params: (dimension_modis, z, latitud, longitud, h_, p2m, t2, q2m, sk, level, temp_era, date_era5, date_modis)
        
        Output: Matrix-> datetimes, angles, surftype, surfgeom, s2m, skin, simplecloud, clwscheme, \
            icecloud, zeeman, p, t
        
        Call example: datetimes, angles, surftype, surfgeom, s2m, skin, simplecloud, clwscheme, Icecloud, \
            zeeman, p, t = create_profiles(dimension_modis, z, latitud, longitud, h_, p2m, t2, q2m, sk, level, temp_era)
        '''

        try:

            datetimes = np.empty((dimension_modis,6), order='F', dtype=np.int32)
            datetimes[:,:] = np.array([int(year),int(month),int(day),0,0,0])
            datetimes = datetimes.transpose()
            
            angles = np.empty((z.shape[0],4), order='F', dtype=np.float32)
            angles[:,0] = z
            angles = angles.transpose()
            
            surftype = np.empty((dimension_modis,2), order='F', dtype=np.int32)
            surftype[:,0] = 0
            surftype[:,1] = 0
            surftype = surftype.transpose()
            
            surfgeom = np.empty((dimension_modis,3), order='F', dtype=np.float64)
            surfgeom[:,0] = latitud
            surfgeom[:,1] = longitud
            surfgeom[:,2] = (h_/1000)
            surfgeom = surfgeom.transpose()
            
            s2m = np.empty((dimension_modis,6), order='F', dtype=np.float64)
            s2m[:,0] = p2m
            s2m[:,1] = t2
            s2m[:,2] = q2m
            s2m[:,3:] = 0
            s2m = s2m.transpose()
            
            skin = np.empty((dimension_modis, 10), order='F', dtype=np.float64)
            skin[:,0] = sk
            skin[:,1:] = 0
            skin = skin.transpose()
            
            simplecloud = np.empty((dimension_modis,2), order='F', dtype=np.float64)
            simplecloud[:,0] = 500
            simplecloud[:,1] = 0
            simplecloud = simplecloud.transpose()
            
            clwscheme = np.empty((dimension_modis), order='F', dtype=np.int32)
            clwscheme[:] = 0
            clwscheme = clwscheme.transpose()
            
            icecloud= np.empty((dimension_modis,2), order='F', dtype=np.int32)
            icecloud[:,0] = 0
            icecloud[:,1] = 0
            icecloud = icecloud.transpose()
            
            zeeman = np.empty((dimension_modis,2), order='F', dtype=np.float64)
            zeeman = zeeman.transpose()
            
            p = np.empty((dimension_modis, 25), order='F', dtype=np.float64)
            p[:,:] = level
            p = p.transpose()
            
            t = np.empty((25, dimension_modis), order='F', dtype=np.float64)
            t[:,:] = temp_era
            
            return datetimes, angles, surftype, surfgeom, s2m, skin, simplecloud, clwscheme, icecloud, zeeman, p, t

        except OSError as err:
            print("OS error: {0}".format(err))

    @classmethod      
    def call_rttov(cls, path_Rttov_coef, datetimes, angles, surfgeom, surftype, s2m, skin, simplecloud, clwscheme, \
                        icecloud, zeeman, p, t, he):
        
        ''' 
        Resum: Function process RTTOV 
        
        Params: (datetimes, angles, surfgeom, surftype, s2m, skin, simplecloud, clwscheme, \
                        icecloud, zeeman, p, t, he)
        
        Output: Matrix-> bt, radtotal, radup, raddown, tautotal
        
        Call example: bt, radtotal, radup, raddown, tautotal = call_rttov(datetimes, angles, \
                surfgeom, surftype, s2m, skin, simplecloud, clwscheme, icecloud, zeeman, p, t, he)
        '''
        try:
            print('RUN RTTOV')
            nprofiles = t.shape[1]
            nlevels = 25
            gas_units = 1  
            mmr_cldaer = 1
            
            # See wrapper user guide for gas IDs
            gas_id_q = 1
            gas_id = np.array([gas_id_q], dtype=np.int32)
                    
            gases = np.empty((25, t.shape[1], len(gas_id)), order='F', dtype=np.float64)
            gases[:,:,0] = he
            
    
            # =================================================================
            # Load the instrument
            
            # Specify RTTOV and wrapper options. In this case:
            # - turn interpolation on
            # - supply CO2 as a variable gas
            # - turn cloudy IR simulations on
            # - provide access to the full radiance structure after calling RTTOV
            # - turn on the verbose wrapper option
            # NB the spaces in the string between option names and values are important!
            #'opts%rt_all%addrefrac 0 '   \
            opts_str = 'opts%interpolation%addinterp 1 ' \
                        'opts%config%verbose 1 '    \
                        'opts%rt_ir%addsolar 0 '    \
                        'opts%config%do_checkinput 0 '  \
                        'verbose_wrapper 0 '         \
                        'nthreads 2 '                \
                        'nprofs_per_call 30000 '       \
                        'check_opts 1 '              \
                        'store_trans 1 '             \
                        'store_rad 1 '               \
                        'store_rad2 1 '
            
          
            # Specify instrument and channel list and add coefficient files to the options string
            # rtcoef_dir = '/usr/local/rttov12/rtcoef_rttov12/'
            rtcoef_dir = path_Rttov_coef
            
            rtcoef_file = rtcoef_dir + 'rttov9pred54L/rtcoef_eos_1_modis.dat'
            #sccldcoef_file = rtcoef_dir + 'cldaer_ir/sccldcoef_noaa_19_hirs.dat'
            
            nchannels = 36
            #print(nchannels)
            channel_list = np.arange(1, nchannels+1, 1, dtype=np.int32)
            
            #print(channel_list)
            
            opts_str += ' file_coef ' + rtcoef_file 
            #print(opts_str)
            
            # Call the wrapper subroutine to load the instrument and check we obtained a valid instrument ID
            inst_id = rttov_load_inst(opts_str, channel_list)
            if inst_id < 1:
                print('Error loading instrument')
                sys.exit(1)
            # =================================================================
            err = rttov_print_options(inst_id)
            #print(err)
            
            # Canales a procesar
            channels = 3
            
            # =================================================================
            # Declare arrays for other inputs and outputs
            
            # Define array for input/output surface emissivity and BRDF
            surfemisrefl = np.empty((channels, nprofiles, 2), order='F', dtype=np.float64)
        
            # Define direct model outputs
            btrefl  = np.empty((channels, nprofiles), order='F', dtype=np.float64)
            rad = np.empty((channels, nprofiles), order='F', dtype=np.float64)
            # =================================================================
        
            # =================================================================
            # Call RTTOV
            
            # Initialise the surface emissivity and reflectance before every call to RTTOV:
            # in this case we specify a negative number to use the IR atlas over land
            # (because we initialised it above) and to use RTTOV's emissivity models over sea surfaces
            surfemisrefl[:,:,:] = -1.
            #print('call direct model')
            #Call the wrapper subroutine to run RTTOV direct

            err = rttov_call_direct(inst_id, channel_list[[28,30,31]], datetimes, angles, surfgeom, surftype, skin, s2m, \
                                    simplecloud, clwscheme, icecloud, zeeman, p, t, gas_units, mmr_cldaer, \
                                    gas_id, gases, surfemisrefl, btrefl, rad)
            if err != 0:
                print('Error running RTTOV direct')
                sys.exit(1)
            # =================================================================
        
            # =================================================================
            # Examine outputs
            
            # Outputs available are:
            # - surfemisrefl array contains surface emissivities (and reflectances) used by RTTOV
            # - rad array contains RTTOV radiance%total array
            # - btrefl array contains RTTOV radiance%bt and radiance%refl arrays (depending on channel wavelength)
            # - it is also possible to access the whole radiance structure because we set the store_rad option above
            
            #print('Surface emissivity used by RTTOV')
            #print(surfemisrefl[:,:,0].transpose())
            
            #print('Total cloudy BT')    # This example has no visible/near-IR channels so this array contains BTs only
            #print(btrefl.transpose())
            
            # To obtain data from RTTOV output structures, declare an array and call the relevant wrapper subroutine.
            
            bt = np.empty((channels, nprofiles), order='F', dtype=np.float64)
            err = rttov_get_bt(inst_id, bt)
            #print('CALCULATED BRIGHTNEES TEMPERATURE (K)')
            #print(bt.transpose())
            
            radtotal = np.empty((channels, nprofiles), order='F', dtype=np.float64)
            err = rttov_get_rad_total(inst_id, radtotal)
            #print('CALCULATED TOTAL RADIANCES (mW/m2/sr/cm-1)')
            #print(radtotal.transpose())
            
            radup = np.empty((channels, nprofiles), order='F', dtype=np.float64)
            err = rttov_get_rad2_upclear(inst_id, radup)
            #print('Radiance Up')
            #print(radup.transpose())
            
            raddown = np.empty((channels, nprofiles), order='F', dtype=np.float64)
            err = rttov_get_rad2_dnclear(inst_id, raddown)
            #print('Radiance Down')
            #print(raddown.transpose())
            
            tautotal = np.empty((channels, nprofiles), order='F', dtype=np.float64)
            err = rttov_get_tau_total(inst_id, tautotal)
            #print('Total Transmittance')
            #print(tautotal.transpose())
            
            # =================================================================
            
            
            # =================================================================
            # Deallocate memory for all instruments and atlases
            
            err = rttov_drop_all()
            print('Finish RTTOV')
            if err != 0: print('Error deallocating wrapper')
            #=================================================================
            
            
            return bt, radtotal, radup, raddown, tautotal
        except Exception as err:
          print("Error run RTTOV", err)
        
    
    @classmethod
    def variables(cls, sk):    
    
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
    
    @classmethod
    def chance_units(cls, consA, consB, bt, radtotal, radup, raddown, tautotal, emissivity, nOnda29, nOnda31, nOnda32, lonOnda29, lonOnda31, \
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

                         
    @classmethod
    def tes_modis(cls, lo, lup, ldown, trans, radiance, z=False, aux=False, recal=False):
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
            
            eq1[:,:] = [d1_1[i]*trans[i,:]+d2_1[i]*trans[i,:]**2+d3_1[i]*z[:]+d4_1[i]*z[:]**2+d5_1[i]*trans[i,:]*z[:]+d6_1[i] for i in range(3)]
            eq2[:,:] = [f1_1[i]*lup[i,:]+f2_1[i]*lup[i,:]**2+f3_1[i]*z[:]+f4_1[i]*z[:]**2+f5_1[i]*lup[i,:]*z[:]+f6_1[i] for i in range(3)]
            erad[:,:]=[(((0.003*radiance[i,:]/trans[i,:])**2+(eq2[i,:]/trans[i,:])**2+(eq1[i,:]*((radiance[i,:]-lup[i,:]))/(trans[i,:]**2))**2)**0.5) for i in range(3)]
           
            return Ts.ravel(), e, BT, rad, R, erad

        except OSError as err:
            print("OS error: {0}".format(err))
            
    @classmethod        
    def recl_e(cls, emiss, dimension):
        
        mask_e = np.where(emiss > 0.992)
        e_max = emiss[mask_e]
        dif = e_max - 0.992
        e_ori_dif = emiss[:,mask_e] - dif
        e_mod = np.zeros(shape=(3,dimension),dtype = np.float64)
        e_mod = emiss
        e_mod[:,mask_e] = e_ori_dif
        
        return e_mod
    
    @classmethod
    def FVC(cls, ndvi, e31, e32):
        
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
    
    @classmethod
    def sw(cls, lo, radiance, dimension, e_29_original, e31_fvc, e32_fvc, ldown, R, trans, Ts, aux = False, aux1 = False):
        
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
    
    
                
    @classmethod
    def new_array(cls, array, mask, dimension_original, data_type):
        new = np.empty([dimension_original, 1354], dtype = data_type)
        new[:] = 0
        new[mask] = array
        
        return new
    
    
    @classmethod
    def create_nc_outfile(cls, path_output, year, month, day, date_modis, dimension_original,\
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

    @classmethod
    def write_csv_files(cls, path ,file, year, month):  
        try:
           # open the file in the write mode
           with open(path + year + month +'.csv', 'a', newline='') as f:
               writer = csv.writer(f)
               writer.writerow([file])
           print('file added to the general file!!!')
        except OSError as err:
            print("OS error: {0}".format(err))
            
    @classmethod
    def read_csv_files(cls, path, year, month):  
        try:
           # open the file in the write mode
           with open(path + year + month +'.csv', 'r') as f:
               line = f.readlines()
               line = line[-1]
               day = line[10:12]
               hour = line[13:15] + '00'
               print('day:',day,'hour:',hour)
               
           return day, hour               
           
        except OSError as err:
            print("OS error: {0}".format(err))
    
    @classmethod
    def packed_value(cls, input_matrix, add_offset, scale_factor, data_type):
        if input_matrix.ndim == 2:
            result = np.empty((input_matrix.shape[0],input_matrix.shape[1]), dtype = data_type)
        elif input_matrix.ndim == 1:
            result = np.empty(input_matrix.shape[0], dtype = data_type)
        result[:] = (input_matrix - add_offset) / scale_factor
        return result
    
    @classmethod
    def unpacked_value(cls, packed_value, add_offset, scale_factor):
        return (packed_value * scale_factor) + add_offset
    

