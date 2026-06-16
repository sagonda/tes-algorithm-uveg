#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TES Algorithm UVEG - Setup Configuration

This file is part of TES Algorithm UVEG.
© 2020-2026 Daniel Salinas, Drazen Skokovic, University of Valencia
Licensed under CC BY-NC 4.0: https://creativecommons.org/licenses/by-nc/4.0/
"""

from setuptools import setup, find_packages
import os

# Read the long description from README
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements from requirements.txt
with open(os.path.join(os.path.dirname(__file__), 'requirements.txt'), encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='tes-algorithm-uveg',
    version='1.1.0',
    author='Daniel Salinas González, Drazen Skokovic',
    author_email='daniel.salinas@uv.es',
    maintainer='Daniel Salinas González',
    maintainer_email='daniel.salinas@uv.es',
    url='https://github.com/uv-uveg/tes-algorithm-uveg',
    description='Thermal Emissivity and Surface Temperature Retrieval Algorithm (UVEG Edition)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='CC BY-NC 4.0 (Creative Commons Attribution-NonCommercial 4.0 International)',
    
    # Project classification
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: Other/Proprietary',
        'Natural Language :: English',
        'Natural Language :: Spanish',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'Topic :: Scientific/Engineering :: Remote Sensing',
        'Topic :: Scientific/Engineering :: Image Processing',
    ],
    
    # Project metadata
    keywords=[
        'remote-sensing',
        'modis',
        'satellite',
        'land-surface-temperature',
        'thermal-infrared',
        'geospatial',
        'tes-algorithm',
        'teledetection',
    ],
    
    python_requires='>=3.8',
    install_requires=requirements,
    
    packages=find_packages(exclude=['tests', 'tests.*', 'docs', 'pruebas']),
    include_package_data=True,
    
    entry_points={
        'console_scripts': [
            'tes-algorithm=tes_algorithm.cli:main',
        ],
    },
    
    project_urls={
        'Documentation': 'https://github.com/uv-uveg/tes-algorithm-uveg#readme',
        'Source': 'https://github.com/uv-uveg/tes-algorithm-uveg',
        'Tracker': 'https://github.com/uv-uveg/tes-algorithm-uveg/issues',
        'License': 'https://creativecommons.org/licenses/by-nc/4.0/',
    },
    
    # Additional metadata
    zip_safe=False,
    platforms=['any'],
)
