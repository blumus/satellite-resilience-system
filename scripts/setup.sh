#!/bin/bash
# Setup script for the Satellite Resilience System
# Initializes the system environment and configuration

echo "Setting up Satellite Resilience System..."

# Create data directories if they don't exist
mkdir -p data/input/camera
mkdir -p data/input/sensors
mkdir -p data/staging
mkdir -p data/output
mkdir -p data/logs

echo "Data directories created successfully."
echo "Setup complete!"
