#!/usr/bin/env python3
import re

RED="\033[91m"; YEL="\033[93m"; GRN="\033[92m"; BOLD="\033[1m"; RESET="\033[0m"

print(f"""
{BOLD}┌─────────────────────────────────────────────────────────┐
│     REVISIÓN DE CONFIGURACIÓN SSH (MÓDULO 9) 🔥           │
│     Analiza /etc/ssh/sshd_config en busca de fallos       │
└─────────────────────────────────────────────────────────┘{RESET}
""")

CRITICAL = []
WARNING = []

rules_critical = {
    r"^\s*PermitRootLogin\s+yes": "PermitRootLogin YES → acceso directo a root",
    r"^\s*PasswordAuthentication\s+yes": "PasswordAuthentication YES → fuerza bruta posible",
    r"^\s*PermitEmptyPasswords\s+yes": "Passwords vacías permitidas",
    r"^\s*Protocol\s+1": "SSH usando Protocol 1 (inseguro)",
}

rules_warning = {
    r"^\s*X11Forwarding\s+yes": "X11Forwarding activo (riesgo medio)",
    r"^\s*AllowUsers\s*$": "AllowUsers vacío → todos los usuarios pueden conectarse",
    r"^\s*AllowGroups\s*$": "AllowGroups vacío → grupos sin restricción",
}

try:
    with open("/etc/ssh/sshd_config", "r") as f:
        lines = f.readlines()
except PermissionError:
    print(f"{RED}[ERROR] Necesitas ejecutar este módulo como root.{RESET}")
    exit(1)

for num, line in enumerate(lines, 1):
    l = line.strip()

    # CRÍTICOS
    for pattern, msg in rules_critical.items():
        if re.search(pattern, l, re.IGNORECASE):
            CRITICAL.append(f"{RED}[CRÍTICO]{RESET} Línea {num}: {msg} → '{l}'")

    # WARNING
    for pattern, msg in rules_warning.items():
        if re.search(pattern, l, re.IGNORECASE):
            WARNING.append(f"{YEL}[AVISO]{RESET} Línea {num}: {msg} → '{l}'")

print(f"\n{RED}{BOLD}=== FALLOS CRÍTICOS ENCONTRADOS ==={RESET}")
if CRITICAL:
    for c in CRITICAL:
        print(c)
else:
    print("  No se encontraron fallos críticos.")

print(f"\n{YEL}{BOLD}=== ADVERTENCIAS IMPORTANTES ==={RESET}")
if WARNING:
    for w in WARNING:
        print(w)
else:
    print("  No hay advertencias importantes.")

print(f"\n{GRN}{BOLD}[✓] Análisis de SSH completado (Módulo 9){RESET}\n")
