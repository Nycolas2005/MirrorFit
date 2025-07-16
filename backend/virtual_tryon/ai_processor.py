import cv2
import numpy as np
from PIL import Image, ImageDraw
import mediapipe as mp
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import io
import logging

logger = logging.getLogger(__name__)

class VirtualTryOnProcessor:
    def __init__(self):
        # Inicializar MediaPipe para detecção de pose
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=True,
            min_detection_confidence=0.5
        )
        self.mp_face = mp.solutions.face_detection
        self.face_detection = self.mp_face.FaceDetection(
            model_selection=0,
            min_detection_confidence=0.5
        )
    
    def process_try_on(self, session):
        """
        Processa o try-on virtual usando IA
        """
        try:
            # Carregar imagem original
            image_path = session.original_photo.path
            image = cv2.imread(image_path)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Detectar pose e rosto
            pose_results = self.pose.process(image_rgb)
            face_results = self.face_detection.process(image_rgb)
            
            if not pose_results.pose_landmarks:
                return {
                    'success': False,
                    'error': 'Não foi possível detectar a pose na imagem'
                }
            
            # Extrair pontos chave do corpo
            body_landmarks = self.extract_body_landmarks(pose_results.pose_landmarks)
            
            # Detectar rosto
            face_bbox = None
            if face_results.detections:
                face_bbox = self.extract_face_bbox(face_results.detections[0], image.shape)
            
            # Aplicar roupas virtuais
            result_image = self.apply_virtual_clothing(
                image_rgb, 
                body_landmarks, 
                face_bbox,
                session.selected_clothing
            )
            
            # Salvar resultado
            result_path = self.save_result_image(result_image, session.id)
            
            return {
                'success': True,
                'result_image': result_path
            }
            
        except Exception as e:
            logger.error(f"Erro no processamento de IA: {str(e)}")
            return {
                'success': False,
                'error': f'Erro no processamento: {str(e)}'
            }
    
    def extract_body_landmarks(self, pose_landmarks):
        """
        Extrai pontos chave do corpo
        """
        landmarks = {}
        
        # Pontos importantes para try-on
        important_points = {
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
        
        for name, landmark_id in important_points.items():
            landmark = pose_landmarks.landmark[landmark_id]
            landmarks[name] = {
                'x': landmark.x,
                'y': landmark.y,
                'z': landmark.z,
                'visibility': landmark.visibility
            }
        
        return landmarks
    
    def extract_face_bbox(self, detection, image_shape):
        """
        Extrai bounding box do rosto
        """
        bbox = detection.location_data.relative_bounding_box
        h, w, _ = image_shape
        
        return {
            'x': int(bbox.xmin * w),
            'y': int(bbox.ymin * h),
            'width': int(bbox.width * w),
            'height': int(bbox.height * h)
        }
    
    def apply_virtual_clothing(self, image, body_landmarks, face_bbox, selected_clothing):
        """
        Aplica roupas virtuais na imagem
        """
        result_image = image.copy()
        h, w, _ = result_image.shape
        
        # Converter landmarks para coordenadas de pixel
        pixel_landmarks = {}
        for name, landmark in body_landmarks.items():
            pixel_landmarks[name] = {
                'x': int(landmark['x'] * w),
                'y': int(landmark['y'] * h),
                'visibility': landmark['visibility']
            }
        
        # Aplicar camiseta
        if selected_clothing.get('shirt'):
            result_image = self.apply_shirt(result_image, pixel_landmarks, selected_clothing['shirt'])
        
        # Aplicar calça/bermuda
        if selected_clothing.get('pants'):
            result_image = self.apply_pants(result_image, pixel_landmarks, selected_clothing['pants'])
        elif selected_clothing.get('shorts'):
            result_image = self.apply_shorts(result_image, pixel_landmarks, selected_clothing['shorts'])
        
        # Aplicar tênis
        if selected_clothing.get('shoes'):
            result_image = self.apply_shoes(result_image, pixel_landmarks, selected_clothing['shoes'])
        
        return result_image
    
    def apply_shirt(self, image, landmarks, shirt_id):
        """
        Aplica camiseta virtual
        """
        # Definir cor baseada no ID da camiseta
        colors = {
            'shirt1': (255, 255, 255),  # Branco
            'shirt2': (50, 50, 50),     # Preto
        }
        color = colors.get(shirt_id, (128, 128, 128))
        
        # Calcular área da camiseta
        left_shoulder = landmarks['left_shoulder']
        right_shoulder = landmarks['right_shoulder']
        left_hip = landmarks['left_hip']
        right_hip = landmarks['right_hip']
        
        if all(p['visibility'] > 0.5 for p in [left_shoulder, right_shoulder, left_hip, right_hip]):
            # Criar máscara da camiseta
            points = np.array([
                [left_shoulder['x'], left_shoulder['y']],
                [right_shoulder['x'], right_shoulder['y']],
                [right_hip['x'], right_hip['y']],
                [left_hip['x'], left_hip['y']]
            ], np.int32)
            
            # Aplicar cor com transparência
            overlay = image.copy()
            cv2.fillPoly(overlay, [points], color)
            image = cv2.addWeighted(image, 0.7, overlay, 0.3, 0)
        
        return image
    
    def apply_pants(self, image, landmarks, pants_id):
        """
        Aplica calça virtual
        """
        color = (0, 100, 200)  # Azul jeans
        
        left_hip = landmarks['left_hip']
        right_hip = landmarks['right_hip']
        left_ankle = landmarks['left_ankle']
        right_ankle = landmarks['right_ankle']
        
        if all(p['visibility'] > 0.5 for p in [left_hip, right_hip, left_ankle, right_ankle]):
            # Perna esquerda
            left_points = np.array([
                [left_hip['x'] - 20, left_hip['y']],
                [left_hip['x'] + 20, left_hip['y']],
                [left_ankle['x'] + 15, left_ankle['y']],
                [left_ankle['x'] - 15, left_ankle['y']]
            ], np.int32)
            
            # Perna direita
            right_points = np.array([
                [right_hip['x'] - 20, right_hip['y']],
                [right_hip['x'] + 20, right_hip['y']],
                [right_ankle['x'] + 15, right_ankle['y']],
                [right_ankle['x'] - 15, right_ankle['y']]
            ], np.int32)
            
            overlay = image.copy()
            cv2.fillPoly(overlay, [left_points], color)
            cv2.fillPoly(overlay, [right_points], color)
            image = cv2.addWeighted(image, 0.7, overlay, 0.3, 0)
        
        return image
    
    def apply_shorts(self, image, landmarks, shorts_id):
        """
        Aplica bermuda virtual
        """
        color = (200, 180, 140)  # Bege
        
        left_hip = landmarks['left_hip']
        right_hip = landmarks['right_hip']
        left_knee = landmarks['left_knee']
        right_knee = landmarks['right_knee']
        
        if all(p['visibility'] > 0.5 for p in [left_hip, right_hip, left_knee, right_knee]):
            points = np.array([
                [left_hip['x'] - 25, left_hip['y']],
                [right_hip['x'] + 25, right_hip['y']],
                [right_knee['x'] + 20, right_knee['y']],
                [left_knee['x'] - 20, left_knee['y']]
            ], np.int32)
            
            overlay = image.copy()
            cv2.fillPoly(overlay, [points], color)
            image = cv2.addWeighted(image, 0.7, overlay, 0.3, 0)
        
        return image
    
    def apply_shoes(self, image, landmarks, shoes_id):
        """
        Aplica tênis virtual
        """
        colors = {
            'shoes1': (255, 255, 255),  # Branco
            'shoes2': (50, 50, 50),     # Preto
            'shoes3': (0, 100, 200),    # Azul
        }
        color = colors.get(shoes_id, (128, 128, 128))
        
        left_ankle = landmarks['left_ankle']
        right_ankle = landmarks['right_ankle']
        
        if left_ankle['visibility'] > 0.5:
            cv2.ellipse(image, 
                       (left_ankle['x'], left_ankle['y'] + 20), 
                       (30, 15), 0, 0, 360, color, -1)
        
        if right_ankle['visibility'] > 0.5:
            cv2.ellipse(image, 
                       (right_ankle['x'], right_ankle['y'] + 20), 
                       (30, 15), 0, 0, 360, color, -1)
        
        return image
    
    def save_result_image(self, image, session_id):
        """
        Salva imagem resultado
        """
        # Converter para PIL Image
        pil_image = Image.fromarray(image)
        
        # Salvar em buffer
        buffer = io.BytesIO()
        pil_image.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Salvar no storage
        filename = f'result_photos/result_{session_id}.png'
        path = default_storage.save(filename, ContentFile(buffer.read()))
        
        return path
