#!/usr/bin/env python3
import subprocess
import os

# =====================================================
# COLORES ANSI
# =====================================================
RESET  = "\033[0m"
BOLD   = "\033[1m"
RED    = "\033[91m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
WHITE  = "\033[97m"

# =====================================================
# FUNCIONES AUXILIARES
# =====================================================
def run_cmd(command):
    """Ejecuta un comando shell y devuelve su salida o None."""
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL)
        return output.decode().strip()
    except:
        return None

def print_section(title, content, color=WHITE):
    """Imprime una sección con formato uniforme y colores."""
    print(f"{GREEN}{BOLD}  ➤ {title}:{RESET}")
    if content:
        print(f"{color}{content}{RESET}\n")
    else:
        print(f"{RED}  [No disponible]{RESET}\n")

# =====================================================
# MAIN
# =====================================================
def main():
    print(f"""
{CYAN}{BOLD}┌──────────────────────────────────────────────┐
│           IMPRESORAS DEL SISTEMA 🔥            │
│           lpstat -a y configuración actual    │
└──────────────────────────────────────────────┘{RESET}
""")

    # ===== Buscar impresoras instaladas =====
    printers = run_cmd("lpstat -a")
    print_section("Impresoras configuradas (lpstat -a)", printers)

    print(f"{GREEN}{BOLD}[✓] Auditoría completada: Impresoras del Sistema{RESET}\n")

# =====================================================
# EJECUCIÓN DIRECTA
# =====================================================
if __name__ == "__main__":
    main()
