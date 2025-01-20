#!/bin/bash

# Start the Python API server
cd "$(dirname "$0")/.." && PYTHONPATH=$PWD python3 -m face_swap.app &

# Wait a moment for the API to initialize
sleep 2

# Start the React frontend
cd frontend && npm start
