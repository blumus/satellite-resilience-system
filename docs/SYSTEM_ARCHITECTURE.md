# Satellite Resilience System Architecture

## System Overview
A robust, fault-tolerant system designed to process satellite data streams (camera, sensors, communications) with resilience against board resets, faulty software, and security threats. Development POC running on M1 ARM chip via Jetpack, designed for eventual Jetson deployment.

## Core Components

### Input Manager
- **Purpose**: Centralized input handling for all data sources
- **Interfaces**:
  - **Camera/Sensors**: File-based monitoring (predictable data streams)
  - **Ground Commands**: gRPC interface (bursty, real-time communication)
- **Responsibilities**:
  - File system monitoring for camera/sensor data
  - gRPC server for ground command reception
  - Input validation and sanitization
  - Task queuing for processing

### Processing Queue
- **Technology**: Celery + SQLite backend
- **Purpose**: Persistent, resilient task distribution
- **Benefits**: Python-native, file-based persistence, automatic recovery

### Processing Engines
Three specialized engines handling different data types:

**Note:** While we've defined three main engine categories, each engine can handle multiple specific tasks. The system is designed to be flexible - new tasks can be added to existing engines or new engines can be created as needed.

#### Picture Processing Engine
- YOLO object detection (`etc/test/yolo_bus_detection.py`)
- Image classification and analysis
- Video stream processing
- AI model inference

#### Sensor Processing Engine
- Sensor data analysis and validation
- Trend detection and anomaly identification
- Data aggregation and reporting
- Environmental monitoring

#### Communication Processing Engine
- Ground command execution
- Response generation and formatting
- Command validation and safety checks
- System status reporting

### Output Manager
- **Purpose**: Centralized output handling and distribution
- **Responsibilities**:
  - Processed data delivery to ground control
  - Result storage and management
  - Output format standardization

### Cleanup Queue
- **Purpose**: Parallel file deletion management
- **Operation**: Processing Engine marks files for deletion → Cleanup Queue handles actual deletion
- **Cleanup Timing**: Files are deleted immediately when marked for cleanup
- **Benefits**: Non-blocking cleanup, better resource management

## Resilience Components

### Security Monitor
- **Unauthorized access detection** - Monitors for unauthorized system access attempts
- **Suspicious command detection** - Identifies unusual or dangerous ground commands
- **Resource abuse detection** - Monitors for excessive resource consumption

### Fault Detector
- **Process crash detection** - Monitors component health and status
- **Memory leak detection** - Tracks memory usage patterns over time
- **High CPU usage detection** - Identifies stuck processes and infinite loops
- **Disk space monitoring** - Prevents storage exhaustion
- **Communication failure detection** - Monitors inter-component connectivity

### Watchdog Monitor
- **Fault-dependent responses**:
  - **Minor faults** → Restart just that component
  - **Major faults** → Reset the entire system
  - **Critical faults** → Trigger full system reset
- **Automatic recovery** - Self-healing without manual intervention

## Data Flow

### Camera Data Flow
1. Camera → saves image/video file
2. Input Manager → detects new file, validates it
3. Input Manager → sends to Processing Queue
4. Picture Processing Engine → picks up task, processes with AI
5. Picture Processing Engine → sends result to Output Manager
6. Picture Processing Engine → marks original file for cleanup
7. Cleanup Queue → deletes original file

### Sensor Data Flow
1. Sensors → save readings to data files
2. Input Manager → detects new sensor file, validates it
3. Input Manager → sends to Processing Queue
4. Sensor Processing Engine → picks up task, analyzes data
5. Sensor Processing Engine → sends processed results to Output Manager
6. Sensor Processing Engine → marks original sensor file for cleanup
7. Cleanup Queue → deletes original sensor file

### Communication Data Flow
1. Ground Control → sends command via gRPC
2. Input Manager → receives command, validates it
3. Input Manager → sends to Processing Queue
4. Communication Processing Engine → picks up task, executes command
5. Communication Processing Engine → sends response to Output Manager
6. Output Manager → sends response back to ground control via gRPC

## Failure Scenarios

### Scenario 1: Single Processing Engine Failure
- **What happens**: One Processing Engine crashes
- **Response**: Fault Detector detects crash, Watchdog restarts just that engine
- **Result**: Minimal disruption, tasks resume automatically

