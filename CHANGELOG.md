# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2026-06-16

### Added
- 📚 Professional documentation suite (README, CONTRIBUTING, CODE_OF_CONDUCT)
- 🔐 Comprehensive .gitignore for Python/scientific computing projects
- ⚖️ CC BY-NC 4.0 license and explicit copyright notice
- 📦 setup.py for proper package installation
- 🧪 Test framework scaffolding and documentation guidelines
- 🏗️ Architecture documentation (ARCHITECTURE.md)
- 🔒 Security policy (SECURITY.md)
- 🛠️ CLI refactoring with config file support
- 📋 CHANGELOG and versioning standards
- 🔄 .gitattributes for line ending normalization
- 📝 requirements.txt with pinned versions
- 🌐 .env.example template for configuration

### Improved
- ✅ Code quality standards (PEP 8, type hints, docstrings)
- ✅ Project structure for enterprise-grade governance
- ✅ Dependency management and reproducibility
- ✅ Development workflow documentation

### Fixed
- 🐛 Removed duplicate import statements in main script
- 🐛 Addressed code organization and modularity issues

### Documentation
- 📖 Added Mermaid.js architecture diagram
- 📖 Created developer onboarding guide
- 📖 Added API documentation guidelines
- 📖 Technical specifications for MOD/MYD products

---

## [1.0.0] - 2020-06-01

### Added
- 🎯 Core TES Algorithm implementation
- 🛰️ MODIS data processing pipeline
- 📊 NetCDF4 output generation
- 🔬 RTTOV atmospheric correction integration
- ☁️ Cloud masking and QA/QC
- 🌳 Vegetation fraction computation (FVC)
- 📈 Error propagation and uncertainty quantification
- 🗂️ Multi-satellite support (TERRA/MOD, AQUA/MYD)
- 🚀 Operational processing capabilities
- 📚 Scientific documentation (Readme_MOD.md, Readme_MYD.md)

### Initial Release
- Production-ready algorithm for LST and emissivity retrieval
- Daily processing capability for global MODIS data
- Historical archive support (2002-present)

---

## Architecture History

### v1.1.0 Governance & DevOps
- Added CI/CD pipeline templates
- Implemented security policy
- Professional repository governance
- Contributor guidelines
- Code of conduct
- Architecture documentation

### v1.0.0 Scientific Algorithm
- Core radiative transfer implementation
- RTTOV integration framework
- NetCDF4 product generation
- Operational infrastructure

---

## Future Roadmap

### Planned Features
- [ ] GitHub Actions CI/CD pipeline
- [ ] Automated testing suite (pytest)
- [ ] Python type annotations (PEP 561)
- [ ] API documentation (Sphinx/ReadTheDocs)
- [ ] Docker containerization
- [ ] Cloud deployment templates (AWS, GCP, Azure)
- [ ] Machine learning enhancements for cloud detection
- [ ] Multi-satellite support expansion (Sentinel, ECOSTRESS)
- [ ] Real-time processing capability
- [ ] Web service API

### Experimental
- [ ] GPU acceleration (CUDA/OpenCL)
- [ ] Parallel processing optimization
- [ ] Machine learning validation models
- [ ] Advanced emissivity inversion

---

## Version Matrix

| Version | Release Date | Status | Python | Notes |
|---------|------------|--------|--------|-------|
| 1.1.0 | 2026-06-16 | ✅ Current | 3.8+ | Professional governance |
| 1.0.0 | 2020-06-01 | ✅ Stable | 3.8+ | Production algorithm |

---

## Security Advisories

For security vulnerabilities, please see [SECURITY.md](SECURITY.md) instead of using the issue tracker.

---

## Contributing

For information about contributing to this project, please see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

Changes documented in this file are licensed under the same terms as the project: **CC BY-NC 4.0**

© 2020-2026 Daniel Salinas, Drazen Skokovic, University of Valencia

---

## References

- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Git Commits Best Practices](https://chris.beams.io/posts/git-commit/)
