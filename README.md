# Recursos del webinar "De media buyer saturado a gestor con sistemas: cómo Claude Code multiplica tu capacidad en PPC" · AdData Academy

Tres recursos para los registrados al webinar del **martes 8 de septiembre, 19:00 hora peninsular**.

| Recurso | Qué es | Enlace |
|---|---|---|
| 📘 Guía **"Las 10 tareas de PPC que puedes automatizar hoy"** | PDF de 13 páginas: una ficha por tarea (qué hace la skill, tiempo a mano frente a con la skill, el prompt exacto, qué devuelve, la trampa que evita). | [Descargar PDF](https://github.com/guille-arch/claude-code-paid-media-recursos/releases/latest/download/Guia-10-tareas-PPC-AdData.pdf) |
| 🧮 **Calculadora de horas y euros** | Cuántas horas recuperas al mes automatizando la operativa, cuánto valen y a cuántas cuentas más podrías llegar. | [Abrir calculadora](https://claude.ai/code/artifact/f28d3874-ea37-4df3-892e-48492130eca7) |
| ✍️ **Skill "copies-ads"** para Claude Code | Genera los textos de anuncio de Google Ads (RSA) y Meta a partir de una URL, los valida y los exporta en CSV. Sin API key. | [Descargar skill-copies-ads.zip](https://github.com/guille-arch/claude-code-paid-media-recursos/releases/latest/download/skill-copies-ads.zip) · [Página de la release con instrucciones](https://github.com/guille-arch/claude-code-paid-media-recursos/releases/latest) · [Ver el código](skill-copies-ads/) |

## Cómo instalar la skill en Claude (claude.ai)

1. Descarga **skill-copies-ads.zip** (no lo descomprimas).
2. En claude.ai: **Configuración → Capacidades** → activa "Ejecución de código y archivos" y "Skills" → en Skills, **"Subir skill"** y elige el zip.
3. Abre una conversación y pídeselo: *"Crea los copies de Google Ads y Meta para https://www.tu-cliente.com"*.

¿Usas Claude Code (terminal o claude.ai/code)? Descomprime el zip, copia la carpeta `copies-ads` en `.claude/skills/` de tu workspace y ejecuta `pip install requests beautifulsoup4`.

Detalle completo en [skill-copies-ads/INSTALACION.md](skill-copies-ads/INSTALACION.md).

---
Guillermo Pareja · AdData Academy · Google Premier Partner · [addata.academy](https://www.addata.academy)