### Scenario 2: Multiple Processing Engine Failure
- **What happens**: Several engines crash simultaneously
- **Response**: Fault Detector detects multiple failures, Watchdog triggers full system reset
- **Result**: System reboots, all engines restart fresh

### Scenario 3: Input Manager Failure
- **What happens**: Input Manager stops detecting new files/commands
- **Response**: Fault Detector detects Input Manager failure, Watchdog restarts it
- **Result**: Some data might be lost during restart, but system continues

### Scenario 4: Processing Queue Failure
- **What happens**: Queue system (Celery + SQLite) stops working
- **Response**: Fault Detector detects queue failure, Watchdog triggers full system reset
- **Result**: System reboots, everything starts fresh

## Security Considerations

### Access Control
- **Ground commands** → Only accepted from authorized sources
- **Authentication** → Commands must include valid credentials
- **Authorization** → Commands are checked against allowed operations
- **Result**: Unauthorized commands are rejected

### Command Validation
- **Input sanitization** → Commands are checked for dangerous content
- **Parameter limits** → Commands can't request unlimited resources
- **Rate limiting** → Commands can't be sent too frequently
- **Result**: Malicious or dangerous commands are blocked

### Resource Monitoring
- **Memory limits** → Processes can't use unlimited memory
- **CPU limits** → Processes can't consume all CPU resources
- **Disk limits** → Processes can't fill up all storage
- **Result**: Resource abuse is detected and stopped

## Implementation Guidelines

### Component Isolation
- **Each component** → runs as a separate process
- **Independent restart** → One component can restart without affecting others
- **Shared resources** → Only through well-defined interfaces (queues, files)
- **Result**: System is modular and resilient

### Error Handling
- **Graceful degradation** → If one part fails, others continue working
- **Detailed logging** → Record what went wrong for debugging
- **Recovery actions** → Automatic steps to fix common problems
- **Result**: System handles errors without crashing

### Testing Strategy
- **Unit tests** → Test each component individually
- **Integration tests** → Test how components work together
- **Failure injection** → Intentionally break parts to test recovery
- **Stress tests** → Test system under heavy load and extreme conditions
- **Result**: System is proven to work under various conditions

## Future Enhancements

### Container Orchestration (k3s)
- **What it is**: Manage multiple containers across different machines
- **Benefits**: Better resource management, easier scaling
- **When to add**: When you need to run on multiple boards
- **Result**: More sophisticated deployment and management

### Advanced AI Models
- **What it is**: More sophisticated AI processing beyond YOLO
- **Examples**: Multi-modal AI, real-time video analysis, predictive analytics
- **Benefits**: Better data processing, more intelligent responses
- **When to add**: When basic AI processing is working well
- **Result**: More intelligent satellite system

### Ground Station Integration
- **What it is**: Connect to another card/board that handles ground control
- **Examples**: Communication card, command processing card, telemetry card
- **Benefits**: Distributed processing, specialized ground control handling
- **When to add**: When mock system is fully tested and stable
- **Result**: Multi-board satellite system with dedicated ground control

## System Block Diagram
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Camera        │    │   Sensors       │    │ Ground Control  │
│   (Files)       │    │   (Files)       │    │   (gRPC)        │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │      Input Manager        │
                    │  (File Monitor + gRPC)   │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │    Processing Queue       │
                    │   (Celery + SQLite)      │
                    └─────────────┬─────────────┘
                                  │
          ┌───────────────────────┼───────────────────────┐
          │                       │                       │
┌─────────▼─────────┐  ┌─────────▼─────────┐  ┌─────────▼─────────┐
│ Picture Processing│  │Sensor Processing │  │Communication     │
│ Engine            │  │Engine            │  │Processing Engine │
└─────────┬─────────┘  └─────────┬─────────┘  └─────────┬─────────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │     Output Manager        │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │    Cleanup Queue          │
                    └───────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    Resilience Components                        │
├─────────────────┬─────────────────┬───────────────────────────┤
│ Security Monitor│ Fault Detector  │   Watchdog Monitor        │
│                 │                 │                           │
└─────────────────┴─────────────────┴───────────────────────────┘
```

## Data Flow Diagram
```
Input Sources → Input Manager → Processing Queue → Processing Engines
                                                      ↓
Output Manager ← Processed Results ← AI Processing ← Data Files
     ↓
Ground Control (via gRPC)

Cleanup Queue ← Marked Files (parallel process)
```
