"""Health check endpoints"""
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.core.health import HealthCheck
from app.core.logging import app_logger

router = APIRouter()

@router.get("/health")
async def get_health_status():
    """Get application health status"""
    try:
        result = HealthCheck.check_all()
        app_logger.info("Health check completed successfully")
        return JSONResponse(content=result)
    except Exception as e:
        app_logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )