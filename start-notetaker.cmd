@echo off
rem Starts Meeting Notes in the tray (no console window) and opens the dashboard.
cd /d "%~dp0"
start "" uvw run --gui-script notetaker.py open
