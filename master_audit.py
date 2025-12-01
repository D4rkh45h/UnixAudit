#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import subprocess
import getpass
import os
import sys
import time
import datetime

# ============================================================
# CONFIGURACIÓN DE MÓDULOS
# ============================================================

# Ruta relativa a la carpeta "modules" junto al master
MODULE_PATH = os.path.join(os.path.dirname(__file__), "modules")

MODULES = {
    2: "apache_audit.py",
    3: "arp_audit.py",
    4: "authlog_audit.py",
    5: "bash_history_audit.py",
    6: "cron_root.py",
    7: "cron_system.py",
    8: "compiladores_audit.py",
    9: "kernel_info.py",
    10: "distro_info.py",
    11: "login_history_audit.py",
    12: "netstat_audit.py",
    13: "password_finder.py",
    14: "root_processes.py",
    15: "services_info.py",
    16: "ssh_keys_audit.py",
    17: "ssh_audit.py",
    18: "suid_enum.py",
    19: "suid_sgid_enum.py",
    20: "mounted_partitions_audit.py",
    21: "printer_info.py",
    22: "shadow_audit.py",
    23: "startup_services.py",
    24: "world_writable.py",
    25: "download_tools_audit.py",
}

CATEGORIES = {
    26: [18, 19, 13, 22, 24, 14, 6, 25],         # Escalada de privilegios
    27: [12, 3, 17, 16],                         # Red
    28: [15, 23, 20, 21, 2],                     # Servicios
    29: [5, 11, 4],                              # Actividad usuario
    30: [13, 22, 16, 17],                        # Credenciales
}

# ============================================================
# FUNCIONES DE UTILIDAD
# ============================================================

def clear_screen():
    os.system("clear" if os.name != "nt" else "cls")

def timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def write_log(logfile, text):
    if logfile:
        with open(logfile, "a", encoding="utf8") as f:
            f.write(text + "\n")

def pause(args):
    if not args.no_pause:
        input("\nPresiona ENTER para continuar...")

def header(text):
    print("\n" + "─" * 70)
    print(f"🔍 {text}")
    print("─" * 70)

def footer():
    print("─" * 70 + "\n")

def check_module_exists(module_filename):
    """Comprueba si el módulo existe dentro de la carpeta modules."""
    module_path = os.path.join(MODULE_PATH, module_filename)
    return os.path.isfile(module_path)

def check_dependencies():
    missing = []
    for dep in ["python3", "sudo", "grep", "awk"]:
        if subprocess.call(f"which {dep} >/dev/null 2>&1", shell=True) != 0:
            missing.append(dep)
    return missing

# ============================================================
# EJECUCIÓN DE MÓDULOS
# ============================================================

def run_module(module_filename, args, user, password):
    """
    module_filename: nombre de archivo dentro de modules/, p.ej. 'apache_audit.py'
    """

    module_path = os.path.join(MODULE_PATH, module_filename)

    if not os.path.isfile(module_path):
        print(f"[ERROR] El módulo '{module_filename}' no existe en {MODULE_PATH}.")
        return

    if not args.silent:
        header(f"EJECUTANDO MÓDULO: {module_filename} ({timestamp()})")

    cmd = ["python3", module_path]

    if user:
        cmd += ["--user", user]
    if password:
        cmd += ["--password", password]

    if args.silent:
        cmd.append("--silent")

    if args.json:
        cmd.append("--json")

    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        text = output.decode(errors="ignore")
        if not args.silent:
            print(text)
    except subprocess.CalledProcessError as e:
        text = e.output.decode(errors="ignore")
        if not args.silent:
            print(text)
    except Exception as e:
        text = f"[ERROR] No se pudo ejecutar {module_filename}: {str(e)}"
        if not args.silent:
            print(text)

    if args.log:
        write_log(args.log, f"\n===== {module_filename} :: {timestamp()} =====\n{text}\n")

    if not args.silent:
        footer()

