# HelloFace - Quick Start Guide

## ⚠️ Important: First-Time Setup

The backend needs to download ML models (~100MB) on first run. This is a **one-time process** that takes 2-5 minutes.

## 🚀 Step-by-Step Setup

### 1. Install Backend Dependencies

```bash
cd /Users/rishit/projects/helloface/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies (this will take a few minutes)
pip install -r requirements.txt
```

### 2. Start Backend Server

```bash
# Still in backend directory with venv activated
uvicorn main:app --reload --port 8000
```

**Wait for this message:**
```
✅ HelloFace backend ready!
INFO:     Application startup complete.
```

This may take 2-5 minutes on first run as InsightFace downloads models.

### 3. Start Frontend (in a new terminal)

```bash
cd /Users/rishit/projects/helloface/frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

### 4. Access the Application

Open your browser to: **http://localhost:5173**

---

## 🐛 Troubleshooting

### "Failed to fetch" error

**Cause:** Backend is still starting up or models are downloading.

**Solution:**
1. Check backend terminal for "✅ HelloFace backend ready!"
2. Wait for models to download (first run only)
3. Test backend: `curl http://localhost:8000/health`
4. If it returns JSON, backend is ready!

### Backend won't start

**Error:** `ModuleNotFoundError` or import errors

**Solution:**
```bash
cd backend
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Models downloading slowly

**Solution:** Be patient! InsightFace downloads ~100MB of models on first run. This is normal and only happens once.

---

## ✅ Verification

Once both servers are running:

1. **Backend health check:**
   ```bash
   curl http://localhost:8000/health
   ```
   Should return: `{"status":"healthy","models_loaded":true,...}`

2. **Frontend access:**
   Open http://localhost:5173 - you should see the HelloFace UI

3. **Test enrollment:**
   - Go to Enroll page
   - Allow webcam
   - Capture photo
   - Fill name/email
   - Click Enroll

---

## 📝 Notes

- **First startup:** 2-5 minutes (model download)
- **Subsequent startups:** ~10 seconds
- **Models stored in:** `~/.insightface/models/`
- **Data stored in:** `backend/data/`

---

## 🆘 Still Having Issues?

Check the backend terminal output for specific error messages. Common issues:

1. **Port already in use:** Kill process on port 8000
   ```bash
   lsof -ti:8000 | xargs kill -9
   ```

2. **Python version:** Requires Python 3.9+
   ```bash
   python3 --version
   ```

3. **Missing system libraries:** Install OpenCV dependencies
   ```bash
   # macOS
   brew install opencv
   ```
