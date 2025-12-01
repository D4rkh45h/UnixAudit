#!/usr/bin/env python3
import os

# ================================
# Colores y estilos universales
# ================================
RED    = "\033[91m"
YEL    = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"
GREEN  = "\033[92m"
WHITE  = "\033[97m"

# =====================================================
# Archivo de historial
# =====================================================
HIST_FILE = os.path.expanduser("~/.bash_history")

# =====================================================
# Cabecera visual
# =====================================================
print(f"""
{CYAN}{BOLD}┌──────────────────────────────────────────────┐
│  AUDITORÍA DEL HISTORIAL BASH (MÓDULO 11) 🔥    │
│  Busca contraseñas, tokens y comandos peligrosos │
└──────────────────────────────────────────────────┘{RESET}
""")

if not os.path.exists(HIST_FILE):
    print(f"{RED}[CRÍTICO]{RESET} No existe ~/.bash_history (no hay historial).")
    exit(0)

# =====================================================
# Patrones críticos y advertencias
# =====================================================
CRITICAL_PATTERNS = [
    "password", "passwd", "pwd=", "token", "secret",
    "api_key", "mysql -u", "--password", "sshpass",
    "curl -u", "export ", "AWS_SECRET", "AWS_KEY"
]

WARNING_PATTERNS = [
    "ssh ", "scp ", "sftp ", "ftp ", "mysql ",
    "psql ", "sudo ", "chmod 777", "chown ", "wget ", "curl "
]

critical_hits = []
warnings = []

# =====================================================
# Análisis del historial
# =====================================================
with open(HIST_FILE, "r", errors="ignore") as f:
    for num, line in enumerate(f, 1):
        l = line.strip().lower()

        # CRÍTICOS
        if any(p in l for p in CRITICAL_PATTERNS):
            critical_hits.append(f"{RED}[CRÍTICO]{RESET} Línea {num}: {line.strip()}")
            continue

        # ADVERTENCIAS
        if any(w in l for w in WARNING_PATTERNS):
            warnings.append(f"{YEL}[AVISO]{RESET} Línea {num}: {line.strip()}")

# =====================================================
# Salida ordenada
# =====================================================
print(f"{RED}{BOLD}=== RESULTADOS CRÍTICOS ==={RESET}")
if critical_hits:
    for c in critical_hits:
        print(c)
else:
    print("  No se encontraron elementos críticos.")

print(f"\n{YEL}{BOLD}=== ADVERTENCIAS IMPORTANTES ==={RESET}")
if warnings:
    for w in warnings:
        print(w)
else:
    print("  No se encontraron comandos sensibles.")

print(f"\n{GREEN}{BOLD}[✓] Auditoría completada (Módulo 11){RESET}\n")
