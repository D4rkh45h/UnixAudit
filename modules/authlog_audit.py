#!/usr/bin/env python3
import os
import gzip

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
{CYA}{BOLD}┌────────────────────────────────────────────────────────┐
│       AUDITORÍA DE AUTENTICACIÓN (MÓDULO 15 UNIVERSAL) 🔥 │
│       Compatible con Linux, macOS y BSD + logs rotados   │
└────────────────────────────────────────────────────────┘{RESET}
""")

if USER:
    print(f"{CYA}{BOLD}→ Usando credenciales enviadas desde el master: {USER}{RESET}\n")
else:
    print(f"{YEL}→ Sin credenciales (se ejecuta como el usuario actual).{RESET}\n")

# =====================================================
#  RUTAS Y PATRONES
# =====================================================
LOG_PATHS = [
    "/var/log/auth.log",
    "/var/log/secure",
    "/var/log/system.log",
    "/private/var/log/system.log",
]

CRITICAL_PATTERNS = [
    "authentication failure",
    "failed password",
    "invalid user",
    "root login",
    "sudo: .*authentication failure",
    "session opened for user root",
]

WARN_PATTERNS = [
    "sudo",
    "failed",
    "invalid",
    "session opened",
    "session closed",
]

# Listas de eventos
normal_entries = []
warnings = []
critical_events = []

# =====================================================
#  FUNCIONES
# =====================================================
def analyze_line(line):
    l = line.lower()
    if any(p.lower() in l for p in CRITICAL_PATTERNS):
        critical_events.append(line.strip())
    elif any(w.lower() in l for w in WARN_PATTERNS):
        warnings.append(line.strip())
    else:
        normal_entries.append(line.strip())

def read_plaintext(path):
    try:
        with open(path, "r", errors="ignore") as f:
            for line in f:
                analyze_line(line)
    except:
        pass

def read_gzip(path):
    try:
        with gzip.open(path, "rt", errors="ignore") as f:
            for line in f:
                analyze_line(line)
    except:
        pass

# =====================================================
#  FUNCIÓN PRINCIPAL
# =====================================================
def run_module():
    # Escanear logs principales y sus rotaciones
    for base in LOG_PATHS:
        if os.path.exists(base):
            read_plaintext(base)

            # Rotados: .1
            if os.path.exists(base + ".1"):
                read_plaintext(base + ".1")

            # Comprimidos: .2.gz … .9.gz
            for i in range(2, 10):
                gz = f"{base}.{i}.gz"
                if os.path.exists(gz):
                    read_gzip(gz)

    # ==============================
    #         SALIDA ORDENADA
    # ==============================
    print(f"{GREEN}{BOLD}\n=== REGISTROS NORMALES (últimos 15) ==={RESET}")
    if normal_entries:
        for l in normal_entries[-15:]:
            print(f"{WHITE}{l}{RESET}")
    else:
        print("-- No entries --")

    print(f"{YEL}{BOLD}\n=== ADVERTENCIAS IMPORTANTES ==={RESET}")
    if warnings:
        for w in warnings[-20:]:
            print(f"{YEL}{w}{RESET}")
    else:
        print("-- No warnings --")

    print(f"{RED}{BOLD}\n=== EVENTOS CRÍTICOS (ABAJO DEL TODO) ==={RESET}")
    if critical_events:
        for c in critical_events:
            print(f"{RED}{BOLD}[CRÍTICO]{RESET} {c}")
    else:
        print("No se detectaron eventos críticos.")

    print(f"\n{CYA}{BOLD}[✓] Auditoría completada (Módulo 15 Universal){RESET}\n")


# ================================
#  EJECUCIÓN DIRECTA
# ================================
if __name__ == "__main__":
    run_module()
