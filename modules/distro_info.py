#!/usr/bin/env python3
import subprocess
import os

# =====================================================
# COLORES ANSI (estándar para todos los módulos)
# =====================================================
RESET  = "\033[0m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
WHITE  = "\033[97m"
BOLD   = "\033[1m"
RED    = "\033[91m"

# =====================================================
# FUNCIONES AUXILIARES
# =====================================================
def run_cmd(cmd):
    """Ejecuta un comando y devuelve su salida si funciona."""
    try:
        output = subprocess.check_output(cmd.split(), stderr=subprocess.DEVNULL).decode().strip()
        return output
    except:
        return None

def detect_distro():
    """Devuelve la distribución Linux detectada."""
    # === Método 1: /etc/os-release ===
    if os.path.exists("/etc/os-release"):
        data = {}
        with open("/etc/os-release") as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    data[k] = v.replace('"', '')
        name = data.get("PRETTY_NAME") or data.get("NAME")
        if name:
            return name

    # === Método 2: lsb_release -d ===
    lsb = run_cmd("lsb_release -d")
    if lsb:
        return lsb.replace("Description:\t", "")

    # === Método 3: /etc/issue ===
    if os.path.exists("/etc/issue"):
        return open("/etc/issue").read().strip()

    return None

# =====================================================
# MAIN
# =====================================================
def main():
    distro = detect_distro()

    print(f"""
{CYAN}{BOLD}┌────────────────────────────────────────────────────────┐
│      DETECCIÓN DE DISTRIBUCIÓN (MÓDULO 12 UNIVERSAL) 🔥   │
│      Compatible con Linux y derivados                     │
└────────────────────────────────────────────────────────┘{RESET}
""")

    if distro:
        print(f"{GREEN}{BOLD}  ➤ Distribución Detectada:{RESET} {WHITE}{distro}{RESET}\n")
    else:
        print(f"{RED}{BOLD}  ➤ No se pudo detectar la distribución.{RESET}\n")

    print(f"{CYAN}{BOLD}[✓] Auditoría completada (Módulo 12 Universal){RESET}\n")


# =====================================================
# EJECUCIÓN DIRECTA
# =====================================================
if __name__ == '__main__':
    main()
