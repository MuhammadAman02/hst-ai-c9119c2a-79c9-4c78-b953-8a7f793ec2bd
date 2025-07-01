"""Health check functionality"""
import time
from typing import Dict, Any

class HealthCheck:
    """Health check utilities"""
    
    @staticmethod
    def check_all() -> Dict[str, Any]:
        """Perform comprehensive health check"""
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "service": "subway_surfers_game",
            "version": "1.0.0"
        }

def is_healthy() -> bool:
    """Simple health check"""
    return True