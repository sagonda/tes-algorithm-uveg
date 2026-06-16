# -*- coding: utf-8 -*-
"""
TES Algorithm UVEG - Test Suite Package

This package contains unit tests, integration tests, and fixtures for
validating the TES algorithm components.

This file is part of TES Algorithm UVEG.
© 2020-2026 Daniel Salinas, Drazen Skokovic, University of Valencia
Licensed under CC BY-NC 4.0: https://creativecommons.org/licenses/by-nc/4.0/

Testing Strategy:
    - Unit tests for individual services
    - Integration tests for pipeline stages
    - Fixture-based setup for reusable test data
    - Coverage target: 80% minimum

Running Tests:
    pytest tests/ -v              # Verbose output
    pytest --cov=services         # Coverage report
    pytest -m "not slow"          # Skip slow tests
"""

import pytest
import numpy as np
from pathlib import Path

# Test markers
def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


@pytest.fixture
def sample_radiance_data():
    """Sample MODIS radiance data for testing.
    
    Returns:
        np.ndarray: Shape (3, 100) - 3 bands, 100 pixels
    """
    np.random.seed(42)
    return np.random.uniform(10, 20, size=(3, 100)).astype(np.float64)


@pytest.fixture
def sample_atmospheric_data():
    """Sample atmospheric correction data.
    
    Returns:
        tuple: (transmittance, lup, ldown)
    """
    np.random.seed(42)
    tau = np.random.uniform(0.7, 0.95, size=(3, 1))
    lup = np.ones((3, 100)) * 2.0
    ldown = np.ones((3, 100)) * 4.0
    return tau, lup, ldown


@pytest.fixture
def mock_netcdf_file(tmp_path):
    """Create a mock NetCDF4 file for testing.
    
    Returns:
        Path: Temporary file path
    """
    return tmp_path / "test_output.nc"


__all__ = [
    'sample_radiance_data',
    'sample_atmospheric_data',
    'mock_netcdf_file',
]
