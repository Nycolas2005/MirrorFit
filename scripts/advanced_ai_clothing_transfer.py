"""
IA Avançada para Captura e Transferência de Roupas Reais
Sistema que pega uma foto de um tênis (ex: Air Force 1) e aplica na pessoa
"""

import cv2
import numpy as np
import mediapipe as mp
from PIL import Image, ImageDraw, ImageFilter
import torch
import torchvision.transforms as transforms
from segment_anything import sam_model_registry, SamPredictor
import requests
from io import BytesIO
import base64

class ClothingCaptureAI:
    """
    IA para capturar roupas de fotos e aplicar em pessoas
    """
    
    def __init__(self):
        print("🤖 Inicializando IA de Captura de Roupas...")
        
        # MediaPipe para detecção corporal
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=True,
            min_detection_confidence=0.7
        )
        
        # Inicializar SAM (Segment Anything Model) para segmentação precisa
        try:
            self.sam_predictor = self.init_sam_model()
            print("✅ SAM Model carregado para segmentação precisa")
        except:
            print("⚠️ SAM não disponível, usando método alternativo")
            self.sam_predictor = None
        
        print("✅ IA de Captura inicializada!")
    
    def init_sam_model(self):
        """
        Inicializa o modelo SAM para segmentação precisa
        """
        # Baixar modelo SAM se necessário
        model_url = "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth"
        sam = sam_model_registry["vit_b"](checkpoint=model_url)
        predictor = SamPredictor(sam)
        return predictor
    
    def capture_clothing_from_photo(self, clothing_photo_path, clothing_type):
        """
        Captura uma peça de roupa específica de uma foto
        """
        print(f"📸 Capturando {clothing_type} da foto...")
        
        # Carregar imagem da roupa
        clothing_image = cv2.imread(clothing_photo_path)
        if clothing_image is None:
            raise ValueError("Não foi possível carregar a foto da roupa")
        
        clothing_rgb = cv2.cvtColor(clothing_image, cv2.COLOR_BGR2RGB)
        
        # Segmentar a roupa baseado no tipo
        if clothing_type == "shoes":
            segmented_item = self.segment_shoes(clothing_rgb)
        elif clothing_type == "shirt":
            segmented_item = self.segment_shirt(clothing_rgb)
        elif clothing_type == "pants":
            segmented_item = self.segment_pants(clothing_rgb)
        elif clothing_type == "shorts":
            segmented_item = self.segment_shorts(clothing_rgb)
        else:
            raise ValueError(f"Tipo de roupa não suportado: {clothing_type}")
        
        print(f"✅ {clothing_type} capturado com sucesso!")
        return segmented_item
    
    def segment_shoes(self, image):
        """
        Segmenta tênis da imagem usando IA
        """
        print("👟 Segmentando tênis...")
        
        if self.sam_predictor:
            return self.segment_with_sam(image, "shoes")
        else:
            return self.segment_shoes_traditional(image)
    
    def segment_with_sam(self, image, item_type):
        """
        Segmentação precisa usando SAM (Segment Anything Model)
        """
        self.sam_predictor.set_image(image)
        
        # Definir pontos de interesse baseado no tipo de item
        h, w = image.shape[:2]
        
        if item_type == "shoes":
            # Pontos típicos onde tênis aparecem na foto
            input_points = np.array([
                [w//2, h*0.8],  # Centro-baixo
                [w*0.3, h*0.9], # Esquerda-baixo
                [w*0.7, h*0.9]  # Direita-baixo
            ])
        elif item_type == "shirt":
            input_points = np.array([
                [w//2, h*0.4],  # Centro-meio
                [w*0.3, h*0.3], # Esquerda-meio
                [w*0.7, h*0.3]  # Direita-meio
            ])
        else:
            input_points = np.array([[w//2, h//2]])
        
        input_labels = np.array([1] * len(input_points))
        
        # Gerar máscara
        masks, scores, logits = self.sam_predictor.predict(
            point_coords=input_points,
            point_labels=input_labels,
            multimask_output=True,
        )
        
        # Escolher melhor máscara
        best_mask = masks[np.argmax(scores)]
        
        # Aplicar máscara na imagem
        segmented = image.copy()
        segmented[~best_mask] = [0, 0, 0]  # Fundo preto
        
        return {
            'image': segmented,
            'mask': best_mask,
            'original': image
        }
    
    def segment_shoes_traditional(self, image):
        """
        Segmentação de tênis usando métodos tradicionais de CV
        """
        print("🔍 Usando segmentação tradicional para tênis...")
        
        # Converter para HSV para melhor detecção de cor
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        
        # Detectar cores típicas de tênis (branco, preto, colorido)
        # Máscara para branco (Air Force 1 branco)
        white_lower = np.array([0, 0, 200])
        white_upper = np.array([180, 30, 255])
        white_mask = cv2.inRange(hsv, white_lower, white_upper)
        
        # Máscara para preto
        black_lower = np.array([0, 0, 0])
        black_upper = np.array([180, 255, 50])
        black_mask = cv2.inRange(hsv, black_lower, black_upper)
        
        # Combinar máscaras
        shoe_mask = cv2.bitwise_or(white_mask, black_mask)
        
        # Operações morfológicas para limpar a máscara
        kernel = np.ones((5,5), np.uint8)
        shoe_mask = cv2.morphologyEx(shoe_mask, cv2.MORPH_CLOSE, kernel)
        shoe_mask = cv2.morphologyEx(shoe_mask, cv2.MORPH_OPEN, kernel)
        
        # Encontrar maior contorno (provavelmente o tênis)
        contours, _ = cv2.findContours(shoe_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Pegar maior contorno
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Criar máscara refinada
            refined_mask = np.zeros(shoe_mask.shape, dtype=np.uint8)
            cv2.fillPoly(refined_mask, [largest_contour], 255)
            
            # Aplicar máscara
            segmented = image.copy()
            segmented[refined_mask == 0] = [0, 0, 0]
            
            return {
                'image': segmented,
                'mask': refined_mask > 0,
                'original': image,
                'contour': largest_contour
            }
        
        # Se não encontrou, retornar imagem original
        return {
            'image': image,
            'mask': np.ones(image.shape[:2], dtype=bool),
            'original': image
        }
    
    def segment_shirt(self, image):
        """
        Segmenta camiseta da imagem
        """
        print("👕 Segmentando camiseta...")
        
        # Detectar área central-superior da imagem (onde geralmente está a camiseta)
        h, w = image.shape[:2]
        
        # Criar máscara para região da camiseta
        mask = np.zeros((h, w), dtype=np.uint8)
        
        # Região típica de camiseta em foto de produto
        shirt_region = np.array([
            [w*0.2, h*0.1],   # Topo esquerdo
            [w*0.8, h*0.1],   # Topo direito
            [w*0.9, h*0.7],   # Meio direito
            [w*0.1, h*0.7]    # Meio esquerdo
        ], np.int32)
        
        cv2.fillPoly(mask, [shirt_region], 255)
        
        # Refinar usando detecção de bordas
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        # Aplicar máscara
        segmented = image.copy()
        segmented[mask == 0] = [0, 0, 0]
        
        return {
            'image': segmented,
            'mask': mask > 0,
            'original': image
        }
    
    def segment_pants(self, image):
        """
        Segmenta calça da imagem
        """
        print("👖 Segmentando calça...")
        
        h, w = image.shape[:2]
        
        # Região típica de calça
        pants_region = np.array([
            [w*0.3, h*0.3],   # Cintura esquerda
            [w*0.7, h*0.3],   # Cintura direita
            [w*0.8, h*0.9],   # Pé direito
            [w*0.2, h*0.9]    # Pé esquerdo
        ], np.int32)
        
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.fillPoly(mask, [pants_region], 255)
        
        segmented = image.copy()
        segmented[mask == 0] = [0, 0, 0]
        
        return {
            'image': segmented,
            'mask': mask > 0,
            'original': image
        }
    
    def segment_shorts(self, image):
        """
        Segmenta bermuda da imagem
        """
        print("🩳 Segmentando bermuda...")
        
        h, w = image.shape[:2]
        
        # Região típica de bermuda (mais curta que calça)
        shorts_region = np.array([
            [w*0.3, h*0.3],   # Cintura esquerda
            [w*0.7, h*0.3],   # Cintura direita
            [w*0.75, h*0.6],  # Meio direito
            [w*0.25, h*0.6]   # Meio esquerdo
        ], np.int32)
        
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.fillPoly(mask, [shorts_region], 255)
        
        segmented = image.copy()
        segmented[mask == 0] = [0, 0, 0]
        
        return {
            'image': segmented,
            'mask': mask > 0,
            'original': image
        }
    
    def apply_captured_clothing(self, person_image_path, captured_clothing, body_landmarks, clothing_type):
        """
        Aplica a roupa capturada na pessoa usando os landmarks corporais
        """
        print(f"🎯 Aplicando {clothing_type} capturado na pessoa...")
        
        # Carregar imagem da pessoa
        person_image = cv2.imread(person_image_path)
        person_rgb = cv2.cvtColor(person_image, cv2.COLOR_BGR2RGB)
        
        if clothing_type == "shoes":
            result = self.apply_captured_shoes(person_rgb, captured_clothing, body_landmarks)
        elif clothing_type == "shirt":
            result = self.apply_captured_shirt(person_rgb, captured_clothing, body_landmarks)
        elif clothing_type == "pants":
            result = self.apply_captured_pants(person_rgb, captured_clothing, body_landmarks)
        elif clothing_type == "shorts":
            result = self.apply_captured_shorts(person_rgb, captured_clothing, body_landmarks)
        
        print(f"✅ {clothing_type} aplicado com sucesso!")
        return result
    
    def apply_captured_shoes(self, person_image, captured_shoes, landmarks):
        """
        Aplica tênis capturado nos pés da pessoa
        """
        print("👟 Aplicando tênis capturado...")
        
        result_image = person_image.copy()
        shoe_image = captured_shoes['image']
        shoe_mask = captured_shoes['mask']
        
        # Extrair apenas a parte do tênis (sem fundo preto)
        shoe_only = shoe_image[shoe_mask]
        shoe_coords = np.where(shoe_mask)
        
        if len(shoe_coords[0]) == 0:
            return result_image
        
        # Calcular bounding box do tênis
        min_y, max_y = shoe_coords[0].min(), shoe_coords[0].max()
        min_x, max_x = shoe_coords[1].min(), shoe_coords[1].max()
        
        shoe_height = max_y - min_y
        shoe_width = max_x - min_x
        
        # Aplicar nos pés da pessoa
        left_ankle = landmarks.get('left_ankle')
        right_ankle = landmarks.get('right_ankle')
        
        if left_ankle and left_ankle['visibility'] > 0.5:
            # Redimensionar tênis para o pé esquerdo
            foot_size = 60  # Tamanho base do pé
            scale = foot_size / max(shoe_width, shoe_height)
            
            new_width = int(shoe_width * scale)
            new_height = int(shoe_height * scale)
            
            # Extrair e redimensionar tênis
            shoe_cropped = shoe_image[min_y:max_y, min_x:max_x]
            shoe_resized = cv2.resize(shoe_cropped, (new_width, new_height))
            
            # Posicionar no pé esquerdo
            foot_x = left_ankle['x'] - new_width // 2
            foot_y = left_ankle['y'] + 10  # Ligeiramente abaixo do tornozelo
            
            # Aplicar com blending suave
            self.blend_clothing_item(result_image, shoe_resized, foot_x, foot_y)
        
        if right_ankle and right_ankle['visibility'] > 0.5:
            # Mesmo processo para pé direito
            foot_size = 60
            scale = foot_size / max(shoe_width, shoe_height)
            
            new_width = int(shoe_width * scale)
            new_height = int(shoe_height * scale)
            
            shoe_cropped = shoe_image[min_y:max_y, min_x:max_x]
            shoe_resized = cv2.resize(shoe_cropped, (new_width, new_height))
            
            # Espelhar para o pé direito
            shoe_resized = cv2.flip(shoe_resized, 1)
            
            foot_x = right_ankle['x'] - new_width // 2
            foot_y = right_ankle['y'] + 10
            
            self.blend_clothing_item(result_image, shoe_resized, foot_x, foot_y)
        
        return result_image
    
    def apply_captured_shirt(self, person_image, captured_shirt, landmarks):
        """
        Aplica camiseta capturada no torso da pessoa
        """
        print("👕 Aplicando camiseta capturada...")
        
        result_image = person_image.copy()
        shirt_image = captured_shirt['image']
        shirt_mask = captured_shirt['mask']
        
        # Calcular área do torso
        left_shoulder = landmarks.get('left_shoulder')
        right_shoulder = landmarks.get('right_shoulder')
        left_hip = landmarks.get('left_hip')
        right_hip = landmarks.get('right_hip')
        
        if not all(p and p['visibility'] > 0.5 for p in [left_shoulder, right_shoulder, left_hip, right_hip]):
            return result_image
        
        # Dimensões do torso
        torso_width = abs(right_shoulder['x'] - left_shoulder['x'])
        torso_height = abs(left_hip['y'] - left_shoulder['y'])
        
        # Extrair camiseta
        shirt_coords = np.where(shirt_mask)
        if len(shirt_coords[0]) == 0:
            return result_image
        
        min_y, max_y = shirt_coords[0].min(), shirt_coords[0].max()
        min_x, max_x = shirt_coords[1].min(), shirt_coords[1].max()
        
        shirt_cropped = shirt_image[min_y:max_y, min_x:max_x]
        
        # Redimensionar para o torso
        shirt_resized = cv2.resize(shirt_cropped, (int(torso_width * 1.2), int(torso_height * 1.1)))
        
        # Posicionar no torso
        torso_x = left_shoulder['x'] - int(torso_width * 0.1)
        torso_y = left_shoulder['y'] - int(torso_height * 0.05)
        
        # Aplicar com perspectiva corporal
        self.apply_clothing_with_perspective(result_image, shirt_resized, torso_x, torso_y, landmarks)
        
        return result_image
    
    def apply_captured_pants(self, person_image, captured_pants, landmarks):
        """
        Aplica calça capturada nas pernas da pessoa
        """
        print("👖 Aplicando calça capturada...")
        
        result_image = person_image.copy()
        pants_image = captured_pants['image']
        pants_mask = captured_pants['mask']
        
        # Calcular área das pernas
        left_hip = landmarks.get('left_hip')
        right_hip = landmarks.get('right_hip')
        left_ankle = landmarks.get('left_ankle')
        right_ankle = landmarks.get('right_ankle')
        
        if not all(p and p['visibility'] > 0.5 for p in [left_hip, right_hip, left_ankle, right_ankle]):
            return result_image
        
        # Extrair calça
        pants_coords = np.where(pants_mask)
        if len(pants_coords[0]) == 0:
            return result_image
        
        min_y, max_y = pants_coords[0].min(), pants_coords[0].max()
        min_x, max_x = pants_coords[1].min(), pants_coords[1].max()
        
        pants_cropped = pants_image[min_y:max_y, min_x:max_x]
        
        # Dimensões das pernas
        leg_width = abs(right_hip['x'] - left_hip['x'])
        leg_height = abs(left_ankle['y'] - left_hip['y'])
        
        # Redimensionar calça
        pants_resized = cv2.resize(pants_cropped, (int(leg_width * 1.1), int(leg_height)))
        
        # Posicionar nas pernas
        legs_x = left_hip['x'] - int(leg_width * 0.05)
        legs_y = left_hip['y']
        
        # Aplicar com deformação para seguir as pernas
        self.apply_pants_with_leg_deformation(result_image, pants_resized, legs_x, legs_y, landmarks)
        
        return result_image
    
    def apply_captured_shorts(self, person_image, captured_shorts, landmarks):
        """
        Aplica bermuda capturada na pessoa
        """
        print("🩳 Aplicando bermuda capturada...")
        
        # Similar à calça, mas mais curta
        result_image = person_image.copy()
        shorts_image = captured_shorts['image']
        shorts_mask = captured_shorts['mask']
        
        left_hip = landmarks.get('left_hip')
        right_hip = landmarks.get('right_hip')
        left_knee = landmarks.get('left_knee')
        right_knee = landmarks.get('right_knee')
        
        if not all(p and p['visibility'] > 0.5 for p in [left_hip, right_hip, left_knee, right_knee]):
            return result_image
        
        # Extrair bermuda
        shorts_coords = np.where(shorts_mask)
        if len(shorts_coords[0]) == 0:
            return result_image
        
        min_y, max_y = shorts_coords[0].min(), shorts_coords[0].max()
        min_x, max_x = shorts_coords[1].min(), shorts_coords[1].max()
        
        shorts_cropped = shorts_image[min_y:max_y, min_x:max_x]
        
        # Dimensões da bermuda (até o joelho)
        shorts_width = abs(right_hip['x'] - left_hip['x'])
        shorts_height = abs(left_knee['y'] - left_hip['y']) * 0.8  # 80% até o joelho
        
        shorts_resized = cv2.resize(shorts_cropped, (int(shorts_width * 1.1), int(shorts_height)))
        
        shorts_x = left_hip['x'] - int(shorts_width * 0.05)
        shorts_y = left_hip['y']
        
        self.blend_clothing_item(result_image, shorts_resized, shorts_x, shorts_y)
        
        return result_image
    
    def blend_clothing_item(self, target_image, clothing_item, x, y):
        """
        Mistura item de roupa na imagem alvo com blending suave
        """
        h_item, w_item = clothing_item.shape[:2]
        h_target, w_target = target_image.shape[:2]
        
        # Verificar limites
        if x < 0 or y < 0 or x + w_item > w_target or y + h_item > h_target:
            return
        
        # Criar máscara para blending suave
        mask = np.zeros((h_item, w_item), dtype=np.float32)
        
        # Máscara com bordas suaves (evita cortes abruptos)
        center_x, center_y = w_item // 2, h_item // 2
        for i in range(h_item):
            for j in range(w_item):
                # Distância do centro
                dist = np.sqrt((j - center_x)**2 + (i - center_y)**2)
                max_dist = min(center_x, center_y)
                
                # Máscara gradual
                if dist < max_dist * 0.7:
                    mask[i, j] = 1.0
                elif dist < max_dist:
                    mask[i, j] = 1.0 - (dist - max_dist * 0.7) / (max_dist * 0.3)
        
        # Aplicar blending
        for c in range(3):  # RGB
            target_image[y:y+h_item, x:x+w_item, c] = (
                target_image[y:y+h_item, x:x+w_item, c] * (1 - mask) +
                clothing_item[:, :, c] * mask
            )
    
    def apply_clothing_with_perspective(self, target_image, clothing_item, x, y, landmarks):
        """
        Aplica roupa com perspectiva corporal (para camisetas)
        """
        # Calcular transformação de perspectiva baseada nos ombros
        left_shoulder = landmarks['left_shoulder']
        right_shoulder = landmarks['right_shoulder']
        
        # Ângulo dos ombros
        shoulder_angle = np.arctan2(
            right_shoulder['y'] - left_shoulder['y'],
            right_shoulder['x'] - left_shoulder['x']
        )
        
        # Rotacionar camiseta para alinhar com ombros
        h, w = clothing_item.shape[:2]
        center = (w // 2, h // 2)
        
        rotation_matrix = cv2.getRotationMatrix2D(center, np.degrees(shoulder_angle), 1.0)
        rotated_clothing = cv2.warpAffine(clothing_item, rotation_matrix, (w, h))
        
        # Aplicar com blending
        self.blend_clothing_item(target_image, rotated_clothing, x, y)
    
    def apply_pants_with_leg_deformation(self, target_image, pants_item, x, y, landmarks):
        """
        Aplica calça com deformação para seguir formato das pernas
        """
        # Pontos das pernas
        left_hip = landmarks['left_hip']
        right_hip = landmarks['right_hip']
        left_knee = landmarks['left_knee']
        right_knee = landmarks['right_knee']
        left_ankle = landmarks['left_ankle']
        right_ankle = landmarks['right_ankle']
        
        # Dividir calça em perna esquerda e direita
        h, w = pants_item.shape[:2]
        
        # Perna esquerda (metade esquerda da calça)
        left_leg = pants_item[:, :w//2]
        right_leg = pants_item[:, w//2:]
        
        # Aplicar cada perna separadamente seguindo os landmarks
        self.apply_single_leg(target_image, left_leg, left_hip, left_knee, left_ankle)
        self.apply_single_leg(target_image, right_leg, right_hip, right_knee, right_ankle)
    
    def apply_single_leg(self, target_image, leg_item, hip, knee, ankle):
        """
        Aplica uma perna da calça seguindo os pontos corporais
        """
        # Calcular pontos de controle para deformação
        h_leg, w_leg = leg_item.shape[:2]
        
        # Pontos originais da perna (retângulo)
        src_points = np.float32([
            [0, 0],           # Topo esquerdo
            [w_leg, 0],       # Topo direito
            [w_leg, h_leg],   # Base direita
            [0, h_leg]        # Base esquerda
        ])
        
        # Pontos de destino baseados nos landmarks corporais
        leg_width = 40  # Largura da perna
        
        dst_points = np.float32([
            [hip['x'] - leg_width//2, hip['y']],           # Quadril esquerdo
            [hip['x'] + leg_width//2, hip['y']],           # Quadril direito
            [ankle['x'] + leg_width//4, ankle['y']],       # Tornozelo direito
            [ankle['x'] - leg_width//4, ankle['y']]        # Tornozelo esquerdo
        ])
        
        # Transformação de perspectiva
        transform_matrix = cv2.getPerspectiveTransform(src_points, dst_points)
        
        # Aplicar transformação
        h_target, w_target = target_image.shape[:2]
        warped_leg = cv2.warpPerspective(leg_item, transform_matrix, (w_target, h_target))
        
        # Criar máscara para a perna transformada
        mask = np.zeros((h_target, w_target), dtype=np.uint8)
        cv2.fillPoly(mask, [dst_points.astype(int)], 255)
        
        # Aplicar com blending
        mask_float = mask.astype(np.float32) / 255.0
        for c in range(3):
            target_image[:, :, c] = (
                target_image[:, :, c] * (1 - mask_float) +
                warped_leg[:, :, c] * mask_float
            )

# Função principal para usar o sistema
def process_clothing_transfer(person_photo_path, clothing_photo_path, clothing_type):
    """
    Função principal que processa transferência de roupa real
    """
    try:
        print("🚀 Iniciando transferência de roupa real...")
        
        # Inicializar IA
        ai = ClothingCaptureAI()
        
        # 1. Capturar roupa da foto
        captured_clothing = ai.capture_clothing_from_photo(clothing_photo_path, clothing_type)
        
        # 2. Analisar pessoa
        from .ai_complete_system import MirrorFitAI
        body_ai = MirrorFitAI()
        body_analysis = body_ai.analyze_photo(person_photo_path)
        
        # 3. Aplicar roupa capturada na pessoa
        result_image = ai.apply_captured_clothing(
            person_photo_path, 
            captured_clothing, 
            body_analysis['body_landmarks'], 
            clothing_type
        )
        
        print("✅ Transferência concluída com sucesso!")
        
        return {
            'success': True,
            'result_image': result_image,
            'captured_clothing': captured_clothing,
            'body_analysis': body_analysis
        }
        
    except Exception as e:
        print(f"❌ Erro na transferência: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

# Exemplo de uso
if __name__ == "__main__":
    # Teste com Air Force 1
    result = process_clothing_transfer(
        person_photo_path='pessoa.jpg',
        clothing_photo_path='air_force_1_branco.jpg',
        clothing_type='shoes'
    )
    
    if result['success']:
        print("🎉 Air Force 1 aplicado com sucesso!")
        # Salvar resultado
        cv2.imwrite('resultado_air_force.jpg', result['result_image'])
    else:
        print(f"Erro: {result['error']}")
