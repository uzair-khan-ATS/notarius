@echo off
rem Builds dist\Notarius.exe (a launcher with the logo; see launcher.py).
cd /d "%~dp0"
uv run --no-project --python 3.12 --with pyinstaller python -m PyInstaller --noconfirm --clean --onefile --windowed ^
  --name Notarius --icon assets\logo.ico ^
  --add-data "notarius.py;." --add-data "dashboard.html;." ^
  launcher.py
echo.
echo Built: %~dp0dist\Notarius.exe
