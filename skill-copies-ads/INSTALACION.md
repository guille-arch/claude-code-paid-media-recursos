# Skill "copies-ads" para Claude Code

Genera los textos de anuncio de Google Ads (RSA: 15 titulares + 4 descripciones) y de Meta Ads (3-5 ángulos con texto principal, titular y descripción) a partir de la URL de cualquier web, los valida contra los límites de cada plataforma y los exporta en CSV listos para Google Ads Editor y Meta. Español de España por defecto. No necesita ninguna API key: el script solo lee la página y Claude redacta dentro de tu sesión.

## Instalación en Claude (claude.ai, versión de navegador)

1. Descarga **skill-copies-ads.zip** de la página de la release y no lo descomprimas.
2. En claude.ai ve a **Configuración → Capacidades**: activa "Ejecución de código y archivos" y "Skills" (planes Pro, Max, Team y Enterprise). En Skills, pulsa **"Subir skill"** y elige el zip.
3. Abre una conversación nueva y pídeselo en lenguaje natural:
   > Crea los copies de Google Ads y Meta para https://www.tu-cliente.com

Claude leerá la web, te propondrá categorías y ángulos, redactará, validará y te dará el JSON y los dos CSV para descargar. Si quieres otro tono o mercado, díselo ("en español neutro", "más directo", "solo Meta").

## Instalación en Claude Code (terminal o claude.ai/code)

1. Descomprime el zip y copia la carpeta `copies-ads` dentro de `.claude/skills/` de tu workspace (créala si no existe).
2. En la terminal, dentro del workspace: `pip install requests beautifulsoup4`
3. Abre Claude Code y pídeselo igual que arriba. Los archivos quedan en `reports/`.

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
