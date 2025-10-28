#!/bin/bash

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the project root directory
PROJECT_ROOT="$(dirname "$0")/.."
cd "$PROJECT_ROOT"

echo -e "${GREEN}Face Swap - Starting Services${NC}"
echo "================================"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python 3 is not installed${NC}"
    echo ""
    echo "Please install Python 3 to continue."
    echo ""
    echo "For macOS, you can install Python using:"
    echo "  1. Homebrew: brew install python3"
    echo "  2. Download from: https://www.python.org/downloads/"
    echo ""
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓${NC} Found $PYTHON_VERSION"

# Set up virtual environment
VENV_DIR="$PROJECT_ROOT/venv"

if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv "$VENV_DIR"
    echo -e "${GREEN}✓${NC} Virtual environment created"
else
    echo -e "${GREEN}✓${NC} Virtual environment exists"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source "$VENV_DIR/bin/activate"
echo -e "${GREEN}✓${NC} Virtual environment activated"

# Install/update Python dependencies
if [ -f "$PROJECT_ROOT/backend/requirements.txt" ]; then
    echo -e "${YELLOW}Installing Python dependencies...${NC}"
    pip install -q --upgrade pip
    pip install -q -r "$PROJECT_ROOT/backend/requirements.txt"
    echo -e "${GREEN}✓${NC} Python dependencies installed"
fi

# Build frontend and copy to backend/public
echo -e "${YELLOW}Building frontend...${NC}"
./scripts/build.sh
echo -e "${GREEN}✓${NC} Frontend built"

# Start the Python API server (which also serves frontend)
echo ""
echo -e "${GREEN}Starting FastAPI server...${NC}"
echo "================================"
cd backend && uvicorn discovita.app:app --reload
