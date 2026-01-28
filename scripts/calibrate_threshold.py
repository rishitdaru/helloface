"""Threshold calibration utility."""
import argparse
import numpy as np
from pathlib import Path
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from face_detector import FaceDetector
from face_embedder import FaceEmbedder


def calibrate_threshold(dataset_path: str):
    """
    Calibrate recognition threshold using a test dataset.
    
    Dataset structure:
    dataset_path/
        person1/
            image1.jpg
            image2.jpg
        person2/
            image1.jpg
            image2.jpg
    """
    print("🔧 Threshold Calibration Tool")
    print("=" * 50)
    
    # Initialize models
    print("Loading models...")
    detector = FaceDetector()
    embedder = FaceEmbedder()
    
    # Load dataset
    dataset = Path(dataset_path)
    if not dataset.exists():
        print(f"❌ Dataset path not found: {dataset_path}")
        return
    
    # Collect embeddings per person
    person_embeddings = {}
    
    for person_dir in dataset.iterdir():
        if not person_dir.is_dir():
            continue
            
        person_name = person_dir.name
        embeddings = []
        
        for image_path in person_dir.glob("*.jpg"):
            try:
                # Read image
                import cv2
                image = cv2.imread(str(image_path))
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                
                # Detect face
                faces = detector.detect_faces(image)
                if len(faces) == 0:
                    print(f"⚠️  No face in {image_path}")
                    continue
                
                # Get embedding
                face_crop, _ = faces[0]
                embedding = embedder.get_embedding(face_crop)
                
                if embedding is not None:
                    embeddings.append(embedding)
                    
            except Exception as e:
                print(f"❌ Error processing {image_path}: {e}")
        
        if embeddings:
            person_embeddings[person_name] = embeddings
            print(f"✅ {person_name}: {len(embeddings)} images")
    
    if len(person_embeddings) < 2:
        print("❌ Need at least 2 people in dataset")
        return
    
    # Calculate similarities
    print("\n📊 Calculating similarities...")
    
    same_person_scores = []
    different_person_scores = []
    
    # Same person comparisons
    for person, embeddings in person_embeddings.items():
        for i in range(len(embeddings)):
            for j in range(i + 1, len(embeddings)):
                similarity = embedder.cosine_similarity(embeddings[i], embeddings[j])
                same_person_scores.append(similarity)
    
    # Different person comparisons
    people = list(person_embeddings.keys())
    for i in range(len(people)):
        for j in range(i + 1, len(people)):
            person1_embeddings = person_embeddings[people[i]]
            person2_embeddings = person_embeddings[people[j]]
            
            for emb1 in person1_embeddings:
                for emb2 in person2_embeddings:
                    similarity = embedder.cosine_similarity(emb1, emb2)
                    different_person_scores.append(similarity)
    
    # Analyze results
    print("\n📈 Results:")
    print(f"Same person comparisons: {len(same_person_scores)}")
    print(f"  Mean: {np.mean(same_person_scores):.3f}")
    print(f"  Min:  {np.min(same_person_scores):.3f}")
    print(f"  Max:  {np.max(same_person_scores):.3f}")
    
    print(f"\nDifferent person comparisons: {len(different_person_scores)}")
    print(f"  Mean: {np.mean(different_person_scores):.3f}")
    print(f"  Min:  {np.min(different_person_scores):.3f}")
    print(f"  Max:  {np.max(different_person_scores):.3f}")
    
    # Find optimal threshold
    print("\n🎯 Threshold Analysis:")
    for threshold in [0.45, 0.50, 0.55, 0.60, 0.65]:
        true_positives = sum(1 for s in same_person_scores if s >= threshold)
        false_negatives = len(same_person_scores) - true_positives
        
        true_negatives = sum(1 for s in different_person_scores if s < threshold)
        false_positives = len(different_person_scores) - true_negatives
        
        accuracy = (true_positives + true_negatives) / (len(same_person_scores) + len(different_person_scores))
        
        print(f"\nThreshold: {threshold:.2f}")
        print(f"  Accuracy: {accuracy * 100:.1f}%")
        print(f"  False Positives: {false_positives}/{len(different_person_scores)} ({false_positives/len(different_person_scores)*100:.1f}%)")
        print(f"  False Negatives: {false_negatives}/{len(same_person_scores)} ({false_negatives/len(same_person_scores)*100:.1f}%)")
    
    print("\n✅ Calibration complete!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calibrate recognition threshold")
    parser.add_argument("--dataset", type=str, required=True, help="Path to test dataset")
    args = parser.parse_args()
    
    calibrate_threshold(args.dataset)
