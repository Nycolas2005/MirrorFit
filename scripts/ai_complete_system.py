"""
Sistema Completo de IA para MirrorFit
Este script contém toda a implementação da IA para detecção corporal e aplicação virtual de roupas
"""

import cv2
import numpy as np
import mediapipe as mp
from PIL import Image, ImageDraw, ImageFilter
import json
import base64
import io
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

class MirrorFitAI:
    """
    Classe principal da IA do MirrorFit
    Responsável por:
    1. Detectar corpo e rosto na foto
    2. Calcular medidas corporais
    3. Aplicar roupas virtualmente
    """
    
    def __init__(self):
        # Inicializar MediaPipe para detecção de pose
        self.mp_pose = mp.solutions.pose
        self.mp_face = mp.solutions.face_detection
        self.mp_selfie_segmentation = mp.solutions.selfie_segmentation
        
        # Configurar modelos
        self.pose = self.mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=True,
            min_detection_confidence=0.7
        )
        
        self.face_detection = self.mp_face.FaceDetection(
            model_selection=1,  # Modelo para imagens de alta resolução
            min_detection_confidence=0.7
        )
        
        self.segmentation = self.mp_selfie_segmentation.SelfieSegmentation(
            model_selection=1
        )
        
        print("🤖 IA MirrorFit inicializada com sucesso!")
    
    def analyze_photo(self, image_path):
        """
        Analisa a foto do usuário e extrai informações corporais
        """
        print(f"📸 Analisando foto: {image_path}")
        
        # Carregar imagem
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Não foi possível carregar a imagem")
        
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width = image.shape[:2]
        
        # 1. Detectar pose corporal
        pose_results = self.pose.process(image_rgb)
        if not pose_results.pose_landmarks:
            raise ValueError("Não foi possível detectar a pose na imagem. Certifique-se de que a pessoa está visível de corpo inteiro.")
        
        # 2. Detectar rosto
        face_results = self.face_detection.process(image_rgb)
        
        # 3. Segmentação da pessoa
        segmentation_results = self.segmentation.process(image_rgb)
        
        # 4. Extrair dados corporais
        body_data = self.extract_body_measurements(pose_results.pose_landmarks, width, height)
        face_data = self.extract_face_data(face_results, width, height) if face_results.detections else None
        
        analysis_result = {
            'body_landmarks': body_data['landmarks'],
            'body_measurements': body_data['measurements'],
            'face_data': face_data,
            'segmentation_mask': segmentation_results.segmentation_mask,
            'image_dimensions': {'width': width, 'height': height}
        }
        
        print("✅ Análise corporal concluída!")
        print(f"   - Pontos corporais detectados: {len(body_data['landmarks'])}")
        print(f"   - Medidas calculadas: {len(body_data['measurements'])}")
        print(f"   - Rosto detectado: {'Sim' if face_data else 'Não'}")
        
        return analysis_result
    
    def extract_body_measurements(self, pose_landmarks, width, height):
        """
        Extrai medidas corporais precisas dos landmarks
        """
        landmarks = {}
        measurements = {}
        
        # Mapear pontos importantes
        key_points = {
            'nose': self.mp_pose.PoseLandmark.NOSE,
            'left_shoulder': self.mp_pose.PoseLandmark.LEFT_SHOULDER,
            'right_shoulder': self.mp_pose.PoseLandmark.RIGHT_SHOULDER,
            'left_elbow': self.mp_pose.PoseLandmark.LEFT_ELBOW,
            'right_elbow': self.mp_pose.PoseLandmark.RIGHT_ELBOW,
            'left_wrist': self.mp_pose.PoseLandmark.LEFT_WRIST,
            'right_wrist': self.mp_pose.PoseLandmark.RIGHT_WRIST,
            'left_hip': self.mp_pose.PoseLandmark.LEFT_HIP,
            'right_hip': self.mp_pose.PoseLandmark.RIGHT_HIP,
            'left_knee': self.mp_pose.PoseLandmark.LEFT_KNEE,
            'right_knee': self.mp_pose.PoseLandmark.RIGHT_KNEE,
            'left_ankle': self.mp_pose.PoseLandmark.LEFT_ANKLE,
            'right_ankle': self.mp_pose.PoseLandmark.RIGHT_ANKLE,
        }
        
        # Extrair coordenadas dos pontos
        for name, landmark_id in key_points.items():
            landmark = pose_landmarks.landmark[landmark_id]
            landmarks[name] = {
                'x': int(landmark.x * width),
                'y': int(landmark.y * height),
                'z': landmark.z,
                'visibility': landmark.visibility
            }
        
        # Calcular medidas corporais
        if all(landmarks[p]['visibility'] > 0.5 for p in ['left_shoulder', 'right_shoulder']):
            shoulder_width = abs(landmarks['left_shoulder']['x'] - landmarks['right_shoulder']['x'])
            measurements['shoulder_width'] = shoulder_width
        
        if all(landmarks[p]['visibility'] > 0.5 for p in ['left_hip', 'right_hip']):
            hip_width = abs(landmarks['left_hip']['x'] - landmarks['right_hip']['x'])
            measurements['hip_width'] = hip_width
        
        if all(landmarks[p]['visibility'] > 0.5 for p in ['nose', 'left_ankle', 'right_ankle']):
            avg_ankle_y = (landmarks['left_ankle']['y'] + landmarks['right_ankle']['y']) / 2
            body_height = abs(landmarks['nose']['y'] - avg_ankle_y)
            measurements['body_height'] = body_height
        
        if all(landmarks[p]['visibility'] > 0.5 for p in ['left_shoulder', 'left_hip']):
            torso_length = abs(landmarks['left_shoulder']['y'] - landmarks['left_hip']['y'])
            measurements['torso_length'] = torso_length
        
        if all(landmarks[p]['visibility'] > 0.5 for p in ['left_hip', 'left_knee']):
            thigh_length = abs(landmarks['left_hip']['y'] - landmarks['left_knee']['y'])
            measurements['thigh_length'] = thigh_length
        
        return {
            'landmarks': landmarks,
            'measurements': measurements
        }
    
    def extract_face_data(self, face_results, width, height):
        """
        Extrai dados do rosto detectado
        """
        if not face_results.detections:
            return None
        
        detection = face_results.detections[0]
        bbox = detection.location_data.relative_bounding_box
        
        return {
            'bbox': {
                'x': int(bbox.xmin * width),
                'y': int(bbox.ymin * height),
                'width': int(bbox.width * width),
                'height': int(bbox.height * height)
            },
            'confidence': detection.score[0]
        }
    
    def apply_virtual_clothing(self, image_path, body_analysis, selected_clothing):
        """
        Aplica roupas virtuais na imagem usando IA avançada
        """
        print("👕 Aplicando roupas virtuais...")
        
        # Carregar imagem original
        image = cv2.imread(image_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result_image = image_rgb.copy()
        
        landmarks = body_analysis['body_landmarks']
        measurements = body_analysis['body_measurements']
        
        # Aplicar cada tipo de roupa
        if selected_clothing.get('shirt'):
            result_image = self.apply_shirt_ai(result_image, landmarks, selected_clothing['shirt'])
        
        if selected_clothing.get('pants'):
            result_image = self.apply_pants_ai(result_image, landmarks, selected_clothing['pants'])
        elif selected_clothing.get('shorts'):
            result_image = self.apply_shorts_ai(result_image, landmarks, selected_clothing['shorts'])
        
        if selected_clothing.get('shoes'):
            result_image = self.apply_shoes_ai(result_image, landmarks, selected_clothing['shoes'])
        
        print("✅ Roupas aplicadas com sucesso!")
        return result_image
    
    def apply_shirt_ai(self, image, landmarks, shirt_id):
        """
        Aplica camiseta com IA avançada considerando anatomia
        """
        # Definir propriedades das camisetas
        shirt_properties = {
            'shirt1': {'color': (255, 255, 255), 'style': 'basic', 'fit': 'regular'},
            'shirt2': {'color': (40, 40, 40), 'style': 'graphic', 'fit': 'slim'}
        }
        
        props = shirt_properties.get(shirt_id, shirt_properties['shirt1'])
        color = props['color']
        
        # Pontos da camiseta
        left_shoulder = landmarks['left_shoulder']
        right_shoulder = landmarks['right_shoulder']
        left_hip = landmarks['left_hip']
        right_hip = landmarks['right_hip']
        
        # Verificar visibilidade dos pontos
        if not all(p['visibility'] > 0.5 for p in [left_shoulder, right_shoulder, left_hip, right_hip]):
            print("⚠️ Pontos da camiseta não visíveis suficientemente")
            return image
        
        # Calcular pontos da camiseta com ajuste anatômico
        shirt_points = self.calculate_shirt_contour(landmarks, props['fit'])
        
        # Criar máscara da camiseta
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.fillPoly(mask, [shirt_points], 255)
        
        # Aplicar textura e sombreamento
        overlay = image.copy()
        overlay[mask > 0] = color
        
        # Adicionar sombreamento realista
        overlay = self.add_clothing_shading(overlay, mask, landmarks)
        
        # Misturar com a imagem original
        alpha = 0.7
        result = cv2.addWeighted(image, 1-alpha, overlay, alpha, 0)
        
        return result
    
    def calculate_shirt_contour(self, landmarks, fit_type):
        """
        Calcula contorno anatômico da camiseta
        """
        left_shoulder = landmarks['left_shoulder']
        right_shoulder = landmarks['right_shoulder']
        left_hip = landmarks['left_hip']
        right_hip = landmarks['right_hip']
        
        # Ajustar largura baseado no tipo de caimento
        width_multiplier = 1.2 if fit_type == 'regular' else 1.0
        
        # Calcular pontos do contorno
        shoulder_width = abs(right_shoulder['x'] - left_shoulder['x'])
        hip_width = abs(right_hip['x'] - left_hip['x'])
        
        # Pontos da camiseta
        points = np.array([
            # Ombro esquerdo
            [left_shoulder['x'] - int(shoulder_width * 0.1 * width_multiplier), left_shoulder['y']],
            # Ombro direito
            [right_shoulder['x'] + int(shoulder_width * 0.1 * width_multiplier), right_shoulder['y']],
            # Lateral direita
            [right_hip['x'] + int(hip_width * 0.15 * width_multiplier), right_hip['y']],
            # Quadril direito
            [right_hip['x'], right_hip['y'] + 20],
            # Quadril esquerdo
            [left_hip['x'], left_hip['y'] + 20],
            # Lateral esquerda
            [left_shoulder['x'] - int(hip_width * 0.15 * width_multiplier), left_hip['y']],
        ], np.int32)
        
        return points
    
    def apply_pants_ai(self, image, landmarks, pants_id):
        """
        Aplica calça com detecção anatômica precisa
        """
        color = (20, 60, 120)  # Azul jeans
        
        left_hip = landmarks['left_hip']
        right_hip = landmarks['right_hip']
        left_knee = landmarks['left_knee']
        right_knee = landmarks['right_knee']
        left_ankle = landmarks['left_ankle']
        right_ankle = landmarks['right_ankle']
        
        # Verificar visibilidade
        required_points = [left_hip, right_hip, left_knee, right_knee, left_ankle, right_ankle]
        if not all(p['visibility'] > 0.5 for p in required_points):
            print("⚠️ Pontos da calça não visíveis suficientemente")
            return image
        
        # Calcular largura das pernas
        hip_width = abs(right_hip['x'] - left_hip['x'])
        leg_width = int(hip_width * 0.25)
        
        # Perna esquerda
        left_leg_points = np.array([
            [left_hip['x'] - leg_width//2, left_hip['y']],
            [left_hip['x'] + leg_width//2, left_hip['y']],
            [left_knee['x'] + leg_width//3, left_knee['y']],
            [left_ankle['x'] + 15, left_ankle['y']],
            [left_ankle['x'] - 15, left_ankle['y']],
            [left_knee['x'] - leg_width//3, left_knee['y']],
        ], np.int32)
        
        # Perna direita
        right_leg_points = np.array([
            [right_hip['x'] - leg_width//2, right_hip['y']],
            [right_hip['x'] + leg_width//2, right_hip['y']],
            [right_knee['x'] + leg_width//3, right_knee['y']],
            [right_ankle['x'] + 15, right_ankle['y']],
            [right_ankle['x'] - 15, right_ankle['y']],
            [right_knee['x'] - leg_width//3, right_knee['y']],
        ], np.int32)
        
        # Aplicar calça
        overlay = image.copy()
        cv2.fillPoly(overlay, [left_leg_points], color)
        cv2.fillPoly(overlay, [right_leg_points], color)
        
        # Adicionar textura jeans
        overlay = self.add_jeans_texture(overlay, [left_leg_points, right_leg_points])
        
        return cv2.addWeighted(image, 0.3, overlay, 0.7, 0)
    
    def apply_shorts_ai(self, image, landmarks, shorts_id):
        """
        Aplica bermuda com ajuste anatômico
        """
        color = (180, 160, 120)  # Bege
        
        left_hip = landmarks['left_hip']
        right_hip = landmarks['right_hip']
        left_knee = landmarks['left_knee']
        right_knee = landmarks['right_knee']
        
        if not all(p['visibility'] > 0.5 for p in [left_hip, right_hip, left_knee, right_knee]):
            return image
        
        # Calcular pontos da bermuda (até meio da coxa)
        thigh_length = abs(left_knee['y'] - left_hip['y'])
        shorts_length = int(thigh_length * 0.6)  # 60% da coxa
        
        hip_width = abs(right_hip['x'] - left_hip['x'])
        
        shorts_points = np.array([
            [left_hip['x'] - int(hip_width * 0.2), left_hip['y']],
            [right_hip['x'] + int(hip_width * 0.2), right_hip['y']],
            [right_hip['x'] + int(hip_width * 0.15), right_hip['y'] + shorts_length],
            [left_hip['x'] - int(hip_width * 0.15), left_hip['y'] + shorts_length],
        ], np.int32)
        
        overlay = image.copy()
        cv2.fillPoly(overlay, [shorts_points], color)
        
        return cv2.addWeighted(image, 0.3, overlay, 0.7, 0)
    
    def apply_shoes_ai(self, image, landmarks, shoes_id):
        """
        Aplica tênis com detecção precisa dos pés
        """
        shoe_colors = {
            'shoes1': (255, 255, 255),  # Branco
            'shoes2': (50, 50, 50),     # Preto
            'shoes3': (30, 80, 150),    # Azul
        }
        
        color = shoe_colors.get(shoes_id, (128, 128, 128))
        
        left_ankle = landmarks['left_ankle']
        right_ankle = landmarks['right_ankle']
        
        if left_ankle['visibility'] > 0.5:
            # Tênis esquerdo
            shoe_center = (left_ankle['x'], left_ankle['y'] + 25)
            cv2.ellipse(image, shoe_center, (35, 18), 0, 0, 360, color, -1)
            # Sola
            cv2.ellipse(image, (shoe_center[0], shoe_center[1] + 5), (38, 8), 0, 0, 360, (80, 80, 80), -1)
        
        if right_ankle['visibility'] > 0.5:
            # Tênis direito
            shoe_center = (right_ankle['x'], right_ankle['y'] + 25)
            cv2.ellipse(image, shoe_center, (35, 18), 0, 0, 360, color, -1)
            # Sola
            cv2.ellipse(image, (shoe_center[0], shoe_center[1] + 5), (38, 8), 0, 0, 360, (80, 80, 80), -1)
        
        return image
    
    def add_clothing_shading(self, image, mask, landmarks):
        """
        Adiciona sombreamento realista às roupas
        """
        # Criar gradiente de luz baseado na posição dos ombros
        left_shoulder = landmarks['left_shoulder']
        right_shoulder = landmarks['right_shoulder']
        
        # Simular fonte de luz vinda de cima-esquerda
        light_source = (left_shoulder['x'] - 100, left_shoulder['y'] - 100)
        
        # Aplicar sombreamento gradual
        h, w = image.shape[:2]
        for y in range(h):
            for x in range(w):
                if mask[y, x] > 0:
                    # Calcular distância da fonte de luz
                    dist = np.sqrt((x - light_source[0])**2 + (y - light_source[1])**2)
                    # Normalizar e aplicar sombreamento
                    shade_factor = max(0.7, 1.0 - (dist / (w + h)))
                    image[y, x] = image[y, x] * shade_factor
        
        return image
    
    def add_jeans_texture(self, image, leg_polygons):
        """
        Adiciona textura de jeans realista
        """
        # Criar máscara para as pernas
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        for poly in leg_polygons:
            cv2.fillPoly(mask, [poly], 255)
        
        # Adicionar ruído para simular textura
        noise = np.random.randint(-20, 20, image.shape, dtype=np.int16)
        textured = image.astype(np.int16) + noise
        textured = np.clip(textured, 0, 255).astype(np.uint8)
        
        # Aplicar apenas na área das calças
        result = image.copy()
        result[mask > 0] = textured[mask > 0]
        
        return result
    
    def save_result(self, result_image, session_id):
        """
        Salva o resultado final
        """
        # Converter para PIL
        pil_image = Image.fromarray(result_image)
        
        # Melhorar qualidade
        pil_image = pil_image.filter(ImageFilter.SMOOTH)
        
        # Salvar
        buffer = io.BytesIO()
        pil_image.save(buffer, format='PNG', quality=95)
        buffer.seek(0)
        
        filename = f'ai_results/mirrorfit_result_{session_id}.png'
        path = default_storage.save(filename, ContentFile(buffer.read()))
        
        return path

# Função principal para processar try-on
def process_virtual_tryon(image_path, selected_clothing, session_id):
    """
    Função principal que processa o try-on virtual completo
    """
    try:
        print("🚀 Iniciando processamento de IA...")
        
        # Inicializar IA
        ai = MirrorFitAI()
        
        # 1. Analisar foto
        body_analysis = ai.analyze_photo(image_path)
        
        # 2. Aplicar roupas virtuais
        result_image = ai.apply_virtual_clothing(image_path, body_analysis, selected_clothing)
        
        # 3. Salvar resultado
        result_path = ai.save_result(result_image, session_id)
        
        print("✅ Processamento concluído com sucesso!")
        
        return {
            'success': True,
            'result_path': result_path,
            'body_analysis': {
                'measurements': body_analysis['body_measurements'],
                'landmarks_count': len(body_analysis['body_landmarks']),
                'face_detected': body_analysis['face_data'] is not None
            }
        }
        
    except Exception as e:
        print(f"❌ Erro no processamento: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

# Exemplo de uso
if __name__ == "__main__":
    # Teste da IA
    test_clothing = {
        'shirt': 'shirt1',
        'pants': 'pants1',
        'shoes': 'shoes1'
    }
    
    result = process_virtual_tryon(
        image_path='test_photo.jpg',
        selected_clothing=test_clothing,
        session_id='test_123'
    )
    
    print("Resultado do teste:", result)
