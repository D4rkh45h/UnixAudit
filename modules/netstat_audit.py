#!/usr/bin/env python3
import subprocess
import os

# ==== COLORES ANSI ====
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
GREEN = "\033[92m"
WHITE = "\033[97m"

# ============================
#   CREDENCIALES MASTER (opcional)
# ============================
username = os.environ.get("MODULE_USER")
password = os.environ.get("MODULE_PASS")

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

def main():
    print(f"""
{CYAN}{BOLD}┌───────────────────────────────────────────────────────────────┐
│     CONEXIONES ACTIVAS Y PUERTOS ABIERTOS (MÓDULO 13) 🔥           │
│     'netstat -antpx' ordenado por criticidad                     │
└───────────────────────────────────────────────────────────────────┘{RESET}
""")

    output = run_cmd(["netstat", "-antpx"])
    if not output:
        print(f"{RED}[CRÍTICO]{RESET} No se pudo ejecutar netstat.")
        return

    lines = output.strip().split("\n")

    normal = []
    warnings = []
    critical = []

    for line in lines:
        l = line.lower()
        # CRÍTICOS → Servicio escuchando públicamente
        if "0.0.0.0:" in l or ":::" in l:
            critical.append(line)
        # ADVERTENCIAS → conexiones ESTABLISHED
        elif "established" in l:
            warnings.append(line)
        else:
            normal.append(line)

    # ===== SALIDA =====
    print_section("Conexiones normales detectadas", "\n".join(normal), WHITE)
    print_section("Advertencias (conexiones establecidas)", "\n".join(warnings), YELLOW)
    print_section("CRÍTICOS (servicios escuchando públicamente)", "\n".join(critical), RED)

    print(f"{GREEN}{BOLD}[✓] Análisis completado (Módulo 13){RESET}\n")


if __name__ == "__main__":
    main()
