"""
Script de instalação rápida do MirrorFit
Execute: python quick_install.py
"""

import os
import subprocess
import sys
import platform
from pathlib import Path

def run_command(command, description):
    """Executa comando e mostra progresso"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Concluído!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro em {description}: {e}")
        print(f"Output: {e.output}")
        return False

def check_python():
    """Verifica versão do Python"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} - Necessário Python 3.8+")
        return False

def create_project_structure():
    """Cria estrutura do projeto"""
    print("📁 Criando estrutura do projeto...")
    
    directories = [
        "mirrorfit-complete",
        "mirrorfit-complete/frontend",
        "mirrorfit-complete/backend",
        "mirrorfit-complete/backend/mirrorfit",
        "mirrorfit-complete/backend/virtual_tryon",
        "mirrorfit-complete/media",
        "mirrorfit-complete/temp"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Estrutura criada!")

def install_backend():
    """Instala e configura backend"""
    print("🐍 Configurando Backend...")
    
    os.chdir("mirrorfit-complete/backend")
    
    # Criar ambiente virtual
    if not run_command("python -m venv venv", "Criando ambiente virtual"):
        return False
    
    # Ativar ambiente virtual e instalar dependências
    if platform.system() == "Windows":
        activate_cmd = "venv\\Scripts\\activate && "
    else:
        activate_cmd = "source venv/bin/activate && "
    
    # Criar requirements.txt
    requirements = """Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
opencv-python==4.8.1.78
mediapipe==0.10.8
Pillow==10.1.0
numpy==1.24.3
python-decouple==3.8"""
    
    with open("requirements.txt", "w") as f:
        f.write(requirements)
    
    # Instalar dependências
    if not run_command(f"{activate_cmd}pip install --upgrade pip", "Atualizando pip"):
        return False
    
    if not run_command(f"{activate_cmd}pip install -r requirements.txt", "Instalando dependências"):
        return False
    
    print("✅ Backend configurado!")
    return True

def create_django_files():
    """Cria arquivos básicos do Django"""
    print("⚙️ Criando arquivos Django...")
    
    # Criar diretórios necessários
    os.makedirs("mirrorfit", exist_ok=True)
    os.makedirs("virtual_tryon", exist_ok=True)
    
    # manage.py
    manage_content = '''#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mirrorfit.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
'''
    
    with open("manage.py", "w") as f:
        f.write(manage_content)
    
    # settings.py básico
    settings_content = '''
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-mirrorfit-dev-key-change-in-production'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'virtual_tryon',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mirrorfit.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mirrorfit.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_ALL_ORIGINS = True  # Para desenvolvimento
CORS_ALLOW_CREDENTIALS = True

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
'''
    
    with open("mirrorfit/settings.py", "w") as f:
        f.write(settings_content)
    
    # urls.py principal
    urls_content = '''from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('virtual_tryon.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''
    
    with open("mirrorfit/urls.py", "w") as f:
        f.write(urls_content)
    
    # wsgi.py
    wsgi_content = '''import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mirrorfit.settings')
application = get_wsgi_application()
'''
    
    with open("mirrorfit/wsgi.py", "w") as f:
        f.write(wsgi_content)
    
    # __init__.py files
    Path("mirrorfit/__init__.py").touch()
    Path("virtual_tryon/__init__.py").touch()
    
    print("✅ Arquivos Django criados!")

def create_virtual_tryon_app():
    """Cria arquivos da app virtual_tryon"""
    print("🤖 Criando app virtual_tryon...")
    
    # models.py
    models_content = '''from django.db import models
import uuid

class TryOnSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_photo = models.ImageField(upload_to='original_photos/')
    result_photo = models.ImageField(upload_to='result_photos/', null=True, blank=True)
    selected_clothing = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pendente'),
        ('processing', 'Processando'),
        ('completed', 'Concluído'),
        ('failed', 'Falhou'),
    ], default='pending')

    class Meta:
        ordering = ['-created_at']

class ClothingItem(models.Model):
    CLOTHING_TYPES = [
        ('shirt', 'Camiseta'),
        ('pants', 'Calça'),
        ('shorts', 'Bermuda'),
        ('shoes', 'Tênis'),
    ]
    
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=CLOTHING_TYPES)
    image = models.ImageField(upload_to='clothing_items/')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
