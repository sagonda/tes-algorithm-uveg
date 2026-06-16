#!/usr/bin/env python3
"""
GitHub Push Helper con Token Personal
Facilita el push a GitHub usando Personal Access Token
"""

import subprocess
import sys
import getpass
from pathlib import Path


class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.ENDC}")
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.ENDC}\n")


def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.ENDC}")


def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")


def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")


def main():
    print_header("GitHub Push con Personal Access Token")

    # Verificar que es repositorio git
    if not Path('.git').exists():
        print_error("No es un repositorio git válido")
        sys.exit(1)

    print("Necesitas un GitHub Personal Access Token para hacer push.")
    print("\n📖 Para generar el token:")
    print("   1. Ve a: https://github.com/settings/tokens/new")
    print("   2. Name: tes-algorithm-uveg-push")
    print("   3. Marca: repo, write:repo_hook")
    print("   4. Copia el token generado (aparece solo una vez)")
    print()

    # Solicitar token
    while True:
        token = getpass.getpass(
            f"{Colors.BLUE}Pega tu GitHub Personal Access Token: {Colors.ENDC}"
        )

        if not token:
            print_error("El token no puede estar vacío")
            continue

        if not token.startswith("ghp_") and not token.startswith("github_pat_"):
            print_warning("El token no parece válido (debe empezar con ghp_ o github_pat_)")
            response = input(
                f"{Colors.YELLOW}¿Continuar de todas formas? (s/n): {Colors.ENDC}"
            )
            if response.lower() != 's':
                continue

        break

    # Obtener configuración
    print("\n" + Colors.BLUE + "─" * 80 + Colors.ENDC)

    result = subprocess.run(
        ["git", "config", "user.name"],
        capture_output=True,
        text=True
    )
    username = result.stdout.strip() if result.returncode == 0 else "unknown"

    result = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        capture_output=True,
        text=True
    )
    remote_url = result.stdout.strip() if result.returncode == 0 else "unknown"

    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True
    )
    branch = result.stdout.strip() if result.returncode == 0 else "main"

    print(f"Usuario Git: {Colors.BLUE}{username}{Colors.ENDC}")
    print(f"Remote: {Colors.BLUE}{remote_url}{Colors.ENDC}")
    print(f"Rama: {Colors.BLUE}{branch}{Colors.ENDC}")
    print(Colors.BLUE + "─" * 80 + Colors.ENDC)

    # Crear URL con credenciales
    # Extraer host del remote URL
    if "github.com" in remote_url:
        # Formato: https://github.com/username/repo.git
        remote_parts = remote_url.split("github.com/")
        if len(remote_parts) == 2:
            auth_url = f"https://sagonda:{token}@github.com/{remote_parts[1]}"
        else:
            print_error("No se pudo extraer información del remote")
            sys.exit(1)
    else:
        print_error("El remote no parece ser de GitHub")
        sys.exit(1)

    # Realizar push
    print("\n" + Colors.BLUE + "Iniciando push a GitHub..." + Colors.ENDC)
    print()

    result = subprocess.run(
        ["git", "push", "-u", "origin", branch],
        input="",
        env={**subprocess.os.environ, "GIT_ASKPASS": "echo"},
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    # Intentar con autenticación en URL
    if result.returncode != 0:
        print("Intentando con autenticación en URL...")
        result = subprocess.run(
            f"git push -u '{auth_url.replace('@', '%40')}' {branch}".split(),
            capture_output=True,
            text=True
        )

        # Fallback: intentar nuevamente con entrada estándar
        if result.returncode != 0:
            print_warning("Intentando con credenciales vía stdin...")

            # Preparar entrada con credenciales
            proc = subprocess.Popen(
                ["git", "push", "-u", "origin", branch],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            output, _ = proc.communicate(input=f"sagonda\n{token}\n")

            if proc.returncode == 0:
                print_success("✓ PUSH EXITOSO")
                print()
                print(f"Repositorio: {Colors.BLUE}https://github.com/sagonda/tes-algorithm-uveg{Colors.ENDC}")
                print(f"Rama: {Colors.BLUE}{branch}{Colors.ENDC}")
                return 0
            else:
                print_error("✗ Error durante el push")
                print()
                print("Output:")
                print(output)
                sys.exit(1)

    # Si llegamos aquí, el push fue exitoso
    if "error" not in result.stdout.lower() and "fatal" not in result.stdout.lower():
        print_success("✓ PUSH EXITOSO")
        print()
        print(f"Repositorio: {Colors.BLUE}https://github.com/sagonda/tes-algorithm-uveg{Colors.ENDC}")
        print(f"Rama: {Colors.BLUE}{branch}{Colors.ENDC}")
    else:
        print_error("✗ Error durante el push")
        print()
        print("Output:")
        print(result.stdout)
        sys.exit(1)

    # Limpiar token de la memoria
    del token
    del auth_url


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelado por el usuario.")
        sys.exit(0)
    except Exception as e:
        print_error(f"Error inesperado: {e}")
        sys.exit(1)
