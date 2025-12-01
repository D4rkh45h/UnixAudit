#!/usr/bin/env python3
import os
import subprocess

# ================================
# Colores y estilos universales
# ================================
RED    = "\033[91m"
YEL    = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"
GREEN  = "\033[92m"
WHITE  = "\033[97m"

# =====================================================
# Cabecera visual
# =====================================================
print(f"""
{CYAN}{BOLD}┌──────────────────────────────────────────────────────────┐
│  BÚSQUEDA DE COMPILADORES (MÓDULO 17 UNIVERSAL) 🔥           │
│  Localiza gcc, clang, tcc y otros — útil para exploits locales │
└──────────────────────────────────────────────────────────┘{RESET}
""")

# =====================================================
# Compiladores relevantes
# =====================================================
COMPILERS = ["gcc", "g++", "clang", "clang++", "cc", "tcc", "musl-gcc"]

found = []
critical = []

def search_compiler(name):
    try:
        out = subprocess.check_output(
            ["find", "/", "-type", "f", "-name", name+"*"],
            stderr=subprocess.DEVNULL,
            text=True
        )
        paths = [x for x in out.split("\n") if x.strip() != ""]
        return paths
    except:
        return []

# =====================================================
# Búsqueda y clasificación
# =====================================================
for comp in COMPILERS:
    paths = search_compiler(comp)
    for p in paths:
        found.append((comp, p))
        # Si está en /usr/bin o /bin → crítico
        if p.startswith("/usr/bin") or p.startswith("/bin"):
            critical.append(p)

# =====================================================
# Salida ordenada
# =====================================================
print(f"{CYAN}{BOLD}=== COMPILADORES ENCONTRADOS ==={RESET}")
if not found:
    print("  No se encontraron compiladores.")
else:
    for comp, path in found:
        print(f"{YEL}[{comp}]{RESET} → {path}")

print(f"\n{RED}{BOLD}=== COMPILADORES CRÍTICOS (ABAJO DEL TODO) ==={RESET}")
if not critical:
    print("  No se encontraron compiladores críticos.")
else:
    for c in critical:
        print(f"{RED}[CRÍTICO] {c}{RESET}")

print(f"\n{CYAN}{BOLD}[✓] Análisis completado (Módulo 17 Universal){RESET}\n")
