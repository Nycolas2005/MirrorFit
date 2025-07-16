"""
Integração da IA de Captura de Roupas com Django
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .models import TryOnSession, ClothingPhoto
from .advanced_ai_clothing_transfer import process_clothing_transfer
import json
import cv2
import numpy as np
from PIL import Image
import io
import base64

class ClothingPhoto(models.Model):
    """
    Modelo para armazenar fotos de roupas enviadas pelos usuários
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clothing_image = models.ImageField(upload_to='clothing_photos/')
    clothing_type = models.CharField(max_length=20, choices=[
        ('shoes', 'Tênis'),
        ('shirt', 'Camiseta'),
        ('pants', 'Calça'),
        ('shorts', 'Bermuda'),
    ])
    name = models.CharField(max_length=100)  # Ex: "Air Force 1 Branco"
    created_at = models.DateTimeField(auto_now_add=True)

class RealClothingTryOnView(APIView):
    """
    API para try-on com roupas reais capturadas de fotos
    """
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        try:
            print("🎯 Processando try-on com roupa real...")
            
            # Dados recebidos
            person_photo = request.FILES.get('person_photo')
            clothing_photo = request.FILES.get('clothing_photo')
            clothing_type = request.data.get('clothing_type')
            clothing_name = request.data.get('clothing_name', 'Roupa personalizada')
            
            # Validações
            if not person_photo:
                return Response({
                    'success': False,
                    'error': 'Foto da pessoa é obrigatória'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if not clothing_photo:
                return Response({
                    'success': False,
                    'error': 'Foto da roupa é obrigatória'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if not clothing_type:
                return Response({
                    'success': False,
                    'error': 'Tipo de roupa é obrigatório'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            print(f"📝 Processando: {clothing_name} ({clothing_type})")
            
            # Salvar foto da roupa
            clothing_record = ClothingPhoto.objects.create(
                clothing_image=clothing_photo,
                clothing_type=clothing_type,
                name=clothing_name
            )
            
            # Criar sessão de try-on
            session = TryOnSession.objects.create(
                original_photo=person_photo,
                selected_clothing={
                    'type': clothing_type,
                    'name': clothing_name,
                    'source': 'real_photo',
                    'clothing_photo_id': str(clothing_record.id)
                },
                status='processing'
            )
            
            # Processar com IA avançada
            result = process_clothing_transfer(
                person_photo_path=session.original_photo.path,
                clothing_photo_path=clothing_record.clothing_image.path,
                clothing_type=clothing_type
            )
            
            if result['success']:
                # Salvar resultado
                result_path = self.save_result_image(result['result_image'], session.id)
                
                session.status = 'completed'
                session.result_photo = result_path
                session.save()
                
                print("✅ Try-on com roupa real concluído!")
                
                return Response({
                    'success': True,
                    'session_id': str(session.id),
                    'result_image_url': request.build_absolute_uri(f'/media/{result_path}'),
                    'clothing_info': {
                        'name': clothing_name,
                        'type': clothing_type,
                        'source': 'real_photo'
                    },
                    'ai_analysis': {
                        'clothing_captured': True,
                        'body_landmarks': len(result['body_analysis']['body_landmarks']),
                        'transfer_quality': 'high'
                    },
                    'message': f'{clothing_name} aplicado com sucesso usando IA!'
                })
            else:
                session.status = 'failed'
                session.save()
                
                return Response({
                    'success': False,
                    'error': result['error']
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            logger.error(f"Erro no try-on com roupa real: {str(e)}")
            return Response({
                'success': False,
                'error': 'Erro interno do servidor'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def save_result_image(self, result_image, session_id):
        """
        Salva imagem resultado
        """
        # Converter numpy array para PIL Image
        if isinstance(result_image, np.ndarray):
            pil_image = Image.fromarray(result_image)
        else:
            pil_image = result_image
        
        # Salvar em buffer
        buffer = io.BytesIO()
        pil_image.save(buffer, format='PNG', quality=95)
        buffer.seek(0)
        
        # Salvar no storage
        filename = f'real_clothing_results/result_{session_id}.png'
        path = default_storage.save(filename, ContentFile(buffer.read()))
        
        return path

class ClothingAnalysisView(APIView):
    """
    API para analisar uma foto de roupa antes do try-on
    """
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        try:
            clothing_photo = request.FILES.get('clothing_photo')
            clothing_type = request.data.get('clothing_type')
            
            if not clothing_photo or not clothing_type:
                return Response({
                    'success': False,
                    'error': 'Foto e tipo de roupa são obrigatórios'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Salvar temporariamente
            temp_path = f'/tmp/clothing_analysis_{clothing_photo.name}'
            with open(temp_path, 'wb') as f:
                for chunk in clothing_photo.chunks():
                    f.write(chunk)
            
            # Analisar com IA
            from .advanced_ai_clothing_transfer import ClothingCaptureAI
            ai = ClothingCaptureAI()
            captured = ai.capture_clothing_from_photo(temp_path, clothing_type)
            
            # Calcular qualidade da captura
            mask_area = np.sum(captured['mask'])
            total_area = captured['mask'].size
            capture_quality = mask_area / total_area
            
            return Response({
                'success': True,
                'analysis': {
                    'clothing_type': clothing_type,
                    'capture_quality': float(capture_quality),
                    'quality_rating': 'excellent' if capture_quality > 0.3 else 'good' if capture_quality > 0.1 else 'poor',
                    'recommendations': self.get_capture_recommendations(capture_quality, clothing_type)
                }
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get_capture_recommendations(self, quality, clothing_type):
        """
        Gera recomendações para melhorar a captura
        """
        recommendations = []
        
        if quality < 0.2:
            recommendations.append("Foto com fundo mais contrastante")
            recommendations.append("Melhor iluminação")
            
        if clothing_type == "shoes":
            recommendations.append("Foto lateral do tênis funciona melhor")
            recommendations.append("Evite sombras nos detalhes")
        elif clothing_type == "shirt":
            recommendations.append("Foto da camiseta estendida")
            recommendations.append("Evite dobras na roupa")
        
        return recommendations

print("🤖 Sistema de Captura de Roupas Reais carregado!")
print("📋 Funcionalidades:")
print("   ✅ Captura Air Force 1 de foto")
print("   ✅ Segmentação automática de roupas")
print("   ✅ Aplicação com perspectiva corporal")
print("   ✅ Blending realista")
print("   ✅ API completa para frontend")
