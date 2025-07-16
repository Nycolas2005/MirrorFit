@echo off
echo 🚀 Executando MirrorFit no Windows
echo ==================================

echo.
echo 📁 Criando estrutura de pastas...
if not exist "frontend" mkdir frontend
if not exist "backend" mkdir backend
if not exist "backend\mirrorfit" mkdir backend\mirrorfit
if not exist "backend\virtual_tryon" mkdir backend\virtual_tryon

echo.
echo 🐍 Configurando Backend...
cd backend

echo Criando ambiente virtual...
python -m venv venv

echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo Instalando dependências...
pip install -r requirements.txt

echo Configurando banco de dados...
python manage.py makemigrations
python manage.py migrate

echo.
echo 🌐 Iniciando servidores...
echo.
echo Backend Django iniciando em http://localhost:8000
start cmd /k "python manage.py runserver"

echo.
echo Aguardando 3 segundos...
timeout /t 3 /nobreak > nul

echo Frontend iniciando em http://localhost:8080
cd ..\frontend
start cmd /k "python -m http.server 8080"

echo.
echo ✅ MirrorFit executando!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:8080
echo.
echo Pressione qualquer tecla para abrir o navegador...
pause > nul

start http://localhost:8080

echo.
echo Para parar os servidores, feche as janelas do terminal.
pause
