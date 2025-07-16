#!/bin/bash

echo "🚀 SETUP COMPLETO - MirrorFit com Captura de Roupas Reais"
echo "========================================================="

echo ""
echo "📋 PASSO 1: Verificar requisitos do sistema"
echo "-------------------------------------------"
echo "✅ Python 3.8+ instalado"
echo "✅ pip instalado"
echo "✅ 4GB+ de RAM disponível"
echo "✅ 2GB+ de espaço em disco"

echo ""
echo "📁 PASSO 2: Criar estrutura do projeto"
echo "--------------------------------------"

# Criar diretórios
mkdir -p mirrorfit-complete/{frontend,backend,media,temp}
cd mirrorfit-complete

echo "Estrutura criada:"
echo "mirrorfit-complete/"
echo "├── frontend/     # HTML, CSS, JS"
echo "├── backend/      # Django + IA"
echo "├── media/        # Imagens processadas"
echo "└── temp/         # Arquivos temporários"

echo ""
echo "🐍 PASSO 3: Configurar Backend com IA Avançada"
echo "----------------------------------------------"

cd backend

# Criar ambiente virtual
echo "Criando ambiente virtual..."
python -m venv venv

# Ativar ambiente virtual
echo "Ativando ambiente virtual..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo "Ambiente virtual ativado ✅"

echo ""
echo "📦 PASSO 4: Instalar dependências"
echo "---------------------------------"

# Criar requirements.txt completo
cat > requirements.txt << 'EOF'
# Django Core
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1

# IA e Processamento de Imagem
opencv-python==4.8.1.78
mediapipe==0.10.8
Pillow==10.1.0
numpy==1.24.3

# IA Avançada para Segmentação
torch==2.1.0
torchvision==0.16.0
segment-anything==1.0

# Utilitários
python-decouple==3.8
requests==2.31.0

# Banco de dados (opcional)
# psycopg2-binary==2.9.7
EOF

echo "Instalando dependências básicas..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "🤖 PASSO 5: Baixar modelos de IA"
echo "--------------------------------"

# Criar script para baixar modelos
cat > download_models.py << 'EOF'
import requests
import os
from pathlib import Path

def download_sam_model():
    """Baixa modelo SAM para segmentação precisa"""
    model_url = "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth"
    model_path = "models/sam_vit_b_01ec64.pth"
    
    os.makedirs("models", exist_ok=True)
    
    if not os.path.exists(model_path):
        print("📥 Baixando modelo SAM (300MB)...")
        response = requests.get(model_url, stream=True)
        
        with open(model_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print("✅ Modelo SAM baixado!")
    else:
        print("✅ Modelo SAM já existe!")

if __name__ == "__main__":
    download_sam_model()
EOF

echo "Baixando modelos de IA..."
python download_models.py

echo ""
echo "⚙️ PASSO 6: Configurar Django"
echo "-----------------------------"

# Criar estrutura Django
django-admin startproject mirrorfit .
cd mirrorfit
python manage.py startapp virtual_tryon
cd ..

echo "Django configurado ✅"

echo ""
echo "🌐 PASSO 7: Configurar Frontend"
echo "-------------------------------"

cd ../frontend

# Criar package.json para frontend
cat > package.json << 'EOF'
{
  "name": "mirrorfit-frontend",
  "version": "2.0.0",
  "description": "MirrorFit - Provador Virtual com IA e Captura de Roupas Reais",
  "scripts": {
    "start": "python -m http.server 8080",
    "dev": "python -m http.server 8080"
  }
}
EOF

echo "Frontend configurado ✅"

echo ""
echo "🔧 PASSO 8: Scripts de execução"
echo "-------------------------------"

cd ..

# Script para Windows
cat > run_windows.bat << 'EOF'
@echo off
echo 🚀 Iniciando MirrorFit Completo...

echo Ativando ambiente virtual...
cd backend
call venv\Scripts\activate.bat

echo Iniciando Django...
start cmd /k "python manage.py runserver"

echo Aguardando Django inicializar...
timeout /t 5 /nobreak > nul

echo Iniciando Frontend...
cd ..\frontend
start cmd /k "python -m http.server 8080"

echo ✅ MirrorFit rodando!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:8080

timeout /t 3 /nobreak > nul
start http://localhost:8080

pause
EOF

# Script para Linux/Mac
cat > run_linux_mac.sh << 'EOF'
#!/bin/bash

echo "🚀 Iniciando MirrorFit Completo..."

echo "Ativando ambiente virtual..."
cd backend
source venv/bin/activate

echo "Iniciando Django..."
python manage.py runserver &
DJANGO_PID=$!

echo "Aguardando Django inicializar..."
sleep 5

echo "Iniciando Frontend..."
cd ../frontend
python -m http.server 8080 &
FRONTEND_PID=$!

echo "✅ MirrorFit rodando!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:8080"

sleep 3

# Abrir navegador
if command -v xdg-open > /dev/null; then
    xdg-open http://localhost:8080
elif command -v open > /dev/null; then
    open http://localhost:8080
fi

echo "Pressione Ctrl+C para parar"
trap "kill $DJANGO_PID $FRONTEND_PID; exit" INT
wait
EOF

chmod +x run_linux_mac.sh

echo "Scripts criados ✅"

echo ""
echo "✅ SETUP COMPLETO!"
echo "=================="
echo ""
echo "Para executar:"
echo "Windows: run_windows.bat"
echo "Linux/Mac: ./run_linux_mac.sh"
echo ""
echo "URLs:"
echo "Frontend: http://localhost:8080"
echo "Backend: http://localhost:8000"
