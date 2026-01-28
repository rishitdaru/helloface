"""Pydantic models for request/response validation."""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class EnrollRequest(BaseModel):
    """Request model for user enrollment."""
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    image: str = Field(..., description="Base64 encoded image")


class EnrollResponse(BaseModel):
    """Response model for successful enrollment."""
    user_id: int
    name: str
    email: str
    enrolled_at: datetime
    message: str = "User enrolled successfully"


class RecognizeRequest(BaseModel):
    """Request model for face recognition."""
    image: str = Field(..., description="Base64 encoded image")


class FaceMatch(BaseModel):
    """Model for a single face match result."""
    user_id: int
    name: str
    email: str
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    bounding_box: Optional[dict] = Field(None, description="Face bounding box coordinates")


class RecognizeResponse(BaseModel):
    """Response model for face recognition."""
    recognized: bool
    match: Optional[FaceMatch] = None
    message: str


class UserResponse(BaseModel):
    """Response model for user information."""
    user_id: int
    name: str
    email: str
    enrolled_at: datetime


class UsersListResponse(BaseModel):
    """Response model for list of users."""
    users: List[UserResponse]
    total: int


class DeleteResponse(BaseModel):
    """Response model for user deletion."""
    message: str
    user_id: int


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    models_loaded: bool
    database_connected: bool
    vector_store_ready: bool
