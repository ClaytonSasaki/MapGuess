#!/bin/bash

# Setup script for MapGuess
echo "🌍 Setting up MapGuess..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Add your Google Maps API key to templates/index.html"
echo "2. Run: python app.py"
echo "3. Open: http://localhost:5000"
echo ""
echo "To activate the virtual environment later, run:"
echo "  source venv/bin/activate  (Mac/Linux)"
echo "  venv\\Scripts\\activate     (Windows)"
