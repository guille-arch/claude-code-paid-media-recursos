# Recursos del webinar "De media buyer saturado a gestor con sistemas: cómo Claude Code multiplica tu capacidad en PPC" · AdData Academy

Tres recursos para los registrados al webinar del **martes 8 de septiembre, 19:00 hora peninsular**.

| Recurso | Qué es | Enlace |
|---|---|---|
| 📘 Guía **"Las 10 tareas de PPC que puedes automatizar hoy"** | PDF de 13 páginas: una ficha por tarea (qué hace la skill, tiempo a mano frente a con la skill, el prompt exacto, qué devuelve, la trampa que evita). | [Descargar PDF](https://github.com/guille-arch/claude-code-paid-media-recursos/releases/latest/download/Guia-10-tareas-PPC-AdData.pdf) |
| 🧮 **Calculadora de horas y euros** | Cuántas horas recuperas al mes automatizando la operativa, cuánto valen y a cuántas cuentas más podrías llegar. | [Abrir calculadora](https://claude.ai/code/artifact/f28d3874-ea37-4df3-892e-48492130eca7) |
| ✍️ **Skill "copies-ads"** para Claude Code | Genera los textos de anuncio de Google Ads (RSA) y Meta a partir de una URL, los valida y los exporta en CSV. Sin API key. | [Descargar ZIP para Claude Code](https://github.com/guille-arch/claude-code-paid-media-recursos/releases/latest/download/skill-copies-ads.zip) · [ZIP para subir a claude.ai](https://github.com/guille-arch/claude-code-paid-media-recursos/releases/latest/download/copies-ads-claude-ai.zip) · [Ver el código](skill-copies-ads/) |

## Cómo instalar la skill en 3 pasos

1. Descarga el ZIP y copia la carpeta `copies-ads` dentro de `.claude/skills/` de tu workspace de Claude Code (créala si no existe).
2. En la terminal, dentro del workspace: `pip install requests beautifulsoup4`
3. Abre Claude Code y pídeselo: *"Crea los copies de Google Ads y Meta para https://www.tu-cliente.com"*

## ¿Y en la versión de navegador de Claude?

- **Claude Code en la web (claude.ai/code):** sube la carpeta `copies-ads` a `.claude/skills/` de tu repositorio de GitHub y abre ese repo desde claude.ai/code. Funciona igual que en local.
- **Chat de claude.ai:** en los planes que tienen "Skills", ve a Configuración → Capacidades → Skills → "Subir skill" y sube [copies-ads-claude-ai.zip](https://github.com/guille-arch/claude-code-paid-media-recursos/releases/latest/download/copies-ads-claude-ai.zip) (solo la carpeta de la skill). Activa también "Ejecución de código". Ahí el sandbox no tiene internet, así que Claude lee la web con su navegación y luego valida y exporta con los mismos scripts.

Detalle completo en [skill-copies-ads/INSTALACION.md](skill-copies-ads/INSTALACION.md).

---
Guillermo Pareja · AdData Academy · Google Premier Partner · [addata.academy](https://www.addata.academy)
