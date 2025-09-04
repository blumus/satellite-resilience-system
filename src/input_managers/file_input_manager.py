"""
File Input Manager for the Satellite Resilience System.

Monitors designated directories for new camera and sensor data files.
Creates and sends processing tasks to the Processing Queue.

Architecture Reference: SYSTEM_ARCHITECTURE.md - File Input Manager
"""

import time
from src.utils.base_component import BaseComponent


class FileInputManager(BaseComponent):
    """Manages file input monitoring for camera and sensor data."""
    
    def __init__(self):
        super().__init__("file_input_manager")
        self.monitored_dirs = [
            'data/input/camera',
            'data/input/sensors'
        ]
        self.file_count = 0
        
    def _start_component(self):
        """Start file monitoring."""
        self.logger.info(f"Monitoring directories: {self.monitored_dirs}")
        # TODO: Implement actual file watching in Phase 2
        self.logger.info("File monitoring started (skeleton implementation)")
        
    def _stop_component(self):
        """Stop file monitoring."""
        self.logger.info("File monitoring stopped")
        
    def _check_health(self) -> bool:
        """Check if file monitoring is healthy."""
        # Basic health check - just verify we're running
        return self.is_running
        
    def get_file_count(self) -> int:
        """Get count of files processed."""
        return self.file_count
        
    def simulate_file_detection(self):
        """Simulate file detection for testing."""
        self.file_count += 1
        self.logger.info(f"Simulated file detection. Total files: {self.file_count}")
