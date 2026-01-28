"""Vector storage and similarity search using FAISS."""
import faiss
import numpy as np
from typing import List, Tuple, Optional
import os
import pickle
from threading import Lock


class VectorStore:
    """FAISS-based vector store for face embeddings."""
    
    def __init__(self, embedding_dim: int = 512, index_path: str = "data/faiss_index"):
        """
        Initialize FAISS vector store.
        
        Args:
            embedding_dim: Dimension of embeddings (512 for ArcFace)
            index_path: Path to save/load FAISS index
        """
        self.embedding_dim = embedding_dim
        self.index_path = index_path
        self.mapping_path = index_path + "_mapping.pkl"
        
        # Thread safety
        self.lock = Lock()
        
        # Create index (IndexFlatIP for cosine similarity with normalized vectors)
        self.index = faiss.IndexFlatIP(embedding_dim)
        
        # Mapping from FAISS index position to user_id
        self.id_mapping = []  # List where index = FAISS position, value = user_id
        
        # Load existing index if available
        self._load_index()
    
    def add_embedding(self, user_id: int, embedding: np.ndarray) -> None:
        """
        Add a face embedding to the index.
        
        Args:
            user_id: User ID to associate with embedding
            embedding: Face embedding vector (512-dim, L2 normalized)
        """
        with self.lock:
            # Ensure embedding is 2D array for FAISS
            if embedding.ndim == 1:
                embedding = embedding.reshape(1, -1)
            
            # Add to FAISS index
            self.index.add(embedding.astype('float32'))
            
            # Add to mapping
            self.id_mapping.append(user_id)
            
            # Save to disk
            self._save_index()
    
    def search(self, query_embedding: np.ndarray, k: int = 1) -> List[Tuple[int, float]]:
        """
        Search for most similar embeddings.
        
        Args:
            query_embedding: Query face embedding
            k: Number of nearest neighbors to return
            
        Returns:
            List of tuples (user_id, similarity_score)
        """
        with self.lock:
            if self.index.ntotal == 0:
                return []
            
            # Ensure query is 2D array
            if query_embedding.ndim == 1:
                query_embedding = query_embedding.reshape(1, -1)
            
            # Search (returns distances and indices)
            # For IndexFlatIP with normalized vectors, distance = cosine similarity
            distances, indices = self.index.search(query_embedding.astype('float32'), min(k, self.index.ntotal))
            
            # Convert to list of (user_id, similarity)
            results = []
            for dist, idx in zip(distances[0], indices[0]):
                if idx != -1:  # Valid result
                    user_id = self.id_mapping[idx]
                    similarity = float(dist)  # Already cosine similarity
                    results.append((user_id, similarity))
            
            return results
    
    def remove_embedding(self, user_id: int) -> bool:
        """
        Remove embedding by user_id.
        
        Note: FAISS doesn't support efficient deletion, so we rebuild the index.
        
        Args:
            user_id: User ID to remove
            
        Returns:
            True if removed, False if not found
        """
        with self.lock:
            # Find all positions with this user_id
            positions_to_remove = [i for i, uid in enumerate(self.id_mapping) if uid == user_id]
            
            if not positions_to_remove:
                return False
            
            # Get all embeddings except the ones to remove
            all_embeddings = []
            new_mapping = []
            
            for i in range(self.index.ntotal):
                if i not in positions_to_remove:
                    # Reconstruct embedding from index
                    embedding = self.index.reconstruct(i)
                    all_embeddings.append(embedding)
                    new_mapping.append(self.id_mapping[i])
            
            # Rebuild index
            self.index = faiss.IndexFlatIP(self.embedding_dim)
            self.id_mapping = []
            
            if all_embeddings:
                embeddings_array = np.array(all_embeddings).astype('float32')
                self.index.add(embeddings_array)
                self.id_mapping = new_mapping
            
            # Save to disk
            self._save_index()
            
            return True
    
    def get_total_embeddings(self) -> int:
        """Get total number of embeddings in the index."""
        return self.index.ntotal
    
    def _save_index(self) -> None:
        """Save FAISS index and mapping to disk."""
        # Create directory if needed
        os.makedirs(os.path.dirname(self.index_path) if os.path.dirname(self.index_path) else ".", exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(self.index, self.index_path)
        
        # Save mapping
        with open(self.mapping_path, 'wb') as f:
            pickle.dump(self.id_mapping, f)
    
    def _load_index(self) -> None:
        """Load FAISS index and mapping from disk."""
        if os.path.exists(self.index_path) and os.path.exists(self.mapping_path):
            try:
                # Load FAISS index
                self.index = faiss.read_index(self.index_path)
                
                # Load mapping
                with open(self.mapping_path, 'rb') as f:
                    self.id_mapping = pickle.load(f)
                    
                print(f"Loaded FAISS index with {self.index.ntotal} embeddings")
            except Exception as e:
                print(f"Error loading index: {e}. Starting with empty index.")
                self.index = faiss.IndexFlatIP(self.embedding_dim)
                self.id_mapping = []
    
    def clear(self) -> None:
        """Clear all embeddings from the index."""
        with self.lock:
            self.index = faiss.IndexFlatIP(self.embedding_dim)
            self.id_mapping = []
            self._save_index()