'''
    
    with open("virtual_tryon/models.py", "w") as f:
        f.write(models_content)
    
    # views.py
    views_content = '''from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
import json

class TryOnAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        try:
            photo = request.FILES.get('photo')
            clothing_data = request.data.get('clothing')
            
            if not photo:
                return Response({
                    'success': False,
                    'error': 'Foto é obrigatória'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Simulação de processamento
            return Response({
                'success': True,
                'message': 'IA em desenvolvimento! Sistema funcionando.',
                'session_id': 'demo-123',
                'result_image_url': '/media/demo-result.jpg'
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HealthCheckView(APIView):
    def get(self, request):
        return Response({
            'status': 'OK',
            'message': 'MirrorFit Backend funcionando!',
            'version': '1.0.0'
        })
'''
    
    with open("virtual_tryon/views.py", "w") as f:
        f.write(views_content)
    
    # urls.py da app
    app_urls_content = '''from django.urls import path
from .views import TryOnAPIView, HealthCheckView

urlpatterns = [
    path('try-on/', TryOnAPIView.as_view(), name='try-on'),
    path('health/', HealthCheckView.as_view(), name='health-check'),
]
'''
    
    with open("virtual_tryon/urls.py", "w") as f:
        f.write(app_urls_content)
    
    # apps.py
    apps_content = '''from django.apps import AppConfig

class VirtualTryonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'virtual_tryon'
'''
    
    with open("virtual_tryon/apps.py", "w") as f:
        f.write(apps_content)
    
    print("✅ App virtual_tryon criada!")

def create_frontend_files():
    """Cria arquivos básicos do frontend"""
    print("🌐 Criando arquivos Frontend...")
    
    os.chdir("../frontend")
    
    # index.html básico
    html_content = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MirrorFit - Provador Virtual com IA</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header class="header">
        <div class="container">
            <h1 class="logo">MirrorFit</h1>
            <p class="tagline">Provador Virtual com IA Avançada</p>
        </div>
    </header>

    <main class="main-content">
        <div class="container">
            <section class="upload-section">
                <h2>Faça upload da sua foto</h2>
                <div class="upload-area" id="uploadArea">
                    <div class="upload-content">
                        <p>📸 Clique aqui ou arraste sua foto</p>
                        <small>Formatos aceitos: JPG, PNG (máx. 5MB)</small>
                    </div>
                    <input type="file" id="photoInput" accept="image/*" hidden>
                </div>
            </section>

            <section class="real-clothing-section">
                <div class="real-clothing-banner">
                    <h3>🔥 Novo! Use suas próprias roupas</h3>
                    <p>Faça upload de uma foto do seu Air Force 1, bermuda ou qualquer roupa!</p>
                    <button id="realClothingBtn" class="real-clothing-btn">
                        📸 Upload de Roupa Real
                    </button>
                </div>
            </section>

            <section class="try-on-section">
                <button class="try-on-btn" id="tryOnBtn" disabled>
                    <span class="btn-text">🤖 Experimentar com IA</span>
                </button>
            </section>
        </div>
    </main>

    <script src="script.js"></script>
    <script src="real-clothing-upload.js"></script>
</body>
</html>'''
    
    with open("index.html", "w") as f:
        f.write(html_content)
    
    # CSS básico
    css_content = '''
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

.header {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    padding: 1rem 0;
    text-align: center;
    color: white;
}

.logo {
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}

section {
    background: white;
    margin: 2rem 0;
    padding: 2rem;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.upload-area {
    border: 3px dashed #cbd5e0;
    border-radius: 10px;
    padding: 3rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
}

.upload-area:hover {
    border-color: #667eea;
    background: #f8f9ff;
}

.real-clothing-banner {
    background: linear-gradient(135deg, #ff6b6b, #ffa500);
    color: white;
    padding: 1.5rem;
    border-radius: 12px;
    text-align: center;
}

.real-clothing-btn {
    background: rgba(255, 255, 255, 0.2);
    color: white;
    border: 2px solid white;
    padding: 0.8rem 2rem;
    border-radius: 25px;
    font-weight: bold;
    cursor: pointer;
    margin-top: 1rem;
}

.try-on-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 1rem 3rem;
    font-size: 1.2rem;
    font-weight: bold;
    border-radius: 50px;
    cursor: pointer;
    display: block;
    margin: 0 auto;
}

.try-on-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}
'''
    
    with open("styles.css", "w") as f:
        f.write(css_content)
    
    # JavaScript básico
    js_content = '''
class MirrorFitApp {
    constructor() {
        this.uploadedPhoto = null;
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        const uploadArea = document.getElementById("uploadArea");
        const photoInput = document.getElementById("photoInput");
        const tryOnBtn = document.getElementById("tryOnBtn");

        uploadArea.addEventListener("click", () => photoInput.click());
        photoInput.addEventListener("change", this.handleFileSelect.bind(this));
        tryOnBtn.addEventListener("click", this.tryOnClothes.bind(this));
    }

    handleFileSelect(e) {
        const file = e.target.files[0];
        if (file) {
            this.uploadedPhoto = file;
            document.getElementById("tryOnBtn").disabled = false;
            alert("Foto carregada! Agora você pode experimentar roupas.");
        }
    }

    async tryOnClothes() {
        alert("🤖 IA em desenvolvimento! Em breve você poderá experimentar roupas reais.");
    }
}

// Tornar disponível globalmente
window.mirrorFitApp = new MirrorFitApp();

document.addEventListener("DOMContentLoaded", () => {
    console.log("🚀 MirrorFit carregado!");
});
'''
    
    with open("script.js", "w") as f:
        f.write(js_content)
    
    # real-clothing-upload.js (arquivo vazio por enquanto)
    with open("real-clothing-upload.js", "w") as f:
        f.write("// Upload de roupas reais - Em desenvolvimento")
    
    print("✅ Frontend criado!")

def create_run_scripts():
    """Cria scripts de execução"""
    print("🔧 Criando scripts de execução...")
    
    os.chdir("..")
    
    # Script Windows
    bat_content = '''@echo off
echo 🚀 Iniciando MirrorFit...

cd backend
call venv\\Scripts\\activate.bat
start cmd /k "python manage.py runserver"

timeout /t 3 /nobreak > nul

cd ..\\frontend
start cmd /k "python -m http.server 8080"

echo ✅ MirrorFit rodando!
echo Frontend: http://localhost:8080
echo Backend: http://localhost:8000

timeout /t 2 /nobreak > nul
start http://localhost:8080
'''
    
    with open("run.bat", "w") as f:
        f.write(bat_content)
    
    # Script Linux/Mac
    sh_content = '''#!/bin/bash
echo "🚀 Iniciando MirrorFit..."

cd backend
source venv/bin/activate
python manage.py runserver &
BACKEND_PID=$!

sleep 3

cd ../frontend
python -m http.server 8080 &
FRONTEND_PID=$!

echo "✅ MirrorFit rodando!"
echo "Frontend: http://localhost:8080"
echo "Backend: http://localhost:8000"

sleep 2
if command -v xdg-open > /dev/null; then
    xdg-open http://localhost:8080
elif command -v open > /dev/null; then
    open http://localhost:8080
fi

trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
'''
    
    with open("run.sh", "w") as f:
        f.write(sh_content)
    
    os.chmod("run.sh", 0o755)
    
    print("✅ Scripts criados!")

def main():
    """Função principal de instalação"""
    print("🚀 INSTALAÇÃO RÁPIDA DO MIRRORFIT")
    print("=================================")
    print()
    
    # Verificar Python
    if not check_python():
        print("❌ Instale Python 3.8+ e tente novamente")
        return
    
    # Criar estrutura
    create_project_structure()
    
    # Configurar backend
    if not install_backend():
        print("❌ Erro na configuração do backend")
        return
    
    # Criar arquivos Django
    create_django_files()
    
    # Criar app virtual_tryon
    create_virtual_tryon_app()
    
    # Criar frontend
    create_frontend_files()
    
    # Criar scripts
    create_run_scripts()
    
    print()
    print("🎉 INSTALAÇÃO CONCLUÍDA!")
    print("========================")
    print()
    print("Para executar:")
    if platform.system() == "Windows":
        print("  run.bat")
    else:
        print("  ./run.sh")
    print()
    print("URLs:")
    print("  Frontend: http://localhost:8080")
    print("  Backend: http://localhost:8000")
    print()
    print("✨ Divirta-se com o MirrorFit!")

if __name__ == "__main__":
    main()
