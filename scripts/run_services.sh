#!/bin/bash

# Exit on any error
set -e

# Store the root directory
ROOT_DIR="$(dirname "$0")/.."
cd "$ROOT_DIR"

# Function to cleanup background processes on exit
cleanup() {
    echo "Shutting down services..."
    kill $(jobs -p) 2>/dev/null || true
}

# Set up cleanup trap
trap cleanup EXIT

# Start the Python API server
echo "Starting FastAPI server..."
uvicorn face_swap.app:app --reload &
API_PID=$!

# Wait for API to be ready
echo "Waiting for API to initialize..."
sleep 2

# Check if API server started successfully
if ! kill -0 $API_PID 2>/dev/null; then
    echo "Failed to start API server"
    exit 1
fi

# Start the React frontend
echo "Starting frontend development server..."
cd frontend
npm run dev &
FRONTEND_PID=$!

# Wait for frontend to be ready
sleep 2

# Check if frontend started successfully
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo "Failed to start frontend server"
    exit 1
fi

echo "All services are running!"
echo "API: http://localhost:8000"
echo "Frontend: http://localhost:5173"

# Wait for all background processes
wait
