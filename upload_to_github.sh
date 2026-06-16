#!/bin/bash
#
# Script automatizado para subir TES Algorithm UVEG a GitHub
# Uso: ./upload_to_github.sh USERNAME
#
# Ejemplo: ./upload_to_github.sh sagonda
#

set -e  # Salir si hay error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_step() {
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✓ $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Validar argumentos
if [ $# -eq 0 ]; then
    echo -e "${RED}Error: Debes proporcionar tu usuario de GitHub${NC}"
    echo ""
    echo "Uso: $0 USERNAME"
    echo "Ejemplo: $0 sagonda"
    echo ""
    echo "Puedes obtener tu USERNAME en: https://github.com/settings/profile"
    exit 1
fi

USERNAME=$1
REPO_NAME="tes-algorithm-uveg"
GITHUB_URL="https://github.com/${USERNAME}/${REPO_NAME}.git"

print_step "INICIANDO UPLOAD A GITHUB"
echo ""
echo "Usuario GitHub: ${BLUE}${USERNAME}${NC}"
echo "Repositorio: ${BLUE}${GITHUB_URL}${NC}"
echo ""

# Paso 1: Verificar estado del repositorio
print_step "Paso 1: Verificando estado del repositorio local"
if ! git status > /dev/null 2>&1; then
    print_error "No es un repositorio git válido"
    exit 1
fi

STATUS=$(git status --porcelain)
if [ ! -z "$STATUS" ]; then
    print_warning "El área de trabajo no está limpia. Cambios pendientes:"
    echo "$STATUS"
    read -p "¿Deseas continuar? (s/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo "Cancelado."
        exit 1
    fi
fi

# Paso 2: Verificar remoto
print_step "Paso 2: Configurando remoto de GitHub"
if git remote | grep -q "^origin$"; then
    CURRENT_URL=$(git config --get remote.origin.url)
    echo "Remote 'origin' ya existe: ${CURRENT_URL}"
    read -p "¿Deseas actualizar a ${GITHUB_URL}? (s/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        git remote set-url origin "$GITHUB_URL"
        echo "✓ Remote actualizado"
    fi
else
    echo "Agregando remote origin..."
    git remote add origin "$GITHUB_URL"
    echo "✓ Remote agregado"
fi

# Paso 3: Verificar rama main
print_step "Paso 3: Verificando rama 'main'"
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "Rama actual: ${BLUE}${CURRENT_BRANCH}${NC}"

if [ "$CURRENT_BRANCH" != "main" ]; then
    read -p "¿Deseas cambiar a rama 'main'? (s/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        git branch -M main
        echo "✓ Rama renombrada a 'main'"
    else
        print_warning "Continuando con rama '${CURRENT_BRANCH}'"
    fi
fi

# Paso 4: Contar commits
print_step "Paso 4: Resumen de commits locales"
COMMIT_COUNT=$(git rev-list --all --count)
echo "Total de commits en repositorio: ${BLUE}${COMMIT_COUNT}${NC}"
echo ""
echo "Últimos 5 commits:"
git log --oneline -5

# Paso 5: Mostrar archivos
print_step "Paso 5: Archivos a subir"
FILE_COUNT=$(git ls-files | wc -l)
TOTAL_SIZE=$(du -sh . | cut -f1)
echo "Archivos rastreados: ${BLUE}${FILE_COUNT}${NC}"
echo "Tamaño total: ${BLUE}${TOTAL_SIZE}${NC}"

# Paso 6: Verificar autenticación
print_step "Paso 6: Información de autenticación"
echo ""
echo "GitHub requiere autenticación. Tienes dos opciones:"
echo ""
echo "1. Token Personal Access (Recomendado):"
echo "   - URL: https://github.com/settings/tokens"
echo "   - Permisos: repo, write:repo_hook"
echo ""
echo "2. SSH (Para uso recurrente):"
echo "   - Verificar: ls -la ~/.ssh/id_ed25519"
echo "   - Si no existe: ssh-keygen -t ed25519"
echo ""

# Paso 7: Confirmación final
print_step "Paso 7: Confirmación final"
echo ""
echo "URLs y configuración:"
echo "  Remote: ${BLUE}${GITHUB_URL}${NC}"
echo "  Rama: ${BLUE}main${NC}"
echo "  Commits: ${BLUE}${COMMIT_COUNT}${NC}"
echo "  Archivos: ${BLUE}${FILE_COUNT}${NC}"
echo ""
read -p "¿Estás listo para hacer push a GitHub? (s/n): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    echo "Cancelado."
    exit 0
fi

# Paso 8: Hacer push
print_step "Paso 8: Haciendo push a GitHub"
echo "Esto puede tomar unos segundos..."
echo ""

if git push -u origin main; then
    print_step "✓ PUSH EXITOSO"
    echo ""
    echo "Tu repositorio está en: ${BLUE}https://github.com/${USERNAME}/${REPO_NAME}${NC}"
    echo ""
    echo "Próximos pasos:"
    echo "1. Verifica que el repositorio sea público en GitHub"
    echo "2. Comprueba que el README.md se renderiza correctamente"
    echo "3. Valida que ves todos los archivos"
    echo "4. Comparte la URL con los revisores"
    echo ""
    print_warning "Recuerda: Este repositorio usa licencia CC BY-NC 4.0"
    print_warning "Uso comercial requiere permiso explícito de los titulares"
else
    print_error "Error durante el push"
    echo ""
    echo "Posibles soluciones:"
    echo "1. Verifica tu conexión a internet"
    echo "2. Comprueba tu autenticación en GitHub"
    echo "3. Confirma que el repositorio existe en:"
    echo "   https://github.com/new"
    echo ""
    echo "Si aún hay problemas, ejecuta manualmente:"
    echo "  git push -u origin main --verbose"
    exit 1
fi

echo ""
print_step "Proceso completado"
