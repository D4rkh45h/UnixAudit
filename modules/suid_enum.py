#!/usr/bin/env python3
import subprocess
import os

# ==== COLORES UNIVERSALES ====
RESET="\033[0m"; BOLD="\033[1m"
RED="\033[91m"; YELLOW="\033[93m"; CYAN="\033[96m"
GREEN="\033[92m"; WHITE="\033[97m"

# ================================
#  Credenciales del master
# ================================
USER = os.environ.get("AUDIT_USER")
PASS = os.environ.get("AUDIT_PASS")


# ================================
# Función para ejecutar comandos
# ================================
def run_cmd(command):
    try:
        out = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL)
        return out.decode().strip()
    except:
        return None


# ================================
# Resaltado de binarios peligrosos
# ================================
def highlight_interesting_binaries(paths):
    if not paths:
        return None

    interesting = [
        "bash", "sh", "dash", "zsh",
        "python", "python3",
        "perl", "ruby",
        "find",
        "nmap",
        "vim", "vi",
        "gcc",
        "pkexec",
        "sudo",
        "passwd"
    ]

    lines = []
    for line in paths.split("\n"):
        name = os.path.basename(line)

        if name in interesting:
            lines.append(f"{YELLOW}{BOLD}{line}{RESET}   ← 🔥 POTENCIAL PRIVESC")
        else:
            lines.append(f"{WHITE}{line}{RESET}")

    return "\n".join(lines)


# ================================
# Sección con formato
# ================================
def print_section(title, content):
    print(f"{GREEN}{BOLD}  ➤ {title}:{RESET}")
    if content:
        print(content + "\n")
    else:
        print(f"{RED}  [No disponible]{RESET}\n")


# ================================
# MÓDULO PRINCIPAL
# ================================
def run_module():

    # Encabezado homogéneo
    print(f"""
{CYAN}{BOLD}┌──────────────────────────────────────────────┐
│   ENUMERACIÓN DE BINARIOS SUID / SGID 🔥       │
│   Vectores directos de escalada de privilegios │
└──────────────────────────────────────────────┘{RESET}
""")

    if USER:
        print(f"{CYAN}{BOLD}→ Usando credenciales del master: {USER}{RESET}\n")
    else:
        print(f"{YELLOW}→ Sin credenciales: ejecutando como usuario actual.{RESET}\n")

    # === MÉTODO 1 ===
    suid = run_cmd("/usr/bin/find / -perm -u=s -type f 2>/dev/null")

    # === MÉTODO 2 ===
    if not suid:
        suid = run_cmd("find / -perm -4000 -type f 2>/dev/null")

    # === MÉTODO 3 ===
    critical_notes = []
    if not suid:
        suid = "⚠️  No se detectaron binarios SUID. ¿Sistema restringido / contenedor?"
        critical_notes.append("No hay SUID detectados. Restricción severa o contenedor.")


    suid_highlighted = highlight_interesting_binaries(suid)
    print_section("Binarios SUID encontrados", suid_highlighted)

    # =============================
    # SECCIÓN CRÍTICOS AL FINAL
    # =============================
    print(f"\n{RED}{BOLD}=== CRÍTICO (ABAJO DEL TODO) ==={RESET}")

    if critical_notes:
        for c in critical_notes:
            print(f"{RED}[CRÍTICO]{RESET} {c}")
    else:
        print(f"{RED}No se detectaron condiciones críticas.{RESET}")

    print(f"\n{CYAN}{BOLD}[✓] Finalizado correctamente: suid_enum{RESET}\n")


# ================================
# EJECUCIÓN DIRECTA
# ================================
if __name__ == "__main__":
    run_module()
