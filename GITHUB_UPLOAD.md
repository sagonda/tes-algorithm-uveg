#!/bin/bash
# TES Algorithm UVEG - GitHub Upload Instructions
# Prepared: June 16, 2026

cat << 'EOF'
╔══════════════════════════════════════════════════════════════════════════════╗
║            INSTRUCCIONES PARA SUBIR A GITHUB - TES ALGORITHM UVEG           ║
╚══════════════════════════════════════════════════════════════════════════════╝

✅ ESTADO ACTUAL
═══════════════════════════════════════════════════════════════════════════════
✓ Repositorio local: LIMPIO y LISTO
✓ Commits: 7 commits organizados y profesionales
✓ Documentación: COMPLETA y PROFESIONAL
✓ Licencia: CC BY-NC 4.0 (RESTRICTIVA - non-commercial only)
✓ Archivos: 50 archivos rastreados, 917 MB total

════════════════════════════════════════════════════════════════════════════════

📋 PASOS PARA SUBIR A GITHUB
════════════════════════════════════════════════════════════════════════════════

PASO 1: CREAR REPOSITORIO EN GITHUB
────────────────────────────────────

1. Abre https://github.com/new
2. Rellena los datos:
   - Repository name: tes-algorithm-uveg
   - Description: Thermal Emissivity and Surface Temperature (TES) Algorithm - UVEG Edition
   - Visibility: Public (para investigación académica)
   - ⚠️ NO INICIALICES CON README, .gitignore, LICENSE
     (ya los tenemos en el repositorio local)

3. Haz click en "Create repository"

════════════════════════════════════════════════════════════════════════════════

PASO 2: AGREGAR REMOTE Y HACER PUSH
────────────────────────────────────

Ejecuta estos comandos en la terminal:

```bash
cd /home/sagonda/Documentos/git/projects/TES_ALGORITHM_UVEG

# Agregar el repositorio remoto (reemplaza USERNAME para tu usuario)
git remote add origin https://github.com/USERNAME/tes-algorithm-uveg.git

# Renombrar rama main si es necesario (algunas versiones usan 'master')
git branch -M main

# Hacer push inicial (requiere autenticación)
git push -u origin main
```

────────────────────────────────────

⚠️ AUTENTICACIÓN EN GITHUB
────────────────────────────────────

GitHub requiere autenticación. Tienes dos opciones:

OPCIÓN A: Token Personal (Recomendado)
1. Ve a GitHub Settings → Developer settings → Personal access tokens
2. Genera un nuevo token con permisos: repo, write:repo_hook
3. Copia el token (verás solo una vez)
4. Al hacer push, usa:
   - Username: USERNAME
   - Password: [PEGA EL TOKEN AQUÍ]

OPCIÓN B: SSH (Para uso recurrente)
1. Genera clave SSH: ssh-keygen -t ed25519 -C "tu@email.com"
2. Agrega clave pública a GitHub Settings → SSH and GPG keys
3. Cambia el remote a SSH:
   git remote set-url origin git@github.com:USERNAME/tes-algorithm-uveg.git
4. Push sin credenciales:
   git push -u origin main

════════════════════════════════════════════════════════════════════════════════

PASO 3: VERIFICAR EN GITHUB
────────────────────────────────────

Después del push exitoso:
✓ Verifica que https://github.com/USERNAME/tes-algorithm-uveg esté público
✓ Confirma que ves todos los archivos
✓ Comprueba que el README.md se renderiza correctamente
✓ Valida el diagrama Mermaid en README

════════════════════════════════════════════════════════════════════════════════

PASO 4: CONFIGURACIÓN ADICIONAL EN GITHUB
────────────────────────────────────────────

Una vez en GitHub:

1. HABILITAR PROTECCIONES DE RAMA:
   ├─ Settings → Branches → Add rule (main)
   ├─ Require pull request reviews: ON
   ├─ Require status checks to pass: ON
   └─ Allow force pushes: OFF

2. AGREGAR TEMAS (TOPICS):
   ├─ remote-sensing
   ├─ satellite-data
   ├─ land-surface-temperature
   ├─ teledetection
   ├─ modis
   ├─ python
   └─ geospatial

