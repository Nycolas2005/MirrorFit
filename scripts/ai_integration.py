"""
Integração da IA com o Django - Views atualizadas
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .models import TryOnSession
from .ai_complete_system import process_virtual_tryon
import json
import logging

logger = logging.getLogger(__name__)

class AITryOnView(APIView):
    """
    View principal que usa a IA para processar try-on
    """
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        try:
            print("🎯 Recebendo requisição de try-on...")
            
            # Validar dados
            photo = request.FILES.get('photo')
            clothing_data = request.data.get('clothing')
            
            if not photo:
                return Response({
                    'success': False,
                    'error': 'Foto é obrigatória'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if not clothing_data:
                return Response({
                    'success': False,
                    'error': 'Seleção de roupas é obrigatória'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Parse clothing data
            if isinstance(clothing_data, str):
                clothing_data = json.loads(clothing_data)
            
            print(f"📝 Roupas selecionadas: {clothing_data}")
            
            # Criar sessão
            session = TryOnSession.objects.create(
                original_photo=photo,
                selected_clothing=clothing_data,
                status='processing'
            )
            
            print(f"💾 Sessão criada: {session.id}")
            
            # Processar com IA
            result = process_virtual_tryon(
                image_path=session.original_photo.path,
                selected_clothing=clothing_data,
                session_id=str(session.id)
            )
            
            if result['success']:
                # Atualizar sessão com sucesso
                session.status = 'completed'
                session.result_photo = result['result_path']
                session.save()
                
                print("✅ Try-on processado com sucesso!")
                
                return Response({
                    'success': True,
                    'session_id': str(session.id),
                    'result_image_url': request.build_absolute_uri(f'/media/{result["result_path"]}'),
                    'ai_analysis': result['body_analysis'],
                    'message': 'Roupas aplicadas com sucesso usando IA!'
                })
            else:
                # Atualizar sessão com erro
                session.status = 'failed'
                session.save()
                
                print(f"❌ Erro no processamento: {result['error']}")
                
                return Response({
                    'success': False,
                    'error': result['error']
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            logger.error(f"Erro na view de try-on: {str(e)}")
            return Response({
                'success': False,
                'error': 'Erro interno do servidor'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AIAnalysisView(APIView):
    """
    View para análise corporal sem aplicar roupas
    """
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        try:
            photo = request.FILES.get('photo')
            if not photo:
                return Response({
                    'success': False,
                    'error': 'Foto é obrigatória'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Salvar foto temporariamente
            temp_path = f'/tmp/analysis_{photo.name}'
            with open(temp_path, 'wb') as f:
                for chunk in photo.chunks():
                    f.write(chunk)
            
            # Analisar com IA
            from .ai_complete_system import MirrorFitAI
            ai = MirrorFitAI()
            analysis = ai.analyze_photo(temp_path)
            
            return Response({
                'success': True,
                'analysis': {
                    'body_measurements': analysis['body_measurements'],
                    'landmarks_detected': len(analysis['body_landmarks']),
                    'face_detected': analysis['face_data'] is not None,
                    'image_dimensions': analysis['image_dimensions']
                }
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

print("🤖 Sistema de IA MirrorFit carregado!")
print("📋 Funcionalidades disponíveis:")
print("   ✅ Detecção corporal com MediaPipe")
print("   ✅ Análise facial")
print("   ✅ Cálculo de medidas corporais")
print("   ✅ Aplicação virtual de roupas")
print("   ✅ Sombreamento e texturas realistas")
print("   ✅ Integração completa com Django")
