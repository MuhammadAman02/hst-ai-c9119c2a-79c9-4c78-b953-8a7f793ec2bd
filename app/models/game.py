"""Game-related SQLAlchemy models"""
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float, DateTime, func
from datetime import datetime
from app.core.database import Base

class GameSession(Base):
    """Game session model for tracking individual games"""
    __tablename__ = "game_sessions"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    player_name: Mapped[str] = mapped_column(String(100), default="Anonymous")
    score: Mapped[int] = mapped_column(Integer, default=0)
    coins_collected: Mapped[int] = mapped_column(Integer, default=0)
    distance: Mapped[float] = mapped_column(Float, default=0.0)
    duration: Mapped[float] = mapped_column(Float, default=0.0)  # Game duration in seconds
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    
    def __repr__(self) -> str:
        return f"<GameSession(id={self.id}, player='{self.player_name}', score={self.score})>"

class HighScore(Base):
    """High score model for leaderboard"""
    __tablename__ = "high_scores"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    player_name: Mapped[str] = mapped_column(String(100))
    score: Mapped[int] = mapped_column(Integer)
    coins_collected: Mapped[int] = mapped_column(Integer, default=0)
    distance: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    
    def __repr__(self) -> str:
        return f"<HighScore(id={self.id}, player='{self.player_name}', score={self.score})>"