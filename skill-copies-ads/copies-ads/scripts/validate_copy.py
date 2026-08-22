#!/usr/bin/env python3
"""
validate_copy.py - Valida y exporta el set de copies generado por la skill copies-ads.

    python .claude/skills/copies-ads/scripts/validate_copy.py reports/copies_marca_2026-08-27.json
    python .claude/skills/copies-ads/scripts/validate_copy.py reports/copies_marca_2026-08-27.json --csv

Comprueba límites de caracteres (Google RSA y Meta), duplicados, comillas dobles,
mayúsculas completas, exclamaciones repetidas, estructura 15/3/3 y presencia de la
keyword principal en ≥2 titulares. Con --csv exporta:
  - <base>_google.csv : una fila por RSA (Campaign, Ad group, Final URL, Headline 1..15, Description 1..4)
  - <base>_meta.csv   : una fila por variante de texto principal (ángulo, texto, titular, descripción, CTA)

Sin dependencias externas (solo stdlib). Código de salida 1 si hay errores.
"""
from __future__ import annotations

import csv
import json
import re
import sys
import unicodedata
from pathlib import Path

LIMITS = {
    "headline": 30, "description": 90,
    "sitelink_text": 25, "sitelink_desc": 35, "callout": 25,
    "meta_headline": 40, "meta_description": 30, "meta_primary_recommended": 125,
}
META_CTAS = {
    "Más información", "Registrarte", "Comprar", "Reservar", "Contactarnos", "Descargar",
    "Solicitar presupuesto", "Suscribirte", "Enviar mensaje", "Enviar mensaje de WhatsApp",
    "Ver más", "Obtener oferta", "Solicitar ahora", "Empezar", "Inscribirse",
}


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]+", " ", s).strip()


def _len(s: str) -> int:
    return len(s.strip())


class Report:
    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.lines: list[str] = []

    def err(self, m): self.errors.append(m)
    def warn(self, m): self.warnings.append(m)
    def line(self, m): self.lines.append(m)


def check_text(rep: Report, where: str, text: str, limit: int, hard: bool = True):
    n = _len(text)
    flag = ""
    if n > limit:
        flag = f"  <-- {n}/{limit} SUPERA"
        (rep.err if hard else rep.warn)(f"{where}: {n} caracteres (máx. {limit}): \"{text}\"")
    if '"' in text:
        rep.err(f"{where}: contiene comillas dobles: \"{text}\"")
    if re.search(r"!{2,}|\?{2,}", text):
        rep.err(f"{where}: signos repetidos: \"{text}\"")
    words = [w for w in re.findall(r"[A-ZÁÉÍÓÚÑ]{4,}", text)]
    if words and any(len(w) >= 5 for w in words):
        rep.warn(f"{where}: palabra en MAYÚSCULAS completas (evítalo salvo siglas): \"{text}\"")
    if re.search(r"\b(haz clic aquí|click aquí|pincha aquí)\b", text, re.I):
        rep.err(f"{where}: 'haz clic aquí' no está permitido: \"{text}\"")
    rep.line(f"  [{n:>3}/{limit}] {text}{flag}")


