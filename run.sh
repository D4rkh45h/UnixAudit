#!/bin/bash

# Colores
CYA="\033[96m"
BOLD="\033[1m"
RESET="\033[0m"

echo -e "${CYA}${BOLD}"
echo "┌──────────────────────────────────────────────────────────┐"
echo "│  UNIVERSAL UNIX PRIVILEGE ESCALATION SUITE – LAUNCHER   │"
echo "└──────────────────────────────────────────────────────────┘"
echo -e "${RESET}"

# Detectar ruta absoluta del script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Ejecutar el master
python3 "$SCRIPT_DIR/master.py" "$@"
