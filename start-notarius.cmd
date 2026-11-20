@echo off
rem Starts Notarius in the tray (no console window) and opens the dashboard.
cd /d "%~dp0"
start "" uvw run --script notarius.py open
