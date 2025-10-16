#!/bin/bash
# Setup script for TestAutomationClaudeCode

echo "Setting up TestAutomationClaudeCode..."

# Install python3-venv if not already installed
if ! dpkg -l | grep -q python3.12-venv; then
    echo "Installing python3.12-venv..."
    sudo apt install -y python3.12-venv
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To run tests, use:"
echo "  pytest"
