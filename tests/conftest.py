"""
conftest.py - Pytest Configuration and Fixtures

Global test configuration and reusable fixtures for the test suite.

This file is part of TES Algorithm UVEG.
© 2020-2026 Daniel Salinas, Drazen Skokovic, University of Valencia
Licensed under CC BY-NC 4.0: https://creativecommons.org/licenses/by-nc/4.0/
"""

import pytest
import numpy as np
from pathlib import Path


@pytest.fixture(scope="session")
def test_data_dir():
    """Return path to test data directory."""
    return Path(__file__).parent / "data"


@pytest.fixture
def sample_modis_data():
    """Create sample MODIS-like data for testing.
    
    Returns:
        dict: Dictionary with typical MODIS data arrays
    """
    np.random.seed(42)
    
    return {
        'radiance': np.random.uniform(10, 20, size=(3, 100, 100)),
        'latitude': np.random.uniform(-90, 90, size=(100, 100)),
        'longitude': np.random.uniform(-180, 180, size=(100, 100)),
        'height': np.random.uniform(0, 5000, size=(100, 100)),
        'angle_zenith': np.random.uniform(0, 70, size=(100, 100)),
    }


@pytest.fixture
def sample_atmospheric_profiles():
    """Create sample atmospheric profile data.
    
    Returns:
        dict: Dictionary with temperature, humidity, pressure profiles
    """
    np.random.seed(42)
    
    n_profiles = 50
    n_levels = 37
    
    return {
        'temperature': np.random.uniform(200, 320, size=(n_profiles, n_levels)),
        'humidity': np.random.uniform(0, 1, size=(n_profiles, n_levels)),
        'pressure': np.random.uniform(100, 1050, size=(n_profiles, n_levels)),
        'latitude': np.random.uniform(-90, 90, size=(n_profiles,)),
        'longitude': np.random.uniform(-180, 180, size=(n_profiles,)),
    }


@pytest.fixture
def temporary_output_file(tmp_path):
    """Create a temporary output file path.
    
    Returns:
        Path: Path to temporary file
    """
    return tmp_path / "test_output.nc"


# Custom markers
def pytest_configure(config):
    """Register custom pytest markers."""
    config.addinivalue_line(
        "markers",
        "unit: marks test as a unit test"
    )
    config.addinivalue_line(
        "markers",
        "integration: marks test as an integration test"
    )
    config.addinivalue_line(
        "markers",
        "slow: marks test as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers",
        "requires_rttov: marks test as requiring RTTOV executable"
    )
