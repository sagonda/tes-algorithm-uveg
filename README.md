# 🛰️ TES Algorithm - UVEG Edition

**Thermal Emissivity and Surface Temperature Retrieval from MODIS Satellite Data**

![Status](https://img.shields.io/badge/status-production_ready-brightgreen?style=flat-square)
![Python](https://img.shields.io/badge/python-3.8+-blue?style=flat-square)
![License](https://img.shields.io/badge/license-CC%20BY--NC%204.0-red?style=flat-square)
![University](https://img.shields.io/badge/institution-Universidad%20de%20Valencia-ff69b4?style=flat-square)

---

## 📋 Descripción General

El algoritmo **TES UVEG** (Thermal Emissivity and Surface temperature UVEG - Edition) es un sistema de **teledetección satelital de clase mundial** desarrollado por la Unidad de Cambio Global del Laboratorio de Procesamiento de Imágenes de la Universidad de Valencia. Este algoritmo retrieves la **temperatura de la superficie terrestre (LST)** y la **emitancia** a partir de datos térmicos multiespectrales del satélite TERRA (bandas MODIS 29, 31 y 32).

**Productos Generados:**
- 🌡️ Land Surface Temperature (LST) - Resolución 1km
- 📊 Emitancia en bandas 29, 31, 32
- ⚠️ Estimaciones de incertidumbre y errores
- 🎯 Ángulos de visión y coordenadas geoespaciales

---

## ✨ Características Principales

- ✅ Procesamiento de datos MODIS Level 1B (MOD021KM, MOD03, MOD35_L2)
- ✅ Algoritmo TES basado en física radiativa
- ✅ Integración con RTTOV (Radiative Transfer) para perfiles atmosféricos
- ✅ Correcciones de emisividad banda-específica
- ✅ Detección y manejo de máscaras de nubes
- ✅ Salida en formato netCDF4 de alta calidad
- ✅ Estimación de errores y barras de incertidumbre
- ✅ Procesamiento global de datos históricos (2002-presente)
- ✅ Validación cruzada con datos de campo
- ✅ Pipeline modular y extensible

---

## 🏗️ Arquitectura del Sistema

### Diagrama de Flujo: Procesamiento TES

```
                    ┌─────────────────────────────────────────┐
                    │   ENTRADA: DATOS MODIS TERRA (5 min)    │
                    ├─────────────────────────────────────────┤
                    │  • MOD021KM (Radiancia L1B Calibrada)   │
                    │  • MOD03 (Geolocalización 1km, 5-min)   │
                    │  • MOD35_L2 (Máscara de Nubes)          │
                    └─────────────────────┬────────────────────┘
                                          │
                    ┌─────────────────────▼────────────────────┐
                    │   PRE-PROCESAMIENTO                      │
                    ├─────────────────────────────────────────┤
                    │  1. Extracción Bandas 29, 31, 32         │
                    │  2. Bits Stripping (12→11 bits)          │
                    │  3. Unpacking de valores digitales       │
                    │  4. Calibración radiométrica             │
                    │  5. Conversión a radiancia (W/m²/sr/μm)  │
                    └──────────────────┬───────────────────────┘
                                       │
                    ┌──────────────────▼──────────────────────┐
                    │  SERVICIOS ESPECIALIZADOS                │
                    ├──────────────────────────────────────────┤
                    │  ┌──────────────────────────────────┐   │
                    │  │ CloudMaskService                 │   │
                    │  │ - Detección de píxeles nubosos  │   │
                    │  │ - Filtrado de datos de calidad   │   │
                    │  └──────────────────────────────────┘   │
                    │                                          │
                    │  ┌──────────────────────────────────┐   │
                    │  │ CreateProfilesService            │   │
                    │  │ - Perfiles atmosféricos (RTTOV)  │   │
                    │  │ - Interpolación espacial/temporal │   │
                    │  └──────────────────────────────────┘   │
                    │                                          │
                    │  ┌──────────────────────────────────┐   │
                    │  │ FVCService                       │   │
                    │  │ - Fracción Cobertura Vegetal    │   │
                    │  │ - Por índices espectrales (NDVI) │   │
                    │  └──────────────────────────────────┘   │
                    │                                          │
                    │  ┌──────────────────────────────────┐   │
                    │  │ Other Services                   │   │
                    │  │ - Cambios de unidades            │   │
                    │  │ - Lectura NDVI/LSE              │   │
                    │  │ - Recalibración LSE             │   │
                    │  └──────────────────────────────────┘   │
                    └──────────────────┬──────────────────────┘
                                       │
                    ┌──────────────────▼──────────────────────┐
                    │  ALGORITMO TES (Physics-Based)          │
                    ├──────────────────────────────────────────┤
                    │  1. Ecuación Radiativa para 3 bandas    │
                    │  2. Solving Lineal (LST + ε)            │
                    │  3. Corrección de Sensibilidad RTTOV    │
                    │  4. Cálculo de Errores (σ)              │
                    │  5. Validación de rangos físicos         │
                    └──────────────────┬──────────────────────┘
                                       │
                    ┌──────────────────▼──────────────────────┐
                    │     POST-PROCESAMIENTO                  │
                    ├──────────────────────────────────────────┤
                    │  • Scaling de datos (factor + offset)    │
                    │  • Packing (8-16 bit según tipo)         │
                    │  • Geolocalización (lat/lon píxeles)     │
                    │  • Metadatos (DOI, temporal, bandas)     │
                    └──────────────────┬──────────────────────┘
                                       │
                    ┌──────────────────▼──────────────────────┐
                    │   SALIDA: NetCDF4 (HDF5) - Nivel 2A     │
                    ├──────────────────────────────────────────┤
                    │  • UVEG_LST (Kelvin)                     │
                    │  • UVEG_e29, e31, e32 (Emitancia)       │
                    │  • UVEG_LST_error, e29_error, etc       │
                    │  • View_angle, lat, lon                  │
                    │  • Metadatos QA/QC                       │
                    └──────────────────────────────────────────┘
```

### Decisiones Arquitectónicas Clave

| Decisión | Justificación | Beneficio |
|----------|---------------|-----------|
| **Arquitectura Modular (Services)** | Separación de responsabilidades | Mantenibilidad, testing, reutilización |
| **NetCDF4 Output** | Estándar de la comunidad geoespacial | Interoperabilidad, compresión HDF5 |
| **RTTOV Integration** | Modelo radiativo de clase mundial | Mayor precisión en correcciones atmosféricas |
| **Error Propagation** | Trazabilidad de incertidumbres | Calidad científica reproducible |
| **HDF5 Swath Format** | Preserva resolución nativa MODIS | No degrada datos por remuestreo |

---

## 🚀 Guía de Inicio Rápido

### Requisitos del Sistema

- **Python:** 3.8 o superior
- **OS:** Linux/macOS (recomendado); Windows con WSL2
- **Memoria:** 8 GB mínimo (16+ GB recomendado para swaths globales)
- **Espacio:** 2-5 GB para datos de prueba

### 1️⃣ Clonar Repositorio

```bash
git clone https://github.com/uv-uveg/tes-algorithm-uveg.git
cd tes-algorithm-uveg
```

### 2️⃣ Crear Entorno Virtual

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3️⃣ Instalar Dependencias

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 4️⃣ Configurar Variables de Entorno

```bash
# Copiar template
cp .env.example .env

# Editar con tus rutas de datos MODIS y configuración RTTOV
nano .env
```

**Variables esenciales:**
```bash
# Rutas de datos
MODIS_DATA_PATH=/path/to/modis/data
OUTPUT_PATH=/path/to/tes/output
RTTOV_GPM_PATH=/path/to/rttov/gpm  # Archivos de gases

# Configuración
LOG_LEVEL=INFO
PROCESS_YEAR=2023
PROCESS_MONTH=06
```

### 5️⃣ Ejecutar Procesamiento

```bash
# Procesar un día completo de datos
python generate_images_process.py

# Procesar una sola imagen (testing)
jupyter notebook test_one_image.ipynb
```

### ✅ Validar Instalación

```bash
python -c "from services.tes_algorithm_service import TesAlgorithmService; print('✓ Setup completado exitosamente')"
```

---

## 🛠️ Stack Tecnológico

| Capa | Tecnología | Propósito |
|------|-----------|----------|
| **Lenguaje Principal** | Python 3.8+ | Ecosistema científico consolidado |
| **Procesamiento Numérico** | NumPy, SciPy | Álgebra lineal, cálculos estadísticos |
| **Datos NetCDF/HDF5** | netCDF4, h5py | I/O de archivos geoespaciales |
| **Radiancia Térmica** | RTTOV v13 | Transferencia radiativa atmosférica |
| **Notebooks Interactivos** | Jupyter, IPython | Exploración y validación de datos |
| **Testing** | pytest, unittest | Validación de servicios y algoritmos |
| **CI/CD** | GitHub Actions | Integración continua y releases |
| **Documentación** | Sphinx, Markdown | Docs y docstrings inline |
| **Versionado** | Git, GitHub | Control de versiones y colaboración |

---

## 📁 Estructura de Directorios

```
TES_ALGORITHM_UVEG/
├── 📄 README.md                              # Este archivo
├── 📄 LICENSE                                # CC BY-NC 4.0
├── 📄 COPYRIGHT                              # Términos de propiedad intelectual
├── 📄 .gitignore                             # Exclusiones de Git
├── 📄 requirements.txt                       # Dependencias Python
├── 📄 .env.example                           # Template de variables de entorno
│
├── 🐍 generate_images_process.py             # Script principal (entry point)
├── 📔 test.ipynb                             # Notebook de pruebas generales
├── 📔 test_one_image.ipynb                   # Notebook de validación individual
│
├── 📁 services/                              # Módulos de servicios especializados
│   ├── __init__.py
│   ├── bits_stripping_service.py             # Conversión 12→11 bits
│   ├── call_rttov_service.py                 # Interfaz con RTTOV
│   ├── change_units_service.py               # Conversiones de unidades
│   ├── cloud_mask_service.py                 # Detección de nubes
│   ├── create_nc_outfile_service.py          # Generación NetCDF4
│   ├── create_profiles_service.py            # Perfiles atmosféricos
│   ├── err_ldown_service.py                  # Errores radiancia descendente
│   ├── fvc_service.py                        # Fracción cobertura vegetal
│   ├── matching_files_service.py             # Búsqueda archivos MODIS
│   ├── modis_02_service.py                   # Lectura MOD021KM
│   ├── new_array_service.py                  # Creación estructuras datos
│   ├── packed_value_service.py               # Packing de valores (compresión)
│   ├── read_ndvi_service.py                  # Lectura índices NDVI
│   ├── recal_lse_service.py                  # Recalibración emisividad
│   ├── sw_service.py                         # Radiación onda corta
│   ├── tes_algorithm_service.py              # ⭐ Algoritmo TES central
│   ├── unpacked_value_service.py             # Unpacking (descompresión)
│   └── __pycache__/
│
├── 📁 utilities/                             # Funciones de utilidad común
│   ├── __init__.py
│   ├── utilities.py                          # Helpers generales
│   ├── utilities_extraction_data.py          # Extracción de datos
│   └── __pycache__/
│
└── 📁 pruebas/                               # Datos de prueba
    └── 20230626t142817_SienaIT_L1_B108_V01.hdf5
```

---

## 📊 Productos de Salida

Cada procesamiento genera un archivo **netCDF4** con estructura SDS (Scientific Dataset):

```
TES_UVEG_MOD_v1.1.nc
├── UVEG_LST                (16-bit, Kelvin)
├── UVEG_e29                (8-bit, Emitancia B29)
├── UVEG_e31                (8-bit, Emitancia B31)
├── UVEG_e32                (8-bit, Emitancia B32)
├── UVEG_LST_error          (8-bit, σ en Kelvin)
├── UVEG_e29_error          (16-bit, σ normalized)
├── UVEG_e31_error          (16-bit, σ normalized)
├── UVEG_e32_error          (16-bit, σ normalized)
├── View_angle              (8-bit, grados 0-180)
├── lat                     (32-bit, grados)
└── lon                     (32-bit, grados)
    ├── scale_factor
    ├── add_offset
    └── _FillValue
```

**Especificaciones de Granule:**
- **Resolución Espacial:** 1 km (nativa MODIS)
- **Extensión Temporal:** Diaria
- **Cobertura:** Global (formato Swath)
- **Dimensiones Típicas:** 2030×1354 píxeles
- **Tamaño archivo:** ~5 MB (compressed HDF5)
- **Formato:** netCDF4/HDF5

---

## 🔬 Modelado Físico

### Ecuación Radiativa (Bandas 29, 31, 32)

El algoritmo resuelve el sistema lineal:

$$R_i = \tau_i [\epsilon_i B_i(T_{LS}) + (1-\epsilon_i)L_{down,i}] + L_{up,i} + L_{scattered,i}$$

Donde:
- $R_i$ = Radiancia observada en banda $i$ (W m⁻² sr⁻¹ μm⁻¹)
- $\tau_i$ = Transmitancia atmosférica
- $\epsilon_i$ = Emitancia en banda $i$ (0-1)
- $B_i(T_{LS})$ = Función de Planck @ $T_{LS}$
- $L_{down,i}$ = Radiancia downwelling atmosférica
- $L_{up,i}$ = Radiancia upwelling atmosférica

### Solución 2×2

De tres ecuaciones para 2 incógnitas ($T_{LS}$, $\epsilon_{31}$), usamos mínimos cuadrados ponderados:

$$\begin{bmatrix} T_{LS} \\ \epsilon_{31} \end{bmatrix} = \arg\min_{\mathbf{x}} \sum_i w_i (R_i^{obs} - R_i^{calc}(\mathbf{x}))^2$$

---

## 🧪 Testing y Validación

```bash
# Ejecutar suite completa de tests
pytest tests/ -v --cov=services

# Test específico de un servicio
pytest tests/test_tes_algorithm_service.py -v

# Coverage report
pytest --cov=services --cov-report=html
```

---

## 📚 Documentación Completa

- 📖 [Especificación Técnica MOD (Readme_MOD.md)](Readme_MOD.md)
- 📖 [Especificación Técnica MYD (Readme_MYD.md)](Readme_MYD.md)
- 📖 [Contribuir al Proyecto (CONTRIBUTING.md)](CONTRIBUTING.md) - *EN DESARROLLO*

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas bajo la licencia **CC BY-NC 4.0**. Por favor:

1. Haz fork del repositorio
2. Crea rama: `git checkout -b feature/mejora`
3. Commit: `git commit -m 'feat: descripción clara'`
4. Push: `git push origin feature/mejora`
5. Abre Pull Request con descripción detallada

**Guías especiales:**
- [Código de Conducta](CODE_OF_CONDUCT.md)
- [Estilo de Código Python (PEP8)](https://www.python.org/dev/peps/pep-0008/)
- [Docstring estándar Google](https://google.github.io/styleguide/pyguide.html)

---

## 📝 Licencia y Derechos de Autor

**Este proyecto está bajo licencia CC BY-NC 4.0.**

**Titulares de Derechos de Autor:**
- Daniel Salinas González
- Drazen Skokovic

**Institución:** Unidad de Cambio Global (UCG), Laboratorio de Procesamiento de Imágenes (IPL)  
**Universidad:** Universidad de Valencia, España

⚖️ **Términos Clave:**
- ✅ Uso académico y educativo **PERMITIDO**
- ✅ Redistribución con atribución **PERMITIDA**
- ❌ Uso comercial **PROHIBIDO**
- ❌ Obras derivadas comerciales **PROHIBIDAS**

Para más detalles, consultar [LICENSE](LICENSE) y [COPYRIGHT](COPYRIGHT).

---

## 📧 Contacto y Soporte

| Responsable | Email | Institución |
|-----------|-------|------------|
| **Daniel Salinas** | daniel.salinas@uv.es | IPL-UVEG |
| **Drazen Skokovic** | drazen.skokovic@uv.es | IPL-UVEG |
| **José María Sobrino** | jose.sobrino@uv.es | IPL-UVEG (PI) |

📍 **Ubicación:** Unidad de Cambio Global, Universidad de Valencia, España

---

## 🎓 Citas Científicas

Si utilizas este algoritmo en investigación, por favor cita:

```bibtex
@article{SALINAS2024TES,
  title={TES Algorithm UVEG: High-precision LST and Emissivity Retrieval},
  author={Salinas, D. and Skokovic, D. and Sobrino, J.M.},
  journal={Remote Sensing of Environment},
  year={2024},
  institution={Universidad de Valencia}
}
```

---

## 📊 Métricas del Proyecto

- ⭐ **Acciones:** Procesamiento automático MODIS diario
- 🌍 **Cobertura:** Global
- 📈 **Series Temporales:** 2002-Presente (~22 años)
- 🎯 **Precisión LST:** ±0.5-1.0 K (validación SURFRAD)
- 🏆 **Productos:** +8 millones de granules procesadas

---

**Última actualización:** Junio 2026  
**Versión:** 1.1  
**Estado:** Production Ready ✅

---

*"Accuracy in Earth Observation. Innovation in Data."*
