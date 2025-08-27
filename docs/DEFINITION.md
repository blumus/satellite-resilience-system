### Problem Definition: Mock Satellite System Architecture

The goal of this two-to-three-day project is to define a robust system architecture for a mock embedded system. The system will run on a single **M1 ARM** chip, which will serve as a substitute for an **NVIDIA Jetson** in a satellite environment. The project is an exercise to gain experience and draw conclusions about internal resilience, rather than to build a perfect, production-ready system.

The system's core function is to process and mock various data streams, including **video feeds and sensor readings**, which are then fed into a mocked AI for processing. The expected outputs are **pictures and processed video feeds**.

The architecture must demonstrate resilience against a defined set of critical failure modes. It needs to be resilient to **board resets**, ensuring it can gracefully restart and recover. It must also be robust against **faulty software**, as it is difficult to upload patches. Finally, the system's architecture needs to be secure against **hackers**.

The architecture will not focus on the complexities of satellite communications but must take into account that **uplink time and bandwidth are very limited**. The final product will not be a physical satellite, but a conceptual model to prove the robustness of the software architecture.

The success of this mock system will be measured by its ability to perform with verifiable reliability and transparency. This includes the ability to automatically recover from a simulated board reset without manual intervention, and for internal system logging to be comprehensive enough to diagnose a software failure and a security breach with minimal effort.

### Minimum Viable Implementation (2.5 Days)

Given the hard deadline constraint, the implementation will focus on demonstrating core architectural principles rather than comprehensive feature coverage.

**Core Components:**
- Data stream simulator generating mock sensor readings and basic video frames
- Simple "AI processing" pipeline performing basic image transformations
- Output generation system saving processed images and video clips
- Basic system monitoring and logging infrastructure

**Primary Resilience Focus:**
- **Board Reset Recovery**: Implement automatic restart mechanisms and state persistence
- **Basic Fault Tolerance**: Restart failed components without full system restart
- **Simple Security Model**: Process isolation and basic access control

**Implementation Timeline:**
- **Day 1 (Tuesday)**: Architecture design and system structure setup
- **Day 2 (Wednesday)**: Core implementation and primary resilience feature
- **Day 3 (Thursday)**: Testing, documentation, and demo preparation

**Key Concerns & Limitations:**
- Limited testing depth due to time constraints
- Focus on one primary failure mode rather than comprehensive coverage
- Simplified security model (basic isolation, not advanced hardening)
- Mock data processing (simple transformations, not real ML algorithms)
- Basic logging and monitoring (sufficient for demo, not production-grade)

**Success Criteria (Adjusted for Timeline):**
- System can automatically recover from simulated board resets
- Basic fault tolerance demonstrated through component restart
- Simple security isolation prevents basic attack vectors
- Comprehensive logging shows system behavior during failures
- Working demo that proves the chosen resilience feature
