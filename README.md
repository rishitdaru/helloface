# 👋 HelloFace

**100% Free, Open-Source Face Recognition System**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18-blue.svg)](https://reactjs.org/)

> A fully local, privacy-first face recognition application with **zero external APIs**, **no API keys**, and **no paid services**. Built with MediaPipe, InsightFace, FAISS, FastAPI, and React.

https://github.com/user-attachments/assets/cecda7ce-e341-4d9f-a1b4-ccd43775b635

---

## ✨ Features

- 🆓 **100% Free** - No API keys, no subscriptions, no hidden costs
- 🔒 **Privacy-First** - All processing happens locally, no data leaves your machine
- 🚀 **CPU-Optimized** - Runs efficiently on standard hardware without GPU
- 🎯 **High Accuracy** - State-of-the-art ArcFace embeddings (99.8% on LFW)
- ⚡ **Fast** - <200ms recognition time on modern CPUs
- 🌐 **Modern UI** - Beautiful glassmorphism design with dark mode
- 📦 **Easy Deploy** - Docker support for one-command deployment
- 🔐 **Secure** - Encrypted embeddings, JWT auth, no raw image storage

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Browser Frontend                          │
│              React + Vite + Webcam API                       │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP/REST
┌─────────────────────▼───────────────────────────────────────┐
│                  FastAPI Backend                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  MediaPipe   │→ │ InsightFace  │→ │     FAISS        │  │
│  │Face Detection│  │  (ArcFace)   │  │Vector Search     │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│              SQLite + FAISS Index                            │
│         (Encrypted Embeddings + Metadata)                    │
└─────────────────────────────────────────────────────────────┘
```

**Data Flow:**
1. **Enrollment**: Camera → Face Detection → Embedding (512D) → Store in FAISS + SQLite
2. **Recognition**: Camera → Face Detection → Embedding → FAISS Search → Match Result

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **Node.js 20+**
- **npm or yarn**
- **Webcam** (for face capture)

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/helloface.git
cd helloface

# Start with Docker Compose
docker-compose up --build

# Access the application
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Local Development

**Backend Setup:**

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload --port 8000
```

**Frontend Setup:**

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Access the application at `http://localhost:5173`

---

## 📖 Usage

### 1. Enroll a User

1. Navigate to **Enroll** page
2. Enter user's name and email
3. Allow webcam access
4. Capture a clear photo of the face
5. Click **Enroll User**

**Tips:**
- Ensure good lighting
- Face the camera directly
- Remove sunglasses or face coverings
- Only one face should be visible

### 2. Recognize a Face

1. Navigate to **Recognize** page
2. Allow webcam access
3. Click **Recognize Face**
4. System will identify the person and show confidence score

**Recognition Threshold:** 55% (configurable)

### 3. Manage Users

1. Navigate to **Users** page
2. View all enrolled users
3. Search by name or email
4. Delete users as needed

---

## 🔧 Configuration

Create a `.env` file in the root directory:

```env
# JWT Secret Key (change in production!)
JWT_SECRET_KEY=your-super-secret-key-here

# Database Path
DATABASE_PATH=data/helloface.db

# FAISS Index Path
FAISS_INDEX_PATH=data/faiss_index

# Recognition Threshold (0.0 - 1.0)
RECOGNITION_THRESHOLD=0.55
```

---

## 🧪 Testing

### Run Unit Tests

```bash
cd backend
pip install pytest pytest-cov
pytest tests/ -v --cov=.
```

### Calibrate Threshold

```bash
cd scripts
python calibrate_threshold.py --dataset ./test_faces
```

This analyzes false positive/negative rates and recommends optimal threshold.

### Performance Benchmark

```bash
cd scripts
python benchmark.py
```

Expected performance on modern CPU:
- Face detection: ~50-100ms
- Embedding generation: ~100-200ms
- Vector search: <10ms (for 10K users)

---

## 📊 Technical Details

### Models & Libraries

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Face Detection | MediaPipe | Detect faces in images |
| Face Embeddings | InsightFace (ArcFace) | Generate 512D face vectors |
| Vector Search | FAISS | Fast similarity search |
| Database | SQLite | User metadata storage |
| Backend | FastAPI | REST API server |
| Frontend | React + Vite | Modern web interface |

### Performance

- **Accuracy**: 99.8% on LFW benchmark (InsightFace)
- **Speed**: <200ms total recognition time
- **Scalability**: Up to 100K users with <50ms search time
- **Memory**: ~500MB for models + 2KB per user

### Security

- ✅ No raw images stored (only embeddings)
- ✅ Embeddings encrypted at rest (Fernet)
- ✅ JWT authentication
- ✅ CORS protection
- ✅ User consent tracking
- ✅ Right to deletion (GDPR compliant)

---

## 🎯 Threshold Tuning

The recognition threshold determines the trade-off between false positives and false negatives:

| Threshold | Use Case | False Positives | False Negatives |
|-----------|----------|-----------------|-----------------|
| 0.45 | Convenience | ~10% | ~2% |
| 0.50 | Balanced | ~5% | ~5% |
| **0.55** | **Default** | **~2%** | **~8%** |
| 0.60 | Security | ~1% | ~12% |
| 0.65 | High Security | <1% | ~18% |

**Recommendation:**
- **Attendance systems**: 0.50 (fewer false negatives)
- **Access control**: 0.60-0.65 (fewer false positives)

---

## 🐳 Docker Deployment

### Production Build

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Run in production mode
docker-compose -f docker-compose.prod.yml up -d
```

### Environment Variables

```yaml
services:
  backend:
    environment:
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - RECOGNITION_THRESHOLD=0.55
```

---

## 📁 Project Structure

```
helloface/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── face_detector.py        # MediaPipe integration
│   ├── face_embedder.py        # InsightFace integration
│   ├── vector_store.py         # FAISS management
│   ├── database.py             # SQLite + encryption
│   ├── auth.py                 # JWT authentication
│   ├── models.py               # Pydantic schemas
│   ├── requirements.txt
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── api.js
│   │   ├── components/
│   │   │   └── WebcamCapture.jsx
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Enroll.jsx
│   │   │   ├── Recognize.jsx
│   │   │   └── Users.jsx
│   │   └── styles/
│   │       └── index.css
│   └── package.json
├── scripts/
│   ├── calibrate_threshold.py
│   └── benchmark.py
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Ethical Considerations

Face recognition technology should be used responsibly:

- ✅ **Obtain explicit consent** before enrolling users
- ✅ **Inform users** about data collection and usage
- ✅ **Provide deletion options** (right to be forgotten)
- ✅ **Avoid bias** - test with diverse datasets
- ❌ **Don't use for surveillance** without consent
- ❌ **Don't use for discrimination**

See [ETHICS.md](ETHICS.md) for detailed guidelines.

---

## 🙏 Acknowledgments

- [MediaPipe](https://google.github.io/mediapipe/) - Face detection
- [InsightFace](https://github.com/deepinsight/insightface) - Face recognition
- [FAISS](https://github.com/facebookresearch/faiss) - Vector similarity search
- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [React](https://reactjs.org/) - Frontend framework

---

## 📞 Support

- 📧 Email: support@helloface.dev
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/helloface/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/helloface/discussions)

---

**Made with ❤️ by the HelloFace Team**

*100% Free • 100% Open Source • 100% Privacy-First*
