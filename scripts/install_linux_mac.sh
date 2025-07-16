#!/bin/bash

echo "🚀 INSTALAÇÃO AUTOMÁTICA - MirrorFit Linux/Mac"
echo "==============================================="

echo ""
echo "Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado!"
    echo "Instale com: sudo apt install python3 python3-pip (Ubuntu)"
    echo "ou: brew install python3 (Mac)"
    exit 1
fi

echo "✅ Python encontrado!"

echo ""
echo "📥 Baixando instalador..."
curl -o quick_install.py https://raw.githubusercontent.com/seu-repo/mirrorfit/main/quick_install.py

echo ""
echo "🔧 Executando instalação..."
python3 quick_install.py

echo ""
echo "✅ Instalação concluída!"
echo ""
echo "Para executar o MirrorFit:"
echo "  cd mirrorfit-complete"
echo "  ./run.sh"
echo ""
