#!/usr/bin/env python3
import subprocess

# ==== COLORES ANSI ====
RESET  = "\033[0m"
BOLD   = "\033[1m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
WHITE  = "\033[97m"

# ==== FUNCIONES AUXILIARES ====
def run_cmd(command):
    """Ejecuta un comando shell y devuelve su salida o None."""
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL)
        return output.decode().strip()
    except:
        return None

def print_section(title, content, color=WHITE):
    """Imprime una sección con formato uniforme y colores."""
    print(f"{GREEN}{BOLD}  ➤ {title}:{RESET}")
    if content:
        print(f"{color}{content}{RESET}\n")
    else:
        print(f"{RED}  [No disponible]{RESET}\n")

# ==== MAIN ====
def main():
    print(f"""
{CYAN}{BOLD}┌────────────────────────────────────────────────┐
│      SERVICIOS QUE ARRANCAN AL INICIO (Nivel 3) │
│      SysV + systemd — detección de servicios     │
└────────────────────────────────────────────────┘{RESET}
""")

    # ===== Comandos clásicos y modernos =====
    runlevel3 = run_cmd("chkconfig --list | grep 3:on")
    systemd_services = run_cmd("systemctl list-unit-files --state=enabled 2>/dev/null")

    print_section("Servicios en runlevel 3 (chkconfig)", runlevel3)
    print_section("Servicios habilitados en systemd", systemd_services)

    # ===== Contador de servicios =====
    if runlevel3:
        count = len(runlevel3.split("\n"))
        print(f"{GREEN}{BOLD}  Total servicios activos en nivel 3:{RESET} {WHITE}{count}{RESET}\n")

    # ===== Servicios interesantes/sensibles =====
    print(f"{GREEN}{BOLD}  ➤ Servicios destacados (interesantes o sensibles):{RESET}")
    INTERESANTES = [
        "ssh", "apache", "nginx", "mysql", "docker", "cron", "crond",
        "rsync", "ftp", "telnet", "samba", "firewalld", "iptables",
        "fail2ban", "network", "rpc", "nfs", "cups"
    ]

    encontrados = False
    if runlevel3:
        for line in runlevel3.split("\n"):
            if any(service in line.lower() for service in INTERESANTES):
                print(f"{YELLOW}{BOLD}{line}{RESET}")
                encontrados = True
    if not encontrados:
        print(f"{RED}  [Ningún servicio destacado encontrado]{RESET}\n")

    # ===== Servicios potencialmente peligrosos =====
    peligrosos = run_cmd("chkconfig --list | egrep 'telnet|rsh|rlogin|ftp|tftp'")
    print_section("⚠ Servicios inseguros o peligrosos detectados", peligrosos, YELLOW)

    print(f"{GREEN}{BOLD}[✓] Auditoría completada: runlevel3_services{RESET}\n")

# ==== EJECUCIÓN DIRECTA ====
if __name__ == '__main__':
    main()
