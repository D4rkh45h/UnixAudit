#!/usr/bin/env python3
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
│       REVISIÓN DE CLAVES SSH (MÓDULO 10) 🔥     │
│       Archivos en ~/.ssh — claves expuestas     │
└─────────────────────────────────────────────────┘{RESET}
""")

if USER:
    print(f"{CYA}{BOLD}→ Usando credenciales enviadas desde el master: {USER}{RESET}\n")
else:
    print(f"{YEL}→ Sin credenciales (se ejecuta como el usuario actual).{RESET}\n")

# =====================================================
#  DEFINICIONES
# =====================================================
SSH_DIR = os.path.expanduser("~/.ssh")
PRIVATE_KEY_NAMES = ["id_rsa", "id_dsa", "id_ecdsa", "id_ed25519"]
SENSITIVE_FILES = ["authorized_keys", "known_hosts", "config", "id_rsa.pub"]

critical_hits = []
warnings = []

# =====================================================
#  FUNCIONES
# =====================================================
def check_ssh_dir():
    if not os.path.exists(SSH_DIR):
        print(f"{RED}{BOLD}[CRÍTICO]{RESET} No existe el directorio ~/.ssh (no hay claves).")
        return False
    return True

def scan_ssh_files():
    entries = os.listdir(SSH_DIR)
    for entry in entries:
        full = os.path.join(SSH_DIR, entry)
        if entry in PRIVATE_KEY_NAMES:
            critical_hits.append(f"{RED}[CRÍTICO]{RESET} {full} → CLAVE PRIVADA EXPUESTA")
        elif entry in SENSITIVE_FILES:
            warnings.append(f"{YEL}[AVISO]{RESET} {full}")

def run_module():
    if not check_ssh_dir():
        return

    scan_ssh_files()

    # =====================================================
    # Mostrar resultados
    # =====================================================
    print(f"{RED}{BOLD}=== ARCHIVOS CRÍTICOS ==={RESET}")
    if critical_hits:
        for c in critical_hits:
            print(c)
    else:
        print("  No se detectaron claves privadas.")

    print(f"\n{YEL}{BOLD}=== ADVERTENCIAS IMPORTANTES ==={RESET}")
    if warnings:
        for w in warnings:
            print(w)
    else:
        print("  No hay archivos sensibles relevantes.")

    print(f"\n{GREEN}{BOLD}[✓] Análisis completado (Módulo 10 Universal){RESET}\n")

# ================================
#  EJECUCIÓN DIRECTA
# ================================
if __name__ == "__main__":
    run_module()
