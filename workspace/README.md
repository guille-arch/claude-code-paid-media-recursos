# Archivos del workspace del curso "Claude Code para Paid Media"

Esta carpeta tiene la versión vigente de los scripts del workspace del curso que las lecciones le piden a Claude Code descargar cuando tu workspace es de una versión anterior. Las rutas son las mismas que dentro de tu workspace.

| Archivo | Qué hace |
|---|---|
| `scripts/setup/save_env_var.py` | Guarda cada credencial como variable de entorno de tu usuario, en Mac, Windows y Linux. En Windows no necesita permisos de administrador. Nunca muestra los valores. `--check` dice qué variables existen y `--run` ejecuta un script con las variables recién guardadas. |
| `scripts/setup/get_meta_long_lived_token.py` | Convierte el token corto de Meta en uno de larga duración. Toma el App ID y el App Secret de las variables de entorno y funciona en la consola de Windows. |

No hace falta descargarlos a mano: los prompts de las lecciones le indican a Claude Code de dónde bajarlos y que los lea antes de usarlos. Versión: 5.8 (13 de octubre de 2026). El historial completo está en `NOVEDADES.md` dentro del workspace.
