#!/bin/bash

# HelloFace Quick Start Script
# This script helps you get HelloFace up and running quickly

set -e

echo "👋 HelloFace Quick Start"
echo "========================"
echo ""

# Check prerequisites
echo "🔍 Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Python $PYTHON_VERSION found"

# Check Node
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
fi

NODE_VERSION=$(node --version)
echo "✅ Node $NODE_VERSION found"

echo ""
echo "📦 Choose installation method:"
echo "1) Docker (recommended - easiest)"
echo "2) Local development (manual setup)"
read -p "Enter choice (1 or 2): " choice

if [ "$choice" = "1" ]; then
    echo ""
    echo "🐳 Starting with Docker..."
    
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    echo "Building and starting containers..."
    docker-compose up --build
    
elif [ "$choice" = "2" ]; then
    echo ""
    echo "🔧 Setting up local development..."
    
    # Backend setup
    echo ""
    echo "1️⃣ Setting up backend..."
    cd backend
    
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    echo "Activating virtual environment..."
    source venv/bin/activate
    
    echo "Installing Python dependencies (this may take a few minutes)..."
    pip install -q --upgrade pip
    pip install -q -r requirements.txt
    
    echo "✅ Backend setup complete!"
    
    # Start backend in background
    echo "Starting backend server..."
    uvicorn main:app --reload --port 8000 &
    BACKEND_PID=$!
    
    cd ..
    
    # Frontend setup
    echo ""
    echo "2️⃣ Setting up frontend..."
    cd frontend
    
    if [ ! -d "node_modules" ]; then
        echo "Installing Node dependencies (this may take a few minutes)..."
        npm install
    fi
    
    echo "✅ Frontend setup complete!"
    
    # Start frontend
    echo "Starting frontend server..."
    npm run dev &
    FRONTEND_PID=$!
    
    cd ..
    
    echo ""
    echo "✅ HelloFace is starting!"
    echo ""
    echo "📍 Access the application:"
    echo "   Frontend: http://localhost:5173"
    echo "   Backend API: http://localhost:8000"
    echo "   API Docs: http://localhost:8000/docs"
    echo ""
    echo "Press Ctrl+C to stop all servers"
    
    # Wait for Ctrl+C
    trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
    wait
    
else
    echo "❌ Invalid choice. Please run the script again and choose 1 or 2."
    exit 1
fi
