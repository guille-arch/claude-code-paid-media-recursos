---
name: copies-ads
description: Use when the user wants ad copy for Google Ads and/or Meta Ads generated from a website URL ("crea los copies para esta URL", "redacta anuncios para esta landing", "titulares y descripciones para Google Ads de este sitio", "copy para Meta a partir de esta web", "genera el RSA de esta página"). Lee la URL con un script determinista (sin coste, sin API key), Claude redacta en sesión siguiendo reglas fijas (RSA 15 titulares + 4 descripciones con estructura 15/3/3; Meta por ángulos con texto principal, titular y descripción), valida límites de caracteres con scripts/validate_copy.py y exporta JSON + CSV listos para Google Ads Editor y Meta. Español de España por defecto. NO crea campañas (para eso, google-search-campaign) ni genera imágenes.
---

# Copies para Google Ads y Meta Ads a partir de una URL

Genera el set completo de textos de anuncio de un anunciante leyendo su web: un anuncio adaptable de Búsqueda (RSA) por categoría y 3-5 ángulos de Meta con sus variantes. Sin API key: el script solo lee la página; la redacción la haces tú (Claude) en esta sesión; el validador comprueba límites y exporta.

## Reglas fijas (no negociables)

- **Español de España por defecto** (tú, "apúntate", "coge", "reserva tu plaza"). Si el sitio es claramente de otro mercado (dominio .mx/.ar/.co/.cl/.pe, precios en otra moneda, "usted" dominante), usar español neutro sin voseo y decirlo en la entrega. Nunca voseo.
- **Solo datos verificables en la web**: precios, plazos, garantías, cifras y certificaciones se copian del sitio o no se usan. Nada de "el mejor", "n.º 1", "garantizado" sin prueba visible. Nunca "de por vida".
- **Límites duros:** titulares RSA ≤ 30 caracteres, descripciones ≤ 90, sitelinks ≤ 25 (+ 2 descripciones ≤ 35), callouts ≤ 25. Meta: titular ≤ 40, descripción ≤ 30, texto principal recomendado ≤ 125 (máx. 3 variantes por ángulo). Sin comillas dobles, sin signos de exclamación repetidos, sin MAYÚSCULAS completas (salvo siglas), sin "haz clic aquí".
- **Políticas:** categorías sensibles (salud, finanzas, empleo, vivienda, apuestas) exigen copy sin atributos personales ("¿Tienes ansiedad?" no; "Atención psicológica online" sí). Si detectas una de estas verticales, avísalo en la entrega.
- **Cadena de alineación:** cada RSA apunta a la URL de su categoría (no a la home) y la keyword principal de la categoría aparece en al menos 2 titulares.
- **Prohibido inventar el negocio:** si la web no deja claro qué vende, a quién y dónde, pregunta antes de redactar.

## Flujo

### 1. Leer la URL (gratis, sin tokens de API)
```bash
python .claude/skills/copies-ads/scripts/site_signals.py https://www.ejemplo.com > /tmp/signals.json
```
Devuelve título, meta description, OG, encabezados, textos de botones/CTAs, extracto del cuerpo y paleta. Léelo y decide:
- **Modelo:** ecommerce (catálogo, carrito, precios por producto) o captación de leads (formulario, teléfono, WhatsApp, presupuesto, reserva).
- **Categorías:** 1 a 4 (un RSA por categoría: servicio, línea de producto o landing). Si la URL es una sola landing, una categoría.
- **Mercado e idioma:** España por defecto (ver reglas).
- Si hay varias páginas de categoría con URL propia, pásalas también por el script.

### 2. Elegir ángulos (3 a 5) con `references/reglas-copy.md`
Beneficio, dolor, prueba social, oferta, cómo funciona, comparación, objeción, autoridad. Cada ángulo de Meta tiene que poder leerse sin el resto; sin repetir la misma promesa con otras palabras.

### 3. Redactar (tú, en sesión)
Por categoría, un **RSA**:
- 15 titulares ≤30 con estructura **15/3/3**: 5 de relevancia (keyword y variantes), 5 de propuesta de valor (beneficio, diferencial, cifra), 5 de acción/urgencia (CTA, oferta, prueba social). Sin dos titulares con el mismo mensaje.
- 4 descripciones ≤90: beneficio + diferencial + CTA; al menos una con cifra o prueba concreta del sitio.
- `pin_suggestion`: como mucho 1 titular pineado a posición 1 (marca o nombre exacto de la categoría) si hace falta consistencia; por defecto ninguno.
- Recursos opcionales: 4 sitelinks (texto ≤25 + 2 descripciones ≤35 + URL), 4 callouts ≤25.

Por ángulo, un bloque de **Meta**:
- `primary_text`: 1-3 variantes, gancho en la primera línea, ≤125 caracteres recomendado (si te pasas, que lo importante quede antes del "ver más" ≈ 125).
- `headline` ≤40, `description` ≤30, `cta` sugerido del catálogo de Meta (Más información, Registrarte, Comprar, Reservar, Contactarnos, Descargar…).

### 4. Guardar y validar
Escribe el JSON con el esquema de `references/ejemplo-salida.json` en `reports/copies_<marca>_<fecha>.json` y ejecuta:
```bash
python .claude/skills/copies-ads/scripts/validate_copy.py reports/copies_<marca>_<fecha>.json --csv
```
El validador imprime un informe (longitud por línea, duplicados, comillas, mayúsculas, cobertura 15/3/3, keyword en ≥2 titulares) y con `--csv` exporta `..._google.csv` (formato de importación de Google Ads Editor: una fila por RSA con Headline 1..15 y Description 1..4) y `..._meta.csv` (una fila por variante: ángulo, texto principal, titular, descripción, CTA). **Si hay errores, corrige el JSON y vuelve a validar**; no entregues con errores.

### 5. Entregar
Resumen al usuario: modelo detectado, categorías, ángulos, tabla de titulares y descripciones por RSA, variantes de Meta, avisos (vertical sensible, datos que no pudiste verificar, idioma elegido) y rutas de los archivos. Ofrecer: ajustar tono, añadir una categoría, o crear la campaña con `/google-search-campaign`.

## Qué no hacer
- No escribir el validador ni el lector de URL "a mano": usar siempre los dos scripts.
- No llamar a ninguna API de pago (Anthropic, OpenAI, Gemini): la redacción es tuya, en sesión.
- No crear campañas ni subir nada a Google Ads o Meta desde esta skill.
- No incluir datos de terceros ni de otros clientes en los ejemplos.

## Protocolo de auto-mejora (obligatorio al cerrar cada corrida)
Al terminar, si (1) el usuario corrigió el output o el criterio, (2) un paso de este SKILL.md resultó desactualizado, o (3) hizo falta un workaround no documentado, **edita este SKILL.md en el momento**: la corrección va como regla permanente en la sección del flujo donde aplica, con ediciones mínimas, sin métricas ni datos de clientes. Los quirks genéricos de entorno (librerías, sitios que bloquean el scraping) van a `learnings.md`, no aquí.
