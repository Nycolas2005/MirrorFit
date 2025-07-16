@echo off
title MirrorFit Windows - IA Avancada
color 0D

echo.
echo 🤖 INSTALACAO IA AVANCADA WINDOWS
echo =================================
echo.
echo Esta instalacao adiciona:
echo ✅ OpenCV para processamento de imagem
echo ✅ MediaPipe para deteccao corporal
echo ✅ NumPy para calculos matematicos
echo.
echo ⚠️ AVISO: Download de ~500MB
echo.

set /p confirm="Deseja continuar? (S/N): "
if /i not "%confirm%"=="S" (
    echo Instalacao cancelada.
    pause
    exit /b 0
)

echo.
echo 🔄 Iniciando instalacao da IA...

REM Verificar se esta na pasta correta
if not exist "backend" (
    echo ❌ Execute dentro da pasta MirrorFit-Windows!
    pause
    exit /b 1
)

cd backend

REM Ativar ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo 📦 Instalando dependencias de IA...
echo.

REM Instalar OpenCV
echo [1/4] Instalando OpenCV...
pip install opencv-python==4.8.1.78
if %errorlevel% neq 0 (
    echo ❌ Erro ao instalar OpenCV
    pause
    exit /b 1
)
echo ✅ OpenCV instalado!

REM Instalar MediaPipe
echo [2/4] Instalando MediaPipe...
pip install mediapipe==0.10.8
if %errorlevel% neq 0 (
    echo ❌ Erro ao instalar MediaPipe
    pause
    exit /b 1
)
echo ✅ MediaPipe instalado!

REM Instalar NumPy
echo [3/4] Instalando NumPy...
pip install numpy==1.24.3
if %errorlevel% neq 0 (
    echo ❌ Erro ao instalar NumPy
    pause
    exit /b 1
)
echo ✅ NumPy instalado!

REM Atualizar requirements.txt
echo [4/4] Atualizando requirements.txt...
echo opencv-python==4.8.1.78>> requirements.txt
echo mediapipe==0.10.8>> requirements.txt
echo numpy==1.24.3>> requirements.txt
echo ✅ Requirements atualizado!

echo.
echo 🧪 Testando instalacao...

REM Testar imports
python -c "import cv2; print('✅ OpenCV OK')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ OpenCV com problemas
) else (
    echo ✅ OpenCV funcionando!
)

python -c "import mediapipe; print('✅ MediaPipe OK')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ MediaPipe com problemas
) else (
    echo ✅ MediaPipe funcionando!
)

python -c "import numpy; print('✅ NumPy OK')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ NumPy com problemas
) else (
    echo ✅ NumPy funcionando!
)

echo.
echo 🎉 IA AVANCADA INSTALADA!
echo =========================
echo.
echo ✅ OpenCV - Processamento de imagem
echo ✅ MediaPipe - Deteccao corporal
echo ✅ NumPy - Calculos matematicos
echo.
echo Agora o MirrorFit pode:
echo 🔍 Detectar corpo e rosto
echo 📏 Calcular medidas corporais
echo 👕 Aplicar roupas virtualmente
echo.
echo Execute: INICIAR_MIRRORFIT.bat
echo.
pause
