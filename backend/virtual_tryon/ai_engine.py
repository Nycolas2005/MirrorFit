"""
🤖 ENGINE DE IA REAL PARA MIRRORFIT
Sistema completo de detecção corporal e aplicação de roupas
"""

import cv2
import numpy as np
import mediapipe as mp
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import io
import base64
import logging

logger = logging.getLogger(__name__)

class MirrorFitAI:
    """
    IA Real do MirrorFit - Detecção corporal e aplicação de roupas
    """
    
    def __init__(self):
        print("🤖 Inicializando IA MirrorFit...")
        
        # Inicializar MediaPipe
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_face = mp.solutions.face_detection
        
        # Configurar modelos
        self.pose = self.mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=True,
            min_detection_confidence=0.7
        )
        
        self.face_detection = self.mp_face.FaceDetection(
            model_selection=1,
            min_detection_confidence=0.7
        )
        
        print("✅ IA MirrorFit inicializada!")
    
    def process_virtual_tryon(self, image_path, selected_clothing):
        """
        Processa try-on virtual completo
        """
        try:
            print(f"📸 Processando imagem: {image_path}")
            print(f"👕 Roupas selecionadas: {selected_clothing}")
            
            # 1. Carregar e analisar imagem
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError("Não foi possível carregar a imagem")
            
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            height, width = image.shape[:2]
            
            print(f"📏 Dimensões da imagem: {width}x{height}")
            
            # 2. Detectar pose corporal
            pose_results = self.pose.process(image_rgb)
            
            if not pose_results.pose_landmarks:
                raise ValueError("❌ Não foi possível detectar pessoa na imagem. Certifique-se de que há uma pessoa visível de corpo inteiro.")
            
            print("✅ Pose corporal detectada!")
            
            # 3. Extrair pontos corporais
            body_landmarks = self.extract_body_landmarks(pose_results.pose_landmarks, width, height)
            
            # 4. Detectar rosto
            face_results = self.face_detection.process(image_rgb)
            face_detected = face_results.detections is not None and len(face_results.detections) > 0
            
            print(f"👤 Rosto detectado: {'Sim' if face_detected else 'Não'}")
            
            # 5. Aplicar roupas virtuais
            result_image = self.apply_virtual_clothing(image_rgb, body_landmarks, selected_clothing)
            
            # 6. Melhorar qualidade da imagem
            result_image = self.enhance_image_quality(result_image)
            
            print("✅ Processamento concluído!")
            
            return {
                'success': True,
                'result_image': result_image,
                'body_landmarks': len(body_landmarks),
                'face_detected': face_detected,
                'applied_items': list(selected_clothing.keys())
            }
            
        except Exception as e:
            print(f"❌ Erro no processamento: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def extract_body_landmarks(self, pose_landmarks, width, height):
        """
        Extrai pontos chave do corpo
        """
        landmarks = {}
        
        # Pontos importantes para aplicação de roupas
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
        
        for name, landmark_id in key_points.items():
            landmark = pose_landmarks.landmark[landmark_id]
            landmarks[name] = {
                'x': int(landmark.x * width),
                'y': int(landmark.y * height),
                'visibility': landmark.visibility
            }
        
        return landmarks
    
    def apply_virtual_clothing(self, image, landmarks, selected_clothing):
        """
        Aplica roupas virtuais na imagem
        """
        result_image = image.copy()
        
        print("🎨 Aplicando roupas virtuais...")
        
        # Aplicar na ordem correta (de baixo para cima)
        if selected_clothing.get('pants'):
            result_image = self.apply_pants(result_image, landmarks, selected_clothing['pants'])
            print("👖 Calça aplicada!")
        
        if selected_clothing.get('shorts'):
            result_image = self.apply_shorts(result_image, landmarks, selected_clothing['shorts'])
            print("🩳 Bermuda aplicada!")
        
        if selected_clothing.get('shirt'):
            result_image = self.apply_shirt(result_image, landmarks, selected_clothing['shirt'])
            print("👕 Camiseta aplicada!")
        
        if selected_clothing.get('shoes'):
            result_image = self.apply_shoes(result_image, landmarks, selected_clothing['shoes'])
            print("👟 Tênis aplicado!")
        
        return result_image
    
    def apply_shirt(self, image, landmarks, shirt_id):
        """
        Aplica camiseta com IA avançada
        """
        # Cores das camisetas
        shirt_colors = {
            'shirt1': (255, 255, 255),  # Branco
            'shirt2': (40, 40, 40),     # Preto
        }
        
        color = shirt_colors.get(shirt_id, (128, 128, 128))
        
        # Pontos necessários
        left_shoulder = landmarks.get('left_shoulder')
        right_shoulder = landmarks.get('right_shoulder')
        left_hip = landmarks.get('left_hip')
        right_hip = landmarks.get('right_hip')
        left_elbow = landmarks.get('left_elbow')
        right_elbow = landmarks.get('right_elbow')
        
        # Verificar se pontos estão visíveis
        required_points = [left_shoulder, right_shoulder, left_hip, right_hip]
        if not all(p and p['visibility'] > 0.5 for p in required_points):
            print("⚠️ Pontos da camiseta não visíveis suficientemente")
            return image
        
        # Calcular dimensões da camiseta
        shoulder_width = abs(right_shoulder['x'] - left_shoulder['x'])
        torso_height = abs(left_hip['y'] - left_shoulder['y'])
        
        # Criar contorno da camiseta com curvas naturais
        shirt_points = []
        
        # Ombros (com curva natural)
        shirt_points.extend([
            [left_shoulder['x'] - int(shoulder_width * 0.15), left_shoulder['y'] - 10],
            [left_shoulder['x'], left_shoulder['y'] - 5],
            [left_shoulder['x'] + int(shoulder_width * 0.1), left_shoulder['y']],
        ])
        
        # Lado direito
        if right_elbow and right_elbow['visibility'] > 0.5:
            shirt_points.extend([
                [right_shoulder['x'] - int(shoulder_width * 0.1), right_shoulder['y']],
                [right_shoulder['x'], right_shoulder['y'] - 5],
                [right_shoulder['x'] + int(shoulder_width * 0.15), right_shoulder['y'] - 10],
                [right_elbow['x'] + 20, right_elbow['y']],
            ])
        
        # Cintura
        shirt_points.extend([
            [right_hip['x'] + int(shoulder_width * 0.1), right_hip['y'] + 20],
            [left_hip['x'] - int(shoulder_width * 0.1), left_hip['y'] + 20],
        ])
        
        # Lado esquerdo
        if left_elbow and left_elbow['visibility'] > 0.5:
            shirt_points.extend([
                [left_elbow['x'] - 20, left_elbow['y']],
            ])
        
        # Converter para numpy array
        shirt_points = np.array(shirt_points, np.int32)
        
        # Criar máscara da camiseta
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.fillPoly(mask, [shirt_points], 255)
        
        # Aplicar sombreamento realista
        overlay = image.copy()
        
        # Aplicar cor base
        overlay[mask > 0] = color
        
        # Adicionar sombreamento baseado na anatomia
        overlay = self.add_clothing_shadows(overlay, mask, landmarks, 'shirt')
        
        # Misturar com a imagem original
        alpha = 0.75
        result = cv2.addWeighted(image, 1-alpha, overlay, alpha, 0)
        
        # Suavizar bordas
        result = self.smooth_clothing_edges(result, image, mask)
        
        return result
    
    def apply_pants(self, image, landmarks, pants_id):
        """
        Aplica calça com detecção anatômica
        """
        color = (20, 60, 120)  # Azul jeans
        
        left_hip = landmarks.get('left_hip')
        right_hip = landmarks.get('right_hip')
        left_knee = landmarks.get('left_knee')
        right_knee = landmarks.get('right_knee')
        left_ankle = landmarks.get('left_ankle')
        right_ankle = landmarks.get('right_ankle')
        
        # Verificar pontos necessários
        required_points = [left_hip, right_hip, left_knee, right_knee, left_ankle, right_ankle]
        if not all(p and p['visibility'] > 0.5 for p in required_points):
            print("⚠️ Pontos da calça não visíveis suficientemente")
            return image
        
        # Calcular largura das pernas
        hip_width = abs(right_hip['x'] - left_hip['x'])
        leg_width = int(hip_width * 0.3)
        
        # Perna esquerda
        left_leg_points = np.array([
            [left_hip['x'] - leg_width//2, left_hip['y']],
            [left_hip['x'] + leg_width//2, left_hip['y']],
            [left_knee['x'] + leg_width//3, left_knee['y']],
            [left_ankle['x'] + 20, left_ankle['y']],
            [left_ankle['x'] - 20, left_ankle['y']],
            [left_knee['x'] - leg_width//3, left_knee['y']],
        ], np.int32)
        
        # Perna direita
        right_leg_points = np.array([
            [right_hip['x'] - leg_width//2, right_hip['y']],
            [right_hip['x'] + leg_width//2, right_hip['y']],
            [right_knee['x'] + leg_width//3, right_knee['y']],
            [right_ankle['x'] + 20, right_ankle['y']],
            [right_ankle['x'] - 20, right_ankle['y']],
            [right_knee['x'] - leg_width//3, right_knee['y']],
        ], np.int32)
        
        # Criar máscaras
        left_mask = np.zeros(image.shape[:2], dtype=np.uint8)
        right_mask = np.zeros(image.shape[:2], dtype=np.uint8)
        
        cv2.fillPoly(left_mask, [left_leg_points], 255)
        cv2.fillPoly(right_mask, [right_leg_points], 255)
        
        # Aplicar calça
        overlay = image.copy()
        overlay[left_mask > 0] = color
        overlay[right_mask > 0] = color
        
        # Adicionar textura jeans
        overlay = self.add_jeans_texture(overlay, left_mask, right_mask)
        
        # Misturar
        alpha = 0.8
        result = cv2.addWeighted(image, 1-alpha, overlay, alpha, 0)
        
        return result
    
    def apply_shorts(self, image, landmarks, shorts_id):
        """
        Aplica bermuda
        """
        color = (180, 160, 120)  # Bege
        
        left_hip = landmarks.get('left_hip')
        right_hip = landmarks.get('right_hip')
        left_knee = landmarks.get('left_knee')
        right_knee = landmarks.get('right_knee')
        
        if not all(p and p['visibility'] > 0.5 for p in [left_hip, right_hip, left_knee, right_knee]):
            return image
        
        # Calcular pontos da bermuda (até meio da coxa)
        thigh_length = abs(left_knee['y'] - left_hip['y'])
        shorts_length = int(thigh_length * 0.6)
        
        hip_width = abs(right_hip['x'] - left_hip['x'])
        
        shorts_points = np.array([
            [left_hip['x'] - int(hip_width * 0.25), left_hip['y']],
            [right_hip['x'] + int(hip_width * 0.25), right_hip['y']],
            [right_hip['x'] + int(hip_width * 0.2), right_hip['y'] + shorts_length],
            [left_hip['x'] - int(hip_width * 0.2), left_hip['y'] + shorts_length],
        ], np.int32)
        
        # Aplicar bermuda
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.fillPoly(mask, [shorts_points], 255)
        
        overlay = image.copy()
        overlay[mask > 0] = color
        
        alpha = 0.75
        result = cv2.addWeighted(image, 1-alpha, overlay, alpha, 0)
        
        return result
    
    def apply_shoes(self, image, landmarks, shoes_id):
        """
        Aplica tênis com detecção precisa dos pés
        """
        shoe_colors = {
            'shoes1': (255, 255, 255),  # Air Force 1 Branco
            'shoes2': (50, 50, 50),     # Air Force 1 Preto
            'shoes3': (30, 80, 150),    # Adidas Azul
        }
        
        color = shoe_colors.get(shoes_id, (128, 128, 128))
        
        left_ankle = landmarks.get('left_ankle')
        right_ankle = landmarks.get('right_ankle')
        
        # Tênis esquerdo
        if left_ankle and left_ankle['visibility'] > 0.5:
            shoe_center = (left_ankle['x'], left_ankle['y'] + 30)
            
            # Sola do tênis
            cv2.ellipse(image, shoe_center, (45, 20), 0, 0, 360, (80, 80, 80), -1)
            
            # Corpo do tênis
            cv2.ellipse(image, (shoe_center[0], shoe_center[1] - 8), (40, 18), 0, 0, 360, color, -1)
            
            # Detalhes do Air Force 1
            if shoes_id in ['shoes1', 'shoes2']:
                # Logo Nike (swoosh simplificado)
                swoosh_points = np.array([
                    [shoe_center[0] - 15, shoe_center[1] - 5],
                    [shoe_center[0] - 5, shoe_center[1] - 10],
                    [shoe_center[0] + 5, shoe_center[1] - 8],
                    [shoe_center[0] - 10, shoe_center[1] - 2],
                ], np.int32)
                cv2.fillPoly(image, [swoosh_points], (200, 200, 200) if shoes_id == 'shoes1' else (150, 150, 150))
        
        # Tênis direito
        if right_ankle and right_ankle['visibility'] > 0.5:
            shoe_center = (right_ankle['x'], right_ankle['y'] + 30)
            
            # Sola do tênis
            cv2.ellipse(image, shoe_center, (45, 20), 0, 0, 360, (80, 80, 80), -1)
            
            # Corpo do tênis
            cv2.ellipse(image, (shoe_center[0], shoe_center[1] - 8), (40, 18), 0, 0, 360, color, -1)
            
            # Detalhes do Air Force 1
            if shoes_id in ['shoes1', 'shoes2']:
                # Logo Nike (swoosh simplificado - espelhado)
                swoosh_points = np.array([
                    [shoe_center[0] + 15, shoe_center[1] - 5],
                    [shoe_center[0] + 5, shoe_center[1] - 10],
                    [shoe_center[0] - 5, shoe_center[1] - 8],
                    [shoe_center[0] + 10, shoe_center[1] - 2],
                ], np.int32)
                cv2.fillPoly(image, [swoosh_points], (200, 200, 200) if shoes_id == 'shoes1' else (150, 150, 150))
        
        return image
    
    def add_clothing_shadows(self, image, mask, landmarks, clothing_type):
        """
        Adiciona sombreamento realista às roupas
        """
        # Simular fonte de luz vinda de cima-esquerda
        h, w = image.shape[:2]
        
        # Criar gradiente de sombra
        y_gradient = np.linspace(0.8, 1.2, h).reshape(-1, 1)
        x_gradient = np.linspace(1.1, 0.9, w).reshape(1, -1)
        shadow_map = y_gradient * x_gradient
        
        # Aplicar sombra apenas na área da roupa
        for c in range(3):
            channel = image[:, :, c].astype(np.float32)
            channel[mask > 0] *= shadow_map[mask > 0]
            image[:, :, c] = np.clip(channel, 0, 255).astype(np.uint8)
        
        return image
    
    def add_jeans_texture(self, image, left_mask, right_mask):
        """
        Adiciona textura de jeans realista
        """
        # Criar ruído para simular textura
        h, w = image.shape[:2]
        noise = np.random.randint(-15, 15, (h, w, 3), dtype=np.int16)
        
        # Aplicar textura apenas nas áreas das calças
        combined_mask = cv2.bitwise_or(left_mask, right_mask)
        
        textured = image.astype(np.int16) + noise
        textured = np.clip(textured, 0, 255).astype(np.uint8)
        
        # Aplicar apenas na área das calças
        result = image.copy()
        result[combined_mask > 0] = textured[combined_mask > 0]
        
        return result
    
    def smooth_clothing_edges(self, result, original, mask):
        """
        Suaviza bordas das roupas para melhor integração
        """
        # Criar máscara suavizada
        smooth_mask = cv2.GaussianBlur(mask.astype(np.float32), (5, 5), 0)
        smooth_mask = smooth_mask / 255.0
        
        # Aplicar suavização
        for c in range(3):
            result[:, :, c] = (
                original[:, :, c] * (1 - smooth_mask) +
                result[:, :, c] * smooth_mask
            ).astype(np.uint8)
        
        return result
    
    def enhance_image_quality(self, image):
        """
        Melhora qualidade final da imagem
        """
        # Converter para PIL para melhor processamento
        pil_image = Image.fromarray(image)
        
        # Melhorar nitidez
        enhancer = ImageEnhance.Sharpness(pil_image)
        pil_image = enhancer.enhance(1.1)
        
        # Melhorar contraste
        enhancer = ImageEnhance.Contrast(pil_image)
        pil_image = enhancer.enhance(1.05)
        
        # Aplicar filtro suave
        pil_image = pil_image.filter(ImageFilter.SMOOTH_MORE)
        
        return np.array(pil_image)
    
    def save_result_image(self, image, session_id):
        """
        Salva imagem resultado
        """
        # Converter para PIL
        pil_image = Image.fromarray(image)
        
        # Salvar em buffer
        buffer = io.BytesIO()
        pil_image.save(buffer, format='PNG', quality=95)
        buffer.seek(0)
        
        return buffer.getvalue()

# Função principal para usar a IA
def process_virtual_tryon_ai(image_path, selected_clothing, session_id):
    """
    Função principal que processa try-on com IA real
    """
    try:
        print("🚀 Iniciando processamento com IA real...")
        
        # Inicializar IA
        ai = MirrorFitAI()
        
        # Processar try-on
        result = ai.process_virtual_tryon(image_path, selected_clothing)
        
        if result['success']:
            # Salvar resultado
            image_data = ai.save_result_image(result['result_image'], session_id)
            
            return {
                'success': True,
                'result_image': result['result_image'],
                'image_data': image_data,
                'body_landmarks': result['body_landmarks'],
                'face_detected': result['face_detected'],
                'applied_items': result['applied_items']
            }
        else:
            return result
            
    except Exception as e:
        print(f"❌ Erro no processamento de IA: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }
