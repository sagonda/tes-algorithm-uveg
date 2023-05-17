import csv
import numpy as np

class Utilities():

    consA      = np.float64(119110000.0)
    consB      = np.float64(14388.0)
    lonOnda29  = np.float64(8.55)
    lonOnda31  = np.float64(11.015)
    lonOnda32  = np.float64(12.02)
    nOnda29    = np.float64(1173.263)
    nOnda31    = np.float64(908.273)
    nOnda32    = np.float64(831.523)
    emissivity = 0.98
    lo = [8.535, 11.015, 12.041]

    c1 = 0.998449
    c2 = -0.654215
    c3 = 0.735536 
    K1 = [2631.58, 735.84, 471.25] 
    K2 = [1686.18, 1306.72, 1195.27]

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


    def chance_units(consA, consB, bt, radtotal, radup, raddown, tautotal, emissivity, nOnda29, nOnda31, nOnda32, lonOnda29, lonOnda31, \
                          lonOnda32, Lbb29, Lbb31, Lbb32):
        try:
            # Cambio de unidades radiancia total
            rt29 = (((radtotal[0,:] * nOnda29)/lonOnda29)/1000)
            rt31 = (((radtotal[1,:] * nOnda31)/lonOnda31)/1000)
            rt32 = (((radtotal[2,:] * nOnda32)/lonOnda32)/1000)

            # Cambio de unidades radiancia upwelling
            lUp29 = (((radup[0,:] * nOnda29)/lonOnda29)/1000)
            lUp31 = (((radup[1,:] * nOnda31)/lonOnda31)/1000)
            lUp32 = (((radup[2,:] * nOnda32)/lonOnda32)/1000)

            Ldown_29 = ((rt29 - lUp29)/(1-emissivity)/tautotal[0,:])
            Ldown_31 = ((rt31 - lUp31)/(1-emissivity)/tautotal[1,:])
            Ldown_32 = ((rt32 - lUp32)/(1-emissivity)/tautotal[2,:])

            # Brigtnees Temperature (K) to radiances
            l29 = (consA) / ((lonOnda29**5)*(np.exp(consB/(bt[0,:]*lonOnda29))-1))
            l31 = (consA) / ((lonOnda31**5)*(np.exp(consB/(bt[1,:]*lonOnda31))-1))
            l32 = (consA) / ((lonOnda32**5)*(np.exp(consB/(bt[2,:]*lonOnda32))-1))

            # Calculo B(T) ECWF
            blonT29 = emissivity * Lbb29 + (1 - emissivity) * Ldown_29
            blonT31 = emissivity * Lbb31 + (1 - emissivity) * Ldown_31
            blonT32 = emissivity * Lbb32 + (1 - emissivity) * Ldown_32

            Lup_29 = l29 - blonT29 * tautotal[0,:]
            Lup_31 = l31 - blonT31 * tautotal[1,:]
            Lup_32 = l32 - blonT32 * tautotal[2,:]        

            Ldown_29 = ((rt29 - lUp29)/(1-emissivity)/tautotal[0,:])#*1.5
            Ldown_31 = ((rt31 - lUp31)/(1-emissivity)/tautotal[1,:])#*1.5
            Ldown_32 = ((rt32 - lUp32)/(1-emissivity)/tautotal[2,:])#*1.5

            return Lup_29, Lup_31, Lup_32, Ldown_29, Ldown_31, Ldown_32

        except OSError as err:
            print("OS error: {0}".format(err))


    def write_csv_files(path ,file, year, month):  
        try:
            with open(path + year + month +'.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([file])
            print('file added to the general file!!!')

        except OSError as err:
            print("OS error: {0}".format(err))


    def create_array_bidimentional(x_dimention, y_dimention):
        newarray = np.zeros(shape=(x_dimention, y_dimention), dtype = np.float64)

        return newarray


    def create_array_unidimentional(x_dimention):
        newarray = np.zeros(shape=(x_dimention), dtype = np.float64)

        return newarray


    def packed_value(input_matrix, add_offset, scale_factor, data_type):
        if input_matrix.ndim == 2:
            result = np.empty((input_matrix.shape[0],input_matrix.shape[1]), dtype = data_type)
        elif input_matrix.ndim == 1:
            result = np.empty(input_matrix.shape[0], dtype = data_type)
        result[:] = (input_matrix - add_offset) / scale_factor

        return result