"""Game-related Pydantic schemas"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class GameSessionBase(BaseModel):
    """Base game session schema"""
    player_name: str = Field(default="Anonymous", max_length=100)
    score: int = Field(default=0, ge=0)
    coins_collected: int = Field(default=0, ge=0)
    distance: float = Field(default=0.0, ge=0.0)
    duration: float = Field(default=0.0, ge=0.0)

class GameSessionCreate(GameSessionBase):
    """Schema for creating a game session"""
    pass

class GameSession(GameSessionBase):
    """Schema for game session response"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class HighScoreBase(BaseModel):
    """Base high score schema"""
    player_name: str = Field(max_length=100)
    score: int = Field(ge=0)
    coins_collected: int = Field(default=0, ge=0)
    distance: float = Field(default=0.0, ge=0.0)

class HighScoreCreate(HighScoreBase):
    """Schema for creating a high score"""
    pass

class HighScore(HighScoreBase):
    """Schema for high score response"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

class GameStats(BaseModel):
    """Game statistics schema"""
    total_games: int
    total_score: int
    total_coins: int
    average_score: float
    best_score: int
    total_distance: float