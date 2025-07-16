"""
🐍 EXECUTAR MIRRORFIT COM PYTHON - WINDOWS
==========================================
Execute este arquivo: python EXECUTAR_PYTHON.py
"""

import os
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def print_titulo():
    print("""
    🐍 MIRRORFIT - EXECUÇÃO PYTHON WINDOWS
    =====================================
    """)

def verificar_python():
    """Verifica se Python está funcionando"""
    print("🔍 Verificando Python...")
    
    try:
        version = sys.version_info
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} encontrado!")
        
        if version.major >= 3 and version.minor >= 8:
            print("✅ Versão do Python OK!")
            return True
        else:
            print("❌ Python muito antigo! Precisa 3.8+")
            return False
    except:
        print("❌ Erro ao verificar Python")
        return False

def criar_estrutura():
    """Cria estrutura básica do projeto"""
    print("\n📁 Criando estrutura do projeto...")
    
    # Criar pastas
    pastas = [
        "MirrorFit-Python",
        "MirrorFit-Python/backend", 
        "MirrorFit-Python/frontend",
        "MirrorFit-Python/media"
    ]
    
    for pasta in pastas:
        Path(pasta).mkdir(parents=True, exist_ok=True)
        print(f"  📂 {pasta}")
    
    print("✅ Estrutura criada!")
    return True

def instalar_django():
    """Instala Django e dependências"""
    print("\n🔧 Instalando Django...")
    
    os.chdir("MirrorFit-Python/backend")
    
    # Criar ambiente virtual
    print("Criando ambiente virtual...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Ambiente virtual criado!")
    except:
        print("❌ Erro ao criar ambiente virtual")
        return False
    
    # Ativar ambiente virtual e instalar
    if os.name == 'nt':  # Windows
        pip_path = "venv\\Scripts\\pip.exe"
        python_path = "venv\\Scripts\\python.exe"
    else:
        pip_path = "venv/bin/pip"
        python_path = "venv/bin/python"
    
    print("Instalando Django...")
    try:
        subprocess.run([pip_path, "install", "django", "djangorestframework", "django-cors-headers", "pillow"], check=True)
        print("✅ Django instalado!")
        return True
    except:
        print("❌ Erro ao instalar Django")
        return False

def criar_projeto_django():
    """Cria projeto Django"""
    print("\n⚙️ Criando projeto Django...")
    
    if os.name == 'nt':  # Windows
        python_path = "venv\\Scripts\\python.exe"
        django_admin = "venv\\Scripts\\django-admin.exe"
    else:
        python_path = "venv/bin/python"
        django_admin = "venv/bin/django-admin"
    
    # Criar projeto
    try:
        subprocess.run([django_admin, "startproject", "mirrorfit", "."], check=True)
        subprocess.run([python_path, "manage.py", "startapp", "virtual_tryon"], check=True)
        print("✅ Projeto Django criado!")
    except:
        print("❌ Erro ao criar projeto Django")
        return False
    
    # Configurar settings.py
    settings_content = '''
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'mirrorfit-python-key-123'
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
    
    with open("mirrorfit/settings.py", "w", encoding='utf-8') as f:
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
    
    with open("mirrorfit/urls.py", "w", encoding='utf-8') as f:
        f.write(urls_content)
    
    # Views da app
    views_content = '''from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class TryOnAPIView(APIView):
    def post(self, request):
        return Response({
            'success': True,
            'message': '🐍 MirrorFit Python funcionando! IA em desenvolvimento.',
            'platform': 'Python Windows'
        })

class HealthView(APIView):
    def get(self, request):
        return Response({
            'status': 'OK', 
            'message': 'Backend Python funcionando!',
            'platform': 'Python Windows'
        })
'''
    
    with open("virtual_tryon/views.py", "w", encoding='utf-8') as f:
        f.write(views_content)
    
    # URLs da app
    app_urls_content = '''from django.urls import path
from .views import TryOnAPIView, HealthView

