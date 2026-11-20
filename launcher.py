"""Notarius.exe: installs Notarius for this Windows user and starts it. Built by build-exe.py.

Like other per-user Windows apps it needs no admin rights. It copies itself and the app to
%LOCALAPPDATA%\\Programs\\Notarius, then notarius.py adds Start-menu and Desktop shortcuts, a login
item and an entry in Settings > Apps that uninstalls it. Running a newer Notarius.exe updates the
installed copy; an older one just starts the installed version. Meetings, voices and speech models
are kept apart, in %LOCALAPPDATA%\\Notarius, so updates and reinstalls never touch them.

The app is notarius.py, run with uv, which installs Python and the dependencies on first use.

Note: Windows Smart App Control blocks unsigned .exe files such as this one. Where it is on, use
the script install from the README instead.
"""
import ctypes
import os
import re
import shutil
import subprocess
import sys
import winreg
from pathlib import Path

APP_NAME = "Notarius"
LOCAL = Path(os.environ.get("LOCALAPPDATA", Path.home()))
INSTALL_DIR = LOCAL / "Programs" / APP_NAME  # must match INSTALL_DIR in notarius.py
INSTALLED_EXE = INSTALL_DIR / f"{APP_NAME}.exe"
OLD_APP_DIR = LOCAL / APP_NAME / "app"  # where versions before 1.1 kept the app
FILES = ("notarius.py", "dashboard.html")
UNINSTALL_KEY = rf"Software\Microsoft\Windows\CurrentVersion\Uninstall\{APP_NAME}"
START_MENU = Path(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", f"{APP_NAME}.lnk")
NO_WINDOW = 0x08000000
# The app runs with uv's console python, which uvw keeps hidden. Not --gui-script: Smart App Control
# can block the unsigned pythonw.exe launcher in uv's script environment, and then nothing starts.


def bundled(name: str) -> Path:
    return Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent)) / name


def message(text: str, icon: int = 0x40) -> None:
    ctypes.windll.user32.MessageBoxW(None, text, APP_NAME, icon)


def version_tuple(v: str | None) -> tuple[int, ...]:
    return tuple(int(n) for n in re.findall(r"\d+", v or ""))


def bundled_version() -> str:
    m = re.search(r'^VERSION = "([^"]+)"', bundled("notarius.py").read_text(encoding="utf-8"), re.M)
    return m.group(1) if m else "0"


def installed_version() -> str | None:
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, UNINSTALL_KEY) as k:
            return winreg.QueryValueEx(k, "DisplayVersion")[0]
    except OSError:
        return None


def app_running() -> bool:
    h = ctypes.windll.kernel32.OpenMutexW(0x00100000, False, "Local\\teams-notetaker-watch")
    if h:
        ctypes.windll.kernel32.CloseHandle(h)
    return bool(h)


def copy_if_changed(src: Path, dst: Path) -> None:
    if dst.exists() and src.read_bytes() == dst.read_bytes():
        return
    tmp = dst.with_name(dst.name + ".new")
    shutil.copyfile(src, tmp)
    os.replace(tmp, dst)


def find_uvw() -> str | None:
    for candidate in (shutil.which("uvw"), Path.home() / ".local" / "bin" / "uvw.exe",
                      Path.home() / ".cargo" / "bin" / "uvw.exe"):
        if candidate and Path(candidate).exists():
            return str(candidate)
    return None


def main() -> None:
    args = sys.argv[1:] or ["open"]
    me = Path(sys.executable).resolve()
    is_installed_copy = me == INSTALLED_EXE.resolve()
    version, installed = bundled_version(), installed_version()

    if args[0] != "uninstall" and not is_installed_copy and INSTALLED_EXE.exists() \
            and version_tuple(version) < version_tuple(installed):
        subprocess.Popen([str(INSTALLED_EXE), *args])  # an older download: start the newer installed copy
        return

    uvw = find_uvw()
    if not uvw:
        message(f"{APP_NAME} needs uv, a small free tool that installs Python for it.\n\n"
                f"The download page will open. Install uv, then start {APP_NAME} again.", 0x30)
        os.startfile("https://docs.astral.sh/uv/getting-started/installation/")
        return
    script = INSTALL_DIR / "notarius.py"
    env = {**os.environ, "NOTARIUS_LAUNCHER": str(INSTALLED_EXE)}

    if args[0] == "uninstall":  # from Settings > Apps
        if not script.exists():
            message(f"{APP_NAME} is already removed.")
            return
        subprocess.Popen([uvw, "run", "--script", str(script), *args], env=env, creationflags=NO_WINDOW)
        return

    first_time = installed is None and not START_MENU.exists()
    INSTALL_DIR.mkdir(parents=True, exist_ok=True)
    try:
        for name in FILES:
            copy_if_changed(bundled(name), INSTALL_DIR / name)
        if getattr(sys, "frozen", False) and not is_installed_copy:
            copy_if_changed(me, INSTALLED_EXE)
    except OSError as e:
        message(f"{APP_NAME} could not be updated, so the installed version will start.\n\n{e}", 0x30)

    if installed != version or not START_MENU.exists():
        if first_time:
            message(f"Setting up {APP_NAME} for the first time.\n\n"
                    "It downloads its speech models (about 3 GB) once, so it can take a few minutes "
                    "to open. After that it starts in seconds and runs in the tray.")
        subprocess.run([uvw, "run", "--script", str(script), "install"], env=env, creationflags=NO_WINDOW)
    if OLD_APP_DIR.exists() and not app_running():
        shutil.rmtree(OLD_APP_DIR, ignore_errors=True)
    subprocess.Popen([uvw, "run", "--script", str(script), *args], env=env, creationflags=NO_WINDOW)


if __name__ == "__main__":
    main()
