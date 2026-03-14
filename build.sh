#!/bin/bash

echo "Building Crypto Trading System..."

# Build frontend
echo "Building frontend..."
cd frontend
npm install
npm run build
cd ..

# Build backend
echo "Building backend..."
cd backend
pip install -r requirements.txt
cd ..

echo "Build complete!"
echo "You can now run: docker compose up"
