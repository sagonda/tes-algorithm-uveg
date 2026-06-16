# System Architecture & Design Documentation

**TES Algorithm UVEG - Architecture Reference v1.1**

---

## 📐 Overview

The TES Algorithm UVEG is a **modular, service-oriented architecture** designed for operational processing of satellite thermal infrared data. This document provides comprehensive architectural analysis for technical reviewers, DevOps engineers, and system architects.

---

## 🏗️ High-Level Architecture

### Layered Architecture Pattern

```
┌─────────────────────────────────────────────────────┐
│         DATA ACCESS LAYER                           │
│  (I/O, File Reading, Data Retrieval)                │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│         SERVICES LAYER                              │
│  (Business Logic, Specialized Operations)           │
│  [15+ Microservices for Specific Tasks]             │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│         ALGORITHM LAYER                             │
│  (TES Core Algorithm)                               │
│  [Thermal Emissivity & Surface Temperature]         │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│         OUTPUT LAYER                                │
│  (NetCDF4 File Generation)                          │
└─────────────────────────────────────────────────────┘
```

### Module Dependencies

```
generate_images_process.py (Main Orchestrator)
    │
    ├─► services/
    │   ├─ tes_algorithm_service        ⭐ CORE
    │   ├─ call_rttov_service           Atmospheric model
    │   ├─ cloud_mask_service           Quality filtering
    │   ├─ modis_02_service             Data reading
    │   ├─ create_profiles_service      Atmosphere profiles
    │   ├─ create_nc_outfile_service    Output generation
    │   ├─ fvc_service                  Vegetation fraction
    │   ├─ recal_lse_service            Emissivity calib
    │   ├─ sw_service                   Split window
    │   ├─ change_units_service         Unit conversion
    │   ├─ err_ldown_service            Error estimation
    │   ├─ read_ndvi_service            NDVI reading
    │   ├─ bits_stripping_service       Data packing
    │   ├─ packed_value_service         Compression
    │   ├─ unpacked_value_service       Decompression
    │   ├─ new_array_service            Array allocation
    │   ├─ matching_files_service       File discovery
    │   └─ __init__.py                  Module exports
    │
    └─► utilities/
        ├─ utilities.py                 Common helpers
        ├─ utilities_extraction_data.py Data extraction
        └─ __init__.py                  Module exports
```

---

## 🔄 Data Flow Architecture

### Processing Pipeline

```
INPUT SOURCES
    │
    ├── MOD021KM (Calibrated Radiances, L1B)       [MODIS Band Data]
    ├── MOD03 (Geolocation, 1km 5-min)             [Geographic Data]
    ├── MOD35_L2 (Cloud Mask)                      [Quality Flags]
    ├── ERA5 / ERA5.1 (Atmospheric Profiles)       [ECMWF Reanalysis]
    └── NDVI Data (Vegetation Index)               [Optional Enhancement]
            │
            ▼
    ┌──────────────────────────────────────────────┐
    │ PRE-PROCESSING STAGE                         │
    │ ─────────────────────────────────────────    │
    │ • Bits stripping (12→11 bit)                 │
    │ • Radiometric calibration                    │
    │ • Unit conversion                            │
    │ • Cloud detection & masking                  │
    └────────────────────┬─────────────────────────┘
            │
            ▼
    ┌──────────────────────────────────────────────┐
    │ ATMOSPHERIC CORRECTION (RTTOV)               │
    │ ─────────────────────────────────────────    │
    │ • Profile creation (T, q, P with height)     │
    │ • RTTOV v13 radiative transfer simulation    │
    │ • Transmittance (τ) & radiance computation    │
    │ • Error propagation (σ_atm)                  │
    └────────────────────┬─────────────────────────┘
            │
            ▼
    ┌──────────────────────────────────────────────┐
    │ TES ALGORITHM (Physics-Based Inversion)      │
    │ ─────────────────────────────────────────    │
    │ • Radiative transfer equation solving        │
    │ • LST estimation (Kelvin)                    │
    │ • Emissivity retrieval (3 bands)             │
    │ • Accuracy: ±0.5-1.0 K (validated SURFRAD)  │
    │ • Error uncertainty propagation              │
    └────────────────────┬─────────────────────────┘
            │
            ▼
    ┌──────────────────────────────────────────────┐
    │ POST-PROCESSING & VALIDATION                 │
    │ ─────────────────────────────────────────    │
    │ • Vegetation fraction correction (FVC)       │
    │ • Split-window algorithm refinement          │
    │ • Physical range validation                  │
    │ • QA/QC flagging                             │
    └────────────────────┬─────────────────────────┘
            │
            ▼
    ┌──────────────────────────────────────────────┐
    │ OUTPUT GENERATION                            │
    │ ─────────────────────────────────────────    │
    │ NetCDF4/HDF5 Format                          │
    │ • LST (16-bit, Kelvin)                       │
    │ • Emissivity B29, B31, B32 (8-bit)           │
    │ • Uncertainty fields (16-bit)                │
    │ • Metadata & provenance                      │
    └────────────────────┬─────────────────────────┘
            │
            ▼
    OUTPUT: TES_UVEG_MOD_v1.1.nc (~5 MB)
```

