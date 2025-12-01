#!/usr/bin/env python3
import subprocess
import os

# =====================================================
# COLORES ANSI (estándar para todos los módulos)
# =====================================================
RESET  = "\033[0m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
WHITE  = "\033[97m"
BOLD   = "\033[1m"
RED    = "\033[91m"
YELLOW = "\033[93m"

# =====================================================
# Funciones auxiliares
# =====================================================
def run_cmd(command):
    """Ejecuta un comando shell y devuelve su salida o None."""
    try:
        output = subprocess.check_output(
            command, shell=True, stderr=subprocess.DEVNULL
        )
        return output.decode().strip()
    except:
        return None


def highlight_cron(lines):
    """Añade colores y marca tareas potencialmente peligrosas."""
    if not lines:
        return lines

    res = []
    for line in lines.split("\n"):
        l = line.strip()

        if l.startswith("#"):
            res.append(f"{CYAN}{line}{RESET}")
        elif "root" in l or "/tmp" in l or "/dev/shm" in l:
            res.append(f"{RED}{BOLD}{line}{RESET}   {YELLOW}[CRÍTICO ⚠]{RESET}")
        else:
            res.append(line)

    return "\n".join(res)


def print_section(title, content):
    """Imprime una sección con formato uniforme."""
    print(f"{GREEN}{BOLD}  ➤ {title}:{RESET}")
    if content:
        print(f"{WHITE}{content}{RESET}\n")
    else:
        print(f"{RED}  [No disponible]{RESET}\n")


# =====================================================
# MAIN
# =====================================================
def main():
    print(f"""
{CYAN}{BOLD}┌────────────────────────────────────────────────────────┐
│            CRONTAB DEL SISTEMA (MÓDULO 14) 🔥               │
│     Auditoría de tareas programadas vulnerables a hijack    │
└────────────────────────────────────────────────────────┘{RESET}
""")

    cron = run_cmd("cat /etc/crontab")

    cron = highlight_cron(cron)

    print_section("Tareas programadas en /etc/crontab", cron)

    print(f"{CYAN}{BOLD}[✓] Auditoría completada (Módulo 14){RESET}\n")


# =====================================================
# EXEC
# =====================================================
if __name__ == '__main__':
    main()