urlpatterns = [
    path('try-on/', TryOnAPIView.as_view()),
    path('health/', HealthView.as_view()),
]
'''
    
    with open("virtual_tryon/urls.py", "w", encoding='utf-8') as f:
        f.write(app_urls_content)
    
    # Migrar banco
    try:
        subprocess.run([python_path, "manage.py", "migrate"], check=True)
        print("✅ Banco de dados configurado!")
    except:
        print("❌ Erro ao migrar banco")
        return False
    
    return True

def criar_frontend():
    """Cria frontend HTML"""
    print("\n🌐 Criando frontend...")
    
    os.chdir("../frontend")
    
    html_content = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🐍 MirrorFit Python</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #3776ab 0%, #ffd43b 100%);
            min-height: 100vh;
            color: #333;
        }
        .container { max-width: 900px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; color: white; padding: 2rem 0; }
        .logo { font-size: 3rem; font-weight: bold; margin-bottom: 0.5rem; }
        .python-badge { 
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
            border: 3px dashed #3776ab; 
            padding: 3rem; 
            text-align: center; 
            border-radius: 10px; 
            cursor: pointer; 
            transition: all 0.3s ease; 
        }
        .upload-area:hover { background: #f0f8ff; }
        .btn { 
            background: linear-gradient(135deg, #3776ab 0%, #ffd43b 100%); 
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
        .python-info {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #3776ab;
        }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1 class="logo">🐍 MirrorFit Python</h1>
            <p>Provador Virtual com IA - Executado com Python</p>
            <span class="python-badge">✅ Rodando com Python</span>
        </header>

        <section class="section">
            <h2>📸 Upload da Foto</h2>
            <div class="upload-area" onclick="document.getElementById('photo').click()">
                <p>🖱️ Clique para enviar sua foto</p>
                <small>JPG, PNG (máx. 5MB) - Python</small>
                <input type="file" id="photo" accept="image/*" style="display: none;">
            </div>
        </section>

        <section class="section">
            <h2>🧪 Testar Sistema Python</h2>
            <button class="btn" onclick="testBackend()">🔧 Testar Backend</button>
            <button class="btn" onclick="testAI()">🤖 Testar IA</button>
            <div id="status" class="status"></div>
        </section>

        <section class="section">
            <h2>🐍 Informações Python</h2>
            <div class="python-info">
                <p><strong>🔧 Como foi executado:</strong></p>
                <p>✅ python EXECUTAR_PYTHON.py</p>
                <p>✅ Django instalado automaticamente</p>
                <p>✅ Servidor rodando com Python</p>
                <p>✅ Frontend servido com Python</p>
            </div>
            <button class="btn" onclick="showPythonInfo()">ℹ️ Mais sobre Python</button>
        </section>
    </div>

    <script>
        let uploadedPhoto = null;

        document.getElementById('photo').addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                uploadedPhoto = file;
                document.querySelector('.upload-area p').textContent = '✅ Foto: ' + file.name;
                showStatus('📸 Foto carregada com Python!', 'success');
            }
        });

        async function testBackend() {
            showStatus('🔄 Testando backend Python...', 'success');
            
            try {
                const response = await fetch('http://localhost:8000/api/health/');
                const data = await response.json();
                
                if (data.status === 'OK') {
                    showStatus('✅ Backend Python OK! ' + data.message, 'success');
                } else {
                    showStatus('⚠️ Backend com problemas', 'error');
                }
            } catch (error) {
                showStatus('❌ Backend não rodando. Verifique o terminal Python.', 'error');
            }
        }

        async function testAI() {
            if (!uploadedPhoto) {
                showStatus('❌ Carregue uma foto primeiro!', 'error');
                return;
            }

            showStatus('🤖 Testando IA Python...', 'success');

            const formData = new FormData();
            formData.append('photo', uploadedPhoto);

            try {
                const response = await fetch('http://localhost:8000/api/try-on/', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (data.success) {
                    showStatus('🎉 IA Python funcionando! ' + data.message, 'success');
                } else {
                    showStatus('❌ Erro na IA', 'error');
                }
            } catch (error) {
                showStatus('❌ Erro de conexão com IA Python', 'error');
            }
        }

        function showPythonInfo() {
            showStatus('🐍 MirrorFit executado 100% com Python! Django + HTTP Server', 'success');
        }

        function showStatus(message, type) {
            const status = document.getElementById('status');
            status.textContent = message;
            status.className = 'status ' + type;
            status.style.display = 'block';
        }

        console.log('🐍 MirrorFit Python carregado!');
    </script>
</body>
</html>'''
    
    with open("index.html", "w", encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Frontend criado!")
    return True

def executar_servidores():
    """Executa os servidores Django e Frontend"""
    print("\n🚀 Iniciando servidores...")
    
    # Voltar para pasta backend
    os.chdir("../backend")
    
    if os.name == 'nt':  # Windows
        python_path = "venv\\Scripts\\python.exe"
    else:
        python_path = "venv/bin/python"
    
    print("🔧 Iniciando Django...")
    
    # Iniciar Django em processo separado
    django_process = subprocess.Popen([python_path, "manage.py", "runserver"])
    
    print("✅ Django iniciado!")
    print("⏳ Aguardando Django inicializar...")
    time.sleep(5)
    
    # Iniciar frontend
    print("🌐 Iniciando Frontend...")
    os.chdir("../frontend")
    
    frontend_process = subprocess.Popen([sys.executable, "-m", "http.server", "8080"])
    
    print("✅ Frontend iniciado!")
    print("⏳ Aguardando Frontend...")
    time.sleep(3)
    
    # Abrir navegador
    print("🌐 Abrindo navegador...")
    webbrowser.open("http://localhost:8080")
    
    print("\n🎉 MIRRORFIT PYTHON RODANDO!")
    print("=" * 40)
    print("🌐 Frontend: http://localhost:8080")
    print("🔧 Backend:  http://localhost:8000")
    print("\n⏹️ Para parar: Pressione Ctrl+C")
    
    try:
        # Aguardar até usuário parar
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Parando servidores...")
        django_process.terminate()
        frontend_process.terminate()
        print("✅ Servidores parados!")

def main():
    """Função principal"""
    print_titulo()
    
    print("🐍 Executando MirrorFit com Python...")
    print("=" * 50)
    
    # Verificar Python
    if not verificar_python():
        input("\nPressione Enter para sair...")
        return
    
    # Verificar se já existe projeto
    if Path("MirrorFit-Python").exists():
        print("\n📁 Projeto já existe!")
        resposta = input("Deseja recriar? (s/n): ").lower()
        if resposta != 's':
            print("Usando projeto existente...")
            os.chdir("MirrorFit-Python/backend")
            if os.name == 'nt':
                python_path = "venv\\Scripts\\python.exe"
            else:
                python_path = "venv/bin/python"
            
            print("🚀 Iniciando Django...")
            django_process = subprocess.Popen([python_path, "manage.py", "runserver"])
            time.sleep(3)
            
            os.chdir("../frontend")
            print("🌐 Iniciando Frontend...")
            frontend_process = subprocess.Popen([sys.executable, "-m", "http.server", "8080"])
            time.sleep(2)
            
            webbrowser.open("http://localhost:8080")
            print("\n✅ MirrorFit rodando!")
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                django_process.terminate()
                frontend_process.terminate()
                print("\n✅ Parado!")
            return
    
    # Instalação completa
    steps = [
        (criar_estrutura, "Criando estrutura"),
        (instalar_django, "Instalando Django"),
        (criar_projeto_django, "Configurando Django"),
        (criar_frontend, "Criando frontend"),
        (executar_servidores, "Executando servidores")
    ]
    
    for step_func, step_name in steps:
        print(f"\n📋 {step_name}...")
        if not step_func():
            print(f"❌ Erro em: {step_name}")
            input("Pressione Enter para sair...")
            return

if __name__ == "__main__":
    main()
