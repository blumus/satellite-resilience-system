# Test Environment Documentation

## Overview
The `/etc/test` directory contains a working computer vision testing environment that demonstrates YOLOv8 object detection capabilities. This serves as a foundation for the satellite system's AI processing pipeline.

## Contents

### Core Scripts
- **`detect.py`** - Main detection script that downloads a sample image, runs YOLOv8 inference, and saves results with bounding boxes
- **`check_environment.py`** - Environment verification script that checks PyTorch version and CUDA availability

### AI Models
- **`yolov8n.pt`** - Pre-trained YOLOv8 nano model (6.2MB) for object detection

### Test Images
- **`bus.jpg`** - Sample input image (134KB) downloaded from ultralytics.com
- **`detected_bus.jpg`** - Output image (357KB) showing detection results with bounding boxes drawn

### Dependencies
- **`requirements.txt`** - Minimal package requirements for the test environment

## Purpose
This test environment provides:
1. **Proof of Concept** - Working AI pipeline that can process images and generate outputs
2. **Baseline Performance** - Established system to build resilience features around
3. **Testing Framework** - Realistic workload for testing fault tolerance and recovery mechanisms

## Usage
```bash
# Check environment
python check_environment.py

# Run detection test
python detect.py
```

## Integration Notes
- The YOLOv8 pipeline can serve as the core "AI processing" component in the satellite system
- Output images demonstrate the system's ability to process data streams and generate results
- Lightweight model (6.2MB) suitable for resource-constrained environments
