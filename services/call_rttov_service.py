import numpy as np
from rttov_wrapper_f2py import *
import sys

class CallRttovService():

    def __init__(self, path_Rttov_coef, datetimes, angles, surfgeom, surftype, s2m, skin, simplecloud, clwscheme, icecloud, zeeman, p, t, he):
        self.path_Rttov_coef = path_Rttov_coef
        self.datetimes       = datetimes
        self.angles          = angles
        self.surfgeom        = surfgeom
        self.surftype        = surftype
        self.s2m             = s2m 
        self.skin            = skin
        self.simplecloud     = simplecloud
        self.clwscheme       = clwscheme
        self.icecloud        = icecloud
        self. zeeman         = zeeman
        self.p               = p
        self.t               = t
        self.he              = he


    def call_rttov(self):
        ''' Resum : Function process RTTOV

            Params: (datetimes, angles, surfgeom, surftype, s2m, skin, simplecloud, clwscheme, \
                            icecloud, zeeman, p, t, he)

            Output: Matrix-> bt, radtotal, radup, raddown, tautotal

            Call example: bt, radtotal, radup, raddown, tautotal = call_rttov(datetimes, angles, \
                surfgeom, surftype, s2m, skin, simplecloud, clwscheme, icecloud, zeeman, p, t, he)
        '''
        try:
            nprofiles    = self.t.shape[1]
            nlevels      = 25
            gas_units    = 1  
            mmr_cldaer   = 1
            gas_id_q     = 1 # See wrapper user guide for gas IDs
            gas_id       = np.array([gas_id_q], dtype=np.int32)
            gases        = np.empty((nlevels, self.t.shape[1], len(gas_id)), order='F', dtype=np.float64)
            gases[:,:,0] = self.he

            ''' Load the instrument
             Specify RTTOV and wrapper options. In this case:
             - turn interpolation on
             - supply CO2 as a variable gas
             - turn cloudy IR simulations on
             - provide access to the full radiance structure after calling RTTOV
             - turn on the verbose wrapper option
             NB the spaces in the string between option names and values are important! '''

            opts_str = 'opts%interpolation%addinterp 1 ' \
                        'opts%config%verbose 1 '         \
                        'opts%rt_ir%addsolar 0 '         \
                        'opts%config%do_checkinput 0 '   \
                        'verbose_wrapper 0 '             \
                        'nthreads 1 '                    \
                        'nprofs_per_call 30000 '         \
                        'check_opts 1 '                  \
                        'store_trans 1 '                 \
                        'store_rad 1 '                   \
                        'store_rad2 1 '
                        #'opts%rt_all%addrefrac 0 ' \

            ''' Specify instrument and channel list and add coefficient files to the options string '''
            rtcoef_dir   = self.path_Rttov_coef
            rtcoef_file  = rtcoef_dir + 'rttov9pred54L/rtcoef_eos_1_modis.dat'            
            nchannels    = 36
            channel_list = np.arange(1, nchannels+1, 1, dtype=np.int32)            
            opts_str    += ' file_coef ' + rtcoef_file 

            ''' Call the wrapper subroutine to load the instrument and check we obtained a valid instrument ID '''
            inst_id = rttov_load_inst(opts_str, channel_list)
            if inst_id < 1:
                print('Error loading instrument')
                sys.exit(1)

            err = rttov_print_options(inst_id)
            channels = 3

            ''' Declare arrays for other inputs and outputs
                Define array for input/output surface emissivity and BRDF '''
            surfemisrefl = np.empty((channels, nprofiles, 2), order='F', dtype=np.float64)

            # Define direct model outputs
            btrefl  = np.empty((channels, nprofiles), order='F', dtype=np.float64)
            rad = np.empty((channels, nprofiles), order='F', dtype=np.float64)

            ''' Call RTTOV
                Initialise the surface emissivity and reflectance before every call to RTTOV:
                in this case we specify a negative number to use the IR atlas over land
                (because we initialised it above) and to use RTTOV's emissivity models over sea surfaces '''
            surfemisrefl[:,:,:] = -1.

            ''' Call the wrapper subroutine to run RTTOV direct '''
            err = rttov_call_direct(inst_id, channel_list[[28,30,31]], self.datetimes, self.angles, self.surfgeom, self.surftype, self.skin, self.s2m, \
                                    self.simplecloud, self.clwscheme, self.icecloud, self.zeeman, self.p, self.t, gas_units, mmr_cldaer, \
                                    gas_id, gases, surfemisrefl, btrefl, rad)
            if err != 0:
                print('Error running RTTOV direct')
                sys.exit(1)

            ''' Examine outputs
                Outputs available are:
                - surfemisrefl array contains surface emissivities (and reflectances) used by RTTOV
                - rad array contains RTTOV radiance%total array
                - btrefl array contains RTTOV radiance%bt and radiance%refl arrays (depending on channel wavelength)
                - it is also possible to access the whole radiance structure because we set the store_rad option above '''

            # To obtain data from RTTOV output structures, declare an array and call the relevant wrapper subroutine.
            bt       = np.empty((channels, nprofiles), order='F', dtype=np.float64)
            err      = rttov_get_bt(inst_id, bt)
            radtotal = np.empty((channels, nprofiles), order='F', dtype=np.float64)
            err      = rttov_get_rad_total(inst_id, radtotal)
            radup    = np.empty((channels, nprofiles), order='F', dtype=np.float64)
            err      = rttov_get_rad2_upclear(inst_id, radup)
            raddown  = np.empty((channels, nprofiles), order='F', dtype=np.float64)
            err      = rttov_get_rad2_dnclear(inst_id, raddown)
            tautotal = np.empty((channels, nprofiles), order='F', dtype=np.float64)
            err      = rttov_get_tau_total(inst_id, tautotal)

            # Deallocate memory for all instruments and atlases
            err = rttov_drop_all()
            if err != 0: print('Error deallocating wrapper')            

            return bt, radtotal, radup, raddown, tautotal
        except Exception as err:
          print("Error run RTTOV", err)