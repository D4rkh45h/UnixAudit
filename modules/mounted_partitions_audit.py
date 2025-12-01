#!/usr/bin/env python3
import subprocess
import re
import os
import sys

# ============================
#   LECTURA DE CREDENCIALES
# ============================
username = os.environ.get("MODULE_USER")
password = os.environ.get("MODULE_PASS")

def run_cmd(cmd):
    """
    Ejecuta comandos.
    - Si hay credenciales → usa sudo -S.
    - Si no → ejecuta normal.
    """
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
        print(f"[CRÍTICO] Error ejecutando {' '.join(cmd)} → {e}")
        sys.exit(1)


print("""
┌────────────────────────────────────────────────────────────┐
│     PARTICIONES MONTADAS (MÓDULO 19 UNIVERSAL) 🔥           │
│     Detecta montajes realmente explotables para escalada    │
└────────────────────────────────────────────────────────────┘
""")

# ============================
#   EJECUTAR MOUNT
# ============================
output = run_cmd(["mount"])
lines = output.strip().split("\n")

print("=== PARTICIONES DETECTADAS ===")
for line in lines:
    print(" ", line)

print("\n=== CRÍTICOS (escalada real) ===")

critical = []


def is_rw(options):
    return "rw" in options.split(",")


# ============================
#  ANÁLISIS DE PARTICIONES
# ============================
for line in lines:
    match = re.search(r"on\s+(\S+)\s+type\s+(\S+)\s+\(([^)]*)\)", line)
    if not match:
        continue

    mountpoint = match.group(1)
    fstype = match.group(2).lower()
    options = match.group(3)

    # === /tmp ===
    if mountpoint == "/tmp" and is_rw(options):
        critical.append(line)
        continue

    # === /dev/shm ===
    if mountpoint == "/dev/shm" and is_rw(options):
        critical.append(line)
        continue

    # === NFS / CIFS / SMB ===
    if fstype in ["nfs", "cifs", "smb", "smbfs"] and is_rw(options):
        critical.append(line)
        continue

    # === FUSE ===
    if fstype.startswith("fuse") and is_rw(options):
        critical.append(line)
        continue

    # === OverlayFS / AUFS ===
    if fstype in ["overlay", "aufs"] and is_rw(options):
        critical.append(line)
        continue

    # === Bind mounts ===
    if "bind" in options and is_rw(options):
        critical.append(line)
        continue


# ============================
#  RESULTADO FINAL
# ============================
if critical:
    for c in critical:
        print("  \033[91m" + c + "\033[0m")
else:
    print("  No se detectaron montajes peligrosos.")

print("\n[✓] Análisis completado (Módulo 19 Universal Mejorado)")