def execute_module_list(module_ids, args, user, password):
    for module_id in module_ids:
        if module_id not in MODULES:
            print(f"[ERROR] ID de módulo desconocido: {module_id}")
            continue
        module_file = MODULES[module_id]
        run_module(module_file, args, user, password)
        pause(args)

# ============================================================
# MENÚ PRINCIPAL
# ============================================================

def show_menu():
    clear_screen()
    print("""
 ┌──────────────────────────────────────────────────────────┐
 │   UNIVERSAL UNIX PRIVILEGE ESCALATION SUITE 🔥           │
 │                 Master Auditor Menu                       │
 └──────────────────────────────────────────────────────────┘

 Modo 1 – Ejecutar TODOS los módulos
  1) Auditoría completa (todos los módulos)

 Modo 2 – Ejecutar módulos individuales:
""")

    for num, mod in MODULES.items():
        print(f"  {num}) Ejecutar {mod}")

    print(f"""
 Modo 3 – Ejecutar por categorías:
  26) Módulos de escalada de privilegios
  27) Módulos de red
  28) Módulos de servicios
  29) Módulos de actividad del usuario
  30) Módulos de credenciales

 Extras:
  80) Introducir credenciales para módulos
  90) Previsualizar todos los módulos
  91) Previsualizar por categorías

 Modo 4 – Salir
  0) Salir
""")

# ============================================================
# MAIN
# ============================================================

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--silent", action="store_true")
    parser.add_argument("--json", action="store_true")

    parser.add_argument("--user", type=str, default=None)
    parser.add_argument("--password", type=str, default=None)

    parser.add_argument("--scan-quick", action="store_true")
    parser.add_argument("--scan-deep", action="store_true")
    parser.add_argument("--check-sudo", action="store_true")
    parser.add_argument("--log", type=str)
    parser.add_argument("--no-pause", action="store_true")

    args = parser.parse_args()

    user = args.user
    password = args.password

    # Dependencias
    missing = check_dependencies()
    if missing and not args.silent:
        print("⚠ Dependencias faltantes:", ", ".join(missing))
        print("Instálalas para obtener mejores resultados.\n")

    # sudo -l
    if args.check_sudo:
        header("EJECUTANDO sudo -l")
        os.system("sudo -l")
        footer()
        pause(args)

    # Scan rápido
    if args.scan_quick:
        quick_modules = [18, 19, 13, 24, 14, 22]
        execute_module_list(quick_modules, args, user, password)
        return

    # Scan profundo
    if args.scan_deep:
        execute_module_list(list(MODULES.keys()), args, user, password)
        return

    # Interactivo
    while True:
        show_menu()
        choice = input("Selecciona una opción: ")

        try:
            choice = int(choice)
        except:
            print("[ERROR] Opción inválida.")
            pause(args)
            continue

        if choice == 0:
            print("Saliendo...")
            sys.exit(0)

        elif choice == 1:
            execute_module_list(list(MODULES.keys()), args, user, password)

        elif choice == 80:
            print("\n🔐 Introducir credenciales para módulos")
            user = input("Usuario: ").strip()
            password = getpass.getpass("Contraseña: ").strip()

            os.environ["AUDIT_USER"] = user
            os.environ["AUDIT_PASS"] = password

            print(f"\n✓ Credenciales cargadas correctamente ({user})\n")
            pause(args)

        elif choice == 90:
            header("Listado de módulos disponibles")
            for n, f in MODULES.items():
                print(f" {n} → {f}")
            footer()
            pause(args)

        elif choice == 91:
            header("Listado de categorías")
            for cat, mods in CATEGORIES.items():
                print(f"\nCategoría {cat}:")
                for m in mods:
                    print(f" - {m}: {MODULES[m]}")
            footer()
            pause(args)

        elif choice in MODULES:
            run_module(MODULES[choice], args, user, password)
            pause(args)

        elif choice in CATEGORIES:
            execute_module_list(CATEGORIES[choice], args, user, password)

        else:
            print("[ERROR] Opción desconocida.")
            pause(args)

if __name__ == "__main__":
    main()
