#!/usr/bin/env python3
import os

# Colores y estilos
RED="\033[91m"; YEL="\033[93m"; CYA="\033[96m"; BOLD="\033[1m"; RESET="\033[0m"

# ================================
#  Cargar credenciales del master
# ================================
USER = os.environ.get("AUDIT_USER")
PASS = os.environ.get("AUDIT_PASS")

# =====================================================
#  ENCABEZADO DEL MÓDULO
# =====================================================
print(f"""
{CYA}{BOLD}┌──────────────────────────────────────────────────────────┐
│        ARCHIVO /etc/shadow (MÓDULO 20 UNIVERSAL) 🔥            │
│        Detección de acceso a hashes de contraseñas            │
└──────────────────────────────────────────────────────────┘{RESET}
""")

# Mostrar si hay credenciales
if USER:
    print(f"{CYA}{BOLD}→ Usando credenciales enviadas desde el master: {USER}{RESET}\n")
else:
    print(f"{YEL}→ Sin credenciales (se ejecuta como el usuario actual).{RESET}\n")

# =====================================================
#  FUNCIÓN PRINCIPAL DEL MÓDULO
# =====================================================
def run_module():
    shadow_file = "/etc/shadow"
    contenido_shadow = []
    critical = []

    try:
        with open(shadow_file, "r") as f:
            lines = f.readlines()
            contenido_shadow.extend(lines)
            # Consideramos crítico si tenemos acceso al archivo
            critical.append(shadow_file)
    except PermissionError:
        print(f"{YEL}❌ No tienes permisos para leer {shadow_file}.{RESET}")
    except Exception as e:
        print(f"{RED}{BOLD}❌ Error inesperado: {e}{RESET}")

    # Mostrar contenido
    print(f"{CYA}{BOLD}=== CONTENIDO DE /etc/shadow ==={RESET}")
    if contenido_shadow:
        for line in contenido_shadow:
            print("  " + line.strip())
    else:
        print("  No se pudo leer el archivo.")

    # Mostrar sección crítica igual que módulo 17
    print(f"\n{RED}{BOLD}=== CRÍTICO (AL FINAL) ==={RESET}")
    if critical:
        for c in critical:
            print(f"{RED}[CRÍTICO] Tienes acceso a {c} → Riesgo de escalada de privilegios{RESET}")
    else:
        print(f"{RED}No se detectaron archivos críticos accesibles.{RESET}")

    print(f"\n{CYA}{BOLD}[✓] Análisis completado (Módulo 20 Universal){RESET}\n")


# ================================
#  EJECUCIÓN DIRECTA
# ================================
if __name__ == "__main__":
    run_module()