---

## 📦 Service Architecture

### Service Responsibilities

| Service | Type | Purpose | Input | Output |
|---------|------|---------|-------|--------|
| **tes_algorithm_service** | Core | TES algorithm solving | Radiance, τ, L↑, L↓ | LST, ε, errors |
| **call_rttov_service** | External | RTTOV interface | Profiles, geometry | Transmittance, radiance |
| **cloud_mask_service** | Filter | Cloud detection | MOD35_L2 | Cloud flags |
| **modis_02_service** | Reader | L1B radiance reading | MOD021KM files | Raw radiance |
| **create_profiles_service** | Transform | Atmospheric profiles | ERA5 + MODIS geo | T, q, P arrays |
| **create_nc_outfile_service** | Writer | NetCDF4 generation | All results | .nc file |
| **fvc_service** | Calculator | Vegetation correction | NDVI, ε | FVC-corrected ε |
| **recal_lse_service** | Calibration | Emissivity recalibration | Raw ε | Corrected ε |
| **sw_service** | Processor | Split-window method | Multiple bands | Refined radiance |
| **change_units_service** | Utility | Unit conversion | Values in native | Converted units |
| **err_ldown_service** | Calculator | Error in L↓ | Multiple params | σ_L↓ field |
| **read_ndvi_service** | Reader | NDVI data retrieval | NDVI files | NDVI array |
| **bits_stripping_service** | Processor | 12→11 bit conversion | Raw bits | Stripped data |
| **packed_value_service** | Encoder | Data compression | Float values | Packed integers |
| **unpacked_value_service** | Decoder | Data decompression | Packed integers | Float values |
| **new_array_service** | Allocator | Array creation | Dimensions | Allocated arrays |
| **matching_files_service** | Finder | File matching logic | File lists | Matched triplets |

---

## 🎯 Design Patterns

### 1. **Service Locator Pattern**
- Each service is a standalone, instantiable class
- Services imported and instantiated directly in main orchestrator
- No dependency injection framework (lightweight design)

```python
# Usage:
service = CloudMaskService(modis_data)
result = service.cloud_mask()
```

### 2. **Strategy Pattern**
- Different processing strategies based on satellite source (MOD vs MYD)
- Conditional logic in `generate_images_process.py`
- Abstract interface not explicitly defined (implicit)

### 3. **Pipeline Pattern**
- Linear processing flow with stages
- Each stage produces intermediate data
- Error handling at each stage

### 4. **Template Method Pattern**
- `generate_images_process._process_images()` orchestrates the overall flow
- Individual methods (`_check_hour_file`, `_date_modis`) implement specific steps

---

## ⚙️ Configuration Management

### Environment-Based Configuration

```yaml
Environment Variables (in .env):
  ├─ MODIS_DATA_PATH         # Data input directory
  ├─ OUTPUT_PATH             # Output base directory
  ├─ RTTOV_ROOT_PATH         # Radiative transfer model
  ├─ PROCESS_YEAR            # Processing year (YYYY)
  ├─ PROCESS_MONTH           # Processing month (MM)
  ├─ NUM_PROCESSES           # Parallelization factor
  └─ LOG_LEVEL               # Logging verbosity
```

