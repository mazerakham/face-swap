#!/bin/bash

# Get the project root directory
PROJECT_ROOT="$(dirname "$0")/.."
cd "$PROJECT_ROOT"

echo "Installing Python dependencies..."
cd backend
python -m pip install -e .

echo "Building frontend..."
cd ../frontend && npm install && npm run build

echo "Copying frontend build to backend/public..."
rm -rf ../backend/public/*
cp -r build/* ../backend/public/

echo "Build complete!"
