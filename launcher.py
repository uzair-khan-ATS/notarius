"""Notarius.exe: a small launcher, built with PyInstaller (see build-exe.cmd).

It carries notarius.py and dashboard.html, copies them to %LOCALAPPDATA%\\Notarius\\app, and runs
them with uv, which installs Python and the dependencies on first use. On the first start it
also creates the Start-menu, Desktop and login shortcuts.

Note: Windows Smart App Control blocks unsigned .exe files such as this one. Where it is on, use
the script install from the README instead.
"""
import ctypes
import os
import shutil
import subprocess
import sys
from pathlib import Path

APP = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "Notarius" / "app"
FILES = ("notarius.py", "dashboard.html")
NO_WINDOW = 0x08000000


def bundled(name: str) -> Path:
    return Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent)) / name


def message(text: str, icon: int = 0x40) -> None:
    ctypes.windll.user32.MessageBoxW(None, text, "Notarius", icon)


def find_uvw() -> str | None:
    for candidate in (shutil.which("uvw"), Path.home() / ".local" / "bin" / "uvw.exe",
                      Path.home() / ".cargo" / "bin" / "uvw.exe"):
        if candidate and Path(candidate).exists():
            return str(candidate)
    return None


def main() -> None:
    APP.mkdir(parents=True, exist_ok=True)
    for name in FILES:  # update the installed copy when the .exe is newer
        src, dst = bundled(name), APP / name
        if not dst.exists() or src.read_bytes() != dst.read_bytes():
            shutil.copyfile(src, dst)

    uvw = find_uvw()
    if not uvw:
        message("Notarius needs uv, a small free tool that installs Python for it.\n\n"
                "The download page will open. Install uv, then start Notarius again.", 0x30)
        os.startfile("https://docs.astral.sh/uv/getting-started/installation/")
        return

    script = str(APP / "notarius.py")
    args = sys.argv[1:] or ["open"]
    start_menu = Path(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Notarius.lnk")
    if args == ["open"] and not start_menu.exists():
        message("Setting up Notarius for the first time.\n\n"
                "It downloads its speech models (about 3 GB) once, so the dashboard can take a few "
                "minutes to open. After that it starts in seconds and runs in the tray.")
        subprocess.run([uvw, "run", "--script", script, "install"], creationflags=NO_WINDOW)
    subprocess.Popen([uvw, "run", "--gui-script", script, *args], creationflags=NO_WINDOW)


if __name__ == "__main__":
    main()
