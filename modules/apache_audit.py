#!/usr/bin/env python3
import os
import re
import subprocess
import sys

# ==== COLORES ANSI ====
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
GREEN = "\033[92m"
CYAN = "\033[96m"
WHITE = "\033[97m"

# ============================
#   CREDENCIALES MASTER
# ============================
username = os.environ.get("MODULE_USER")
password = os.environ.get("MODULE_PASS")

def run_cmd(cmd):
    """Ejecuta un comando con sudo si hay credenciales."""
    try:
        if username and password:
            full_cmd = ["sudo", "-S"] + cmd
            proc = subprocess.Popen(
                full_cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            out, err = proc.communicate(password + "\n")
            return out
        else:
            return subprocess.check_output(cmd, text=True)
    except Exception as e:
        print(f"{RED}[CRÍTICO] Error ejecutando {' '.join(cmd)} → {e}{RESET}")
        sys.exit(1)

# ============================
#   CABECERA VISUAL
# ============================
print(f"""
{CYAN}{BOLD}┌──────────────────────────────────────────────────────────┐
│   AUDITORÍA DE APACHE (MÓDULO 16 UNIVERSAL) 🔥             │
│   Compatible con Linux, macOS, BSD + rutas alternativas   │
└──────────────────────────────────────────────────────────┘{RESET}
""")

# ============================
#   RUTAS DE CONFIGURACIÓN
# ============================
APACHE_PATHS = [
    "/etc/apache2/apache2.conf",
    "/etc/httpd/conf/httpd.conf",
    "/usr/local/etc/apache2/httpd.conf",
    "/opt/local/apache2/conf/httpd.conf",
]

found_files = []
config_data = ""

for path in APACHE_PATHS:
    if os.path.isfile(path):
        found_files.append(path)

if not found_files:
    print(f"{RED}[CRÍTICO] No se encontró ninguna configuración de Apache en el sistema.{RESET}")
    sys.exit(0)

for file in found_files:
    print(f"{GREEN}[✓] Analizando: {file}{RESET}")
    try:
        with open(file, "r", errors="ignore") as f:
            config_data += f.read() + "\n"
    except Exception as e:
        print(f"{RED}[CRÍTICO] No se pudo leer {file} → {e}{RESET}")

# ============================
#   SECCIÓN NORMAL
# ============================
print(f"\n{YELLOW}{BOLD}=== CONFIGURACIÓN ENCONTRADA (extracto) ==={RESET}")
lines = config_data.split("\n")
for line in lines[:20]:
    print("  " + line)

# ============================
#   ADVERTENCIAS
# ============================
warnings = []

if "AllowOverride None" in config_data:
    warnings.append("AllowOverride None → puede impedir .htaccess necesarios.")

if re.search(r"DocumentRoot\s+\/home\/", config_data):
    warnings.append("DocumentRoot apunta a /home → riesgo de exposición de usuarios.")

if "Indexes" in config_data:
    warnings.append("La opción 'Indexes' está habilitada → listado de directorios expuesto.")

print(f"\n{MAGENTA}{BOLD}=== ADVERTENCIAS IMPORTANTES ==={RESET}")
if warnings:
    for w in warnings:
        print(f"{MAGENTA}[AVISO]{RESET} {w}")
else:
    print("-- No warnings --")

# ============================
#   EVENTOS CRÍTICOS
# ============================
criticos = []

credenciales_regex = r"(password|passwd|db_pass|database_password|mysql_pass)\s*[\=\s]+\s*['\"]?([A-Za-z0-9_\-\.]+)['\"]?"
for match in re.finditer(credenciales_regex, config_data, re.IGNORECASE):
    criticos.append(f"Credencial expuesta: {match.group(0)}")

if re.search(r"<Directory\s+\/>(.*?)Allow\s+from\s+all", config_data, re.S):
    criticos.append("El directorio raíz '/' permite acceso a todos. MUY peligroso.")

if "CustomLog /dev/null" in config_data or "ErrorLog /dev/null" in config_data:
    criticos.append("Logging desactivado (/dev/null) → imposible auditar intrusiones.")

print(f"\n{RED}{BOLD}=== EVENTOS CRÍTICOS (ABAJO EN ROJO) ==={RESET}")
if criticos:
    for c in criticos:
        print(f"{RED}[CRÍTICO]{RESET} {c}")
else:
    print(f"{RED}No se detectaron eventos críticos.{RESET}")

print(f"\n{GREEN}{BOLD}[✓] Auditoría completada (Módulo 16 Universal){RESET}\n")
