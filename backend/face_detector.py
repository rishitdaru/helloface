"""Face detection using MediaPipe."""
import cv2
import numpy as np
import mediapipe as mp
from typing import List, Tuple, Optional
import base64
from PIL import Image
import io


class FaceDetector:
    """Face detector using MediaPipe Face Detection."""
    
    def __init__(self, min_detection_confidence: float = 0.7):
        """
        Initialize MediaPipe face detector.
        
        Args:
            min_detection_confidence: Minimum confidence for face detection (0-1)
        """
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=1,  # 1 for full range (better for varied distances)
            min_detection_confidence=min_detection_confidence
        )
        
    def decode_image(self, base64_image: str) -> np.ndarray:
        """
        Decode base64 image to numpy array.
        
        Args:
            base64_image: Base64 encoded image string
            
        Returns:
            Image as numpy array in RGB format
        """
        # Remove data URL prefix if present
        if ',' in base64_image:
            base64_image = base64_image.split(',')[1]
            
        # Decode base64
        image_bytes = base64.b64decode(base64_image)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB numpy array
        image_np = np.array(image.convert('RGB'))
        
        return image_np
    
    def detect_faces(self, image: np.ndarray) -> List[Tuple[np.ndarray, dict]]:
        """
        Detect faces in image and return cropped face regions.
        
        Args:
            image: Input image as numpy array (RGB)
            
        Returns:
            List of tuples (cropped_face, bounding_box_dict)
            bounding_box_dict contains: {x, y, width, height}
        """
        # Convert to RGB if needed (MediaPipe expects RGB)
        if len(image.shape) == 2:  # Grayscale
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        elif image.shape[2] == 4:  # RGBA
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
            
        # Detect faces
        results = self.face_detection.process(image)
        
        faces = []
        if results.detections:
            h, w, _ = image.shape
            
            for detection in results.detections:
                # Get bounding box
                bbox = detection.location_data.relative_bounding_box
                
                # Convert to absolute coordinates
                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                width = int(bbox.width * w)
                height = int(bbox.height * h)
                
                # Add padding (30% on each side) to ensure InsightFace has enough context
                padding_x = int(width * 0.3)
                padding_y = int(height * 0.3)
                
                x = max(0, x - padding_x)
                y = max(0, y - padding_y)
                width = min(w - x, width + 2 * padding_x)
                height = min(h - y, height + 2 * padding_y)
                
                # Crop face region
                face_crop = image[y:y+height, x:x+width]
                
                # Store bounding box info
                bbox_dict = {
                    'x': x,
                    'y': y,
                    'width': width,
                    'height': height
                }
                
                faces.append((face_crop, bbox_dict))
        
        return faces
    
    def detect_from_base64(self, base64_image: str) -> List[Tuple[np.ndarray, dict]]:
        """
        Detect faces from base64 encoded image.
        
        Args:
            base64_image: Base64 encoded image string
            
        Returns:
            List of tuples (cropped_face, bounding_box_dict)
        """
        image = self.decode_image(base64_image)
        return self.detect_faces(image)
    
    def __del__(self):
        """Cleanup MediaPipe resources."""
        if hasattr(self, 'face_detection'):
            self.face_detection.close()
