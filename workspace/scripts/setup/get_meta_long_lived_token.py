"""
Convierte un token de Meta Ads de corta duración (1h) a larga duración (60 días).
Necesitas: App ID, App Secret y el token corto generado en el panel de Meta.

Cómo obtener el token corto:
1. developers.facebook.com → tu app → Marketing API → Herramientas
2. Selecciona permisos: ads_read, ads_management
3. Haz clic en "Generar token de acceso"
4. Copia ese token y ejecúta este script
"""

import os

import requests
import sys

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


def get_long_lived_token(app_id, app_secret, short_token):
    url = "https://graph.facebook.com/v18.0/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": app_secret,
        "fb_exchange_token": short_token,
    }
    response = requests.get(url, params=params)
    data = response.json()

    if "access_token" in data:
        return data["access_token"]
    else:
        raise Exception(f"Error de Meta API: {data}")


def main():
    print("=" * 60)
    print("META ADS — TOKEN DE LARGA DURACIÓN (60 DÍAS)")
    print("=" * 60)
    print()
    print("Necesitas tener a mano:")
    print("  - App ID (en la configuración básica de tu app de Meta)")
    print("  - App Secret (en la configuración básica de tu app)")
    print("  - Token corto (generado en Marketing API → Herramientas)")
    print()

    app_id = os.environ.get("META_APP_ID") or input("App ID: ").strip()
    app_secret = os.environ.get("META_APP_SECRET") or input("App Secret: ").strip()
    short_token = input("Token corto: ").strip()

    print()
    print("Generando token de larga duración...")

    try:
        long_token = get_long_lived_token(app_id, app_secret, short_token)

        print()
        print("=" * 60)
        print("✅ TOKEN GENERADO CORRECTAMENTE (válido ~60 días)")
        print("=" * 60)
        print()
        print("Guárdalo como variable de entorno (Mac, Linux y Windows; Claude Code puede hacerlo por ti):")
        print()
        print(f"   python scripts/setup/save_env_var.py META_ACCESS_TOKEN '{long_token}'")
        print()
        print("Luego cierra TODAS las ventanas de VS Code y vuelve a abrirlo.")
        print()
        print("⚠️  Recuerda: este token expira en ~60 días.")
        print("   Cuando expire, vuelve a ejecutar este script.")

    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("Verifica que el token corto sea válido y que el App ID")
        print("y App Secret correspondan a la misma app.")


if __name__ == "__main__":
    main()
