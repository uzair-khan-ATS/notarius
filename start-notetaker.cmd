@echo off
title notetaker
cd /d "%~dp0"
uv run --script notetaker.py watch
pause
