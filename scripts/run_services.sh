#!/bin/bash

# Start the Python API server
cd "$(dirname "$0")/.." && uvicorn face_swap.app:app --reload &

# Wait a moment for the API to initialize
sleep 2

# Start the React frontend
cd frontend && npm start