### Hardcoded Paths (NEEDS REFACTORING)

⚠️ **ISSUE DETECTED:** Hardcoded paths in `generate_images_process.py` lines 54-98
- Satellite-specific paths (MOD vs MYD)
- Server-specific paths (local vs production)
- ❌ Not environment-variable driven
- ✅ RECOMMENDATION: Move to .env or config file

---

## 🔧 Dependency Architecture

### External Dependencies

```
NumPy (numerical)
  │
  ├─► SciPy (scientific computing)
  │
  └─► netCDF4
      └─► HDF5 (binary I/O)

RTTOV (external executable)
  └─► Compiled Fortran radiative transfer model
```

### Python Dependencies

**Core:**
- numpy ≥ 1.21.0
- netCDF4 ≥ 1.5.7
- scipy ≥ 1.7.0

**Utilities:**
- python-dateutil ≥ 2.8.0
- pytz ≥ 2021.1

**Development:**
- pytest, pytest-cov
- black, flake8, mypy
- jupyter

---

## 📊 Data Model

### Input Data Structure

```
MODIS Swath (MOD021KM):
    → Dimensions: (lines, samples, bands)  [~2030 × 1354 × 38]
    → Dtype: int16 (packed digital counts)
    → Bands of Interest: 29, 31, 32 (thermal IR)

Geolocation (MOD03):
    → Latitude array: (2030 × 1354)
    → Longitude array: (2030 × 1354)
    → View geometry (zenith angles)

Cloud Mask (MOD35_L2):
    → Binary/flag field: (lines × samples)
    → QA bits: Cloud confidence, snow, shadows
```

### Output Data Structure

```
NetCDF4 Output (Swath):
    ├─ Dimension: line × sample
    │
    ├─ Variables:
    │   ├─ UVEG_LST           [uint16]  Scale: 0.02,   Offset: 0
    │   ├─ UVEG_e29           [uint8]   Scale: 0.002,  Offset: 0.49
    │   ├─ UVEG_e31           [uint8]   Scale: 0.002,  Offset: 0.49
    │   ├─ UVEG_e32           [uint8]   Scale: 0.002,  Offset: 0.49
    │   ├─ UVEG_LST_error     [uint8]   Scale: 0.04,   Offset: 0
    │   ├─ UVEG_e29_error     [uint16]  Scale: 0.0001, Offset: 0
    │   ├─ UVEG_e31_error     [uint16]  Scale: 0.0001, Offset: 0
    │   ├─ UVEG_e32_error     [uint16]  Scale: 0.0001, Offset: 0
    │   ├─ View_angle         [uint8]   Scale: 0.5,    Offset: 0
    │   ├─ lat                [int32]   Scale: 10000,  Offset: 0
    │   └─ lon                [int32]   Scale: 10000,  Offset: 0
    │
    └─ Attributes:
        ├─ title:       "TES UVEG LST & Emissivity Product"
        ├─ version:     "1.1"
        ├─ institution: "UV-IPL"
        ├─ created:     "2026-06-16T12:30:00Z"
        └─ doi:         "10.xxxx/xxxxxx" (pending)
```

---

## ⚠️ Issues Detected During Architecture Review

### 🔴 Critical Issues

1. **Configuration Hardcoding**
   - Lines 54-98 in `generate_images_process.py`
   - Server paths hardcoded with if/else logic
   - **Fix:** Migrate to environment variables or config file

2. **Duplicate Imports**
   - `import time` appears twice (lines 12-13)
   - **Fix:** Remove duplicate import

3. **Missing Main Guard**
   - Interactive input at class level (lines 51-52)
   - **Fix:** Move to `__main__` entry point

### 🟡 Medium Issues

4. **no Docstrings in TES Algorithm**
   - `tes_algorithm_service.py` lacks comprehensive docstrings
   - **Fix:** Add function-level documentation with parameter descriptions

5. **No Type Hints**
   - Services lack type annotations
   - **Fix:** Add type hints to function signatures (PEP 561)

