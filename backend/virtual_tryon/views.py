from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse
from .models import TryOnSession
from .ai_engine import process_virtual_tryon_ai
import json
import logging
import uuid
import os
import base64
import io
from PIL import Image
import numpy as np

logger = logging.getLogger(__name__)

class TryOnAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        try:
            print("🎯 Recebendo requisição de try-on com IA...")
            
            # Validar dados recebidos
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
            
            # Parse clothing data se for string
            if isinstance(clothing_data, str):
                clothing_data = json.loads(clothing_data)
            
            print(f"📝 Roupas selecionadas: {clothing_data}")
            
            # Filtrar apenas roupas selecionadas
            selected_items = {k: v for k, v in clothing_data.items() if v is not None}
            
            if not selected_items:
                return Response({
                    'success': False,
                    'error': 'Nenhuma roupa foi selecionada'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Criar sessão
            session = TryOnSession.objects.create(
                original_photo=photo,
                selected_clothing=selected_items,
                status='processing'
            )
            
            print(f"💾 Sessão criada: {session.id}")
            
            # Processar com IA REAL
            result = process_virtual_tryon_ai(
                image_path=session.original_photo.path,
                selected_clothing=selected_items,
                session_id=str(session.id)
            )
            
            if result['success']:
                # Salvar resultado
                result_path = self.save_result_image(result['image_data'], session.id)
                
                session.status = 'completed'
                session.result_photo = result_path
                session.save()
                
                print("✅ Try-on processado com IA real!")
                
                return Response({
                    'success': True,
                    'session_id': str(session.id),
                    'result_image_url': request.build_absolute_uri(f'/media/{result_path}'),
                    'ai_analysis': {
                        'body_landmarks_detected': result['body_landmarks'],
                        'face_detected': result['face_detected'],
                        'applied_items': result['applied_items'],
                        'processing_method': 'Real AI with MediaPipe + OpenCV'
                    },
                    'message': '🤖 Roupas aplicadas com IA real!'
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
                'error': f'Erro interno do servidor: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def save_result_image(self, image_data, session_id):
        """
        Salva imagem resultado no storage
        """
        filename = f'ai_results/mirrorfit_result_{session_id}.png'
        path = default_storage.save(filename, ContentFile(image_data))
        return path

class HealthCheckView(APIView):
    def get(self, request):
        # Testar se IA está funcionando
        try:
            import cv2
            import mediapipe as mp
            import numpy as np
            
            ai_status = "✅ IA Real Funcionando"
            ai_components = {
                'opencv': cv2.__version__,
                'mediapipe': mp.__version__,
                'numpy': np.__version__
            }
        except ImportError as e:
            ai_status = f"❌ IA com problema: {str(e)}"
            ai_components = {}
        
        return Response({
            'status': 'OK',
            'message': 'MirrorFit Backend com IA Real!',
            'version': '2.0.0',
            'ai_status': ai_status,
            'ai_components': ai_components,
            'features': {
                'real_ai_processing': True,
                'body_detection': True,
                'clothing_application': True,
                'image_enhancement': True
            }
        })

class TestAIView(APIView):
    """
    Endpoint para testar IA sem upload
    """
    def get(self, request):
        try:
            from .ai_engine import MirrorFitAI
            
            # Testar inicialização da IA
            ai = MirrorFitAI()
            
            return Response({
                'success': True,
                'message': '🤖 IA MirrorFit inicializada com sucesso!',
                'ai_ready': True
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Erro na IA: {str(e)}',
                'ai_ready': False
            })
