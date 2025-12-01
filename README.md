<div align="center">
  <div style="display: inline-flex; align-items: center; gap: 8px; margin-bottom: 25px; padding-top: 10px;">
    <a href="README.md" style="text-decoration: none; display: inline-flex; align-items: center; gap: 8px; margin-right: 8px;" title="Español">
      <img src="https://flagpedia.net/data/flags/w1600/es.png" alt="Español" width="36" style="vertical-align: middle;">
      <span style="color: white; font-size: 18px; font-weight: 600; font-family: sans-serif;">  Español</span>
    </a>
    <span style="color: grey; font-size: 18px; font-family: sans-serif; margin-right: 8px;">|</span>
    <a href="README.en.md" style="text-decoration: none; display: inline-flex; align-items: center; gap: 8px;" title="English">
      <img src="https://flagpedia.net/data/flags/w1600/us.png" alt="English" width="36" style="vertical-align: middle;">
      <span style="color: deepskyblue; font-size: 18px; font-family: sans-serif; text-decoration: underline;">  English</span>
    </a>
  </div>
</div>

# UNIXAUDIT 🔥🛡️

![Logo de UNIXAUDIT](/unixaudit_logo.png)

**UNIXAUDIT** es una herramienta de auditoría automática para sistemas Unix/Linux.  
Su objetivo es **detectar configuraciones inseguras, recopilar información del sistema y ejecutar módulos de análisis**, todo desde un **menú centralizado**, con posibilidad de usar *credenciales personalizadas* para módulos que lo requieran.

<h2 align="center">Demostración</h2>

<p align="center">
  Aquí puedes ver la herramienta en acción a través de GIFs y capturas de pantalla.
</p>

### GIF de UNIXAUDIT en funcionamiento

<p align="center">
  <img src="URL_DEL_GIF_AQUI" alt="Demostración en GIF" style="max-width: 100%; height: auto; display: block; margin: 0 auto;">
  <em>Demostración rápida mostrando el menú principal y la ejecución de módulos.</em>
</p>

### Capturas de Pantalla

<p align="center">
  <img src="URL_CAPTURA_1" alt="Captura 1" style="max-width: 100%; height: auto; display: block; margin: 0 auto;">
  <em>Vista del menú principal del master_audit.py.</em>
</p>

<p align="center">
  <img src="URL_CAPTURA_2" alt="Captura 2" style="max-width: 100%; height: auto; display: block; margin: 0 auto;">
  <em>Ejemplo de un módulo ejecutándose con credenciales.</em>
</p>

<p align="center">
  <img src="URL_CAPTURA_3" alt="Captura 3" style="max-width: 100%; height: auto; display: block; margin: 0 auto;">
  <em>Salida de un análisis de auditoría del sistema.</em>
</p>

---

## Características

* 🔥 **Ejecución centralizada mediante `master_audit.py`**
* 🔐 **Soporte para usuario y contraseña opcionales** (si el módulo lo requiere)
* 🧩 **Sistema modular:** cada análisis es un archivo independiente dentro de `/modules`
* 🛠️ **Automatiza auditorías comunes de seguridad en Linux**
* 📄 **Resultados claros en pantalla**
* ⚡ **Compatible con cualquier distribución Unix/Linux**
* 🎨 **Interfaz CLI con colores para mayor claridad**

---

## Estructura del Proyecto

```bash
UnixAudit/
├── master_audit.py # Script principal que gestiona el menú y las credenciales
├── run.sh # Script para ejecutar rápidamente la herramienta
├── modules/ # Módulos de auditoría independientes
│ ├── apache_audit.py
│ ├── ssh_audit.py
│ ├── cron_root.py
│ ├── passwords_finder.py
│ └── ...
└── README.md # Este archivo
```
---

## Documentación Adicional

Aquí encontrarás información más detallada sobre el proyecto:

*   🤝 [**Código de Conducta**](.github/CODIGO_DE_CONDUCTA.md) - Normas para una comunidad respetuosa.
*   📬 [**Cómo Contribuir**](.github/COMO_CONTRIBUIR.md) - Pasos para colaborar con el proyecto.
*   🔐 [**Seguridad**](.github/SEGURIDAD.md) - Información sobre cómo reportar vulnerabilidades.
*   ⚠️ [**Aviso Legal**](.github/AVISO_LEGAL.md) - Cláusulas y advertencias legales importantes.
*   📢 [**Soporte**](.github/SOPORTE.md) - Dónde obtener ayuda o hacer preguntas.

---

## Uso

Explica cómo se utiliza tu herramienta. Proporciona ejemplos claros y comandos.

```bash
# Dar permisos de ejecución al lanzador (solo la primera vez)
chmod +x run.sh

# Ejecutar el lanzador
./run.sh

