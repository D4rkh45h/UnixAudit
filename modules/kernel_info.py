#!/usr/bin/env python3
import subprocess
import os

# =====================================================
# COLORES ANSI
# =====================================================
RESET  = "\033[0m"
BOLD   = "\033[1m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
WHITE  = "\033[97m"

# =====================================================
# FUNCIONES AUXILIARES
# =====================================================
def run_cmd(command):
    """Ejecuta un comando de shell y devuelve su salida o None si falla."""
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL)
        return output.decode().strip()
    except:
        return None

def print_section(title, content, color=WHITE):
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
│           INFORMACIÓN DEL KERNEL LINUX 🔥        │
│           Compatible con Linux x86/x64          │
└──────────────────────────────────────────────┘{RESET}
""")

    # ===== Comandos =====
    version_proc = run_cmd("cat /proc/version")
    uname_all = run_cmd("uname -a")
    uname_mrs = run_cmd("uname -mrs")
    rpm_kernel = run_cmd("rpm -q kernel")  # solo funcionará en RedHat-based
    dmesg_kernel = run_cmd("dmesg | grep -i linux | head -n 1")
    boot_kernel = run_cmd("ls /boot | grep vmlinuz-")

    # ===== Detectar si es 64 bits =====
    architecture = run_cmd("uname -m")
    is_64 = "64" in architecture if architecture else False

    # ===== Mostrar info =====
    print_section("Versión (uname -mrs)", uname_mrs)
    print_section("Arquitectura", f"{architecture} ({'64-bit' if is_64 else '32-bit'})")
    print_section("Detalles (/proc/version)", version_proc)
    print_section("uname -a", uname_all)

    if rpm_kernel:
        print_section("rpm -q kernel", rpm_kernel)

    if dmesg_kernel:
        print_section("dmesg (primera línea relevante)", dmesg_kernel)

    print_section("Núcleos en /boot (vmlinuz-*)", boot_kernel or "No se encontraron")

    print(f"{GREEN}{BOLD}[✓] Auditoría completada: Kernel Info{RESET}\n")

# =====================================================
# EJECUCIÓN DIRECTA
# =====================================================
if __name__ == "__main__":
    main()