6. **Error Handling Coverage**
   - Generic `except:` clauses (bare exceptions)
   - **Fix:** Specific exception types and proper error logging

7. **No Logging Framework**
   - Using `print()` for diagnostic output
   - **Fix:** Use `logging` module or `loguru` for production logging

### 🟢 Minor Issues

8. **Magic Numbers**
   - Hard-coded constants (c1=0.998449, K1=[...])
   - **Fix:** Define as module-level constants with documentation

9. **Memory Management**
   - Explicit `del` statements in lines 360-380
   - **Fix:** Use context managers or proper scope management

10. **Missing Tests**
    - No `tests/` directory structure
    - **Fix:** Create test suite with pytest

---

## 🔐 Security Architecture

### Input Validation
- ⚠️ Currently minimal
- Should validate file paths, array dimensions, data ranges

### Secrets Management
- ✅ `.env` template provided
- ✅ `.gitignore` excludes `.env`
- ⚠️ No secrets validation in code

### Data Protection
- ✅ .gitattributes for line endings
- ✅ .gitignore for sensitive data
- ⚠️ No encryption for data at rest (out of scope)

---

## 🚀 Deployment Architecture

### Environment Configurations

```
Development (local)
  ├─ Data: /home/user/MOD/
  ├─ RTTOV: /usr/local/rttov12/
  └─ Logging: console + file

Production (HPC/Cloud)
  ├─ Data: /neodc/modis/data/
  ├─ RTTOV: /gws/nopw/j04/.../rttov12/
  ├─ Logging: centralized
  └─ Monitoring: alerts enabled
```

### Scalability

**Current Limitations:**
- Single-threaded processing
- Sequential granule processing
- No distributed computing

**Recommendations:**
- Implement multiprocessing for granule batches
- Consider Dask for array-level parallelization
- Docker containerization for cloud deployment

---

## 📈 Performance Characteristics

### Computational Complexity

| Operation | Complexity | Time per Granule |
|-----------|-----------|-----------------|
| MODIS file I/O | O(pixels) | 2-3 sec |
| RTTOV call | O(profiles × levels) | 5-10 sec |
| TES algorithm | O(pixels) | 3-5 sec |
| NetCDF write | O(pixels) | 2-3 sec |
| **Total** | - | **15-25 sec** |

### Memory Profile

- Per granule: ~500 MB - 1.5 GB (typical)
- Peak memory: ~2 GB
- Requires: minimum 8 GB system RAM

---

## 🔄 Version & Release Strategy

### Semantic Versioning

```
v1.1.0
 │ │ └─ Patch (bug fixes)
 │ └─── Minor (new features, backward compatible)
 └───── Major (breaking changes)
```

### Release Process

1. Feature development on branches
2. Pull request with testing + review
3. Version bump in CHANGELOG.md
4. Git tag: `git tag -a v1.1.0 -m "Release v1.1.0"`
5. Push to GitHub with release notes

---

## 📚 Cross-References

- **Installation:** See [README.md](README.md#️-guía-de-inicio-rápido)
- **Configuration:** See [.env.example](.env.example)
- **Development:** See [CONTRIBUTING.md](CONTRIBUTING.md)
- **Security:** See [SECURITY.md](SECURITY.md)
- **Changelog:** See [CHANGELOG.md](CHANGELOG.md)

---

## 🎯 Future Architectural Improvements

1. **Refactoring Entry Point**
   - Create `tes_algorithm/cli.py` with argparse
   - Support config file loading
   - Better error handling

2. **Type Safety**
   - Add PEP 561 type hints
   - Enable `mypy --strict` checking

3. **Testing Framework**
   - Unit tests for each service
   - Integration tests for pipeline
   - ~80% code coverage target

4. **Logging Architecture**
   - Structured logging with loguru
   - Audit trail for processing
   - Performance metrics collection

5. **Modular CLI**
   - Support multiple satellites (MOD, MYD, others)
   - Parallel processing configuration
   - Output filtering options

---

**Architecture Document Version:** 1.0  
**Last Updated:** June 2026  
**Status:** Production (v1.1.0)

Prepared for: **Software Architecture Review**  
Audience: Architects, DevOps Engineers, Core Developers

---

