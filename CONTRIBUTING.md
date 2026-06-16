# 🤝 Contributing to TES Algorithm UVEG

Thank you for your interest in contributing to the **TES Algorithm UVEG** project! This document outlines how to contribute effectively while maintaining quality and compliance with our non-commercial license.

---

## 📋 Table of Contents

1. [Code of Conduct](#-code-of-conduct)
2. [Before You Start](#-before-you-start)
3. [Development Workflow](#-development-workflow)
4. [Coding Standards](#-coding-standards)
5. [Testing](#-testing)
6. [Documentation](#-documentation)
7. [Submitting Changes](#-submitting-changes)
8. [Reporting Issues](#-reporting-issues)

---

## 🎯 Code of Conduct

### Our Commitment

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of:
- Experience level
- Nationality or ethnicity
- Gender identity or expression
- Sexual orientation
- Disability
- Physical appearance
- Religion
- Political beliefs

### Expected Behavior

- ✅ Use professional, respectful language
- ✅ Accept constructive criticism gracefully
- ✅ Focus on what is best for the community
- ✅ Show empathy towards other community members
- ✅ Respect intellectual property rights

### Unacceptable Behavior

- ❌ Harassment or intimidation
- ❌ Discriminatory language or behavior
- ❌ Personal attacks
- ❌ Plagiarism or intellectual property theft
- ❌ Unauthorized commercial use of code

### Reporting Violations

Report violations to: daniel.salinas@uv.es with details of the incident.

---

## 🔍 Before You Start

### License Understanding

**CRITICAL:** All contributions must comply with **CC BY-NC 4.0** license:

- ✅ Your code will be licensed under CC BY-NC 4.0
- ✅ You grant copyright rights to the repository maintainers
- ✅ Non-commercial use only
- ✅ Attribution required

By submitting a pull request, you agree to these terms.

### Setup Your Development Environment

```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork locally
git clone https://github.com/YOUR-USERNAME/tes-algorithm-uveg.git
cd tes-algorithm-uveg

# 3. Add upstream remote to sync with main repo
git remote add upstream https://github.com/uv-uveg/tes-algorithm-uveg.git

# 4. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# OR: venv\Scripts\activate  # Windows

# 5. Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy

# 6. Configure Git hooks (recommended)
pre-commit install  # If pre-commit config exists
```

---

## 🚀 Development Workflow

### 1. Create a Feature Branch

```bash
# Update from upstream
git fetch upstream
git rebase upstream/main

# Create feature branch with descriptive name
git checkout -b feature/short-description
# OR for bug fixes: git checkout -b fix/issue-number-short-description
# OR for documentation: git checkout -b docs/what-youre-documenting
```

### 2. Make Your Changes

Follow the [Coding Standards](#-coding-standards) section.

**Commit messages should use Conventional Commits format:**

```bash
git commit -m "feat: add new cloud detection refinement"
git commit -m "fix: resolve NaN handling in emissivity calculation"
git commit -m "docs: update RTTOV setup instructions"
git commit -m "test: add unit tests for tes_algorithm_service"
git commit -m "refactor: optimize numpy array operations in modis_02_service"
```

**Commit Message Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:** feat, fix, docs, style, refactor, perf, test, chore  
**Scope:** services/tes_algorithm_service, utilities, docs, etc.  
**Subject:** Imperative, present tense, lowercase, no period

### 3. Keep Your Branch Up-to-Date

```bash
git fetch upstream
git rebase upstream/main
```

### 4. Push to Your Fork

```bash
git push origin feature/short-description
```

### 5. Create a Pull Request

Go to GitHub and click "Compare & pull request"

**PR Title:** Use same format as commits: `feat: description`

**PR Description Template:**
```markdown
## Description
Brief explanation of what this PR does

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Closes #123

## Changes Made
- Change 1
- Change 2

## Testing
Describe how you tested these changes

## Checklist
- [ ] Code follows PEP 8 style guide
- [ ] All tests pass locally
- [ ] New tests added (if applicable)
- [ ] Documentation updated
- [ ] Commits are well-organized
- [ ] CC BY-NC 4.0 header included in new files
```

---

## ⚙️ Coding Standards

### Python Style Guide

**Follow PEP 8 strictly. Use these tools:**

```bash
# Format code automatically
black services/ utilities/ generate_images_process.py

# Check for style issues
flake8 services/ utilities/ --max-line-length=100

# Static type checking (recommended)
mypy services/tes_algorithm_service.py --strict

# Organize imports
isort services/
```

### File Header for All Python Files

```python
# -*- coding: utf-8 -*-
"""
[Brief module description - 1-2 lines]

[Extended description explaining purpose and usage]

This file is part of TES Algorithm UVEG.
© 2020-2026 Daniel Salinas, Drazen Skokovic, University of Valencia
Licensed under CC BY-NC 4.0: https://creativecommons.org/licenses/by-nc/4.0/

Example:
    Usage example if applicable::
        
        from services.my_service import MyService
        service = MyService()
        result = service.process_data(data)

Attributes:
    CONSTANT_NAME: Description of module-level constants

"""

# Standard library imports first
import sys
import os

# Third-party imports second
import numpy as np
from netCDF4 import Dataset

# Local application imports last
from services.base_service import BaseService

__all__ = ['PublicClass', 'public_function']
```

### Function Documentation

Use Google-style docstrings:

```python
def retrieve_lst_and_emissivity(radiance_b29, radiance_b31, radiance_b32, 
                                 tau, emissivity_prior):
    """Retrieve land surface temperature and spectral emissivity using TES algorithm.
    
    Solves the radiative transfer equation system for LST and emissivity
    using three MODIS thermal bands and atmospheric correction from RTTOV.
    
    Args:
        radiance_b29: Observed radiance in band 29 (W m⁻² sr⁻¹ μm⁻¹)
            Shape: (M, N) or (M,)
        radiance_b31: Observed radiance in band 31 (W m⁻² sr⁻¹ μm⁻¹)
            Shape: (M, N) or (M,)
        radiance_b32: Observed radiance in band 32 (W m⁻² sr⁻¹ μm⁻¹)
            Shape: (M, N) or (M,)
        tau: Atmospheric transmittance (3,) or (3, M, N)
            Transmittance for bands 29, 31, 32
        emissivity_prior: Prior emissivity estimate (float)
            Used as initial guess, typically 0.985
    
    Returns:
        tuple: (lst, emissivity, error_lst, error_emis)
            lst: Land surface temperature (Kelvin)
            emissivity: Spectral emissivity in band 31
            error_lst: LST uncertainty (Kelvin)
            error_emis: Emissivity uncertainty
    
    Raises:
        ValueError: If input arrays have incompatible shapes
        RuntimeError: If algorithm fails to converge
    
    Note:
        This is a physics-based algorithm that assumes:
        - Lambertian surface
        - Constant emissivity within the narrow wavelength range
        - Valid atmospheric corrections from RTTOV
    
    References:
        Gillespie, A. R., et al. (1998). "A Temperature and Emissivity 
            Separation Algorithm for Advanced Spaceborne Thermal 
            Emission and Reflection Radiometer (ASTER) Images."
    """
```

### Class Documentation

```python
class CloudMaskService:
    """Service for cloud detection and quality flagging using MOD35_L2 products.
    
    This service applies cloud masking based on the official MODIS cloud mask
    product (MOD35_L2) and provides various filtering options.
    
    Attributes:
        cloud_mask (np.ndarray): Binary array of cloud detection (1=cloud)
        qa_flags (np.ndarray): Quality assurance flags
        processing_date (str): ISO format processing timestamp
    
    Example:
        >>> service = CloudMaskService()
        >>> mask = service.apply_cloud_mask(modis_data, confidence_level='high')
        >>> clear_pixels = ~mask  # Inverted: 1=clear sky
    """
    
    def __init__(self, confidence_level='medium'):
        """Initialize cloud detection service.
        
        Args:
            confidence_level: 'low', 'medium', or 'high'
        """
        pass
```

### Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Modules | snake_case | `tes_algorithm_service.py` |
| Classes | PascalCase | `CloudMaskService` |
| Functions | snake_case | `create_output_layers()` |
| Constants | UPPER_SNAKE_CASE | `PI_NUMERIC`, `MODIS_BAND_31_WAVELENGTH` |
| Private methods | `_leading_underscore` | `_validate_inputs()` |
| Protected methods | `_single_leading_underscore` | `_internal_calculation()` |

### Line Length & Formatting

- **Max line length:** 100 characters (PEP 8: 79, but 100 acceptable for scientific code)
- **Use trailing commas** in multi-line structures:

```python
# Good
result = calculate_lst(
    radiance_array,
    atmospheric_correction,
    emissivity_prior,
    temperature_range=(250, 330),
)

# Bad
result = calculate_lst(radiance_array, atmospheric_correction, 
                      emissivity_prior, temperature_range=(250, 330))
```

---

## 🧪 Testing

### Writing Tests

Create test files in `tests/` directory:

```bash
tests/
├── test_tes_algorithm_service.py
├── test_cloud_mask_service.py
└── test_utilities.py
```

**Test structure:**

```python
import pytest
import numpy as np
from services.tes_algorithm_service import TesAlgorithmService

class TestTesAlgorithmService:
    """Test suite for TES algorithm core functionality."""
    
    @pytest.fixture
    def service(self):
        """Create service instance for testing."""
        return TesAlgorithmService()
    
    def test_retrieve_lst_basic(self, service):
        """Test basic LST retrieval with known inputs."""
        # Arrange
        radiance = np.array([10.5, 10.2, 10.1])
        tau = np.array([0.8, 0.81, 0.79])
        
        # Act
        result = service.retrieve_lst(radiance, tau)
        
        # Assert
        assert result is not None
        assert isinstance(result, tuple)
        assert len(result) == 4  # (lst, emis, err_lst, err_emis)
        assert 250 < result[0] < 330  # LST in physical range (Kelvin)
    
    def test_retrieve_lst_invalid_input(self, service):
        """Test that invalid inputs raise appropriate errors."""
        with pytest.raises(ValueError):
            service.retrieve_lst(np.array([10, 20]), np.array([1, 2, 3]))
    
    @pytest.mark.parametrize("temperature", [260, 290, 320])
    def test_planck_function_inversion(self, service, temperature):
        """Test Planck function inversion for various temperatures."""
        wavelength = 11e-6  # 11 micrometers
        radiance = service.planck_function(wavelength, temperature)
        recovered_temp = service.planck_inversion(wavelength, radiance)
        assert abs(recovered_temp - temperature) < 0.1
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_tes_algorithm_service.py -v

# Run with coverage report
pytest tests/ --cov=services --cov-report=html

# Run only fast tests
pytest tests/ -m "not slow" -v
```

### Test Coverage Requirements

- **Minimum:** 80% code coverage
- **Target:** 90% code coverage for critical algorithms
- Run: `pytest --cov=services --cov-report=term-missing`

---

## 📚 Documentation

### Code Comments

Use comments sparingly - **code should be self-documenting**:

```python
# ✅ GOOD: Explains WHY, not WHAT
# Use log scale for better visualization of wide dynamic range
flux_log = np.log10(flux_linear + 1e-10)

# ❌ BAD: Explains WHAT (obvious from code)
# Take the log of flux
flux_log = np.log10(flux_linear + 1e-10)
```

### Inline Code Comments

```python
# Use for non-obvious mathematical operations
# TES algorithm: solve 3×3 system for [LST, ε29, ε31]
# See Gillespie et al. (1998) for derivation
A = construct_jacobian_matrix(...)
solution = np.linalg.lstsq(A, b_vector, rcond=None)[0]
```

### Jupyter Notebooks

- **Markdown cells:** Explain sections and concepts
- **Code cells:** Keep focused, well-commented
- **Include file header:**

```markdown
---
**TES Algorithm UVEG - Test Notebook**
© 2020-2026 Daniel Salinas, Drazen Skokovic, University of Valencia
Licensed under CC BY-NC 4.0

Description of what this notebook demonstrates.
---
```

### README Updates

Update `README.md` if you:
- Add new features
- Change installation steps
- Modify core architecture
- Document new algorithms

---

## 📤 Submitting Changes

### Pull Request Checklist

Before submitting, verify:

- [ ] **Code Quality**
  - [ ] Runs `black` formatter: `black .`
  - [ ] Passes `flake8`: `flake8 .`
  - [ ] Passes `mypy` checks: `mypy services/ --strict`
  
- [ ] **Testing**
  - [ ] All new code has tests
  - [ ] Runs `pytest`: `pytest tests/ -v`
  - [ ] Coverage hasn't decreased: `pytest --cov`
  
- [ ] **Documentation**
  - [ ] Docstrings added/updated
  - [ ] Complex logic explained in comments
  - [ ] README updated if relevant
  - [ ] Changelog entry added (if applicable)
  
- [ ] **Legal Compliance**
  - [ ] CC BY-NC 4.0 header added to new files
  - [ ] No proprietary/licensed code included
  - [ ] Copyright notice included
  
- [ ] **Git Hygiene**
  - [ ] Commits are well-organized
  - [ ] Commit messages follow conventions
  - [ ] Branch is updated from upstream
  - [ ] No merge commits (use rebase)

### Addressing Review Comments

- Respond professionally to all feedback
- Make requested changes in new commits
- Push changes and request re-review
- Do not force-push unless explicitly asked

### After Merge

Your contribution is merged! 🎉
- Verify the feature works on main branch
- Delete your feature branch: `git branch -d feature/your-feature`
- Celebrate your contribution to open science!

---

## 🐛 Reporting Issues

### Bug Reports

**Title:** `[BUG] Short description of issue`

**Template:**
```markdown
## Description
Clear description of the bug

## Steps to Reproduce
1. ...
2. ...
3. ...

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [Windows/Linux/macOS]
- Python: 3.8 / 3.9 / 3.10 / 3.11
- NumPy: 1.21.0
- netCDF4: 1.5.8

## Error Message/Output
```
Paste full error traceback here
```

## Additional Context
Screenshots, data samples, etc.
```

### Feature Requests

**Title:** `[FEATURE] Short description of feature`

**Template:**
```markdown
## Description
Clear description of desired feature

## Use Case
Why this feature is needed

## Proposed Solution
Suggested implementation approach

## Alternatives Considered
Other possible approaches

## Additional Context
```

---

## ❓ Questions?

- 📧 **Email:** daniel.salinas@uv.es
- 💬 **GitHub Discussions:** [Coming Soon]
- 🐛 **GitHub Issues:** For bug reports and feature requests

---

## 📄 License

By contributing to this project, you agree that:
1. Your contributions are licensed under CC BY-NC 4.0
2. You have the right to submit the work
3. You understand the non-commercial use restriction
4. You waive any claim against the University of Valencia or copyright holders

---

**Thank you for contributing to advancing remote sensing science! 🛰️🌍**

*Last updated: June 2026*
