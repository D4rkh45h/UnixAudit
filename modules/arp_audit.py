#!/usr/bin/env python3
import subprocess
import re

# ================================
# Colores y estilos universales
# ================================
RED   = "\033[91m"
YEL   = "\033[93m"
CYA   = "\033[96m"
BOLD  = "\033[1m"
RESET = "\033[0m"
GREEN = "\033[92m"

# =====================================================
# Cabecera visual
# =====================================================
print(f"""
{CYA}{BOLD}┌──────────────────────────────────────────────┐
│       REVISIÓN DE TABLA ARP (MÓDULO 14) 🔥      │
│       Busca IPs duplicadas, MAC sospechosas y spoofing │
└──────────────────────────────────────────────┘{RESET}
""")

# =====================================================
# Ejecutar comando arp
# =====================================================
try:
    output = subprocess.check_output(
        ["arp", "-e"],
        text=True,
        stderr=subprocess.STDOUT
    )
except Exception as e:
    print(f"{RED}[CRÍTICO]{RESET} No se pudo ejecutar 'arp -e': {e}")
    exit()

lines = output.strip().split("\n")

normal = []
warnings = []
critical = []

# MACs sospechosas típicas de spoofing
spoof_macs = [
    "00:00:00:00:00:00",
    "ff:ff:ff:ff:ff:ff",
]

seen_ips = {}

# =====================================================
# Analizar entradas
# =====================================================
for line in lines:
    if "IP" in line or line.strip() == "":
        normal.append(line)
        continue

    parts = re.split(r"\s+", line)
    if len(parts) < 3:
        normal.append(line)
        continue

    ip = parts[0]
    mac = parts[2].lower()

    # IP duplicada → crítico
    if ip in seen_ips:
        critical.append(f"[IP DUPLICADA] {line}")
    else:
        seen_ips[ip] = mac

    # MAC sospechosa → crítico
    if mac in spoof_macs:
        critical.append(f"[MAC SOSPECHOSA] {line}")
        continue

    # MAC muy reciente / virtual → aviso
    if mac.startswith(("0a:", "0e:", "12:", "16:", "1a:")):
        warnings.append(f"[POSIBLE SPOOF] {line}")
        continue

    normal.append(line)

# =====================================================
# Salida ordenada
# =====================================================
print(f"{GREEN}{BOLD}=== ENTRADAS NORMALES ==={RESET}")
for n in normal:
    print(n)

if warnings:
    print(f"\n{YEL}{BOLD}=== ADVERTENCIAS IMPORTANTES ==={RESET}")
    for w in warnings:
        print(f"{YEL}{w}{RESET}")

print(f"\n{RED}{BOLD}=== CRÍTICOS ==={RESET}")
if critical:
    for c in critical:
        print(f"{RED}{c}{RESET}")
else:
    print("Ninguna entrada crítica detectada.")

# =====================================================
# Fin del módulo
# =====================================================
print(f"\n{GREEN}{BOLD}[✓] Análisis ARP completado (Módulo 14){RESET}\n")
