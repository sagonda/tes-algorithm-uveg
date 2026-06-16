#!/usr/bin/env python3
"""
Git Push Helper para TES Algorithm UVEG
Facilita el upload a GitHub con interfaz amigable
"""

import subprocess
import sys
import argparse
from pathlib import Path


class Colors:
    """ANSI color codes para terminal"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text):
    """Imprime encabezado"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.ENDC}")
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.ENDC}\n")


def print_section(text):
    """Imprime sección"""
    print(f"{Colors.CYAN}{text}{Colors.ENDC}")


def print_success(text):
    """Imprime mensaje de éxito"""
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")


def print_warning(text):
    """Imprime aviso"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.ENDC}")


def print_error(text):
    """Imprime error"""
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")


def run_command(cmd, description=None):
    """Ejecuta comando y retorna resultado"""
    if description:
        print_section(description)
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        return True, result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stdout.strip(), e.stderr.strip()


def main():
    parser = argparse.ArgumentParser(
        description='Upload TES Algorithm UVEG to GitHub',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 push_to_github.py -u sagonda
  python3 push_to_github.py -u sagonda -r my-tes-repo
  python3 push_to_github.py --help
        """
    )

    parser.add_argument(
        '-u', '--username',
        required=True,
        help='Tu usuario de GitHub'
    )
    parser.add_argument(
        '-r', '--repo',
        default='tes-algorithm-uveg',
        help='Nombre del repositorio (default: tes-algorithm-uveg)'
    )
    parser.add_argument(
        '--branch',
        default='main',
        help='Rama a subir (default: main)'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Fuerza el push sin confirmación'
    )

    args = parser.parse_args()

    # Validar usuario
    if not args.username or len(args.username) < 3:
        print_error("Usuario debe tener al menos 3 caracteres")
        sys.exit(1)

    username = args.username
    repo_name = args.repo
    branch = args.branch
    github_url = f"https://github.com/{username}/{repo_name}.git"

    print_header("TES ALGORITHM UVEG - GitHub Push Helper")

    print_section("Configuración:")
    print(f"  Usuario GitHub: {Colors.BLUE}{username}{Colors.ENDC}")
    print(f"  Repositorio: {Colors.BLUE}{repo_name}{Colors.ENDC}")
    print(f"  URL remoto: {Colors.BLUE}{github_url}{Colors.ENDC}")
    print(f"  Rama: {Colors.BLUE}{branch}{Colors.ENDC}")
    print()

    # Paso 1: Verificar que es un repo git
    print_header("Paso 1: Verificando repositorio git")
    if not Path('.git').exists():
        print_error("No es un repositorio git válido en el directorio actual")
        sys.exit(1)
    print_success("Repositorio git encontrado")

    # Paso 2: Obtener estado
    print_header("Paso 2: Estado del repositorio")
    ok, stdout, stderr = run_command('git status --porcelain')
    
    if stdout:
        print_warning("Hay cambios no rastreados:")
        print(stdout)
        if not args.force:
            response = input(f"\n{Colors.YELLOW}¿Continuar? (s/n): {Colors.ENDC}")
            if response.lower() != 's':
                print("Cancelado.")
                sys.exit(0)

    # Paso 3: Configurar remoto
    print_header("Paso 3: Configurando remoto")
    ok, stdout, stderr = run_command('git remote -v')
    
    if 'origin' in stdout:
        current_urls = [line.split() for line in stdout.split('\n') if 'origin' in line]
        print(f"Remote 'origin' ya existe:")
        for line in current_urls:
            print(f"  {line[0]}: {line[1]}")
        
        if not args.force:
            response = input(f"\n{Colors.YELLOW}¿Actualizar a {github_url}? (s/n): {Colors.ENDC}")
            if response.lower() == 's':
                run_command(f'git remote set-url origin "{github_url}"')
                print_success("Remote actualizado")
        else:
            run_command(f'git remote set-url origin "{github_url}"')
            print_success("Remote actualizado (force mode)")
    else:
        print_section("Agregando nuevo remote...")
        run_command(f'git remote add origin "{github_url}"')
        print_success("Remote agregado")

    # Paso 4: Verificar rama
    print_header("Paso 4: Verificando rama")
    ok, current_branch, _ = run_command('git rev-parse --abbrev-ref HEAD')
    
    print(f"Rama actual: {Colors.BLUE}{current_branch}{Colors.ENDC}")
    
    if current_branch != branch:
        if not args.force:
            response = input(f"\n{Colors.YELLOW}¿Cambiar a rama '{branch}'? (s/n): {Colors.ENDC}")
            if response.lower() == 's':
                run_command(f'git branch -M {branch}')
                print_success(f"Rama cambiada a '{branch}'")
        else:
            run_command(f'git branch -M {branch}')
            print_success(f"Rama cambiada a '{branch}' (force mode)")

    # Paso 5: Resumen
    print_header("Paso 5: Resumen")
    
    ok, commit_count, _ = run_command('git rev-list --all --count')
    ok, latest_commits, _ = run_command('git log --oneline -5')
    ok, file_count, _ = run_command('git ls-files | wc -l')
    ok, total_size, _ = run_command('du -sh . && echo "calculated"')

    total_size = total_size.split('\n')[0].split()[0]  # Extraer solo el tamaño

    print(f"Commits: {Colors.BLUE}{commit_count}{Colors.ENDC}")
    print(f"Archivos: {Colors.BLUE}{file_count}{Colors.ENDC}")
    print(f"Tamaño: {Colors.BLUE}{total_size}{Colors.ENDC}")
    print()
    print("Últimos 5 commits:")
    for line in latest_commits.split('\n'):
        if line:
            print(f"  {line}")

    # Confirmación final
    if not args.force:
        print()
        print_warning("Esta acción subirá tu código a GitHub")
        print_warning("Asegúrate de que el repositorio es público y es seguro subirlo")
        response = input(f"\n{Colors.YELLOW}¿Estás seguro? (s/n): {Colors.ENDC}")
        if response.lower() != 's':
            print("Cancelado.")
            sys.exit(0)

    # Hacer push
    print_header("Paso 6: Push a GitHub")
    print_section(f"Ejecutando: git push -u origin {branch}")
    
    ok, stdout, stderr = run_command(f'git push -u origin {branch}')
    
    if ok:
        print_success("✓ PUSH EXITOSO")
        print()
        print_section(f"Tu repositorio está en:")
        print(f"  {Colors.CYAN}https://github.com/{username}/{repo_name}{Colors.ENDC}")
        print()
        print_section("Próximos pasos:")
        print("  1. Verifica que el repositorio sea público")
        print("  2. Comprueba que ves todos los archivos")
        print("  3. Valida que el README.md se renderiza correctamente")
        print("  4. Comparte el link con los revisores")
        print()
        print_warning("Recuerda: Licencia CC BY-NC 4.0 (restricciones comerciales)")
    else:
        print_error("✗ Error durante el push")
        if stderr:
            print()
            print("Error output:")
            print(stderr)
        print()
        print_section("Soluciones:")
        print("  1. Verifica tu conexión a internet")
        print("  2. Comprueba que el repositorio existe en GitHub")
        print("  3. Intenta crear en: https://github.com/new")
        print("  4. Ejecuta manualmente: git push -u origin main -v")
        sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelado por el usuario.")
        sys.exit(0)
    except Exception as e:
        print_error(f"Error inesperado: {e}")
        sys.exit(1)
