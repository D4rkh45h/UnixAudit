#!/usr/bin/env python3
import os
import subprocess

# =====================================================
# COLORES ANSI
# =====================================================
RESET  = "\033[0m"
BOLD   = "\033[1m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
WHITE  = "\033[97m"

# =====================================================
# CREDENCIALES MASTER (opcional)
# =====================================================
username = os.environ.get("MODULE_USER")
password = os.environ.get("MODULE_PASS")

# =====================================================
# FUNCIONES AUXILIARES
# =====================================================
def run_cmd(cmd):
    """Ejecuta un comando shell, soporta sudo si hay credenciales."""
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
            return out.strip()
        else:
            return subprocess.check_output(cmd, text=True).strip()
    except:
        return None

def print_section(title, content, color=WHITE):
    print(f"{GREEN}{BOLD}  ➤ {title}:{RESET}")
    if content:
        print(f"{color}{content}{RESET}\n")
    else:
        print(f"{RED}  [No disponible]{RESET}\n")

def is_suid_or_capabilities(path):
    """Comprueba si un binario puede escalar privilegios."""
    try:
        st = os.stat(path)

        # SUID root
        if st.st_mode & 0o4000:
            return True

        # Capacidades peligrosas
        caps = run_cmd(["getcap", path])
        if caps and any(c in caps for c in ["cap_setuid", "cap_setgid", "cap_dac_override"]):
            return True

    except:
        pass
    return False

# =====================================================
# MAIN
# =====================================================
def main():

    print(f"""
{CYAN}{BOLD}┌────────────────────────────────────────────────────────────┐
│  BÚSQUEDA DE HERRAMIENTAS DE DESCARGA (MÓDULO 18 UNIVERSAL) 🔥│
│  SOLO crítico si el binario PERMITE ESCALADA DE PRIVILEGIOS    │
└────────────────────────────────────────────────────────────┘{RESET}
""")

    ESCALATION_BINARIES = ["wget", "curl", "rsync", "scp", "busybox", "tftp", "ftp"]

    found = []
    criticals = []

    for root, dirs, files in os.walk("/", topdown=True):
        # Carpetas que molestan
        dirs[:] = [d for d in dirs if d not in ["proc", "sys", "run", "dev", "snap"]]

        for f in files:
            fname = f.lower()
            if fname in ESCALATION_BINARIES:
                full = os.path.join(root, f)
                found.append(full)

                if is_suid_or_capabilities(full):
                    criticals.append(full)

    # ==============================
    # SALIDA ORDENADA
    # ==============================
    print_section("Herramientas encontradas", 
                  "\n".join(found) if found else None,
                  YELLOW)

    print_section("CRÍTICOS (permite escalada de privilegios)",
                  "\n".join(f"{RED}[CRÍTICO]{RESET} {c}" for c in criticals) if criticals else None,
                  RED)

    print(f"{GREEN}{BOLD}[✓] Análisis completado (Módulo 18 Universal){RESET}\n")

# =====================================================
# EJECUCIÓN DIRECTA
# =====================================================
if __name__ == "__main__":
    main()
