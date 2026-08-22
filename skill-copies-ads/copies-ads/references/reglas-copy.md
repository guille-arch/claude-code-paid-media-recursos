# Reglas de copy para Google Ads (RSA) y Meta Ads

Guía de redacción que aplica la skill `copies-ads`. Está pensada para que el copy salga a la primera con los límites de cada plataforma y con un nivel de persuasión de agencia, no de plantilla.

## 1. Antes de escribir: qué tiene que quedar claro del sitio

Del JSON de `site_signals.py` saca y anota (si algo falta, pregunta):
- **Qué vende** (producto/servicio y categorías) y **a quién** (B2C/B2B, perfil).
- **Dónde** (país, ciudad, online/presencial) y **en qué idioma habla la web**.
- **Modelo:** ecommerce (precios, carrito, envíos) o captación de leads (formulario, teléfono, WhatsApp, reserva, presupuesto).
- **Pruebas concretas** que ya muestra el sitio: años, clientes, reseñas, certificaciones, garantías, plazos de envío, precios desde, horario, financiación.
- **La oferta** si la hay (descuento, prueba gratis, primera consulta gratis, envío gratis) y su condición/fecha.
- **El CTA natural** del sitio (reservar, pedir presupuesto, comprar, apuntarse, llamar).

## 2. Ángulos (elige 3 a 5 para Meta; los RSA los mezclan todos)

| Ángulo | Qué hace | Cuándo funciona mejor |
|---|---|---|
| Beneficio | Abre con el resultado, no con la característica | Casi siempre; ideal para titulares de valor |
| Dolor | Nombra el problema que el usuario ya siente | Tráfico frío, servicios |
| Prueba social | Cifras, reseñas, clientes, años | Retargeting y categorías de confianza |
| Oferta | Incentivo concreto + condición | Ecommerce, lead magnets, promociones |
| Cómo funciona | Quita fricción explicando 2-3 pasos | Lead gen, servicios, SaaS |
| Comparación | Antes/después, manera antigua vs nueva | Compras meditadas, cambio de proveedor |
| Objeción | Responde a la duda que frena ("sin permanencia", "sin programar") | Cuando el sitio la resuelve explícitamente |
| Autoridad | Especialización, certificaciones, método propio | Servicios profesionales, B2B |

Regla: dos ángulos no pueden decir lo mismo con otras palabras. Si al leer dos textos principales seguidos suenan iguales, uno sobra.

## 3. Google Ads: anuncio adaptable de Búsqueda (RSA)

**Límites:** 15 titulares ≤ 30 caracteres, 4 descripciones ≤ 90, rutas (path) ≤ 15 cada una. Sin comillas dobles, sin signos repetidos, sin mayúsculas completas, sin "haz clic aquí".

**Estructura 15/3/3 de los titulares (5 por grupo):**
- **Relevancia (5):** la keyword principal y sus variantes tal cual busca la gente ("Clínica dental en Madrid", "Implantes dentales Madrid", "Dentista urgencias Madrid"). Es lo que hace que el anuncio parezca la respuesta exacta.
- **Propuesta de valor (5):** beneficio, diferencial, cifra, prueba ("Primera visita gratis", "20 años de experiencia", "Financiación sin intereses", "Resultados en 24 h").
- **Acción / urgencia (5):** CTA y empuje ("Pide cita hoy", "Reserva tu plaza", "Presupuesto en 24 h", "Plazas limitadas", "Compra con envío gratis").

**Descripciones (4):** cada una completa por sí sola: beneficio + diferencial + CTA. Una con cifra o prueba concreta; una que responda a la objeción principal; una orientada a la oferta si existe; una genérica de marca.

**Pinning:** por defecto ninguno. Como mucho 1 titular pineado a la posición 1 (marca o nombre exacto de la categoría) cuando haga falta que siempre aparezca.

**Recursos (opcionales, recomendados):** 4 sitelinks (texto ≤ 25 + 2 descripciones ≤ 35 + URL propia), 4 callouts ≤ 25 ("Envío en 24 h", "Sin permanencia", "Atención en español"), rutas con la categoría ("/implantes", "/madrid").

**Cadena de alineación:** la URL final de cada RSA es la página de su categoría. Si el sitio no tiene página propia para una categoría, no inventes el RSA: díselo al usuario.

## 4. Meta Ads (Facebook e Instagram)

**Límites de lectura:** texto principal recomendado ≤ 125 caracteres antes del "ver más" (si es más largo, lo importante va en las dos primeras líneas); titular ≤ 40; descripción ≤ 30. Hasta 3 variantes de texto principal por ángulo.

**Anatomía de cada variante:**
1. **Gancho** en la primera línea: pregunta, dato, afirmación contraintuitiva o el dolor con nombre.
2. **Promesa concreta** en la segunda (qué consigue y en cuánto tiempo o a qué coste), con la prueba del sitio si la hay.
3. **CTA** con el botón de Meta sugerido (Más información, Registrarte, Comprar, Reservar, Contactarnos, Descargar, Solicitar presupuesto, Enviar mensaje de WhatsApp) y, si procede, el empuje (plazas, fecha, oferta).

**Titular:** la promesa en 3-6 palabras. **Descripción:** la prueba, la oferta o la condición ("Primera consulta gratis", "Envío en 24 h").

**Políticas:** en salud, finanzas, empleo, vivienda, citas o apuestas, no atribuir nada al lector ("¿Tienes deudas?" no; "Reunificación de deudas con asesoría" sí). Sin antes/después corporales, sin promesas de resultados garantizados, sin "ganar dinero fácil".

## 5. Tono e idioma

- **Español de España por defecto:** tuteo, "apúntate", "reserva tu plaza", "coge", "vale", "coche", "móvil". Si el sitio es de otro mercado, español neutro (tuteo sin regionalismos, nunca voseo) y se indica en la entrega.
- Frases cortas, verbos en activo, cifras en dígitos, sin adjetivos vacíos ("increíble", "único", "el mejor").
- Nada que la web no respalde. Si una cifra no aparece en el sitio, no la pongas; propón al usuario que la confirme.
- Sin guiones largos; usa puntos, comas, dos puntos o paréntesis.

## 6. Checklist antes de validar

- [ ] 15 titulares (5+5+5), 4 descripciones, ninguno repetido en mensaje.
- [ ] Keyword principal en ≥ 2 titulares.
- [ ] URL final de categoría, rutas coherentes.
- [ ] 3-5 ángulos de Meta distintos entre sí, 1-3 variantes por ángulo, titular y descripción en cada uno.
- [ ] Todas las cifras y promesas salen del sitio.
- [ ] Vertical sensible señalada y copy adaptado.
- [ ] `validate_copy.py` sin errores; CSV exportados.
