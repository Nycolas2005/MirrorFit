#!/bin/bash

echo "🚀 Executando MirrorFit no Linux/Mac"
echo "===================================="

echo ""
echo "📁 Criando estrutura de pastas..."
mkdir -p frontend
mkdir -p backend/mirrorfit
mkdir -p backend/virtual_tryon

echo ""
echo "🐍 Configurando Backend..."
cd backend

echo "Criando ambiente virtual..."
python3 -m venv venv

echo "Ativando ambiente virtual..."
source venv/bin/activate

echo "Instalando dependências..."
pip install -r requirements.txt

echo "Configurando banco de dados..."
python manage.py makemigrations
python manage.py migrate

echo ""
echo "🌐 Iniciando Backend..."
echo "Backend Django iniciando em http://localhost:8000"
python manage.py runserver &
BACKEND_PID=$!

echo ""
echo "Aguardando 3 segundos..."
sleep 3

echo "Frontend iniciando em http://localhost:8080"
cd ../frontend
python3 -m http.server 8080 &
FRONTEND_PID=$!

echo ""
echo "✅ MirrorFit executando!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:8080"
echo ""
echo "Abrindo navegador..."
sleep 2

# Tentar abrir navegador
if command -v xdg-open > /dev/null; then
    xdg-open http://localhost:8080
elif command -v open > /dev/null; then
    open http://localhost:8080
fi

echo ""
echo "Pressione Ctrl+C para parar os servidores"

# Aguardar interrupção
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
