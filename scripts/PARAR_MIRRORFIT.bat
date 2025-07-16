@echo off
title MirrorFit Windows - Parando
color 0C

echo.
echo 🛑 PARANDO MIRRORFIT WINDOWS
echo ============================
echo.

echo 🔄 Parando servidores...

REM Matar processos Python (Django e Frontend)
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im pythonw.exe >nul 2>&1

REM Matar processos cmd do MirrorFit
taskkill /f /fi "WINDOWTITLE eq MirrorFit Backend" >nul 2>&1
taskkill /f /fi "WINDOWTITLE eq MirrorFit Frontend" >nul 2>&1

echo ✅ Servidores parados!

echo.
echo 🔄 Limpando portas...

REM Liberar portas (se estiverem ocupadas)
netstat -ano | findstr :8000 >nul 2>&1
if %errorlevel% equ 0 (
    echo Liberando porta 8000...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do taskkill /f /pid %%a >nul 2>&1
)

netstat -ano | findstr :8080 >nul 2>&1
if %errorlevel% equ 0 (
    echo Liberando porta 8080...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8080') do taskkill /f /pid %%a >nul 2>&1
)

echo ✅ Portas liberadas!

echo.
echo ✅ MIRRORFIT PARADO COM SUCESSO!
echo ================================
echo.
echo Para reiniciar: Execute INICIAR_MIRRORFIT.bat
echo.
pause
