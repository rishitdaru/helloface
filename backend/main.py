"""FastAPI main application."""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import numpy as np
from typing import Optional

from models import (
    EnrollRequest, EnrollResponse, RecognizeRequest, RecognizeResponse,
    UserResponse, UsersListResponse, DeleteResponse, HealthResponse, FaceMatch
)
from face_detector import FaceDetector
from face_embedder import FaceEmbedder
from vector_store import VectorStore
from database import Database


# Global instances (initialized on startup)
face_detector: Optional[FaceDetector] = None
face_embedder: Optional[FaceEmbedder] = None
vector_store: Optional[VectorStore] = None
database: Optional[Database] = None

# Recognition threshold (cosine similarity)
RECOGNITION_THRESHOLD = 0.55


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for loading models on startup."""
    global face_detector, face_embedder, vector_store, database
    
    print("🚀 Initializing HelloFace backend...")
    
    # Initialize components
    print("📷 Loading MediaPipe face detector...")
    face_detector = FaceDetector(min_detection_confidence=0.7)
    
    print("🧠 Loading InsightFace embedding model (this may take a moment)...")
    face_embedder = FaceEmbedder(model_name='buffalo_l')
    
    print("🔍 Initializing FAISS vector store...")
    vector_store = VectorStore(embedding_dim=512, index_path="data/faiss_index")
    
    print("💾 Connecting to database...")
    database = Database(db_path="data/helloface.db")
    
    print("✅ HelloFace backend ready!")
    
    yield
    
    # Cleanup on shutdown
    print("👋 Shutting down HelloFace backend...")


# Create FastAPI app
app = FastAPI(
    title="HelloFace API",
    description="100% Free, Open-Source Face Recognition System",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": "HelloFace API - 100% Free Face Recognition",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        models_loaded=face_detector is not None and face_embedder is not None,
        database_connected=database is not None,
        vector_store_ready=vector_store is not None
    )


@app.post("/enroll", response_model=EnrollResponse, tags=["Enrollment"])
async def enroll_user(request: EnrollRequest):
    """
    Enroll a new user with their face.
    
    - Detects face in the provided image
    - Generates face embedding
    - Stores in database and vector store
    """
    try:
        # Check if email already exists
        existing_user = database.get_user_by_email(request.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with email {request.email} already enrolled"
            )
        
        # Detect faces
        faces = face_detector.detect_from_base64(request.image)
        
        if len(faces) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No face detected in image. Please ensure your face is clearly visible."
            )
        
        if len(faces) > 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Multiple faces detected. Please ensure only one face is in the image."
            )
        
        # Get face crop
        face_crop, bbox = faces[0]
        
        # Generate embedding
        embedding = face_embedder.get_embedding(face_crop)
        
        if embedding is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to generate face embedding. Please try with a clearer image."
            )
        
        # Store in database (without embedding for now)
        user = database.create_user(
            name=request.name,
            email=request.email,
            embedding=embedding.tolist()
        )
        
        # Add to vector store
        vector_store.add_embedding(user.id, embedding)
        
        return EnrollResponse(
            user_id=user.id,
            name=user.name,
            email=user.email,
            enrolled_at=user.enrolled_at,
            message=f"User {user.name} enrolled successfully!"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Enrollment failed: {str(e)}"
        )


@app.post("/recognize", response_model=RecognizeResponse, tags=["Recognition"])
async def recognize_face(request: RecognizeRequest):
    """
    Recognize a face in the provided image.
    
    - Detects face in image
    - Generates embedding
    - Searches vector store for match
    - Returns user info if confidence above threshold
    """
    try:
        # Check if any users enrolled
        if vector_store.get_total_embeddings() == 0:
            return RecognizeResponse(
                recognized=False,
                match=None,
                message="No users enrolled yet. Please enroll users first."
            )
        
        # Detect faces
        faces = face_detector.detect_from_base64(request.image)
        
        if len(faces) == 0:
            return RecognizeResponse(
                recognized=False,
                match=None,
                message="No face detected in image."
            )
        
        # Use first detected face
        face_crop, bbox = faces[0]
        
        # Generate embedding
        embedding = face_embedder.get_embedding(face_crop)
        
        if embedding is None:
            return RecognizeResponse(
                recognized=False,
                match=None,
                message="Failed to generate face embedding."
            )
        
        # Search vector store
        results = vector_store.search(embedding, k=1)
        
        if not results:
            return RecognizeResponse(
                recognized=False,
                match=None,
                message="No match found."
            )
        
        # Get best match
        user_id, confidence = results[0]
        
        # Check threshold
        if confidence < RECOGNITION_THRESHOLD:
            return RecognizeResponse(
                recognized=False,
                match=None,
                message=f"Unknown face (confidence: {confidence:.2f}, threshold: {RECOGNITION_THRESHOLD})"
            )
        
        # Get user info
        user = database.get_user(user_id)
        
        if not user:
            return RecognizeResponse(
                recognized=False,
                match=None,
                message="User not found in database."
            )
        
        return RecognizeResponse(
            recognized=True,
            match=FaceMatch(
                user_id=user.id,
                name=user.name,
                email=user.email,
                confidence=confidence,
                bounding_box=bbox
            ),
            message=f"Recognized: {user.name}"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Recognition failed: {str(e)}"
        )


@app.get("/users", response_model=UsersListResponse, tags=["Users"])
async def get_users():
    """Get list of all enrolled users."""
    try:
        users = database.get_all_users()
        
        user_responses = [
            UserResponse(
                user_id=user.id,
                name=user.name,
                email=user.email,
                enrolled_at=user.enrolled_at
            )
            for user in users
        ]
        
        return UsersListResponse(
            users=user_responses,
            total=len(user_responses)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch users: {str(e)}"
        )


@app.delete("/users/{user_id}", response_model=DeleteResponse, tags=["Users"])
async def delete_user(user_id: int):
    """
    Delete a user and their face embedding.
    
    - Removes from database
    - Removes from vector store
    """
    try:
        # Check if user exists
        user = database.get_user(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        
        # Remove from vector store
        vector_store.remove_embedding(user_id)
        
        # Remove from database
        database.delete_user(user_id)
        
        return DeleteResponse(
            message=f"User {user.name} deleted successfully",
            user_id=user_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete user: {str(e)}"
        )


@app.get("/stats", tags=["Statistics"])
async def get_stats():
    """Get system statistics."""
    try:
        return {
            "total_users": database.get_user_count(),
            "total_embeddings": vector_store.get_total_embeddings(),
            "recognition_threshold": RECOGNITION_THRESHOLD,
            "embedding_dimension": 512
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch stats: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