def validate(data: dict) -> Report:
    rep = Report()
    brand = data.get("brand") or "(sin marca)"
    rep.line(f"Marca: {brand} · modelo: {data.get('model','?')} · idioma: {data.get('language','es-ES')}")
    rsas = data.get("google_rsa") or []
    if not rsas:
        rep.warn("No hay bloques google_rsa.")
    for i, rsa in enumerate(rsas, 1):
        name = rsa.get("ad_group") or f"RSA {i}"
        rep.line(f"\n== Google RSA: {name}  ({rsa.get('final_url','sin final_url')})")
        if not rsa.get("final_url"):
            rep.err(f"{name}: falta final_url")
        hs = rsa.get("headlines") or []
        ds = rsa.get("descriptions") or []
        if len(hs) != 15:
            rep.err(f"{name}: {len(hs)} titulares (deben ser exactamente 15)")
        if len(ds) != 4:
            rep.err(f"{name}: {len(ds)} descripciones (deben ser exactamente 4)")
        rep.line("  Titulares:")
        for j, h in enumerate(hs, 1):
            check_text(rep, f"{name} · titular {j}", h, LIMITS["headline"])
        rep.line("  Descripciones:")
        for j, d in enumerate(ds, 1):
            check_text(rep, f"{name} · descripción {j}", d, LIMITS["description"])
        # duplicates
        seen = {}
        for h in hs:
            k = _norm(h)
            if k in seen:
                rep.err(f"{name}: titular duplicado: \"{h}\"")
            seen[k] = 1
        seen = {}
        for d in ds:
            k = _norm(d)
            if k in seen:
                rep.err(f"{name}: descripción duplicada: \"{d}\"")
            seen[k] = 1
        # 15/3/3 coverage
        groups = rsa.get("headline_groups") or {}
        if groups:
            for g in ("relevancia", "valor", "accion"):
                n = len(groups.get(g) or [])
                if n != 5:
                    rep.warn(f"{name}: grupo '{g}' tiene {n} titulares (estructura 15/3/3 = 5 por grupo)")
        else:
            rep.warn(f"{name}: sin 'headline_groups' (no se puede comprobar la estructura 15/3/3)")
        # keyword presence
        kw = rsa.get("main_keyword")
        if kw:
            hits = sum(1 for h in hs if _norm(kw) in _norm(h))
            if hits < 2:
                rep.warn(f"{name}: la keyword principal \"{kw}\" aparece en {hits} titular(es); se recomiendan ≥2")
        # pins
        pins = rsa.get("pin_suggestion") or []
        if len(pins) > 1:
            rep.warn(f"{name}: {len(pins)} titulares pineados; se recomienda como mucho 1")
        # extensions
        for s in rsa.get("sitelinks") or []:
            check_text(rep, f"{name} · sitelink", s.get("text", ""), LIMITS["sitelink_text"])
            for k in ("desc1", "desc2"):
                if s.get(k):
                    check_text(rep, f"{name} · sitelink desc", s[k], LIMITS["sitelink_desc"])
            if not s.get("url"):
                rep.warn(f"{name}: sitelink \"{s.get('text','')}\" sin URL")
        for c in rsa.get("callouts") or []:
            check_text(rep, f"{name} · callout", c, LIMITS["callout"])

    metas = data.get("meta_ads") or []
    if not metas:
        rep.warn("No hay bloques meta_ads.")
    for i, ad in enumerate(metas, 1):
        angle = ad.get("angle") or f"ángulo {i}"
        rep.line(f"\n== Meta · ángulo: {angle}")
        prims = ad.get("primary_text") or []
        if isinstance(prims, str):
            prims = [prims]
        if not prims:
            rep.err(f"Meta {angle}: sin primary_text")
        if len(prims) > 3:
            rep.warn(f"Meta {angle}: {len(prims)} variantes de texto principal (máx. recomendado 3)")
        rep.line("  Texto principal:")
        for j, p in enumerate(prims, 1):
            check_text(rep, f"Meta {angle} · texto {j}", p, LIMITS["meta_primary_recommended"], hard=False)
        rep.line("  Titular / descripción:")
        check_text(rep, f"Meta {angle} · titular", ad.get("headline", ""), LIMITS["meta_headline"])
        check_text(rep, f"Meta {angle} · descripción", ad.get("description", ""), LIMITS["meta_description"])
        cta = ad.get("cta")
        if cta and cta not in META_CTAS:
            rep.warn(f"Meta {angle}: CTA \"{cta}\" no está en el catálogo habitual de Meta ({', '.join(sorted(META_CTAS))})")
    return rep


def export_csv(data: dict, base: Path) -> list[Path]:
    out = []
    g = base.with_name(base.stem + "_google.csv")
    with g.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        head = ["Campaign", "Ad group", "Final URL", "Path 1", "Path 2"]
        head += [f"Headline {i}" for i in range(1, 16)] + [f"Headline {i} position" for i in range(1, 16)]
        head += [f"Description {i}" for i in range(1, 5)]
        w.writerow(head)
        for rsa in data.get("google_rsa") or []:
            hs = (rsa.get("headlines") or [])[:15] + [""] * 15
            ds = (rsa.get("descriptions") or [])[:4] + [""] * 4
            pins = {p.get("headline"): p.get("position") for p in (rsa.get("pin_suggestion") or []) if isinstance(p, dict)}
            row = [data.get("campaign_name") or f"Search - {data.get('brand','')}", rsa.get("ad_group", ""), rsa.get("final_url", ""),
                   rsa.get("path1", ""), rsa.get("path2", "")]
            row += hs[:15] + [pins.get(h, "") for h in hs[:15]] + ds[:4]
            w.writerow(row)
    out.append(g)
    m = base.with_name(base.stem + "_meta.csv")
    with m.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Ángulo", "Variante", "Texto principal", "Titular", "Descripción", "CTA", "URL"])
        for ad in data.get("meta_ads") or []:
            prims = ad.get("primary_text") or []
            if isinstance(prims, str):
                prims = [prims]
            for j, p in enumerate(prims, 1):
                w.writerow([ad.get("angle", ""), j, p, ad.get("headline", ""), ad.get("description", ""), ad.get("cta", ""), ad.get("url") or data.get("url", "")])
    out.append(m)
    return out


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
    path = Path(args[0])
    want_csv = "--csv" in args
    data = json.loads(path.read_text(encoding="utf-8"))
    rep = validate(data)
    print("\n".join(rep.lines))
    print("\n---")
    if rep.warnings:
        print(f"AVISOS ({len(rep.warnings)}):")
        for wmsg in rep.warnings:
            print("  - " + wmsg)
    if rep.errors:
        print(f"ERRORES ({len(rep.errors)}):")
        for e in rep.errors:
            print("  - " + e)
        print("\nResultado: NO VÁLIDO. Corrige el JSON y vuelve a validar.")
    else:
        print("Resultado: VÁLIDO (sin errores).")
    if want_csv:
        files = export_csv(data, path)
        print("CSV exportados:")
        for p in files:
            print("  - " + str(p))
    sys.exit(1 if rep.errors else 0)


if __name__ == "__main__":
    main()
