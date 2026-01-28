"""Face embedding generation using InsightFace."""
import numpy as np
import cv2
from insightface.app import FaceAnalysis
from typing import Optional
import os


class FaceEmbedder:
    """Face embedder using InsightFace (ArcFace model)."""
    
    def __init__(self, model_name: str = 'buffalo_l'):
        """
        Initialize InsightFace model.
        
        Args:
            model_name: Model name ('buffalo_l' for high accuracy, 'buffalo_s' for speed)
        """
        # Initialize FaceAnalysis
        self.app = FaceAnalysis(
            name=model_name,
            providers=['CPUExecutionProvider']  # CPU-only
        )
        
        # Prepare model (downloads if needed)
        self.app.prepare(ctx_id=-1, det_size=(640, 640))
        
        self.embedding_size = 512  # ArcFace produces 512-dim embeddings
        
    def get_embedding(self, face_image: np.ndarray) -> Optional[np.ndarray]:
        """
        Generate face embedding from cropped face image.
        
        Args:
            face_image: Cropped face image as numpy array (RGB)
            
        Returns:
            512-dimensional embedding vector (L2 normalized) or None if no face detected
        """
        # Convert RGB to BGR (InsightFace expects BGR)
        face_bgr = cv2.cvtColor(face_image, cv2.COLOR_RGB2BGR)
        
        # Get face embeddings
        faces = self.app.get(face_bgr)
        
        if len(faces) == 0:
            print(f"DEBUG: InsightFace failed to detect face in crop. Shape: {face_bgr.shape}")
            return None
        
        # Get the first (and should be only) face
        face = faces[0]
        
        # Extract embedding (already L2 normalized by InsightFace)
        embedding = face.embedding
        
        # Ensure it's normalized (cosine similarity)
        embedding = embedding / np.linalg.norm(embedding)
        
        return embedding
    
    def get_embeddings_batch(self, face_images: list) -> list:
        """
        Generate embeddings for multiple faces.
        
        Args:
            face_images: List of cropped face images
            
        Returns:
            List of embeddings (some may be None if face not detected)
        """
        embeddings = []
        for face_image in face_images:
            embedding = self.get_embedding(face_image)
            embeddings.append(embedding)
        return embeddings
    
    @staticmethod
    def cosine_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Cosine similarity score (0-1, higher is more similar)
        """
        # Since embeddings are already L2 normalized, dot product = cosine similarity
        similarity = np.dot(embedding1, embedding2)
        return float(similarity)
