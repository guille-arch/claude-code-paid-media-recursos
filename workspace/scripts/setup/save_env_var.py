"""
Guarda credenciales como variables de entorno permanentes del usuario, en Mac, Linux y Windows.

Uso:
  python scripts/setup/save_env_var.py NOMBRE 'valor'      guarda (o actualiza) una variable
  python scripts/setup/save_env_var.py NOMBRE              pide el valor sin mostrarlo (o lo lee de stdin)
  python scripts/setup/save_env_var.py --check NOMBRE ...  dice cuáles están guardadas, sin mostrar valores
  python scripts/setup/save_env_var.py --run NOMBRE ... -- comando ...
                                                           corre un comando con esas variables cargadas
                                                           (sirve en la misma sesión, antes de reiniciar VS Code)

Dónde guarda:
  Windows     variables de entorno del usuario (registro HKCU\\Environment), sin permisos de administrador
  Mac/Linux   una línea export en ~/.zshrc (o ~/.bashrc si el shell es bash); si ya existe, la reemplaza

Nunca imprime los valores. Si no puede guardar, explica cómo hacerlo a mano y termina con código 1.
"""
import getpass
import os
import platform
import re
import shlex
import subprocess
import sys
from pathlib import Path

IS_WINDOWS = platform.system() == "Windows"
NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

MANUAL_WINDOWS = (
    "Guárdala a mano: Win + R, escribe sysdm.cpl, Enter > Opciones avanzadas > "
    "Variables de entorno > Variables de usuario > Nueva. Después cierra todas las ventanas de VS Code."
)


def _console_utf8():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def _profile_path():
    shell = os.path.basename(os.environ.get("SHELL", ""))
    if shell == "bash" or (not shell and Path.home().joinpath(".bashrc").exists()
                           and not Path.home().joinpath(".zshrc").exists()):
        return Path.home() / ".bashrc"
    return Path.home() / ".zshrc"


# ------------------------------------------------------------------ Windows
def _win_read(name):
    import winreg
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
            value, _ = winreg.QueryValueEx(key, name)
            return value
    except FileNotFoundError:
        return None


def _win_write(name, value):
    import ctypes
    import winreg
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, name, 0, winreg.REG_SZ, value)
    HWND_BROADCAST, WM_SETTINGCHANGE, SMTO_ABORTIFHUNG = 0xFFFF, 0x001A, 0x0002
    result = ctypes.c_ulong()
    ctypes.windll.user32.SendMessageTimeoutW(
        HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment", SMTO_ABORTIFHUNG, 5000, ctypes.byref(result))


# ---------------------------------------------------------------- Mac/Linux
def _export_re(name):
    return re.compile(rf"^\s*export\s+{re.escape(name)}=.*$", re.MULTILINE)


def _unix_read(name):
    profile = _profile_path()
    if not profile.exists():
        return None
    text = profile.read_text(encoding="utf-8", errors="replace")
    matches = _export_re(name).findall(text)
    if not matches:
        return None
    try:
        parts = shlex.split(matches[-1].strip()[len("export "):])
    except ValueError:
        return None
    if not parts or "=" not in parts[0]:
        return None
    return parts[0].split("=", 1)[1]


def _unix_write(name, value):
    profile = _profile_path()
    line = f"export {name}={shlex.quote(value)}"
    text = profile.read_text(encoding="utf-8", errors="replace") if profile.exists() else ""
    pattern = _export_re(name)
    if pattern.search(text):
        text = pattern.sub(lambda _: line, text)
    else:
        if text and not text.endswith("\n"):
            text += "\n"
        text += line + "\n"
    profile.write_text(text, encoding="utf-8")


# ------------------------------------------------------------------- común
def read_saved(name):
    return _win_read(name) if IS_WINDOWS else _unix_read(name)


def save(name, value):
    if not NAME_RE.match(name):
        sys.exit(f"Nombre de variable inválido: {name}")
    if not value:
        sys.exit(f"{name}: el valor está vacío, no se guardó nada.")
    value = value.strip()
    try:
        _win_write(name, value) if IS_WINDOWS else _unix_write(name, value)
    except Exception as exc:
        print(f"No se pudo guardar {name}: {type(exc).__name__}.")
        print(MANUAL_WINDOWS if IS_WINDOWS else f"Agrega a mano en {_profile_path()}: export {name}=\"...\"")
        sys.exit(1)
    if read_saved(name) != value:
        print(f"{name}: se escribió pero al releerla no coincide.")
        print(MANUAL_WINDOWS if IS_WINDOWS else f"Revisa la línea export {name}= en {_profile_path()}")
        sys.exit(1)
    where = "variables de usuario de Windows" if IS_WINDOWS else str(_profile_path())
    print(f"OK {name} guardada en {where} ({len(value)} caracteres).")


def check(names):
    missing = [n for n in names if not read_saved(n)]
    for n in names:
        print(f"{'OK  ' if n not in missing else 'FALTA'} {n}")
    return 1 if missing else 0


def run(names, command):
    env = dict(os.environ)
    missing = []
    for n in names:
        value = read_saved(n)
        if value:
            env[n] = value
        else:
            missing.append(n)
    if missing:
        print("Faltan estas variables, guárdalas primero: " + ", ".join(missing))
        return 1
    env.setdefault("PYTHONUTF8", "1")
    env.setdefault("PYTHONIOENCODING", "utf-8")
    return subprocess.call(command, env=env)


def main(argv):
    _console_utf8()
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if argv[0] == "--check":
        return check(argv[1:])
    if argv[0] == "--run":
        if "--" not in argv:
            sys.exit("Uso: --run NOMBRE ... -- comando ...")
        cut = argv.index("--")
        return run(argv[1:cut], argv[cut + 1:])
    name = argv[0]
    if len(argv) > 1:
        value = argv[1]
    elif sys.stdin.isatty():
        value = getpass.getpass(f"Valor de {name} (no se muestra): ")
    else:
        value = sys.stdin.read()
    save(name, value)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
