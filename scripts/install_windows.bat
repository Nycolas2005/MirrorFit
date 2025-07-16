@echo off
echo 🚀 INSTALAÇÃO AUTOMÁTICA - MirrorFit Windows
echo ============================================

echo.
echo Verificando Python...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado!
    echo Baixe em: https://python.org
    pause
    exit /b 1
)

echo ✅ Python encontrado!

echo.
echo 📥 Baixando instalador...
curl -o quick_install.py https://raw.githubusercontent.com/seu-repo/mirrorfit/main/quick_install.py

echo.
echo 🔧 Executando instalação...
python quick_install.py

echo.
echo ✅ Instalação concluída!
echo.
echo Para executar o MirrorFit:
echo   cd mirrorfit-complete
echo   run.bat
echo.
pause
