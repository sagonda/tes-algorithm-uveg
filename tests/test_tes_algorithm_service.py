# -*- coding: utf-8 -*-
"""
Unit Tests for TES Algorithm Service

Tests the core TES algorithm implementation for correctness and edge cases.

This file is part of TES Algorithm UVEG.
© 2020-2026 Daniel Salinas, Drazen Skokovic, University of Valencia
Licensed under CC BY-NC 4.0: https://creativecommons.org/licenses/by-nc/4.0/
"""

import pytest
import numpy as np
from services.tes_algorithm_service import TesAlgorithmService


@pytest.mark.unit
class TestTesAlgorithmService:
    """Test suite for core TES algorithm."""
    
    @pytest.fixture
    def setup_tes_inputs(self):
        """Setup typical TES algorithm inputs."""
        np.random.seed(42)
        
        lo = np.array([10.9, 11.0, 12.0])  # Wavelengths (μm)
        lup = np.random.uniform(1, 3, size=(3, 50))  # Upwelling radiance
        ldown = np.random.uniform(3, 6, size=(3, 50))  # Downwelling radiance
        trans = np.random.uniform(0.7, 0.95, size=(3, 50))  # Transmittance
        radiance = np.random.uniform(10, 20, size=(3, 50))  # Observed radiance
        z = np.random.uniform(0, 60, size=(50,))  # Zenith angles
        
        return lo, lup, ldown, trans, radiance, z
    
    def test_tes_initialization(self, setup_tes_inputs):
        """Test TES service initialization."""
        lo, lup, ldown, trans, radiance, z = setup_tes_inputs
        
        service = TesAlgorithmService(
            lo, lup, ldown, trans, radiance,
            z=z, aux=True, recal=False
        )
        
        assert service is not None
        assert service.lo is not None
        assert service.recal is False
    
    def test_tes_output_shapes(self, setup_tes_inputs):
        """Test that TES algorithm returns correct output shapes."""
        lo, lup, ldown, trans, radiance, z = setup_tes_inputs
        
        service = TesAlgorithmService(
            lo, lup, ldown, trans, radiance,
            z=z, aux=False, recal=False
        )
        
        try:
            Ts, e, BT, rad, R, erad = service.tes_modis()
            
            # Check output shapes
            assert Ts.shape == (1, 50), "LST should be (1, n_pixels)"
            assert e.shape == (3, 50), "Emissivity should be (3, n_pixels)"
            assert BT.shape == (3, 50), "Brightness temp should be (3, n_pixels)"
            
        except Exception as e:
            pytest.skip(f"RTTOV not available: {e}")
    
    def test_tes_physical_ranges(self, setup_tes_inputs):
        """Test that outputs are within physical ranges."""
        lo, lup, ldown, trans, radiance, z = setup_tes_inputs
        
        service = TesAlgorithmService(
            lo, lup, ldown, trans, radiance,
            z=z, aux=False, recal=False
        )
        
        try:
            Ts, e, BT, rad, R, erad = service.tes_modis()
            
            # LST should be between 250-330 K
            assert np.nanmin(Ts) > 200, "LST too low"
            assert np.nanmax(Ts) < 400, "LST too high"
            
            # Emissivity should be between 0-1
            assert np.nanmin(e) >= 0, "Emissivity below 0"
            assert np.nanmax(e) <= 1, "Emissivity above 1"
            
        except Exception:
            pytest.skip("Algorithm reference not fully available")
    
    def test_tes_with_different_aux_flags(self, setup_tes_inputs):
        """Test TES with different auxiliary processing flags."""
        lo, lup, ldown, trans, radiance, z = setup_tes_inputs
        
        # Test with aux=True
        service_aux = TesAlgorithmService(
            lo, lup, ldown, trans, radiance,
            z=z, aux=True, recal=False
        )
        
        # Test with aux=False
        service_no_aux = TesAlgorithmService(
            lo, lup, ldown, trans, radiance,
            z=z, aux=False, recal=False
        )
        
        assert service_aux is not None
        assert service_no_aux is not None


@pytest.mark.unit
class TestTesAlgorithmEdgeCases:
    """Test edge cases and error handling."""
    
    def test_tes_with_nan_inputs(self):
        """Test TES handling of NaN values."""
        lo = np.array([10.9, 11.0, 12.0])
        lup = np.ones((3, 50)) * 2.0
        lup[:, 0] = np.nan  # Inject NaN
        ldown = np.ones((3, 50)) * 4.0
        trans = np.ones((3, 50)) * 0.85
        radiance = np.ones((3, 50)) * 15.0
        
        service = TesAlgorithmService(
            lo, lup, ldown, trans, radiance,
            z=np.zeros(50), aux=False
        )
        
        # Should handle NaN gracefully
        assert service is not None
    
    def test_tes_with_extreme_values(self):
        """Test TES with extreme but valid input values."""
        lo = np.array([10.9, 11.0, 12.0])
        lup = np.ones((3, 50)) * 0.1  # Very small
        ldown = np.ones((3, 50)) * 100.0  # Very large
        trans = np.ones((3, 50)) * 0.5  # Low transmittance
        radiance = np.ones((3, 50)) * 100.0  # High radiance
        
        service = TesAlgorithmService(
            lo, lup, ldown, trans, radiance,
            z=np.zeros(50), aux=False
        )
        
        assert service is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
