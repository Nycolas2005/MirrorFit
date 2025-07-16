"""
🐍 VERSÃO SUPER SIMPLES - SÓ EXECUTAR
====================================
Execute: python EXECUTAR_SIMPLES.py
"""

import os
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def main():
    print("🐍 MIRRORFIT PYTHON - VERSÃO SIMPLES")
    print("=" * 40)
    
    # Criar pasta
    Path("MirrorFit-Simples").mkdir(exist_ok=True)
    os.chdir("MirrorFit-Simples")
    
    # Instalar Django
    print("📦 Instalando Django...")
    subprocess.run([sys.executable, "-m", "pip", "install", "django", "djangorestframework", "django-cors-headers"], check=True)
    
    # Criar projeto
    print("⚙️ Criando projeto...")
    subprocess.run([sys.executable, "-m", "django", "startproject", "mirrorfit", "."], check=True)
    
    # Settings básico
    settings = '''
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'simples-key'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
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
'''
    
    with open("mirrorfit/settings.py", "w") as f:
        f.write(settings)
    
    # Migrar
    subprocess.run([sys.executable, "manage.py", "migrate"], check=True)
    
    # HTML simples
    html = '''<!DOCTYPE html>
<html>
<head>
    <title>🐍 MirrorFit Python Simples</title>
    <style>
        body { font-family: Arial; background: #3776ab; color: white; text-align: center; padding: 50px; }
        .container { background: white; color: black; padding: 30px; border-radius: 10px; max-width: 600px; margin: 0 auto; }
        .btn { background: #3776ab; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🐍 MirrorFit Python</h1>
        <p>Versão simples executada com Python!</p>
        <button class="btn" onclick="alert('🎉 Python funcionando!')">Testar</button>
        <p><strong>Como executar:</strong></p>
        <p>python EXECUTAR_SIMPLES.py</p>
    </div>
</body>
</html>'''
    
    with open("index.html", "w") as f:
        f.write(html)
    
    print("🚀 Iniciando...")
    
    # Iniciar Django
    django_process = subprocess.Popen([sys.executable, "manage.py", "runserver"])
    time.sleep(3)
    
    # Iniciar frontend
    frontend_process = subprocess.Popen([sys.executable, "-m", "http.server", "8080"])
    time.sleep(2)
    
    # Abrir navegador
    webbrowser.open("http://localhost:8080")
    
    print("✅ Rodando!")
    print("Frontend: http://localhost:8080")
    print("Backend: http://localhost:8000")
    print("Pressione Ctrl+C para parar")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        django_process.terminate()
        frontend_process.terminate()
        print("✅ Parado!")

if __name__ == "__main__":
    main()
