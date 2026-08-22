# Skill "copies-ads" para Claude Code

Genera los textos de anuncio de Google Ads (RSA: 15 titulares + 4 descripciones) y de Meta Ads (3-5 ángulos con texto principal, titular y descripción) a partir de la URL de cualquier web, los valida contra los límites de cada plataforma y los exporta en CSV listos para Google Ads Editor y Meta. Español de España por defecto. No necesita ninguna API key: el script solo lee la página y Claude redacta dentro de tu sesión.

## Instalación en 3 pasos

1. **Descomprime** este zip y copia la carpeta `copies-ads` dentro de la carpeta `.claude/skills/` de tu workspace de Claude Code (si no existe, créala). Debe quedar así:
   ```
   tu-workspace/
   └── .claude/
       └── skills/
           └── copies-ads/
               ├── SKILL.md
               ├── scripts/
               └── references/
   ```
2. **Instala las dos librerías** que usa el lector de URLs (una sola vez, en la terminal, dentro de tu workspace):
   ```
   pip install requests beautifulsoup4
   ```
3. **Abre Claude Code en tu workspace** y pídeselo en lenguaje natural:
   > Crea los copies de Google Ads y Meta para https://www.tu-cliente.com

Claude leerá la web, te propondrá categorías y ángulos, redactará, validará y te dejará los archivos en `reports/`. Si quieres otro tono o mercado, díselo ("en español neutro", "más directo", "solo Meta").

## También en claude.ai (versión de navegador)

- **Claude Code en la web (claude.ai/code):** pon la carpeta `copies-ads` en `.claude/skills/` de tu repositorio de GitHub, abre ese repo desde claude.ai/code y pídeselo igual que en local.
- **Chat de claude.ai:** en planes con "Skills" disponible, ve a Configuración → Capacidades → Skills → "Subir skill" y sube el archivo `copies-ads-claude-ai.zip` (el zip que contiene solo la carpeta `copies-ads`). Activa también "Ejecución de código". En claude.ai el lector de URLs no tiene internet dentro del sandbox, así que Claude leerá la web con su herramienta de navegación y después validará y exportará con los mismos scripts. Si algo falla, pega el texto de la página y sigue igual.

## Qué obtienes

- `reports/copies_<marca>_<fecha>.json`: el set completo.
- `reports/copies_<marca>_<fecha>_google.csv`: una fila por anuncio adaptable, con Headline 1..15 y Description 1..4, importable en Google Ads Editor.
- `reports/copies_<marca>_<fecha>_meta.csv`: una fila por variante de Meta (ángulo, texto principal, titular, descripción, CTA).
- En pantalla: informe de validación (longitudes, duplicados, estructura 15/3/3, keyword en titulares).

## Notas

- Si una web bloquea el acceso automático (403), Claude te pedirá que pegues el texto de la página y seguirá el mismo flujo.
- La skill no crea campañas ni sube nada a las plataformas; solo redacta, valida y exporta.
- Es la misma pieza que usamos en la agencia; la compartimos con los registrados al webinar "Claude Code para Paid Media" de AdData Academy.

AdData Academy · addata.academy
