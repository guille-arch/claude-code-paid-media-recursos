#!/usr/bin/env python3
"""
site_signals.py — Pull raw branding signals from an advertiser URL. NO LLM, NO API cost.

Deterministic extraction only: page title, meta/OG tags, headings, button/CTA text,
a body-text excerpt, the og:image URL, and the brand color palette (hex + rgb mined
from inline styles, <style> blocks and up to two linked stylesheets, ranked by
frequency). Claude (this session, free) reads the JSON this prints and turns it into
the Google Ads + Meta copy set for the copies-ads skill. This script itself calls nothing paid.

    python .claude/skills/copies-ads/scripts/site_signals.py https://www.ejemplo.com
    # -> JSON on stdout

Deps: requests, beautifulsoup4.
"""
from __future__ import annotations

import re
import sys
import json
from collections import Counter
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
HEX_RE = re.compile(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b")
RGB_RE = re.compile(r"rgba?\([0-9.,\s%]+\)")


def _norm_hex(h: str) -> str:
    h = h.lower()
    if len(h) == 4:  # #abc -> #aabbcc
        h = "#" + "".join(c * 2 for c in h[1:])
    return h


def _is_greyish(hex6: str) -> bool:
    try:
        r, g, b = (int(hex6[i:i + 2], 16) for i in (1, 3, 5))
    except ValueError:
        return False
    mx, mn = max(r, g, b), min(r, g, b)
    return (mx - mn) < 18 and (mx > 235 or mn < 20)  # near white/black/grey


def _colors(html: str, base_url: str, session: requests.Session) -> dict:
    counter: Counter = Counter()

    def harvest(text: str):
        for m in HEX_RE.findall(text):
            counter[_norm_hex(m)] += 1
        for m in RGB_RE.findall(text):
            counter[m.lower().replace(" ", "")] += 1

    harvest(html)
    soup = BeautifulSoup(html, "html.parser")
    sheets = [l.get("href") for l in soup.find_all("link", rel="stylesheet") if l.get("href")]
    for href in sheets[:2]:
        try:
            harvest(session.get(urljoin(base_url, href), timeout=8).text)
        except Exception:  # noqa: BLE001
            continue
    ranked = [c for c, _ in counter.most_common(60)]
    brand = [c for c in ranked if c.startswith("#") and not _is_greyish(c)][:12]
    return {"all_ranked": ranked[:24], "brand_candidates": brand}


def get_signals(url: str) -> dict:
    if not urlparse(url).scheme:
        url = "https://" + url
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
                      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"})
    try:
        resp = s.get(url, timeout=20)
        resp.raise_for_status()
    except requests.RequestException as e:
        return {"url": url, "error": f"No se pudo leer la página: {e}",
                "hint": "Si el sitio bloquea el acceso automático (403/429) o tarda demasiado, pide al usuario que pegue el texto visible de la página (título, encabezados, botones, precios) y sigue el flujo con eso."}
    if not resp.encoding or resp.encoding.lower() in ("iso-8859-1", "latin-1"):
        resp.encoding = resp.apparent_encoding or "utf-8"
    html = resp.text
    soup = BeautifulSoup(html, "html.parser")

    def meta(key, attr="property"):
        tag = soup.find("meta", attrs={attr: key})
        return tag.get("content", "").strip() if tag and tag.get("content") else ""

    title = (soup.title.string or "").strip() if soup.title else ""
    headings = [h.get_text(" ", strip=True) for h in soup.find_all(["h1", "h2", "h3"])][:15]
    buttons = list(dict.fromkeys(
        b.get_text(" ", strip=True) for b in soup.find_all(["button", "a"])
        if 2 < len(b.get_text(strip=True)) < 40))[:25]
    colors = _colors(html, url, s)
    for t in soup(["script", "style", "noscript"]):
        t.decompose()
    body = re.sub(r"\s+", " ", soup.get_text(" ", strip=True))[:6000]

    og_image = meta("og:image")
    og_image = urljoin(url, og_image) if og_image else ""

    # Señales de modelo de negocio (lead-gen vs ecommerce) y de contacto
    raw = html.lower()
    hrefs = [a.get("href", "") for a in soup.find_all("a", href=True)]
    tel_links = list(dict.fromkeys(h for h in hrefs if h.startswith("tel:")))[:5]
    wa_links = list(dict.fromkeys(h for h in hrefs if "wa.me" in h or "whatsapp.com" in h or "api.whatsapp" in h))[:5]
    mail_links = list(dict.fromkeys(h for h in hrefs if h.startswith("mailto:")))[:3]
    prices = re.findall(r"(?:\d{1,3}(?:[.\s]\d{3})*(?:,\d{1,2})?\s?(?:€|eur)|(?:€|\$|us\$|mxn|ars|clp|cop|s/)\s?\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{1,2})?)", body, re.I)[:12]
    ecommerce_words = [w for w in ("añadir al carrito", "añadir a la cesta", "comprar ahora", "carrito", "cesta", "checkout", "envío gratis", "envio gratis", "añadir al carro", "agregar al carrito") if w in raw]
    leadgen_words = [w for w in ("presupuesto", "pide cita", "pedir cita", "reserva", "contacta", "contáctanos", "llámanos", "solicita", "consulta gratis", "primera visita", "demo", "cotización", "cotizar") if w in raw]
    forms = len(soup.find_all("form"))
    model_hint = "ecommerce" if (len(ecommerce_words) >= 2 or (prices and ecommerce_words)) else ("lead-gen" if (forms or tel_links or wa_links or leadgen_words) else "indeterminado")

    return {
        "model_hint": model_hint,
        "signals": {"forms": forms, "tel_links": tel_links, "whatsapp_links": wa_links, "mailto": mail_links,
                     "prices_found": prices, "ecommerce_words": ecommerce_words, "leadgen_words": leadgen_words,
                     "lang_attr": (soup.html.get("lang") if soup.html else "") or ""},
        "url": url,
        "title": title,
        "meta_description": meta("description", attr="name"),
        "og_title": meta("og:title"),
        "og_description": meta("og:description"),
        "og_site_name": meta("og:site_name"),
        "theme_color": meta("theme-color", attr="name"),
        "headings": headings,
        "buttons": buttons,
        "palette_brand_candidates": colors["brand_candidates"],
        "palette_all_ranked": colors["all_ranked"],
        "og_image": og_image if og_image.startswith("http") else "",
        "body_excerpt": body,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Uso: python site_signals.py <url>")
    print(json.dumps(get_signals(sys.argv[1]), indent=2, ensure_ascii=False))
