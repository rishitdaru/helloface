"""Performance benchmark script."""
import time
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'backend'))

from face_detector import FaceDetector
from face_embedder import FaceEmbedder
from vector_store import VectorStore


def benchmark():
    """Run performance benchmarks."""
    print("⚡ HelloFace Performance Benchmark")
    print("=" * 50)
    
    # Initialize components
    print("\n1️⃣ Loading models...")
    start = time.time()
    detector = FaceDetector()
    detector_load_time = time.time() - start
    print(f"   MediaPipe loaded in {detector_load_time:.2f}s")
    
    start = time.time()
    embedder = FaceEmbedder()
    embedder_load_time = time.time() - start
    print(f"   InsightFace loaded in {embedder_load_time:.2f}s")
    
    vector_store = VectorStore()
    
    # Create test image (640x480 with random noise)
    print("\n2️⃣ Creating test image...")
    test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    # Benchmark face detection
    print("\n3️⃣ Benchmarking face detection...")
    times = []
    for i in range(10):
        start = time.time()
        faces = detector.detect_faces(test_image)
        times.append(time.time() - start)
    
    print(f"   Average: {np.mean(times)*1000:.1f}ms")
    print(f"   Min: {np.min(times)*1000:.1f}ms")
    print(f"   Max: {np.max(times)*1000:.1f}ms")
    
    # Create a test face crop
    test_face = np.random.randint(0, 255, (112, 112, 3), dtype=np.uint8)
    
    # Benchmark embedding generation
    print("\n4️⃣ Benchmarking embedding generation...")
    times = []
    for i in range(10):
        start = time.time()
        embedding = embedder.get_embedding(test_face)
        times.append(time.time() - start)
    
    print(f"   Average: {np.mean(times)*1000:.1f}ms")
    print(f"   Min: {np.min(times)*1000:.1f}ms")
    print(f"   Max: {np.max(times)*1000:.1f}ms")
    
    # Benchmark vector search
    print("\n5️⃣ Benchmarking vector search...")
    
    # Add test embeddings
    for i in range(1000):
        test_emb = np.random.randn(512).astype('float32')
        test_emb = test_emb / np.linalg.norm(test_emb)
        vector_store.add_embedding(i, test_emb)
    
    query_emb = np.random.randn(512).astype('float32')
    query_emb = query_emb / np.linalg.norm(query_emb)
    
    times = []
    for i in range(100):
        start = time.time()
        results = vector_store.search(query_emb, k=1)
        times.append(time.time() - start)
    
    print(f"   Database size: 1000 embeddings")
    print(f"   Average: {np.mean(times)*1000:.2f}ms")
    print(f"   Min: {np.min(times)*1000:.2f}ms")
    print(f"   Max: {np.max(times)*1000:.2f}ms")
    
    # Summary
    print("\n📊 Summary:")
    print(f"   Model loading: {detector_load_time + embedder_load_time:.2f}s (one-time cost)")
    print(f"   Face detection: ~{np.mean(times)*1000:.0f}ms per image")
    print(f"   Embedding generation: ~{np.mean(times)*1000:.0f}ms per face")
    print(f"   Vector search: ~{np.mean(times)*1000:.1f}ms for 1K users")
    print(f"\n   Total recognition time: ~{(np.mean(times)*3)*1000:.0f}ms per image")
    
    print("\n✅ Benchmark complete!")


if __name__ == "__main__":
    benchmark()
