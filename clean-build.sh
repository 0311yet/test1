#!/bin/bash

echo "=================================================="
echo "🔄 Building Crypto Trading System (Clean Build)"
echo "=================================================="
echo ""

# Clean Docker cache
echo "🧹 Cleaning Docker cache..."
docker compose down
docker system prune -f

# Build frontend without cache
echo "🔨 Building frontend..."
cd frontend
rm -f package-lock.json
npm install --legacy-peer-deps
npm run build
cd ..

# Build backend
echo "🔨 Building backend..."
cd backend
pip install -r requirements.txt --upgrade
cd ..

echo "=================================================="
echo "✅ Build Complete!"
echo "=================================================="
echo ""
echo "To start the system:"
echo "  docker compose up -d"
echo ""
echo "Access points:"
echo "  Frontend: http://localhost:3000"
echo "  Backend: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "=================================================="
