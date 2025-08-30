# Design Considerations - Directory Structure

## Overview
Directory structure for Satellite Resilience System MVP, supporting Camera Data Flow with future scalability.

## Core Principles
- **MVP-First**: Camera Data Flow for 2.5-day MVP, minimal complexity
- **Separation**: `src/` (logic), `config/` (settings), `data/` (flow), `tests/` (testing)
- **Scalability**: Modular structure supports future Sensor/Communication engines

## Directory Purpose
- **`src/`**: Standard Python package organization, component isolation
  - **Subdirs**: `input_managers/`, `processing_engines/`, `queue/`, `output/`, `resilience/` (Security Monitor, Fault Detector, Watchdog Monitor), `utils/` (shared utilities, helper functions), `models/` (data structures, task definitions)
- **`config/`**: Centralized settings, systemd services for MVP resilience
  - **Subdirs**: `systemd/` (service definitions)
- **`data/`**: Clear lifecycle: input → staging → output (matches architecture)
  - **Subdirs**: `input/camera/`, `input/sensors/`, `staging/` (temporary processed results), `output/`, `logs/`
- **`tests/`**: Unit + integration testing with dedicated fixtures
  - **Subdirs**: `unit/`, `integration/`, `fixtures/sample_images/`, `fixtures/sample_sensor_data/`
- **`scripts/`**: Automation and resilience testing tools
  - **Subdirs**: None (contains shell scripts directly)

## Integration
- **Preserves existing**: `etc/test/` YOLO pipeline intact
- **Future integration**: YOLO code moves to `src/processing_engines/`
- **No disruption**: All existing functionality continues working

## Future Path
- **Phase 2 & 3**: Add sensor analysis, gRPC commands, custom fault detection, and security monitoring

## Conclusion
Structure supports MVP implementation while maintaining clarity and future scalability.
