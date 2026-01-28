"""Database operations using SQLAlchemy and SQLite."""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from typing import List, Optional
from cryptography.fernet import Fernet
import os
import json

Base = declarative_base()


class User(Base):
    """User model for storing enrolled users."""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    embedding_encrypted = Column(LargeBinary, nullable=True)  # Encrypted embedding


class Database:
    """Database manager with encryption support."""
    
    def __init__(self, db_path: str = "data/helloface.db", encryption_key: Optional[bytes] = None):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
            encryption_key: Fernet encryption key for embeddings
        """
        # Create data directory if needed
        os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else ".", exist_ok=True)
        
        # Create engine
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
        
        # Create tables
        Base.metadata.create_all(self.engine)
        
        # Create session factory
        self.SessionLocal = sessionmaker(bind=self.engine)
        
        # Setup encryption
        if encryption_key is None:
            # Generate or load encryption key
            key_path = os.path.join(os.path.dirname(db_path) if os.path.dirname(db_path) else ".", "encryption.key")
            if os.path.exists(key_path):
                with open(key_path, 'rb') as f:
                    encryption_key = f.read()
            else:
                encryption_key = Fernet.generate_key()
                with open(key_path, 'wb') as f:
                    f.write(encryption_key)
        
        self.cipher = Fernet(encryption_key)
    
    def get_session(self) -> Session:
        """Get a new database session."""
        return self.SessionLocal()
    
    def encrypt_embedding(self, embedding: list) -> bytes:
        """Encrypt embedding for storage."""
        embedding_json = json.dumps(embedding)
        return self.cipher.encrypt(embedding_json.encode())
    
    def decrypt_embedding(self, encrypted: bytes) -> list:
        """Decrypt embedding from storage."""
        decrypted = self.cipher.decrypt(encrypted)
        return json.loads(decrypted.decode())
    
    def create_user(self, name: str, email: str, embedding: Optional[list] = None) -> User:
        """
        Create a new user.
        
        Args:
            name: User's name
            email: User's email
            embedding: Face embedding (will be encrypted)
            
        Returns:
            Created User object
        """
        session = self.get_session()
        try:
            # Encrypt embedding if provided
            embedding_encrypted = None
            if embedding is not None:
                embedding_encrypted = self.encrypt_embedding(embedding)
            
            user = User(
                name=name,
                email=email,
                embedding_encrypted=embedding_encrypted
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        finally:
            session.close()
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        session = self.get_session()
        try:
            return session.query(User).filter(User.id == user_id).first()
        finally:
            session.close()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        session = self.get_session()
        try:
            return session.query(User).filter(User.email == email).first()
        finally:
            session.close()
    
    def get_all_users(self) -> List[User]:
        """Get all users."""
        session = self.get_session()
        try:
            return session.query(User).all()
        finally:
            session.close()
    
    def delete_user(self, user_id: int) -> bool:
        """
        Delete user by ID.
        
        Args:
            user_id: User ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        session = self.get_session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                session.delete(user)
                session.commit()
                return True
            return False
        finally:
            session.close()
    
    def update_user_embedding(self, user_id: int, embedding: list) -> bool:
        """
        Update user's embedding.
        
        Args:
            user_id: User ID
            embedding: New embedding
            
        Returns:
            True if updated, False if user not found
        """
        session = self.get_session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                user.embedding_encrypted = self.encrypt_embedding(embedding)
                session.commit()
                return True
            return False
        finally:
            session.close()
    
    def get_user_count(self) -> int:
        """Get total number of users."""
        session = self.get_session()
        try:
            return session.query(User).count()
        finally:
            session.close()
