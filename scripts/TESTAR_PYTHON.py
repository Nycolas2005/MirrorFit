"""
🧪 TESTAR SE PYTHON ESTÁ FUNCIONANDO
===================================
Execute: python TESTAR_PYTHON.py
"""

import sys
import subprocess
import platform

def testar_python():
    print("🐍 TESTANDO PYTHON")
    print("=" * 30)
    
    # Versão Python
    version = sys.version_info
    print(f"📋 Python: {version.major}.{version.minor}.{version.micro}")
    print(f"📋 Sistema: {platform.system()}")
    print(f"📋 Arquitetura: {platform.architecture()[0]}")
    
    # Testar pip
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True)
        print("✅ pip funcionando!")
    except:
        print("❌ pip com problema")
    
    # Testar imports básicos
    try:
        import os
        import pathlib
        import webbrowser
        print("✅ Módulos básicos OK!")
    except:
        print("❌ Módulos básicos com problema")
    
    # Testar Django
    try:
        subprocess.run([sys.executable, "-m", "pip", "show", "django"], check=True, capture_output=True)
        print("✅ Django já instalado!")
    except:
        print("⚠️ Django não instalado (será instalado automaticamente)")
    
    print("\n🎯 RESULTADO:")
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python OK para MirrorFit!")
        print("\n🚀 Para executar:")
        print("python EXECUTAR_PYTHON.py")
    else:
        print("❌ Python muito antigo!")
        print("Baixe Python 3.8+ em: https://python.org")

if __name__ == "__main__":
    testar_python()
