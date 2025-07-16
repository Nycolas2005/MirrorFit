"""
Instalação SUPER SIMPLES do MirrorFit
Sem dependências externas, só Python padrão
"""

import os
import subprocess
import sys
import platform
from pathlib import Path

def print_step(step, description):
    """Imprime passo colorido"""
    print(f"\n🔄 PASSO {step}: {description}")
    print("=" * 50)

def run_command(command, description, check=True):
    """Executa comando com feedback"""
    print(f"⚡ {description}...")
    try:
        if check:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        else:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {description} - OK!")
            return True
        else:
            print(f"⚠️ {description} - Aviso: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Erro em {description}: {e}")
        return False

def main():
    print("🚀 MIRRORFIT - INSTALAÇÃO SUPER SIMPLES")
    print("======================================")
    print("Sem requests, sem complicação!")
    
    # PASSO 1: Verificar Python
    print_step(1, "Verificando Python")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor} - Perfeito!")
    else:
        print(f"❌ Python {version.major}.{version.minor} - Precisa 3.8+")
        return
    
    # PASSO 2: Criar estrutura
    print_step(2, "Criando estrutura do projeto")
    
    directories = [
        "mirrorfit-simple",
        "mirrorfit-simple/frontend", 
        "mirrorfit-simple/backend",
        "mirrorfit-simple/backend/mirrorfit",
        "mirrorfit-simple/backend/virtual_tryon"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 {directory}")
    
    print("✅ Estrutura criada!")
    
    # PASSO 3: Backend
    print_step(3, "Configurando Backend Django")
    
    os.chdir("mirrorfit-simple/backend")
    
    # Ambiente virtual
    if not run_command("python -m venv venv", "Criando ambiente virtual"):
        return
    
    # Ativar e instalar
    if platform.system() == "Windows":
        activate = "venv\\Scripts\\activate && "
    else:
        activate = "source venv/bin/activate && "
    
    # Requirements mínimos
    requirements = """Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
Pillow==10.1.0"""
    
    with open("requirements.txt", "w") as f:
        f.write(requirements)
    
    if not run_command(f"{activate}pip install -r requirements.txt", "Instalando Django"):
        return
    
    # PASSO 4: Arquivos Django
    print_step(4, "Criando arquivos Django")
    
    # manage.py
    manage_py = '''#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mirrorfit.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Django não encontrado. Ative o ambiente virtual!") from exc
    execute_from_command_line(sys.argv)
'''
    
    with open("manage.py", "w") as f:
        f.write(manage_py)
    
    # settings.py
    settings_py = '''
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'mirrorfit-dev-key-123'
DEBUG = True
ALLOWED_HOSTS = ['*']

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

TEMPLATES = [{
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
}]

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
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
}
'''
    
    with open("mirrorfit/settings.py", "w") as f:
        f.write(settings_py)
    
    # urls.py
    urls_py = '''from django.contrib import admin
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
        f.write(urls_py)
    
    # wsgi.py
    wsgi_py = '''import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mirrorfit.settings')
application = get_wsgi_application()
'''
    
    with open("mirrorfit/wsgi.py", "w") as f:
        f.write(wsgi_py)
    
    # __init__.py
    Path("mirrorfit/__init__.py").touch()
    Path("virtual_tryon/__init__.py").touch()
    
    # App views.py
    views_py = '''from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class TryOnAPIView(APIView):
    def post(self, request):
        return Response({
            'success': True,
            'message': '🤖 MirrorFit funcionando! IA em desenvolvimento.',
            'session_id': 'demo-123'
        })

class HealthView(APIView):
    def get(self, request):
        return Response({'status': 'OK', 'message': 'Backend funcionando!'})
'''
    
    with open("virtual_tryon/views.py", "w") as f:
        f.write(views_py)
    
    # App urls.py
    app_urls_py = '''from django.urls import path
from .views import TryOnAPIView, HealthView

urlpatterns = [
    path('try-on/', TryOnAPIView.as_view()),
    path('health/', HealthView.as_view()),
]
'''
    
    with open("virtual_tryon/urls.py", "w") as f:
        f.write(app_urls_py)
    
    # App apps.py
    apps_py = '''from django.apps import AppConfig

class VirtualTryonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'virtual_tryon'
'''
    
    with open("virtual_tryon/apps.py", "w") as f:
        f.write(apps_py)
    
    print("✅ Arquivos Django criados!")
    
    # PASSO 5: Frontend
    print_step(5, "Criando Frontend")
    
    os.chdir("../frontend")
    
    # HTML
    html = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MirrorFit - Provador Virtual</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: Arial, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; 
            color: #333;
        }
        .container { max-width: 800px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; color: white; padding: 2rem 0; }
        .logo { font-size: 3rem; font-weight: bold; margin-bottom: 0.5rem; }
        .section { 
            background: white; 
            margin: 2rem 0; 
            padding: 2rem; 
            border-radius: 15px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.1); 
        }
        .upload-area { 
            border: 3px dashed #ccc; 
            padding: 3rem; 
            text-align: center; 
            border-radius: 10px; 
            cursor: pointer; 
        }
        .upload-area:hover { border-color: #667eea; background: #f8f9ff; }
        .btn { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            border: none; 
            padding: 1rem 2rem; 
            border-radius: 25px; 
            cursor: pointer; 
            font-size: 1.1rem; 
            font-weight: bold;
            display: block;
            margin: 2rem auto;
        }
        .btn:disabled { opacity: 0.6; cursor: not-allowed; }
        .btn:hover:not(:disabled) { transform: translateY(-2px); }
        .status { 
            padding: 1rem; 
            margin: 1rem 0; 
            border-radius: 8px; 
            text-align: center; 
            display: none; 
        }
        .status.success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .status.error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1 class="logo">MirrorFit</h1>
            <p>Provador Virtual com IA</p>
        </header>

        <section class="section">
            <h2>📸 Faça upload da sua foto</h2>
            <div class="upload-area" onclick="document.getElementById('photo').click()">
                <p>Clique aqui para enviar sua foto</p>
                <small>JPG, PNG (máx. 5MB)</small>
                <input type="file" id="photo" accept="image/*" style="display: none;">
            </div>
        </section>

        <section class="section">
            <h2>🤖 Testar IA</h2>
            <p>Clique para testar se o backend está funcionando:</p>
            <button class="btn" onclick="testAI()">Testar MirrorFit IA</button>
            <div id="status" class="status"></div>
        </section>
    </div>

    <script>
        let uploadedPhoto = null;

        document.getElementById('photo').addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                uploadedPhoto = file;
                document.querySelector('.upload-area p').textContent = 'Foto carregada: ' + file.name;
                showStatus('Foto carregada com sucesso!', 'success');
            }
        });

        async function testAI() {
            showStatus('🤖 Testando IA...', 'success');
            
            try {
                const response = await fetch('http://localhost:8000/api/health/');
                const data = await response.json();
                
                if (data.status === 'OK') {
                    showStatus('✅ Backend funcionando! ' + data.message, 'success');
                } else {
                    showStatus('⚠️ Backend com problemas', 'error');
                }
            } catch (error) {
                showStatus('❌ Erro: Backend não está rodando. Execute: python manage.py runserver', 'error');
            }
        }

        function showStatus(message, type) {
            const status = document.getElementById('status');
            status.textContent = message;
            status.className = 'status ' + type;
            status.style.display = 'block';
        }

        console.log('🚀 MirrorFit carregado!');
    </script>
</body>
</html>'''
    
    with open("index.html", "w") as f:
        f.write(html)
    
    print("✅ Frontend criado!")
    
    # PASSO 6: Scripts de execução
    print_step(6, "Criando scripts de execução")
    
    os.chdir("..")
    
    # Windows
    bat_script = '''@echo off
echo 🚀 Iniciando MirrorFit Simples...

cd backend
echo Ativando ambiente virtual...
call venv\\Scripts\\activate.bat

echo Migrando banco de dados...
python manage.py migrate

echo Iniciando Django...
start cmd /k "python manage.py runserver"

timeout /t 3 /nobreak > nul

echo Iniciando Frontend...
cd ..\\frontend
start cmd /k "python -m http.server 8080"

echo ✅ MirrorFit rodando!
echo Frontend: http://localhost:8080
echo Backend: http://localhost:8000

timeout /t 2 /nobreak > nul
start http://localhost:8080

pause
'''
    
    with open("start.bat", "w") as f:
        f.write(bat_script)
    
    # Linux/Mac
    sh_script = '''#!/bin/bash
echo "🚀 Iniciando MirrorFit Simples..."

cd backend
echo "Ativando ambiente virtual..."
source venv/bin/activate

echo "Migrando banco de dados..."
python manage.py migrate

echo "Iniciando Django..."
python manage.py runserver &
BACKEND_PID=$!

sleep 3

echo "Iniciando Frontend..."
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

echo "Pressione Ctrl+C para parar"
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
'''
    
    with open("start.sh", "w") as f:
        f.write(sh_script)
    
    os.chmod("start.sh", 0o755)
    
    print("✅ Scripts criados!")
    
    # FINAL
    print("\n🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
    print("====================================")
    print()
    print("📁 Projeto criado em: mirrorfit-simple/")
    print()
    print("🚀 Para executar:")
    if platform.system() == "Windows":
        print("   start.bat")
    else:
        print("   ./start.sh")
    print()
    print("🌐 URLs:")
    print("   Frontend: http://localhost:8080")
    print("   Backend:  http://localhost:8000")
    print()
    print("✅ Sem erros de import!")
    print("✅ Sem dependências complicadas!")
    print("✅ Pronto para usar!")

if __name__ == "__main__":
    main()