3. HABILITAR DISCUSSIONS (Opcional):
   └─ En Settings → Features, activa "Discussions"

4. CONFIGURAR SECURITY:
   └─ Settings → Code security and analysis
       └─ Habilitar: Dependabot alerts

════════════════════════════════════════════════════════════════════════════════

📝 INFORMACIÓN IMPORTANTE PARA EL REPOSITORIO
════════════════════════════════════════════════════════════════════════════════

LICENCIA: ⚖️ CC BY-NC 4.0 (Creative Commons Attribution-NonCommercial)
   ├─ ✅ Investigación académica: PERMITIDA
   ├─ ✅ Educación: PERMITIDA
   ├─ ✅ Uso no comercial: PERMITIDA
   ├─ ❌ Venta de productos: NO PERMITIDA
   ├─ ❌ SaaS comercial: NO PERMITIDA
   └─ ❌ Uso comercial: REQUIERE PERMISO EXPLÍCITO

TITULARES DE DERECHOS:
   ├─ Daniel Salinas González
   ├─ Drazen Skokovic
   └─ Universidad de Valencia (IPL-UVEG)

CONTACTO PARA PERMISOS COMERCIALES:
   └─ daniel.salinas@uv.es

════════════════════════════════════════════════════════════════════════════════

🎯 COMMITS REALIZADOS
════════════════════════════════════════════════════════════════════════════════

1. chore(license): CC BY-NC 4.0 license and copyright notices
2. docs: Comprehensive professional documentation suite
3. build: Packaging, environment, and version control setup
4. test: Pytest framework and test scaffolding
5. refactor: Module init files with professional exports
6. docs(audit): Architecture review and validation reports
7. docs: Jupyter notebooks for testing

════════════════════════════════════════════════════════════════════════════════

📊 ESTADÍSTICAS FINALES
════════════════════════════════════════════════════════════════════════════════

Archivos Rastreados:     50
Tamaño Total:           917 MB
Documentación:          ✅ Completa
Licencia:               ✅ CC BY-NC 4.0
Testing:                ⚠️ Scaffold creado
Auditoría:              ✅ Completada

PUNTUACIÓN: 7.1 / 10 (LISTO PARA REVISIÓN FORMAL)

════════════════════════════════════════════════════════════════════════════════

🚀 PRÓXIMOS PASOS POST-GITHUB
════════════════════════════════════════════════════════════════════════════════

1. INMEDIATO:
   - Crear GitHub issues para hallazgos críticos
   - Compartir URL con arquitecto revisor
   - Solicitar revisión técnica

2. PRIMERA SEMANA:
   - Crear branch de desarrollo (develop)
   - Abrir issues para P0/P1 (hallazgos)
   - Asignar colaboradores

3. PRIMER MES:
   - Implementar hallazgos P1
   - Crear GitHub Actions CI/CD
   - Alcanzar 80% test coverage

════════════════════════════════════════════════════════════════════════════════

⚠️ IMPORTANTE
════════════════════════════════════════════════════════════════════════════════

1. NUNCA HACER COMMIT DE:
   - .env con credenciales reales
   - Datos HDF5/NetCDF grandes (>100 MB)
   - Claves SSH o tokens personales
   - Información sensible de institución

2. SI ALGO SALE MAL EN EL PUSH:
   - NO fuerces push con -f
   - Contacta a daniel.salinas@uv.es
   - Describe el error exacto

3. DESPUÉS DEL PUSH:
   - Verifica que NO hay .env con secretos
   - Comprueba permisos de archivo
   - Valida que README se renderiza

════════════════════════════════════════════════════════════════════════════════

📞 SOPORTE
════════════════════════════════════════════════════════════════════════════════

Para problemas durante el push:
- Daniel Salinas: daniel.salinas@uv.es
- Drazen Skokovic: drazen.skokovic@uv.es

Para seguimiento post-upload:
- Ver CONTRIBUTING.md para workflow colaborativo
- Ver SECURITY.md para políticas de seguridad

════════════════════════════════════════════════════════════════════════════════

✅ REPOSITORIO LOCAL: LISTO PARA GITHUB

Ejecuta: git push -u origin main
(después de configurar el remote y autenticación)

════════════════════════════════════════════════════════════════════════════════
EOF
