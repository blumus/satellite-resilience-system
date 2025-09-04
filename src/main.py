"""
Main entry point for the Satellite Resilience System.

This module serves as the system orchestrator, coordinating all components
as defined in the SYSTEM_ARCHITECTURE.md. It manages the startup sequence
and monitors the overall system health.

Architecture Reference: SYSTEM_ARCHITECTURE.md - System Overview
"""

import logging
import sys
import time
from pathlib import Path
from typing import Dict
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# Import components
from src.input_managers.file_input_manager import FileInputManager
from src.queue.processing_queue import ProcessingQueue
from src.processing_engines.picture_processing_engine import PictureProcessingEngine
from src.output.output_manager import OutputManager
from src.queue.cleanup_queue import CleanupQueue

# Ensure log directory exists
Path('data/logs').mkdir(parents=True, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
    handlers=[
        logging.FileHandler('data/logs/system.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class HealthHandler(BaseHTTPRequestHandler):
    """HTTP handler for health check endpoints."""
    
    def __init__(self, orchestrator, *args, **kwargs):
        self.orchestrator = orchestrator
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            health_data = {
                'status': 'healthy',
                'timestamp': time.time(),
                'service': 'satellite-processor'
            }
            self.wfile.write(json.dumps(health_data).encode())
        elif self.path == '/ready':
            status = self.orchestrator.get_system_status() if self.orchestrator else {'system_health': {'status': 'initializing'}}
            if status['system_health']['status'] == 'running':
                self.send_response(200)
            else:
                self.send_response(503)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(status).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress HTTP server logs
        pass


class SystemOrchestrator:
    """Main system coordinator for the Satellite Resilience System."""
    
    def __init__(self):
        self.components: Dict[str, any] = {}
        self.system_health: Dict[str, str] = {}
        self.startup_time = None
        self.http_server = None
        self.http_thread = None
        
    def initialize_system(self) -> bool:
        """Initialize the satellite resilience system."""
        logger.info("Starting Satellite Resilience System initialization...")
        self.startup_time = time.time()
        
        try:
            # Ensure required directories exist
            self._create_directories()
            
            # Initialize component instances
            self._initialize_components()
            
            # Initialize component status tracking
            self._initialize_component_tracking()
            
            # Log system startup
            logger.info("System initialization completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"System initialization failed: {e}")
            return False
    
    def _create_directories(self):
        """Create required system directories if they don't exist."""
        required_dirs = [
            'data/input/camera',
            'data/input/sensors', 
            'data/staging',
            'data/output',
            'data/logs'
        ]
        
        for dir_path in required_dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            logger.debug(f"Ensured directory exists: {dir_path}")
    
    def _initialize_components(self):
        """Initialize all component instances."""
        self.components = {
            'file_input_manager': FileInputManager(),
            'processing_queue': ProcessingQueue(),
            'picture_processing_engine': PictureProcessingEngine(),
            'output_manager': OutputManager(),
            'cleanup_queue': CleanupQueue()
        }
        logger.info(f"Component instances created for {len(self.components)} components")
    
    def _initialize_component_tracking(self):
        """Initialize component status tracking."""
        self.system_health = {
            'status': 'initializing',
            'startup_time': str(self.startup_time),
            'components_ready': 0,
            'total_components': len(self.components)
        }
        logger.info(f"Component tracking initialized for {len(self.components)} components")
    
    def start_all_components(self) -> bool:
        """Start all system components."""
        logger.info("Starting all system components...")
        success_count = 0
        
        for name, component in self.components.items():
            try:
                if component.start():
                    success_count += 1
                    logger.info(f"Component {name} started successfully")
                else:
                    logger.error(f"Failed to start component {name}")
            except Exception as e:
                logger.error(f"Error starting component {name}: {e}")
        
        self.system_health['components_ready'] = success_count
        self.system_health['status'] = 'running' if success_count == len(self.components) else 'partial'
        
        # Start HTTP health server
        self._start_health_server()
        
        logger.info(f"Started {success_count}/{len(self.components)} components")
        return success_count == len(self.components)
    
    def _start_health_server(self):
        """Start HTTP server for health checks."""
        try:
            def handler(*args, **kwargs):
                return HealthHandler(self, *args, **kwargs)
            
            self.http_server = HTTPServer(('0.0.0.0', 8080), handler)
            self.http_thread = threading.Thread(target=self.http_server.serve_forever, daemon=True)
            self.http_thread.start()
            logger.info("Health check server started on port 8080")
        except Exception as e:
            logger.error(f"Failed to start health server: {e}")
    
    def stop_all_components(self):
        """Stop all system components."""
        logger.info("Stopping all system components...")
        
        for name, component in self.components.items():
            try:
                if component.is_running:
                    component.stop()
                    logger.info(f"Component {name} stopped")
                else:
                    logger.info(f"Component {name} was not running")
            except Exception as e:
                logger.error(f"Error stopping component {name}: {e}")
    
    def get_component_status(self, component_name: str) -> dict:
        """Get status of a specific component."""
        if component_name in self.components:
            return self.components[component_name].get_status()
        return {'error': f'Component {component_name} not found'}
    
    def restart_component(self, component_name: str) -> bool:
        """Restart a specific component."""
        if component_name in self.components:
            component = self.components[component_name]
            logger.info(f"Restarting component {component_name}")
            return component.restart()
        logger.error(f"Cannot restart: Component {component_name} not found")
        return False
    
    def get_system_status(self) -> Dict[str, any]:
        """Get current system status and health information."""
        return {
            'system_health': self.system_health,
            'component_status': {name: comp.get_status() for name, comp in self.components.items()},
            'uptime': time.time() - self.startup_time if self.startup_time else 0
        }
    
    def shutdown_system(self):
        """Gracefully shutdown the system."""
        logger.info("Initiating system shutdown...")
        
        # Stop HTTP server
        if self.http_server:
            self.http_server.shutdown()
            logger.info("Health server stopped")
            
        self.stop_all_components()
        logger.info("System shutdown completed")


def main():
    """Initialize and start the satellite resilience system."""
    orchestrator = SystemOrchestrator()
    
    try:
        # Initialize the system
        if not orchestrator.initialize_system():
            logger.error("Failed to initialize system. Exiting.")
            sys.exit(1)
        
        # Start all components
        if not orchestrator.start_all_components():
            logger.warning("Some components failed to start")
        
        # Log system status
        status = orchestrator.get_system_status()
        logger.info(f"System status: {status['system_health']['status']}")
        
        # Keep system running and monitor components
        try:
            while True:
                time.sleep(5)
                # TODO: Add health monitoring in future phases
        except KeyboardInterrupt:
            logger.info("Received shutdown signal")
            
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}")
        sys.exit(1)
    finally:
        orchestrator.shutdown_system()


if __name__ == "__main__":
    main()
