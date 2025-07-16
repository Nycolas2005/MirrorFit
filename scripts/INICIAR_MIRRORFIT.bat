@echo off
title MirrorFit Windows - Executando
color 0B

echo.
echo  ███╗   ███╗██╗██████╗ ██████╗  ██████╗ ██████╗ ███████╗██╗████████╗
echo  ████╗ ████║██║██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔════╝██║╚══██╔══╝
echo  ██╔████╔██║██║██████╔╝██████╔╝██║   ██║██████╔╝█████╗  ██║   ██║   
echo  ██║╚██╔╝██║██║██╔══██╗██╔══██╗██║   ██║██╔══██╗██╔══╝  ██║   ██║   
echo  ██║ ╚═╝ ██║██║██║  ██║██║  ██║╚██████╔╝██║  ██║██║     ██║   ██║   
echo  ╚═╝     ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝   ╚═╝   
echo.
echo                        INICIANDO WINDOWS
echo                        =================
echo.

REM Verificar se esta na pasta correta
if not exist "backend" (
    echo ❌ Pasta backend nao encontrada!
    echo Execute este arquivo dentro da pasta MirrorFit-Windows
    echo.
    pause
    exit /b 1
)

if not exist "frontend" (
    echo ❌ Pasta frontend nao encontrada!
    echo Execute este arquivo dentro da pasta MirrorFit-Windows
    echo.
    pause
    exit /b 1
)

echo 🔄 Iniciando Backend Django...
cd backend

REM Ativar ambiente virtual
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Ambiente virtual nao encontrado!
    echo Execute primeiro: install_windows_complete.bat
    echo.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

REM Verificar se Django esta instalado
python -c "import django" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Django nao encontrado no ambiente virtual!
    echo Reinstalando dependencias...
    pip install -r requirements.txt
)

echo ✅ Ambiente virtual ativado!

REM Iniciar Django em nova janela
echo 🚀 Iniciando servidor Django...
start "MirrorFit Backend" cmd /k "python manage.py runserver"

REM Aguardar Django inicializar
echo ⏳ Aguardando Django inicializar...
timeout /t 5 /nobreak >nul

REM Testar se Django esta rodando
echo 🧪 Testando conexao com Django...
python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000')" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Django pode estar demorando para iniciar...
    echo Aguarde mais alguns segundos...
)

echo ✅ Backend iniciado!

REM Iniciar Frontend
echo 🔄 Iniciando Frontend...
cd ..\frontend

echo 🚀 Iniciando servidor Frontend...
start "MirrorFit Frontend" cmd /k "python -m http.server 8080"

REM Aguardar Frontend inicializar
echo ⏳ Aguardando Frontend inicializar...
timeout /t 3 /nobreak >nul

echo ✅ Frontend iniciado!

echo.
echo 🎉 MIRRORFIT WINDOWS RODANDO!
echo =============================
echo.
echo 🌐 URLs:
echo    Frontend: http://localhost:8080
echo    Backend:  http://localhost:8000
echo.
echo 📱 Abra seu navegador e acesse:
echo    http://localhost:8080
echo.
echo ⏹️ Para parar: Execute PARAR_MIRRORFIT.bat
echo    ou feche as janelas do terminal
echo.

REM Abrir navegador automaticamente
echo 🌐 Abrindo navegador...
timeout /t 2 /nobreak >nul
start http://localhost:8080

echo.
echo ✅ Tudo funcionando!
echo Pressione qualquer tecla para voltar ao menu...
pause >nul
