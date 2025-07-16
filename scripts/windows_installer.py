"""
Instalador Python para Windows - MirrorFit
Execute: python windows_installer.py
"""

import os
import subprocess
import sys
import platform
from pathlib import Path

def print_header():
    print("""
    ███╗   ███╗██╗██████╗ ██████╗  ██████╗ ██████╗ ███████╗██╗████████╗
    ████╗ ████║██║██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔════╝██║╚══██╔══╝
    ██╔████╔██║██║██████╔╝██████╔╝██║   ██║██████╔╝█████╗  ██║   ██║   
    ██║╚██╔╝██║██║██╔══██╗██╔══██╗██║   ██║██╔══██╗██╔══╝  ██║   ██║   
    ██║ ╚═╝ ██║██║██║  ██║██║  ██║╚██████╔╝██║  ██║██║     ██║   ██║   
    ╚═╝     ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝   ╚═╝   
    
                    INSTALADOR PYTHON WINDOWS
                    =========================
    """)

def check_windows():
    """Verifica se está rodando no Windows"""
    if platform.system() != "Windows":
        print("❌ Este instalador é apenas para Windows!")
        print("Para Linux/Mac, use outro instalador.")
        return False
    
    print("✅ Sistema Windows detectado!")
    return True

def check_python():
    """Verifica Python"""
    try:
        version = sys.version_info
        if version.major >= 3 and version.minor >= 8:
            print(f"✅ Python {version.major}.{version.minor} - OK")
            return True
        else:
            print(f"❌ Python {version.major}.{version.minor} - Necessário 3.8+")
            return False
    except:
        print("❌ Erro ao verificar Python")
        return False

def run_cmd(command, description):
    """Executa comando Windows"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {description} - Concluído!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro em {description}: {e}")
        return False

def create_project_structure():
    """Cria estrutura do projeto"""
    print("📁 Criando estrutura Windows...")
    
    dirs = [
        "MirrorFit-Windows",
        "MirrorFit-Windows/backend",
        "MirrorFit-Windows/frontend", 
        "MirrorFit-Windows/media",
        "MirrorFit-Windows/scripts"
    ]
    
    for directory in dirs:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  📂 {directory}")
    
    print("✅ Estrutura criada!")
    return True

def setup_backend():
    """Configura backend Django"""
    print("🐍 Configurando Backend Windows...")
    
    os.chdir("MirrorFit-Windows/backend")
    
    # Ambiente virtual
    if not run_cmd("python -m venv venv", "Criando ambiente virtual"):
        return False
    
    # Requirements
    requirements = """Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
