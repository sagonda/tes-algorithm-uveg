# -*- coding: utf-8 -*-
"""
TES Algorithm UVEG - Utilities Package

This package contains utility functions and helpers for data extraction,
manipulation, and common tasks across the TES algorithm pipeline.

This file is part of TES Algorithm UVEG.
© 2020-2026 Daniel Salinas, Drazen Skokovic, University of Valencia
Licensed under CC BY-NC 4.0: https://creativecommons.org/licenses/by-nc/4.0/

Modules:
    utilities: Core utility functions (array operations, file I/O, constants)
    utilities_extraction_data: Specialized data extraction functions
"""

__version__ = '1.1.0'
__author__ = 'Daniel Salinas González, Drazen Skokovic'
__license__ = 'CC BY-NC 4.0'

from .utilities import Utilities
from .utilities_extraction_data import UtilitiesExtractionData

__all__ = [
    'Utilities',
    'UtilitiesExtractionData',
]
