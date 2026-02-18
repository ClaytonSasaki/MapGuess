#!/bin/bash

# MapGuess Launcher Script
# This script makes it easy to start MapGuess from anywhere

# Navigate to MapGuess directory
cd ~/Documents/MapGuess

# Activate virtual environment
source venv/bin/activate

# Check if Flask is installed
if ! python -c "import flask" 2>/dev/null; then
    echo "❌ Flask not installed. Running setup..."
    pip install -r requirements.txt
fi

# Start the application
echo "🌍 Starting MapGuess..."
echo "Open your browser to: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
