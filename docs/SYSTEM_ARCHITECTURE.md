# Satellite Resilience System Architecture

## System Overview
A robust, fault-tolerant system designed to process satellite data streams (camera, sensors, communications) with resilience against board resets, faulty software, and security threats. Development POC running on M1 ARM chip via Jetpack, designed for eventual Jetson deployment.

## Core Components

### File Input Manager
- **Purpose**: Handles all file-based data ingestion.
- **Interface**: File system monitoring for camera and sensor data.
- **Responsibilities**:
  - Monitors designated directories for new files.
  - Validates incoming files.
  - Creates and sends processing tasks to the `Processing Queue`.

### Command Input Manager (gRPC)
- **Purpose**: Handles all real-time command and control from the ground.
- **Interface**: gRPC server.
- **Responsibilities**:
  - Listens for incoming gRPC commands.
  - Authenticates and authorizes commands.
  - Creates and sends processing tasks to the `Processing Queue`.

### Processing Queue
- **Technology**: Celery + SQLite backend
- **Purpose**: Persistent, resilient task distribution
- **Benefits**:
  - **Self-Contained**: Uses a simple file for the queue, requiring no external services like RabbitMQ. This is ideal for a single-node embedded system.
  - **Sufficient Resilience**: Ensures tasks persist even if a component crashes, meeting the core resilience goal for the MVP.
  - **Simplicity**: Avoids the setup and management overhead of a separate message broker server.

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
- **Purpose**: Audits and finalizes processed data, creating a verifiable record of system output.
- **Responsibilities**:
  - Monitors a staging directory for newly processed files from the engines.
  - Moves validated files to a final, official output directory.
  - Generates and maintains an `output_manifest.log` to provide an auditable record of all successfully processed data.
  - (Future) Handles delivery of data to ground control.

### Cleanup Queue
- **Purpose**: Parallel file deletion management
- **Operation**: Processing Engine marks files for deletion → Cleanup Queue handles actual deletion
- **Cleanup Timing**: Files are deleted immediately when marked for cleanup
- **Benefits**: Non-blocking cleanup, better resource management

## Data Flow

### Camera Data Flow
1. Camera → saves image/video file
2. File Input Manager → detects new file, validates it
3. File Input Manager → sends to Processing Queue
4. Picture Processing Engine → picks up task, processes with AI
5. Picture Processing Engine → saves result to a temporary staging directory
6. Output Manager → detects new file, moves it to the final output directory, and updates the manifest log
7. Picture Processing Engine → marks original file for cleanup
8. Cleanup Queue → deletes original file

### Sensor Data Flow
1. Sensors → save readings to data files
2. File Input Manager → detects new sensor file, validates it
3. File Input Manager → sends to Processing Queue
4. Sensor Processing Engine → picks up task, analyzes data
5. Sensor Processing Engine → sends processed results to Output Manager
6. Sensor Processing Engine → marks original sensor file for cleanup
7. Cleanup Queue → deletes original sensor file

### Communication Data Flow
1. Ground Control → sends command via gRPC
2. Command Input Manager → receives command, validates it
3. Command Input Manager → sends to Processing Queue
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

### Scenario 3a: File Input Manager Failure
- **What happens**: File Input Manager crashes and stops detecting new files.
- **Response**: Fault Detector detects failure, Watchdog restarts it.
- **Result**: Ground commands continue to be processed. File processing resumes after restart.

### Scenario 3b: Command Input Manager Failure
- **What happens**: The gRPC server crashes.
- **Response**: Fault Detector detects failure, Watchdog restarts it.
- **Result**: File-based processing is unaffected. Ground command capability is restored after restart.

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

## MVP Implementation Strategy

This section outlines the focused plan for the initial 2.5-day Minimum Viable Product (MVP). The components and features described below represent a subset of the complete target architecture described in the main body of this document. The goal is to deliver a demonstrable, resilient system by prioritizing a single, end-to-end data flow. Features from the target architecture not included in the MVP (e.g., Sensor and Communication engines) are deferred for future development cycles.

### 1. Core Component Focus
- **Scope**: The MVP will implement the **Camera Data Flow** only.
- **Components**: This includes the `File Input Manager`, the `Picture Processing Engine`, the `Output Manager`, and the associated `Processing Queue` and `Cleanup Queue`.
- **Rationale**: Focusing on a single data path allows for a complete, end-to-end demonstration of the architecture's resilience principles within the limited timeframe.

### 2. Resilience and Monitoring
- **Technology**: Process supervision and resilience will be managed by **`systemd`**.
- **Implementation**: Each core component will run as a separate `systemd` service.
- **Restart Policy**: Service files will be configured with `Restart=on-failure` to automatically restart any component that crashes, fulfilling the primary resilience requirement.
- **Health Checks**: Components will integrate with the `systemd` watchdog mechanism by sending periodic "heartbeat" signals. This allows `systemd` to detect and restart not only crashed processes but also hung or frozen ones.
- **Rationale**: Using `systemd` leverages a robust, industry-standard tool for process management, providing a powerful resilience foundation without the need to build a custom supervisor from scratch for the MVP.

## Future Enhancements

The items listed below are potential next steps that can be pursued after the MVP is stable. They are not listed in a strict order of priority. The decision to implement these enhancements, or to first complete the remaining components of the target architecture (like the Sensor and Communication engines), will be based on the project's evolving requirements.

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

### Custom Resilience Framework
- **What it is**: A more sophisticated, application-aware resilience layer to complement or replace the foundational `systemd` services.
- **Benefits**: Finer-grained control over fault detection and recovery logic.
- **Components**:
  - **Security Monitor**: Detects unauthorized access, suspicious commands, and resource abuse.
  - **Fault Detector**: Monitors for specific application-level faults like memory leaks, high CPU usage, and inter-component communication failures.
  - **Watchdog Monitor**: Implements complex, fault-dependent responses (e.g., restarting a component vs. resetting the system).

## System Block Diagram
**Note:** This diagram represents the complete target architecture. The MVP implementation focuses on the **Camera Data Flow** path: Camera → File Input Manager → Processing Queue → Picture Processing Engine → Output Manager → Cleanup Queue.

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
