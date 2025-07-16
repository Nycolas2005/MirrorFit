"""
Script para testar se a instalação está funcionando
"""

import subprocess
import requests
import time
import sys

def test_backend():
    """Testa se o backend Django está rodando"""
    try:
        response = requests.get("http://localhost:8000", timeout=5)
        return True
    except:
        return False

def test_frontend():
    """Testa se o frontend está rodando"""
    try:
        response = requests.get("http://localhost:8080", timeout=5)
        return True
    except:
        return False

def main():
    print("🧪 TESTANDO INSTALAÇÃO DO MIRRORFIT")
    print("===================================")
    print()
    
    print("🔍 Verificando se os servidores estão rodando...")
    
    # Testar backend
    if test_backend():
        print("✅ Backend Django - OK (http://localhost:8000)")
    else:
        print("❌ Backend Django - Não está rodando")
        print("   Execute: cd backend && python manage.py runserver")
    
    # Testar frontend
    if test_frontend():
        print("✅ Frontend - OK (http://localhost:8080)")
    else:
        print("❌ Frontend - Não está rodando")
        print("   Execute: cd frontend && python -m http.server 8080")
    
    print()
    print("🎯 Para testar completamente:")
    print("1. Acesse http://localhost:8080")
    print("2. Faça upload de uma foto")
    print("3. Teste o upload de roupa real")
    print("4. Clique em 'Experimentar com IA'")

if __name__ == "__main__":
    main()
