@echo off
title Donkey Kong Rebuild (HD) - Launcher & GUI
echo Iniciando Donkey Kong Rebuild...
py main.py
if errorlevel 1 (
    python main.py
)
