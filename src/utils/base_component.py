"""
Base Component Class for the Satellite Resilience System.

Provides common interface and functionality for all system components.
All components should inherit from this base class.

Architecture Reference: SYSTEM_ARCHITECTURE.md - Component Design
"""

import logging
import time
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseComponent(ABC):
    """Base class for all system components."""
    
    def __init__(self, name: str):
        self.name = name
        self.is_running = False
        self.start_time = None
        self.logger = logging.getLogger(f"component.{name}")
        
    def start(self) -> bool:
        """Start the component."""
        try:
            self.logger.info(f"Starting {self.name}...")
            self._start_component()
            self.is_running = True
            self.start_time = time.time()
            self.logger.info(f"{self.name} started successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start {self.name}: {e}")
            return False
    
    def stop(self) -> bool:
        """Stop the component."""
        try:
            self.logger.info(f"Stopping {self.name}...")
            self._stop_component()
            self.is_running = False
            self.logger.info(f"{self.name} stopped successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to stop {self.name}: {e}")
            return False
    
    def is_healthy(self) -> bool:
        """Check if the component is healthy."""
        if not self.is_running:
            return False
        try:
            return self._check_health()
        except Exception as e:
            self.logger.error(f"Health check failed for {self.name}: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get component status information."""
        return {
            'name': self.name,
            'is_running': self.is_running,
            'is_healthy': self.is_healthy(),
            'start_time': self.start_time,
            'uptime': time.time() - self.start_time if self.start_time else 0
        }
    
    def restart(self) -> bool:
        """Restart the component."""
        self.logger.info(f"Restarting {self.name}...")
        if self.stop() and self.start():
            self.logger.info(f"{self.name} restarted successfully")
            return True
        else:
            self.logger.error(f"Failed to restart {self.name}")
            return False
    
    @abstractmethod
    def _start_component(self):
        """Component-specific startup logic. Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def _stop_component(self):
        """Component-specific shutdown logic. Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def _check_health(self) -> bool:
        """Component-specific health check. Must be implemented by subclasses."""
        pass
