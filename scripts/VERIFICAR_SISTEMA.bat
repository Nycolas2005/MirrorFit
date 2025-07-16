@echo off
title MirrorFit Windows - Verificacao do Sistema
color 0E

echo.
echo 🔍 VERIFICACAO DO SISTEMA WINDOWS
echo =================================
echo.

echo [1/5] Verificando Python...
python --version 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python nao encontrado!
    echo Baixe em: https://python.org/downloads/
    echo Marque "Add Python to PATH"
    goto :error
) else (
    echo ✅ Python encontrado!
)

echo.
echo [2/5] Verificando pip...
pip --version 2>nul
if %errorlevel% neq 0 (
    echo ❌ pip nao encontrado!
    echo Execute: python -m ensurepip --upgrade
    goto :error
) else (
    echo ✅ pip encontrado!
)

echo.
echo [3/5] Verificando estrutura do projeto...
if not exist "backend" (
    echo ❌ Pasta backend nao encontrada!
    echo Execute: install_windows_complete.bat
    goto :error
) else (
    echo ✅ Pasta backend encontrada!
)

if not exist "frontend" (
    echo ❌ Pasta frontend nao encontrada!
    echo Execute: install_windows_complete.bat
    goto :error
) else (
    echo ✅ Pasta frontend encontrada!
)

echo.
echo [4/5] Verificando ambiente virtual...
if not exist "backend\venv" (
    echo ❌ Ambiente virtual nao encontrado!
    echo Execute: install_windows_complete.bat
    goto :error
) else (
    echo ✅ Ambiente virtual encontrado!
)

echo.
echo [5/5] Testando conexoes...
echo Testando porta 8000...
netstat -an | findstr :8000 >nul 2>&1
if %errorlevel% equ 0 (
    echo ⚠️ Porta 8000 em uso (Django pode estar rodando)
) else (
    echo ✅ Porta 8000 livre
)

echo Testando porta 8080...
netstat -an | findstr :8080 >nul 2>&1
if %errorlevel% equ 0 (
    echo ⚠️ Porta 8080 em uso (Frontend pode estar rodando)
) else (
    echo ✅ Porta 8080 livre
)

echo.
echo 🎉 SISTEMA WINDOWS OK!
echo ======================
echo.
echo ✅ Tudo pronto para executar!
echo Execute: INICIAR_MIRRORFIT.bat
echo.
goto :end

:error
echo.
echo ❌ PROBLEMAS ENCONTRADOS!
echo =========================
echo.
echo Corrija os problemas acima e tente novamente.
echo.

:end
pause
