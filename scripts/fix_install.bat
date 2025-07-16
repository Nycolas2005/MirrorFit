@echo off
echo 🔧 CORREÇÃO RÁPIDA - Erro de Import
echo ==================================

echo.
echo Baixando instalador corrigido...
echo.

echo import os > simple_install.py
echo import subprocess >> simple_install.py
echo import sys >> simple_install.py
echo import platform >> simple_install.py
echo from pathlib import Path >> simple_install.py
echo. >> simple_install.py

curl -s https://raw.githubusercontent.com/exemplo/simple_install_content.txt >> simple_install.py

echo.
echo ✅ Instalador corrigido baixado!
echo.
echo Executando instalação sem requests...
python simple_install.py

echo.
echo ✅ Pronto! Execute:
echo   cd mirrorfit-simple
echo   start.bat
echo.
pause
