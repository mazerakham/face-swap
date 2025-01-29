#!/bin/bash

# Get the project root directory
PROJECT_ROOT="$(dirname "$0")/.."
cd "$PROJECT_ROOT"

# Build frontend and copy to backend/public
./scripts/build.sh

# Start the Python API server (which also serves frontend)
cd backend && uvicorn discovita.app:app --reload
