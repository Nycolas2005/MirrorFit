@echo off
title MirrorFit - Instalacao Windows
color 0A

echo.
echo  ███╗   ███╗██╗██████╗ ██████╗  ██████╗ ██████╗ ███████╗██╗████████╗
echo  ████╗ ████║██║██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔════╝██║╚══██╔══╝
echo  ██╔████╔██║██║██████╔╝██████╔╝██║   ██║██████╔╝█████╗  ██║   ██║   
echo  ██║╚██╔╝██║██║██╔══██╗██╔══██╗██║   ██║██╔══██╗██╔══╝  ██║   ██║   
echo  ██║ ╚═╝ ██║██║██║  ██║██║  ██║╚██████╔╝██║  ██║██║     ██║   ██║   
echo  ╚═╝     ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝   ╚═╝   
echo.
echo                    INSTALACAO AUTOMATICA WINDOWS
echo                    ==============================
echo.

REM Verificar Python
echo [1/6] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python nao encontrado!
    echo.
    echo Baixe Python em: https://python.org/downloads/
    echo Marque "Add Python to PATH" durante a instalacao
    echo.
    pause
    exit /b 1
)
echo ✅ Python encontrado!

REM Verificar pip
echo [2/6] Verificando pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip nao encontrado!
    echo Execute: python -m ensurepip --upgrade
    pause
    exit /b 1
)
echo ✅ pip encontrado!

REM Criar estrutura
echo [3/6] Criando estrutura do projeto...
if not exist "MirrorFit-Windows" mkdir MirrorFit-Windows
cd MirrorFit-Windows

if not exist "backend" mkdir backend
if not exist "frontend" mkdir frontend
if not exist "media" mkdir media

echo ✅ Estrutura criada!

REM Configurar Backend
echo [4/6] Configurando Backend Django...
cd backend

echo Criando ambiente virtual...
python -m venv venv
if %errorlevel% neq 0 (
    echo ❌ Erro ao criar ambiente virtual
    pause
    exit /b 1
)

echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo Criando requirements.txt...
echo Django==4.2.7> requirements.txt
echo djangorestframework==3.14.0>> requirements.txt
echo django-cors-headers==4.3.1>> requirements.txt
echo Pillow==10.1.0>> requirements.txt

echo Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Erro ao instalar dependencias
    pause
    exit /b 1
)

echo ✅ Backend configurado!

REM Criar arquivos Django
echo [5/6] Criando arquivos Django...

REM Criar projeto Django
django-admin startproject mirrorfit .
python manage.py startapp virtual_tryon

REM Configurar settings.py
echo import os> mirrorfit\settings.py
echo from pathlib import Path>> mirrorfit\settings.py
echo.>> mirrorfit\settings.py
echo BASE_DIR = Path(__file__^).resolve(^).parent.parent>> mirrorfit\settings.py
echo SECRET_KEY = 'mirrorfit-windows-dev-key'>> mirrorfit\settings.py
echo DEBUG = True>> mirrorfit\settings.py
echo ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']>> mirrorfit\settings.py
echo.>> mirrorfit\settings.py
echo INSTALLED_APPS = [>> mirrorfit\settings.py
echo     'django.contrib.admin',>> mirrorfit\settings.py
echo     'django.contrib.auth',>> mirrorfit\settings.py
echo     'django.contrib.contenttypes',>> mirrorfit\settings.py
echo     'django.contrib.sessions',>> mirrorfit\settings.py
echo     'django.contrib.messages',>> mirrorfit\settings.py
echo     'django.contrib.staticfiles',>> mirrorfit\settings.py
echo     'corsheaders',>> mirrorfit\settings.py
echo     'rest_framework',>> mirrorfit\settings.py
echo     'virtual_tryon',>> mirrorfit\settings.py
echo ]>> mirrorfit\settings.py
echo.>> mirrorfit\settings.py
echo MIDDLEWARE = [>> mirrorfit\settings.py
echo     'corsheaders.middleware.CorsMiddleware',>> mirrorfit\settings.py
echo     'django.middleware.security.SecurityMiddleware',>> mirrorfit\settings.py
echo     'django.contrib.sessions.middleware.SessionMiddleware',>> mirrorfit\settings.py
echo     'django.middleware.common.CommonMiddleware',>> mirrorfit\settings.py
echo     'django.middleware.csrf.CsrfViewMiddleware',>> mirrorfit\settings.py
echo     'django.contrib.auth.middleware.AuthenticationMiddleware',>> mirrorfit\settings.py
echo     'django.contrib.messages.middleware.MessageMiddleware',>> mirrorfit\settings.py
echo     'django.middleware.clickjacking.XFrameOptionsMiddleware',>> mirrorfit\settings.py
echo ]>> mirrorfit\settings.py
echo.>> mirrorfit\settings.py
echo ROOT_URLCONF = 'mirrorfit.urls'>> mirrorfit\settings.py
echo WSGI_APPLICATION = 'mirrorfit.wsgi.application'>> mirrorfit\settings.py
echo.>> mirrorfit\settings.py
echo DATABASES = {>> mirrorfit\settings.py
echo     'default': {>> mirrorfit\settings.py
echo         'ENGINE': 'django.db.backends.sqlite3',>> mirrorfit\settings.py
echo         'NAME': BASE_DIR / 'db.sqlite3',>> mirrorfit\settings.py
echo     }>> mirrorfit\settings.py
echo }>> mirrorfit\settings.py
echo.>> mirrorfit\settings.py
echo LANGUAGE_CODE = 'pt-br'>> mirrorfit\settings.py
echo TIME_ZONE = 'America/Sao_Paulo'>> mirrorfit\settings.py
echo USE_I18N = True>> mirrorfit\settings.py
echo USE_TZ = True>> mirrorfit\settings.py
echo.>> mirrorfit\settings.py
echo STATIC_URL = '/static/'>> mirrorfit\settings.py
echo MEDIA_URL = '/media/'>> mirrorfit\settings.py
echo MEDIA_ROOT = os.path.join(BASE_DIR, 'media'^)>> mirrorfit\settings.py
echo.>> mirrorfit\settings.py
echo CORS_ALLOW_ALL_ORIGINS = True>> mirrorfit\settings.py
echo CORS_ALLOW_CREDENTIALS = True>> mirrorfit\settings.py
echo.>> mirrorfit\settings.py
echo REST_FRAMEWORK = {>> mirrorfit\settings.py
echo     'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],>> mirrorfit\settings.py
echo }>> mirrorfit\settings.py

