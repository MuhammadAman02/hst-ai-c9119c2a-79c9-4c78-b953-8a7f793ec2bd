"""Game API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services.game_service import GameService
from app.schemas.game import GameSession, GameSessionCreate, HighScore, GameStats
from app.core.logging import app_logger

router = APIRouter()

@router.post("/session", response_model=GameSession, status_code=status.HTTP_201_CREATED)
async def create_game_session(
    session_data: GameSessionCreate,
    db: Session = Depends(get_db)
):
    """Create a new game session and save score"""
    try:
        game_service = GameService(db)
        session = game_service.create_game_session(session_data)
        return session
    except Exception as e:
        app_logger.error(f"Error creating game session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save game session"
        )

@router.get("/high-scores", response_model=List[HighScore])
async def get_high_scores(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get top high scores"""
    try:
        game_service = GameService(db)
        high_scores = game_service.get_high_scores(limit)
        return high_scores
    except Exception as e:
        app_logger.error(f"Error getting high scores: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get high scores"
        )

@router.get("/stats", response_model=GameStats)
async def get_game_stats(db: Session = Depends(get_db)):
    """Get overall game statistics"""
    try:
        game_service = GameService(db)
        stats = game_service.get_game_stats()
        return stats
    except Exception as e:
        app_logger.error(f"Error getting game stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get game statistics"
        )