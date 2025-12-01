#!/usr/bin/env python3
import subprocess
import os
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
    """Ejecuta comando con sudo si el master pasó credenciales."""
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


# ============================
#   RESALTAR DIRECTORIOS
# ============================
def highlight_interesting(lines):
    """Marca en rojo los directorios críticos world-writable."""
    if not lines:
        return lines

    out = []
    for line in lines.split("\n"):
        if any(s in line for s in [
            "/etc", "/root", "/bin", "/sbin", "/usr/bin", "/usr/sbin"
        ]):
            out.append(f"{RED}{BOLD}{line}{RESET}   {YELLOW}[CRÍTICO ⚠]{RESET}")
        elif "tmp" in line or "cache" in line:
            out.append(f"{YELLOW}{line}{RESET}   [Común]")
        else:
            out.append(line)
    return "\n".join(out)


# ============================
#   SECCIÓN BONITA
# ============================
def print_section(title, content):
    print(f"{GREEN}{BOLD}  ➤ {title}:{RESET}")
    if content:
        print(f"{WHITE}{content}{RESET}\n")
    else:
        print(f"{RED}  [No disponible]{RESET}\n")


# ============================
#   MAIN HOMOGENIZADO
# ============================
def main():

    print(f"""
{CYAN}{BOLD}┌────────────────────────────────────────────────────────────┐
│        DIRECTORIOS WORLD-WRITABLE (777) — MÓDULO 23 🔥            │
│        Riesgo real: Hijack / Inyección / Priv Escalation         │
└────────────────────────────────────────────────────────────┘{RESET}
""")

    ww = run_cmd(["find", "/", "-perm", "-0002", "-type", "d", "2>/dev/null"])

    ww_highlighted = highlight_interesting(ww)

    print_section("Directorios con permisos world-writable", ww_highlighted)

    # ============================
    #   CRÍTICOS (ABAJO)
    # ============================
    print(f"{RED}{BOLD}=== EVENTOS CRÍTICOS DETECTADOS ==={RESET}")

    if ww:
        dangerous = [
            line for line in ww.split("\n")
            if any(s in line for s in ["/etc", "/root", "/bin", "/sbin", "/usr"])
        ]

        if dangerous:
            for d in dangerous:
                print(f"{RED}[CRÍTICO] {d}{RESET}")
        else:
            print("  No se detectaron directorios críticos world-writable.")
    else:
        print("  No se encontraron rutas world-writable.")

    print(f"\n{GREEN}{BOLD}[✓] Análisis completado (Módulo 23){RESET}\n")


if __name__ == "__main__":
    main()
