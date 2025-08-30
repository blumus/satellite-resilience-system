# Satellite Resilience System

## Overview
This project defines a robust system architecture for a mock embedded system designed to run on a single **M1 ARM** chip, serving as a substitute for an **NVIDIA Jetson** in a satellite environment. The system's core function is to process and mock various data streams, including **video feeds and sensor readings**, which are then fed into a mocked AI for processing.

The architecture demonstrates resilience against critical failure modes:
- **Board resets** - ensuring graceful restart and recovery
- **Faulty software** - robust against software failures in limited patch environments  
- **Security threats** - protection against hackers with limited uplink capabilities

**Note:** The current implementation includes YOLO object detection as a demonstration of the AI processing pipeline, but this is part of the larger satellite resilience architecture project.



## Prerequisites
- Docker container with Python 3.10+
- Internet connection (for downloading YOLO model and sample images)

## System Testing

The following scripts are **test utilities** to verify that the system environment is properly configured and working. These are not the main project components but rather verification tools.

### 1. Setup Test Environment (First time or after container rebuild)
```bash
cd etc/test
./setup.sh
```

### 2. Run Scripts

#### Verify PyTorch and CUDA Environment
```bash
python3 check_pytorch_cuda.py
```
**Expected Output:**
```
PyTorch version: 2.1.0
CUDA available: False
```

#### Test AI Processing Pipeline (YOLO Demo)
```bash
source .venv/bin/activate
python3 yolo_bus_detection.py
```

**Note:** After running the YOLO script, you can deactivate the virtual environment with:
```bash
deactivate
```
**Expected Output:**
```
Downloaded image: bus.jpg
Loading YOLOv8 model...
Running inference...
image 1/1 /home/extra/etc/test/bus.jpg: 640x480 4 persons, 1 bus, 1 stop sign, 180.8ms
Speed: 5.1ms preprocess, 180.8ms inference, 4.4ms postprocess per image at shape (1, 3, 640, 480)

--- Detection Results ---
Detected: bus (Confidence: 0.87)
Detected: person (Confidence: 0.87)
Detected: person (Confidence: 0.85)
Detected: person (Confidence: 0.83)
Detected: person (Confidence: 0.26)
Detected: stop sign (Confidence: 0.26)
Results saved to detected_bus.jpg
```

### Script Details

#### `check_pytorch_cuda.py`
- Verifies PyTorch installation and version
- Checks CUDA availability
- Useful for debugging environment setup

#### `yolo_bus_detection.py`
- Downloads a sample bus image from the internet
- Loads a pre-trained YOLOv8 nano model
- Runs object detection on the image
- Saves results with bounding boxes
- **Note:** The logic in this script forms the basis for the core `Picture Processing Engine` component in the main system architecture.
- Prints detection results with confidence scores









## Project Structure

```
satellite-resilience-system/
├── docs/                          # System architecture and documentation
├── src/                           # Main application code
│   ├── input_managers/           # File and command input handling
│   ├── processing_engines/       # AI processing and data analysis
│   ├── queue/                    # Task distribution and management
│   ├── output/                   # Output validation and manifest logging
│   ├── resilience/               # Fault detection and monitoring
│   ├── utils/                    # Shared utilities and helpers
│   └── models/                   # Data structures and task definitions
├── config/                       # Configuration and systemd services
├── data/                         # Input, staging, and output directories
├── tests/                        # Unit and integration tests
├── scripts/                      # System management scripts
├── etc/test/                     # YOLO testing environment (existing)
└── .devcontainer/                # Development container configuration
```

## Resources
- [Ultralytics Documentation](https://docs.ultralytics.com/)
- [YOLOv8 Paper](https://arxiv.org/abs/2303.07701)
- [PyTorch Documentation](https://pytorch.org/docs/)

## License
This project is for educational and demonstration purposes.