REM Configurar URLs
echo from django.contrib import admin> mirrorfit\urls.py
echo from django.urls import path, include>> mirrorfit\urls.py
echo from django.conf import settings>> mirrorfit\urls.py
echo from django.conf.urls.static import static>> mirrorfit\urls.py
echo.>> mirrorfit\urls.py
echo urlpatterns = [>> mirrorfit\urls.py
echo     path('admin/', admin.site.urls^),>> mirrorfit\urls.py
echo     path('api/', include('virtual_tryon.urls'^)^),>> mirrorfit\urls.py
echo ]>> mirrorfit\urls.py
echo.>> mirrorfit\urls.py
echo if settings.DEBUG:>> mirrorfit\urls.py
echo     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT^)>> mirrorfit\urls.py

REM Configurar App
echo from rest_framework.views import APIView> virtual_tryon\views.py
echo from rest_framework.response import Response>> virtual_tryon\views.py
echo from rest_framework import status>> virtual_tryon\views.py
echo.>> virtual_tryon\views.py
echo class TryOnAPIView(APIView^):>> virtual_tryon\views.py
echo     def post(self, request^):>> virtual_tryon\views.py
echo         return Response({>> virtual_tryon\views.py
echo             'success': True,>> virtual_tryon\views.py
echo             'message': '🤖 MirrorFit Windows funcionando! IA em desenvolvimento.',>> virtual_tryon\views.py
echo             'session_id': 'windows-demo-123'>> virtual_tryon\views.py
echo         }^)>> virtual_tryon\views.py
echo.>> virtual_tryon\views.py
echo class HealthView(APIView^):>> virtual_tryon\views.py
echo     def get(self, request^):>> virtual_tryon\views.py
echo         return Response({'status': 'OK', 'message': 'Backend Windows funcionando!'}^)>> virtual_tryon\views.py

echo from django.urls import path> virtual_tryon\urls.py
echo from .views import TryOnAPIView, HealthView>> virtual_tryon\urls.py
echo.>> virtual_tryon\urls.py
echo urlpatterns = [>> virtual_tryon\urls.py
echo     path('try-on/', TryOnAPIView.as_view(^)^),>> virtual_tryon\urls.py
echo     path('health/', HealthView.as_view(^)^),>> virtual_tryon\urls.py
echo ]>> virtual_tryon\urls.py

echo Migrando banco de dados...
python manage.py migrate

echo ✅ Django configurado!

REM Criar Frontend
echo [6/6] Criando Frontend...
cd ..\frontend

