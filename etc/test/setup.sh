#!/bin/bash

echo "🚀 Setting up YOLO environment..."

# Update package lists
echo "📦 Updating package lists..."
apt update

# Install system dependencies
echo "🔧 Installing system dependencies..."
apt install -y python3.10-venv libgl1-mesa-glx libglib2.0-0

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "🐍 Creating Python virtual environment..."
    python3 -m venv .venv
else
    echo "🐍 Virtual environment already exists"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Install Python dependencies
echo "📚 Installing Python packages..."
pip install ultralytics

echo "✅ Setup complete! You can now run:"
echo "   source .venv/bin/activate"
echo "   python yolo_bus_detection.py"
