#!/bin/bash

# Define Python path
PYTHON_PATH="/Library/Frameworks/Python.framework/Versions/3.13/bin/python3"

# Check if Python exists
if [ ! -f "$PYTHON_PATH" ]; then
    echo "Error: Python not found at $PYTHON_PATH"
    echo "Please install Python 3 or update the PYTHON_PATH in this script"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
"$PYTHON_PATH" -m venv venv

# Check if venv was created successfully
if [ ! -d "venv" ]; then
    echo "Error: Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if activation was successful
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Error: Failed to activate virtual environment"
    exit 1
fi

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install the package in development mode
echo "Installing package in development mode..."
pip install -e .

# Install Stockfish if not already installed
if ! command -v stockfish &> /dev/null; then
    echo "Installing Stockfish..."
    brew install stockfish
fi

echo "Virtual environment setup complete!"
echo "To activate the virtual environment, run: source venv/bin/activate" 