echo ^<!DOCTYPE html^>> index.html
echo ^<html lang="pt-BR"^>>> index.html
echo ^<head^>>> index.html
echo     ^<meta charset="UTF-8"^>>> index.html
echo     ^<meta name="viewport" content="width=device-width, initial-scale=1.0"^>>> index.html
echo     ^<title^>MirrorFit Windows - Provador Virtual^</title^>>> index.html
echo     ^<style^>>> index.html
echo         * { margin: 0; padding: 0; box-sizing: border-box; }>> index.html
echo         body { >> index.html
echo             font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; >> index.html
echo             background: linear-gradient(135deg, #667eea 0%%, #764ba2 100%%^); >> index.html
echo             min-height: 100vh; >> index.html
echo             color: #333; >> index.html
echo         }>> index.html
echo         .container { max-width: 900px; margin: 0 auto; padding: 20px; }>> index.html
echo         .header { text-align: center; color: white; padding: 2rem 0; }>> index.html
echo         .logo { font-size: 3rem; font-weight: bold; margin-bottom: 0.5rem; }>> index.html
echo         .section { >> index.html
echo             background: white; >> index.html
echo             margin: 2rem 0; >> index.html
echo             padding: 2rem; >> index.html
echo             border-radius: 15px; >> index.html
echo             box-shadow: 0 10px 30px rgba(0,0,0,0.1^); >> index.html
echo         }>> index.html
echo         .upload-area { >> index.html
echo             border: 3px dashed #ccc; >> index.html
echo             padding: 3rem; >> index.html
echo             text-align: center; >> index.html
echo             border-radius: 10px; >> index.html
echo             cursor: pointer; >> index.html
echo             transition: all 0.3s ease; >> index.html
echo         }>> index.html
echo         .upload-area:hover { border-color: #667eea; background: #f8f9ff; }>> index.html
echo         .btn { >> index.html
echo             background: linear-gradient(135deg, #667eea 0%%, #764ba2 100%%^); >> index.html
echo             color: white; >> index.html
echo             border: none; >> index.html
echo             padding: 1rem 2rem; >> index.html
echo             border-radius: 25px; >> index.html
echo             cursor: pointer; >> index.html
echo             font-size: 1.1rem; >> index.html
echo             font-weight: bold; >> index.html
echo             display: block; >> index.html
echo             margin: 1rem auto; >> index.html
echo             transition: transform 0.3s ease; >> index.html
echo         }>> index.html
echo         .btn:hover { transform: translateY(-2px^); }>> index.html
echo         .status { >> index.html
echo             padding: 1rem; >> index.html
echo             margin: 1rem 0; >> index.html
echo             border-radius: 8px; >> index.html
echo             text-align: center; >> index.html
echo             display: none; >> index.html
echo         }>> index.html
echo         .status.success { background: #d4edda; color: #155724; }>> index.html
echo         .status.error { background: #f8d7da; color: #721c24; }>> index.html
echo         .windows-badge { >> index.html
echo             background: #0078d4; >> index.html
echo             color: white; >> index.html
echo             padding: 0.5rem 1rem; >> index.html
echo             border-radius: 20px; >> index.html
echo             font-size: 0.9rem; >> index.html
echo             display: inline-block; >> index.html
echo             margin: 0.5rem; >> index.html
echo         }>> index.html
echo     ^</style^>>> index.html
echo ^</head^>>> index.html
echo ^<body^>>> index.html
echo     ^<div class="container"^>>> index.html
echo         ^<header class="header"^>>> index.html
echo             ^<h1 class="logo"^>🪟 MirrorFit Windows^</h1^>>> index.html
echo             ^<p^>Provador Virtual com IA - Versao Windows^</p^>>> index.html
echo             ^<span class="windows-badge"^>✅ Otimizado para Windows^</span^>>> index.html
echo         ^</header^>>> index.html
echo.>> index.html
echo         ^<section class="section"^>>> index.html
echo             ^<h2^>📸 Faça upload da sua foto^</h2^>>> index.html
echo             ^<div class="upload-area" onclick="document.getElementById('photo'^).click(^)"^>>> index.html
echo                 ^<p^>🖱️ Clique aqui para enviar sua foto^</p^>>> index.html
echo                 ^<small^>JPG, PNG (max. 5MB^) - Windows^</small^>>> index.html
echo                 ^<input type="file" id="photo" accept="image/*" style="display: none;"^>>> index.html
echo             ^</div^>>> index.html
echo         ^</section^>>> index.html
echo.>> index.html
echo         ^<section class="section"^>>> index.html
echo             ^<h2^>🤖 Testar Sistema^</h2^>>> index.html
echo             ^<p^>Clique para testar se o backend Windows esta funcionando:^</p^>>> index.html
echo             ^<button class="btn" onclick="testBackend(^)"^>🧪 Testar Backend^</button^>>> index.html
echo             ^<button class="btn" onclick="testAI(^)"^>🤖 Testar IA^</button^>>> index.html
echo             ^<div id="status" class="status"^>^</div^>>> index.html
echo         ^</section^>>> index.html
echo.>> index.html
echo         ^<section class="section"^>>> index.html
echo             ^<h2^>🔥 Upload de Roupa Real^</h2^>>> index.html
echo             ^<p^>Em breve: Fotografe seu Air Force 1 e veja como fica em voce!^</p^>>> index.html
echo             ^<button class="btn" onclick="comingSoon(^)"^>📸 Upload Roupa Real^</button^>>> index.html
echo         ^</section^>>> index.html
echo     ^</div^>>> index.html
echo.>> index.html
echo     ^<script^>>> index.html
echo         let uploadedPhoto = null;>> index.html
echo.>> index.html
echo         document.getElementById('photo'^).addEventListener('change', function(e^) {>> index.html
echo             const file = e.target.files[0];>> index.html
echo             if (file^) {>> index.html
echo                 uploadedPhoto = file;>> index.html
echo                 document.querySelector('.upload-area p'^).textContent = '✅ Foto carregada: ' + file.name;>> index.html
echo                 showStatus('📸 Foto carregada com sucesso no Windows!', 'success'^);>> index.html
echo             }>> index.html
echo         }^);>> index.html
echo.>> index.html
echo         async function testBackend(^) {>> index.html
echo             showStatus('🔄 Testando backend Windows...', 'success'^);>> index.html
echo             >> index.html
echo             try {>> index.html
echo                 const response = await fetch('http://localhost:8000/api/health/'^);>> index.html
echo                 const data = await response.json(^);>> index.html
echo                 >> index.html
echo                 if (data.status === 'OK'^) {>> index.html
echo                     showStatus('✅ Backend Windows funcionando! ' + data.message, 'success'^);>> index.html
echo                 } else {>> index.html
echo                     showStatus('⚠️ Backend com problemas', 'error'^);>> index.html
echo                 }>> index.html
echo             } catch (error^) {>> index.html
echo                 showStatus('❌ Backend nao esta rodando. Execute: INICIAR_MIRRORFIT.bat', 'error'^);>> index.html
echo             }>> index.html
echo         }>> index.html
echo.>> index.html
echo         async function testAI(^) {>> index.html
echo             if (!uploadedPhoto^) {>> index.html
echo                 showStatus('❌ Carregue uma foto primeiro!', 'error'^);>> index.html
echo                 return;>> index.html
echo             }>> index.html
echo.>> index.html
echo             showStatus('🤖 Testando IA Windows...', 'success'^);>> index.html
echo.>> index.html
echo             const formData = new FormData(^);>> index.html
echo             formData.append('photo', uploadedPhoto^);>> index.html
echo.>> index.html
echo             try {>> index.html
echo                 const response = await fetch('http://localhost:8000/api/try-on/', {>> index.html
echo                     method: 'POST',>> index.html
echo                     body: formData>> index.html
echo                 }^);>> index.html
echo.>> index.html
echo                 const data = await response.json(^);>> index.html
echo.>> index.html
echo                 if (data.success^) {>> index.html
echo                     showStatus('🎉 IA Windows funcionando! ' + data.message, 'success'^);>> index.html
echo                 } else {>> index.html
echo                     showStatus('❌ Erro na IA: ' + data.error, 'error'^);>> index.html
echo                 }>> index.html
echo             } catch (error^) {>> index.html
echo                 showStatus('❌ Erro de conexao com IA', 'error'^);>> index.html
echo             }>> index.html
echo         }>> index.html
echo.>> index.html
echo         function comingSoon(^) {>> index.html
echo             showStatus('🔥 Em desenvolvimento! Logo voce podera fotografar roupas reais!', 'success'^);>> index.html
echo         }>> index.html
echo.>> index.html
echo         function showStatus(message, type^) {>> index.html
echo             const status = document.getElementById('status'^);>> index.html
echo             status.textContent = message;>> index.html
echo             status.className = 'status ' + type;>> index.html
echo             status.style.display = 'block';>> index.html
echo         }>> index.html
echo.>> index.html
echo         console.log('🪟 MirrorFit Windows carregado!'^);>> index.html
echo     ^</script^>>> index.html
echo ^</body^>>> index.html
echo ^</html^>>> index.html

echo ✅ Frontend criado!

cd ..

echo.
echo ✅ INSTALACAO CONCLUIDA COM SUCESSO!
echo ====================================
echo.
echo 📁 Projeto criado em: MirrorFit-Windows\
echo.
echo 🚀 Para executar, use um dos arquivos:
echo    INICIAR_MIRRORFIT.bat
echo    PARAR_MIRRORFIT.bat
echo.
echo 🌐 URLs:
echo    Frontend: http://localhost:8080
echo    Backend:  http://localhost:8000
echo.
echo ✅ 100%% Windows!
echo ✅ Sem erros de Linux!
echo ✅ Pronto para usar!
echo.
pause
