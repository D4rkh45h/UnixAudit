#!/usr/bin/env python3
import os
import subprocess
import sys

# ==== COLORES ANSI ====
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
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
#   CABECERA HOMOGÉNEA
# ============================
print(f"""
{CYAN}{BOLD}┌──────────────────────────────────────────────────────────┐
│      BÚSQUEDA DE CREDENCIALES REALES (PRO MODE) 🔍            │
│      Solo resultados críticos, reales y explotables           │
└──────────────────────────────────────────────────────────┘{RESET}
""")

# ============================
#   DEFINICIONES
# ============================
SENSITIVE_FILES = [
    "id_rsa", "id_dsa", "id_ecdsa", "credentials",
    "shadow", "passwd", ".env", "config.php",
    "wp-config.php", "database.yml", ".git-credentials", "settings.py",
]

VALID_EXT = [".sh", ".py", ".js", ".php", ".txt", ".conf", ".env", ".yml", ".json"]

REAL_KEYS = [
    "password=", "password:", "passwd", "pwd=",
    "secret=", "secret:", "token=", "token:",
    "api_key", "private_key", "aws_secret",
]

IGNORE_EXT = [".md", ".markdown"]
IGNORE_PATH = ["tldr", "manpages", ".cache", "/usr/share"]

critical_hits = []

def is_valid_file(path):
    if any(path.endswith(ext) for ext in IGNORE_EXT):
        return False
    if any(skip in path for skip in IGNORE_PATH):
        return False
    if os.path.isdir(path):
        return False
    return True

def might_contain_credentials(file):
    f = file.lower()
    if any(s in f for s in SENSITIVE_FILES):
        return True
    if any(f.endswith(ext) for ext in VALID_EXT):
        return True
    return False

def analyze_file(path):
    try:
        with open(path, "r", errors="ignore") as f:
            for num, line in enumerate(f, 1):
                l = line.strip()
                ll = l.lower()

                if any(k in ll for k in REAL_KEYS):
                    # Filtrar basura habitual
                    if any(x in ll for x in ["{{", "}}", "<password>", "example", "#"]):
                        continue
                    critical_hits.append(f"{RED}[CRÍTICO]{RESET} {path}:{num} → {l}")
    except:
        pass

SCAN_DIRS = ["/home", "/root", "/etc", "/var/www", "/opt"]

# ============================
#   ESCANEO PROFESIONAL
# ============================
for base in SCAN_DIRS:
    for root, dirs, files in os.walk(base, topdown=True):
        # Evitar directorios que causan ruido o bucles infinitos
        dirs[:] = [
            d for d in dirs if d not in 
            ["proc", "sys", "dev", "run", "snap", ".cache"]
        ]

        for file in files:
            full_path = os.path.join(root, file)

            if not is_valid_file(full_path):
                continue

            if might_contain_credentials(file):
                analyze_file(full_path)

# ============================
#   RESULTADOS CRÍTICOS ABAJO
# ============================
print(f"\n{RED}{BOLD}=== RESULTADOS CRÍTICOS REALES ==={RESET}")
if critical_hits:
    for hit in critical_hits:
        print(hit)
else:
    print("  No se encontraron credenciales reales.")

print(f"\n{GREEN}{BOLD}[✓] Análisis completado (PRO MODE){RESET}\n")
