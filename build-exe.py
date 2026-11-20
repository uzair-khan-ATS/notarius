# /// script
# requires-python = ">=3.11,<3.13"
# dependencies = ["pyinstaller>=6.10"]
# ///
"""Builds dist\\Notarius.exe, the installer and launcher (see launcher.py).

    uv run --script build-exe.py

The .exe carries Windows version details (Properties > Details, Task Manager) taken from
VERSION and PUBLISHER in notarius.py, and the logo. It is built without UPX compression, which
makes antivirus scanners flag unsigned files.

Code signing (optional): with a certificate, set NOTARIUS_SIGN_CERT to a .pfx file (and
NOTARIUS_SIGN_PASSWORD) or to a certificate thumbprint in your store, and have signtool.exe
(Windows SDK) on PATH. The build then signs and timestamps the .exe, which stops the SmartScreen
"unknown publisher" warning and lets it run with Smart App Control on.
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"
DIST = ROOT / "dist"


def setting(name: str) -> str:
    m = re.search(rf'^{name} = "([^"]+)"', (ROOT / "notarius.py").read_text(encoding="utf-8"), re.M)
    if not m:
        sys.exit(f"{name} not found in notarius.py")
    return m.group(1)


def version_file(version: str, publisher: str) -> Path:
    nums = (tuple(int(n) for n in re.findall(r"\d+", version)) + (0, 0, 0, 0))[:4]
    m = re.search(r"Copyright \(c\) (\d{4})", (ROOT / "LICENSE").read_text(encoding="utf-8"))
    copyright_ = f"Copyright (c) {m.group(1) if m else ''} {publisher}. MIT License."
    strings = {"CompanyName": publisher, "FileDescription": "Notarius", "FileVersion": version,
               "InternalName": "Notarius", "LegalCopyright": copyright_, "OriginalFilename": "Notarius.exe",
               "ProductName": "Notarius", "ProductVersion": version,
               "Comments": "Minutes of your Teams meetings, taken on your own laptop"}
    table = ",\n        ".join(f"StringStruct({k!r}, {v!r})" for k, v in strings.items())
    path = BUILD / "version-info.txt"
    path.write_text(f"""VSVersionInfo(
  ffi=FixedFileInfo(filevers={nums}, prodvers={nums}, mask=0x3f, flags=0x0, OS=0x40004,
                    fileType=0x1, subtype=0x0, date=(0, 0)),
  kids=[
    StringFileInfo([StringTable('040904B0', [
        {table}])]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
""", encoding="utf-8")
    return path


def sign(exe: Path) -> None:
    cert = os.environ.get("NOTARIUS_SIGN_CERT")
    if not cert:
        print("Not signed (set NOTARIUS_SIGN_CERT to sign; see build-exe.py).")
        return
    signtool = shutil.which("signtool")
    if not signtool:
        sys.exit("NOTARIUS_SIGN_CERT is set but signtool.exe (Windows SDK) is not on PATH.")
    who = (["/f", cert] + (["/p", os.environ["NOTARIUS_SIGN_PASSWORD"]] if os.environ.get("NOTARIUS_SIGN_PASSWORD") else [])
           if cert.lower().endswith(".pfx") else ["/sha1", cert])
    subprocess.run([signtool, "sign", *who, "/fd", "sha256", "/tr", "http://timestamp.digicert.com",
                    "/td", "sha256", "/d", "Notarius", str(exe)], check=True)
    print("Signed.")


def main() -> None:
    version, publisher = setting("VERSION"), setting("PUBLISHER")
    BUILD.mkdir(exist_ok=True)
    subprocess.run([
        sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--onefile", "--windowed", "--noupx",
        "--name", "Notarius", "--icon", str(ROOT / "assets" / "logo.ico"),
        "--version-file", str(version_file(version, publisher)),
        "--add-data", f"{ROOT / 'notarius.py'};.", "--add-data", f"{ROOT / 'dashboard.html'};.",
        "--distpath", str(DIST), "--workpath", str(BUILD / "pyinstaller"), "--specpath", str(BUILD),
        str(ROOT / "launcher.py"),
    ], check=True)
    exe = DIST / "Notarius.exe"
    sign(exe)
    digest = hashlib.sha256(exe.read_bytes()).hexdigest()
    (DIST / "Notarius.exe.sha256").write_text(f"{digest}  Notarius.exe\n", encoding="ascii")
    print(f"\nBuilt {exe}  (version {version})\nSHA-256 {digest}")


if __name__ == "__main__":
    main()
