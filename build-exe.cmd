@echo off
rem Builds dist\Notarius.exe, the installer and launcher. See build-exe.py.
cd /d "%~dp0"
uv run --script build-exe.py
