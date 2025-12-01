#!/usr/bin/env python3
import subprocess
import os

# Colores y estilos universales
RED="\033[91m"; YEL="\033[93m"; CYA="\033[96m"; BOLD="\033[1m"; RESET="\033[0m"
WHITE="\033[97m"; GREEN="\033[92m"

# ================================
#  Cargar credenciales del master
# ================================
USER = os.environ.get("AUDIT_USER")
PASS = os.environ.get("AUDIT_PASS")

# =====================================================
#  ENCABEZADO DEL MÓDULO
# =====================================================
print(f"""
{CYA}{BOLD}┌──────────────────────────────────────────────┐
│ HISTORIAL DE ACCESOS AL SISTEMA (MÓDULO 12) 🔥 │
│ Revisa logins recientes con 'last'             │
└──────────────────────────────────────────────┘{RESET}
""")

if USER:
    print(f"{CYA}{BOLD}→ Usando credenciales enviadas desde el master: {USER}{RESET}\n")
else:
    print(f"{YEL}→ Sin credenciales (se ejecuta como el usuario actual).{RESET}\n")

# =====================================================
# FUNCIONES
# =====================================================
def run_cmd(command):
    try:
        return subprocess.check_output(command, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception as e:
        return f"{RED}[CRÍTICO] Error ejecutando comando: {e}{RESET}"

def run_module():
    output = run_cmd(["last"])
    critical = []

    if output.startswith("[CRÍTICO]"):
        print(output)
        return

    lines = output.split("\n")
    if len(lines) <= 1:
        print(f"{RED}[CRÍTICO] No hay registros de acceso en 'last'.{RESET}")
        return

    print(f"{GREEN}{BOLD}=== ACCESOS RECIENTES DETECTADOS ==={RESET}")
    for line in lines:
        line_strip = line.strip()
        if line_strip and ("system boot" not in line_strip.lower()):
            print(f"  {line_strip}")
            # Marcar root logins como críticos
            if line_strip.lower().startswith("root"):
                critical.append(line_strip)

    # Sección CRÍTICO al final
    print(f"\n{RED}{BOLD}=== CRÍTICO (ABAJO DEL TODO) ==={RESET}")
    if critical:
        for c in critical:
            print(f"{RED}[CRÍTICO]{RESET} {c}")
    else:
        print(f"{RED}No se detectaron accesos críticos.{RESET}")

    print(f"\n{CYA}{BOLD}[✓] Análisis completado (Módulo 12 Universal){RESET}\n")


# ================================
# EJECUCIÓN DIRECTA
# ================================
if __name__ == "__main__":
    run_module()
