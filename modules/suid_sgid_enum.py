#!/usr/bin/env python3
import subprocess
import os

# ==== COLORES GLOBALES ====
RESET="\033[0m"; BOLD="\033[1m"
RED="\033[91m"; YELLOW="\033[93m"; CYAN="\033[96m"
GREEN="\033[92m"; WHITE="\033[97m"

# ==== CREDENCIALES DEL MASTER ====
USER = os.environ.get("AUDIT_USER")
PASS = os.environ.get("AUDIT_PASS")


# ------------------------------------
# Ejecutar comandos de forma segura
# ------------------------------------
def run_cmd(command):
    try:
        out = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL)
        return out.decode().strip()
    except:
        return None


# ------------------------------------
# Resaltado de binarios peligrosos
# ------------------------------------
def highlight_interesting(paths):
    if not paths:
        return None

    keywords = [
        "bash","sh","dash","zsh",
        "python","python3","perl","ruby",
        "find","nmap","vim","vi",
        "less","more",
        "pkexec","sudo","passwd",
        "mount","umount","doas"
    ]

    result = []
    for line in paths.split("\n"):
        name = os.path.basename(line)
        if name in keywords:
            result.append(f"{YELLOW}{BOLD}{line}{RESET}   ← 🔥 POTENCIAL PRIVESC")
        else:
            result.append(f"{WHITE}{line}{RESET}")

    return "\n".join(result)


# ------------------------------------
# Sección con formato
# ------------------------------------
def print_section(title, content):
    print(f"{GREEN}{BOLD}  ➤ {title}:{RESET}")
    if content:
        print(content + "\n")
    else:
        print(f"{RED}  [No disponible]\n{RESET}")


# ------------------------------------
# MÓDULO PRINCIPAL
# ------------------------------------
def run_module():

    print(f"""
{CYAN}{BOLD}┌──────────────────────────────────────────────┐
│           ENUMERACIÓN SUID + SGID 🔥            │
│   Binarios con permisos elevados peligrosos     │
└──────────────────────────────────────────────┘{RESET}
""")

    if USER:
        print(f"{CYAN}{BOLD}→ Usando credenciales del master: {USER}{RESET}\n")
    else:
        print(f"{YELLOW}→ Sin credenciales: ejecutando con el usuario actual.{RESET}\n")

    # Comandos combinados SUID/SGID
    cmds = [
        "/usr/bin/find / -perm -4000 -type f 2>/dev/null",            # SUID
        "/usr/bin/find / -perm -2000 -type f 2>/dev/null",            # SGID
        "/usr/bin/find / -perm -u=s -o -perm -g=s -type f 2>/dev/null" # combinado
    ]

    results = []
    for c in cmds:
        out = run_cmd(c)
        if out:
            results.append(out)

    critical_notes = []

    if not results:
        combined = "⚠️  No se detectaron SUID ni SGID. Sistema muy restringido o contenedor."
        critical_notes.append("No se encontró ningún binario elevado. Revisar endurecimiento del sistema.")
    else:
        combined = "\n".join(results)

    highlighted = highlight_interesting(combined)
    print_section("Binarios SUID/SGID encontrados", highlighted)

    # -----------------------------
    # SECCIÓN CRÍTICA AL FINAL
    # -----------------------------
    print(f"{RED}{BOLD}=== CRÍTICO (ABAJO DEL TODO) ==={RESET}")

    if critical_notes:
        for c in critical_notes:
            print(f"{RED}[CRÍTICO]{RESET} {c}")
    else:
        print(f"{RED}No se registraron condiciones críticas.{RESET}")

    print(f"\n{CYAN}{BOLD}[✓] Finalizado correctamente: suid_sgid_enum{RESET}\n")


# ------------------------------------
# EJECUCIÓN DIRECTA
# ------------------------------------
if __name__ == "__main__":
    run_module()
