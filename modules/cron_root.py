#!/usr/bin/env python3
import os
import subprocess

# Colores y estilos universales
RED="\033[91m"; YEL="\033[93m"; CYA="\033[96m"; BOLD="\033[1m"; RESET="\033[0m"
WHITE="\033[97m"; GREEN="\033[92m"

# ================================
#  Cargar credenciales del master
# ================================
USER = os.environ.get("AUDIT_USER")
PASS = os.environ.get("AUDIT_PASS")

# Palabras clave críticas en cron
CRITICAL_KEYWORDS = ["/tmp", "/dev/shm", "wget", "curl", "nc", "python", "bash"]

# =====================================================
#  ENCABEZADO DEL MÓDULO
# =====================================================
print(f"""
{CYA}{BOLD}┌──────────────────────────────────────────────┐
│               CRON JOBS DE ROOT (MÓDULO XX) 🔥 │
│   Detecta tareas programadas ejecutadas como root│
└──────────────────────────────────────────────┘{RESET}
""")

if USER:
    print(f"{CYA}{BOLD}→ Usando credenciales enviadas desde el master: {USER}{RESET}\n")
else:
    print(f"{YEL}→ Sin credenciales (se ejecuta como el usuario actual).{RESET}\n")

# =====================================================
#  FUNCIONES DE UTILIDAD
# =====================================================
def run_cmd(command):
    try:
        out = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL)
        return out.decode().strip()
    except:
        return None

def safe_cat(path):
    if os.path.exists(path):
        return run_cmd(f"cat {path}")
    return None

def highlight(lines):
    if not lines:
        return lines
    res = []
    for line in lines.split("\n"):
        s = line.strip()
        if s.startswith("#"):
            res.append(f"{CYA}{line}{RESET}")
        elif any(k in line for k in CRITICAL_KEYWORDS):
            res.append(f"{RED}{BOLD}{line}{RESET}   {YEL}[CRÍTICO ⚠]{RESET}")
        else:
            res.append(f"{WHITE}{line}{RESET}")
    return "\n".join(res)

def print_section(title, content):
    print(f"{GREEN}{BOLD}  ➤ {title}:{RESET}")
    if content:
        print(f"{content}\n")
    else:
        print(f"{RED}  [No disponible]\n{RESET}")

# =====================================================
#  FUNCIÓN PRINCIPAL
# =====================================================
def run_module():
    ubicaciones = [
        "/var/spool/cron/crontabs/root",   # Debian, Ubuntu, Kali
        "/var/spool/cron/root",            # CentOS, RHEL, Fedora
        "/etc/cron.d/root"                 # Otras distros personalizadas
    ]

    contenido = None
    usada = None
    critical = []

    for ruta in ubicaciones:
        contenido = safe_cat(ruta)
        if contenido:
            usada = ruta
            break

    if usada:
        contenido = highlight(contenido)
        print_section(f"Tareas encontradas en {usada}", contenido)
        # Marcar líneas críticas
        for line in contenido.split("\n"):
            if any(k in line for k in CRITICAL_KEYWORDS):
                critical.append(line)
    else:
        print_section("Cron propio de root", None)

    # =====================================================
    # Sección CRÍTICO al final
    # =====================================================
    print(f"\n{RED}{BOLD}=== CRÍTICO (AL FINAL) ==={RESET}")
    if critical:
        for c in critical:
            print(f"{RED}[CRÍTICO] {c}{RESET}")
    else:
        print(f"{RED}No se detectaron tareas críticas en cron root.{RESET}")

    print(f"\n{CYA}{BOLD}[✓] Análisis completado (Módulo Cron Root Universal){RESET}\n")


# ================================
#  EJECUCIÓN DIRECTA
# ================================
if __name__ == "__main__":
    run_module()
