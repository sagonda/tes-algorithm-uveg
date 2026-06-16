# -*- coding: utf-8 -*-
"""
TES Algorithm UVEG - Services Package

This package contains specialized service classes for the TES Thermal Emissivity
and Surface Temperature retrieval algorithm.

This file is part of TES Algorithm UVEG.
© 2020-2026 Daniel Salinas, Drazen Skokovic, University of Valencia
Licensed under CC BY-NC 4.0: https://creativecommons.org/licenses/by-nc/4.0/

Modules:
    tes_algorithm_service: Core TES algorithm implementation
    call_rttov_service: RTTOV radiative transfer interface
    cloud_mask_service: Cloud detection and masking
    modis_02_service: MODIS L1B radiance reading
    create_profiles_service: Atmospheric profile creation
    create_nc_outfile_service: NetCDF4 output generation
    fvc_service: Fractional Vegetation Cover computation
    recal_lse_service: Land Surface Emissivity recalibration
    sw_service: Split-window algorithm
    change_units_service: Unit conversion utilities
    err_ldown_service: Downwelling radiance error
    read_ndvi_service: NDVI data reading
    bits_stripping_service: Bit-level data processing
    packed_value_service: Data compression/packing
    unpacked_value_service: Data decompression/unpacking
    new_array_service: Array allocation
    matching_files_service: MODIS file matching logic
"""

__version__ = '1.1.0'
__author__ = 'Daniel Salinas González, Drazen Skokovic'
__license__ = 'CC BY-NC 4.0'

# Core algorithm
from .tes_algorithm_service import TesAlgorithmService

# External model interface
from .call_rttov_service import CallRttovService

# Quality & filtering
from .cloud_mask_service import CloudMaskService

# Data readers
from .modis_02_service import Modis02Service
from .read_ndvi_service import ReadNdviService

# Processing pipeline
from .create_profiles_service import CreateProfilesService
from .fvc_service import FvcService
from .recal_lse_service import RecalLseService
from .sw_service import SwService
from .err_ldown_service import ErrLdownService

# Unit & data transformation
from .change_units_service import ChangeUnitsService
from .bits_stripping_service import BitsStrippingService
from .packed_value_service import PackedValueService
from .unpacked_value_service import UnpackedValueService
from .new_array_service import NewArrayService

# Output & utilities
from .create_nc_outfile_service import CreateNcOutfileService
from .matching_files_service import MatchingFilesService

__all__ = [
    'TesAlgorithmService',
    'CallRttovService',
    'CloudMaskService',
    'Modis02Service',
    'ReadNdviService',
    'CreateProfilesService',
    'FvcService',
    'RecalLseService',
    'SwService',
    'ErrLdownService',
    'ChangeUnitsService',
    'BitsStrippingService',
    'PackedValueService',
    'UnpackedValueService',
    'NewArrayService',
    'CreateNcOutfileService',
    'MatchingFilesService',
]
