#!/usr/bin/env python3
import os
import subprocess
import re

# Colores y estilos universales
RED="\033[91m"; YEL="\033[93m"; CYA="\033[96m"; BOLD="\033[1m"; RESET="\033[0m"

# ================================
#  Cargar credenciales del master
# ================================
USER = os.environ.get("AUDIT_USER")
PASS = os.environ.get("AUDIT_PASS")

# Procesos relevantes que deben resaltarse
INTERESTING = [
    "ssh", "sshd", "apache", "httpd", "cron", "crond", "mysqld", "mysql",
    "postgres", "redis", "docker", "systemd", "sudo", "nginx",
    "python", "php", "perl"
]

# =====================================================
#  ENCABEZADO DEL MÓDULO
# =====================================================
print(f"""
{CYA}{BOLD}┌──────────────────────────────────────────────────────────┐
│     PROCESOS EJECUTÁNDOSE COMO ROOT (MÓDULO XX UNIVERSAL) 🔥    │
│     Identificación de procesos sensibles bajo privilegios root  │
└──────────────────────────────────────────────────────────┘{RESET}
""")

# Mostrar si hay credenciales
if USER:
    print(f"{CYA}{BOLD}→ Usando credenciales enviadas desde el master: {USER}{RESET}\n")
else:
    print(f"{YEL}→ Sin credenciales (se ejecuta como el usuario actual).{RESET}\n")


# =====================================================
#  FUNCIONES DE UTILIDAD
# =====================================================
def run_cmd(command):
    try:
        out = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL)
        return out.decode().strip()
    except:
        return None

def highlight_interesting(line):
    for keyword in INTERESTING:
        if re.search(rf"\\b{keyword}\\b", line, re.IGNORECASE):
            return f"{YEL}{BOLD}{line}{RESET}"
    return line


# =====================================================
#  FUNCIÓN PRINCIPAL DEL MÓDULO
# =====================================================
def run_module():
    print(f"{CYA}{BOLD}=== PROCESOS ROOT DETECTADOS ==={RESET}")

    root_processes = run_cmd("ps aux | grep '^root' | grep -v grep")

    critical = []

    if root_processes:
        for line in root_processes.split("\n"):
            print("  " + highlight_interesting(line))
            # Marcar procesos críticos si son relevantes
            if any(x in line.lower() for x in INTERESTING):
                critical.append(line)
    else:
        print("  No se pudo obtener la lista de procesos de root.")

    # Sección crítica (idéntica a módulo 17 / módulo 20)
    print(f"\n{RED}{BOLD}=== CRÍTICO (AL FINAL) ==={RESET}")
    if critical:
        for c in critical:
            print(f"{RED}[CRÍTICO] Proceso sensible bajo root → {c}{RESET}")
    else:
        print(f"{RED}No se detectaron procesos críticos ejecutándose como root.{RESET}")

    print(f"\n{CYA}{BOLD}[✓] Análisis completado (Módulo Procesos Root Universal){RESET}\n")


# ================================
#  EJECUCIÓN DIRECTA
# ================================
if __name__ == "__main__":
    run_module()