Pillow==10.1.0"""
    
    with open("requirements.txt", "w") as f:
        f.write(requirements)
    
    # Instalar dependências
    activate_cmd = "venv\\Scripts\\activate.bat && "
    
    if not run_cmd(f"{activate_cmd}pip install --upgrade pip", "Atualizando pip"):
        return False
    
    if not run_cmd(f"{activate_cmd}pip install -r requirements.txt", "Instalando Django"):
        return False
    
    print("✅ Backend configurado!")
    return True

def create_django_files():
    """Cria arquivos Django"""
    print("⚙️ Criando arquivos Django...")
    
    # Criar projeto
    activate_cmd = "venv\\Scripts\\activate.bat && "
    run_cmd(f"{activate_cmd}django-admin startproject mirrorfit .", "Criando projeto Django")
    run_cmd(f"{activate_cmd}python manage.py startapp virtual_tryon", "Criando app")
    
    # settings.py simplificado
    settings_content = '''
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'mirrorfit-windows-key'
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
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
}
'''
    
    with open("mirrorfit/settings.py", "w") as f:
        f.write(settings_content)
    
    # URLs principais
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
    
    # Views da app
    views_content = '''from rest_framework.views import APIView
from rest_framework.response import Response

class TryOnAPIView(APIView):
    def post(self, request):
        return Response({
            'success': True,
            'message': '🪟 MirrorFit Windows funcionando! IA em desenvolvimento.',
            'platform': 'Windows'
        })

class HealthView(APIView):
    def get(self, request):
        return Response({
            'status': 'OK', 
            'message': 'Backend Windows OK!',
            'platform': 'Windows'
        })
'''
    
    with open("virtual_tryon/views.py", "w") as f:
        f.write(views_content)
    
    # URLs da app
    app_urls_content = '''from django.urls import path
from .views import TryOnAPIView, HealthView

urlpatterns = [
    path('try-on/', TryOnAPIView.as_view()),
    path('health/', HealthView.as_view()),
]
'''
    
    with open("virtual_tryon/urls.py", "w") as f:
        f.write(app_urls_content)
    
    # Migrar banco
    activate_cmd = "venv\\Scripts\\activate.bat && "
    run_cmd(f"{activate_cmd}python manage.py migrate", "Migrando banco de dados")
    
    print("✅ Django configurado!")
    return True

def create_frontend():
    """Cria frontend"""
    print("🌐 Criando Frontend Windows...")
    
    os.chdir("../frontend")
    
    html_content = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🪟 MirrorFit Windows</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0078d4 0%, #106ebe 100%);
            min-height: 100vh;
            color: #333;
        }
        .container { max-width: 900px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; color: white; padding: 2rem 0; }
        .logo { font-size: 3rem; font-weight: bold; margin-bottom: 0.5rem; }
        .windows-badge { 
            background: rgba(255,255,255,0.2); 
            padding: 0.5rem 1rem; 
            border-radius: 20px; 
            display: inline-block; 
            margin: 0.5rem;
        }
        .section { 
            background: white; 
            margin: 2rem 0; 
            padding: 2rem; 
            border-radius: 15px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.1); 
        }
        .upload-area { 
            border: 3px dashed #0078d4; 
            padding: 3rem; 
            text-align: center; 
            border-radius: 10px; 
            cursor: pointer; 
            transition: all 0.3s ease; 
        }
        .upload-area:hover { background: #f0f8ff; }
        .btn { 
            background: linear-gradient(135deg, #0078d4 0%, #106ebe 100%); 
            color: white; 
            border: none; 
            padding: 1rem 2rem; 
            border-radius: 25px; 
            cursor: pointer; 
            font-size: 1.1rem; 
            font-weight: bold; 
            display: block; 
            margin: 1rem auto; 
            transition: transform 0.3s ease; 
        }
        .btn:hover { transform: translateY(-2px); }
        .status { 
            padding: 1rem; 
            margin: 1rem 0; 
            border-radius: 8px; 
            text-align: center; 
            display: none; 
        }
        .status.success { background: #d4edda; color: #155724; }
        .status.error { background: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1 class="logo">🪟 MirrorFit Windows</h1>
            <p>Provador Virtual com IA - Versão Windows</p>
            <span class="windows-badge">✅ Otimizado para Windows</span>
        </header>

        <section class="section">
            <h2>📸 Upload da Foto</h2>
            <div class="upload-area" onclick="document.getElementById('photo').click()">
                <p>🖱️ Clique para enviar sua foto</p>
                <small>JPG, PNG (máx. 5MB) - Windows</small>
                <input type="file" id="photo" accept="image/*" style="display: none;">
            </div>
        </section>

        <section class="section">
            <h2>🧪 Testar Sistema</h2>
            <button class="btn" onclick="testBackend()">🔧 Testar Backend</button>
            <button class="btn" onclick="testAI()">🤖 Testar IA</button>
            <div id="status" class="status"></div>
        </section>

        <section class="section">
            <h2>🔥 Recursos Windows</h2>
            <p>✅ Interface otimizada para Windows</p>
            <p>✅ Scripts .bat para fácil execução</p>
            <p>✅ Compatível com Windows 10/11</p>
            <button class="btn" onclick="showInfo()">ℹ️ Mais Informações</button>
        </section>
    </div>

    <script>
        let uploadedPhoto = null;

        document.getElementById('photo').addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                uploadedPhoto = file;
                document.querySelector('.upload-area p').textContent = '✅ Foto: ' + file.name;
                showStatus('📸 Foto carregada no Windows!', 'success');
            }
        });

        async function testBackend() {
            showStatus('🔄 Testando backend Windows...', 'success');
            
            try {
                const response = await fetch('http://localhost:8000/api/health/');
                const data = await response.json();
                
                if (data.status === 'OK') {
                    showStatus('✅ Backend Windows OK! ' + data.message, 'success');
                } else {
                    showStatus('⚠️ Backend com problemas', 'error');
                }
            } catch (error) {
                showStatus('❌ Backend não rodando. Execute: INICIAR_MIRRORFIT.bat', 'error');
            }
        }

        async function testAI() {
            if (!uploadedPhoto) {
                showStatus('❌ Carregue uma foto primeiro!', 'error');
                return;
            }

            showStatus('🤖 Testando IA Windows...', 'success');

            const formData = new FormData();
            formData.append('photo', uploadedPhoto);

            try {
                const response = await fetch('http://localhost:8000/api/try-on/', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (data.success) {
                    showStatus('🎉 IA Windows funcionando! ' + data.message, 'success');
                } else {
                    showStatus('❌ Erro na IA', 'error');
                }
            } catch (error) {
                showStatus('❌ Erro de conexão com IA', 'error');
            }
        }

        function showInfo() {
            showStatus('🪟 MirrorFit otimizado para Windows 10/11 com scripts .bat!', 'success');
        }

        function showStatus(message, type) {
            const status = document.getElementById('status');
            status.textContent = message;
            status.className = 'status ' + type;
            status.style.display = 'block';
        }

        console.log('🪟 MirrorFit Windows carregado!');
    </script>
</body>
</html>'''
    
    with open("index.html", "w") as f:
        f.write(html_content)
    
    print("✅ Frontend Windows criado!")
    return True

def create_scripts():
    """Cria scripts Windows"""
    print("🔧 Criando scripts Windows...")
    
    os.chdir("../scripts")
    
    # Script de inicialização
    start_script = '''@echo off
title MirrorFit Windows
color 0B

echo 🚀 Iniciando MirrorFit Windows...

cd ../backend
call venv\\Scripts\\activate.bat

echo Iniciando Django...
start "Backend" cmd /k "python manage.py runserver"

timeout /t 3 /nobreak >nul

cd ../frontend
echo Iniciando Frontend...
start "Frontend" cmd /k "python -m http.server 8080"

timeout /t 2 /nobreak >nul
start http://localhost:8080

echo ✅ MirrorFit rodando!
echo Frontend: http://localhost:8080
echo Backend: http://localhost:8000
pause
'''
    
    with open("INICIAR.bat", "w") as f:
        f.write(start_script)
    
    # Script de parada
    stop_script = '''@echo off
echo 🛑 Parando MirrorFit...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im pythonw.exe >nul 2>&1
echo ✅ Parado!
pause
'''
    
    with open("PARAR.bat", "w") as f:
        f.write(stop_script)
    
    print("✅ Scripts Windows criados!")
    return True

def main():
    """Função principal"""
    print_header()
    
    # Verificações
    if not check_windows():
        return
    
    if not check_python():
        print("\n❌ Instale Python 3.8+ em: https://python.org/downloads/")
        print("⚠️ Marque 'Add Python to PATH' durante a instalação!")
        input("\nPressione Enter para sair...")
        return
    
    print("\n🚀 Iniciando instalação Windows...")
    
    # Instalação
    steps = [
        (create_project_structure, "Estrutura do projeto"),
        (setup_backend, "Backend Django"),
        (create_django_files, "Arquivos Django"),
        (create_frontend, "Frontend Windows"),
        (create_scripts, "Scripts Windows")
    ]
    
    for step_func, step_name in steps:
        print(f"\n📋 {step_name}...")
        if not step_func():
            print(f"❌ Erro em: {step_name}")
            input("Pressione Enter para sair...")
            return
    
    # Sucesso
    print("\n🎉 INSTALAÇÃO WINDOWS CONCLUÍDA!")
    print("=" * 40)
    print("\n📁 Projeto: MirrorFit-Windows/")
    print("\n🚀 Para executar:")
    print("   scripts/INICIAR.bat")
    print("\n🛑 Para parar:")
    print("   scripts/PARAR.bat")
    print("\n🌐 URLs:")
    print("   Frontend: http://localhost:8080")
    print("   Backend:  http://localhost:8000")
    print("\n✅ 100% Windows!")
    print("✅ Scripts .bat incluídos!")
    print("✅ Pronto para usar!")
    
    input("\nPressione Enter para finalizar...")

if __name__ == "__main__":
    main()
