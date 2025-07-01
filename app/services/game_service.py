"""Game service for business logic"""
from sqlalchemy.orm import Session
from sqlalchemy import select, func, desc
from typing import List, Optional
from app.models.game import GameSession, HighScore
from app.schemas.game import GameSessionCreate, HighScoreCreate, GameStats
from app.core.logging import app_logger

class GameService:
    """Service layer for game operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_game_session(self, session_data: GameSessionCreate) -> GameSession:
        """Create a new game session"""
        try:
            db_session = GameSession(**session_data.model_dump())
            self.db.add(db_session)
            self.db.commit()
            self.db.refresh(db_session)
            
            # Check if this is a high score
            if self.is_high_score(session_data.score):
                self.create_high_score(HighScoreCreate(
                    player_name=session_data.player_name,
                    score=session_data.score,
                    coins_collected=session_data.coins_collected,
                    distance=session_data.distance
                ))
            
            app_logger.info(f"Game session created: {db_session.id}")
            return db_session
        except Exception as e:
            app_logger.error(f"Error creating game session: {e}")
            self.db.rollback()
            raise
    
    def create_high_score(self, high_score_data: HighScoreCreate) -> HighScore:
        """Create a new high score entry"""
        try:
            db_high_score = HighScore(**high_score_data.model_dump())
            self.db.add(db_high_score)
            self.db.commit()
            self.db.refresh(db_high_score)
            app_logger.info(f"High score created: {db_high_score.id}")
            return db_high_score
        except Exception as e:
            app_logger.error(f"Error creating high score: {e}")
            self.db.rollback()
            raise
    
    def get_high_scores(self, limit: int = 10) -> List[HighScore]:
        """Get top high scores"""
        try:
            stmt = select(HighScore).order_by(desc(HighScore.score)).limit(limit)
            result = self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            app_logger.error(f"Error getting high scores: {e}")
            return []
    
    def is_high_score(self, score: int) -> bool:
        """Check if score qualifies as a high score"""
        try:
            stmt = select(func.count(HighScore.id)).where(HighScore.score >= score)
            count = self.db.execute(stmt).scalar()
            return count < 10  # Top 10 high scores
        except Exception as e:
            app_logger.error(f"Error checking high score: {e}")
            return False
    
    def get_game_stats(self) -> GameStats:
        """Get overall game statistics"""
        try:
            # Get basic stats
            total_games = self.db.execute(select(func.count(GameSession.id))).scalar() or 0
            total_score = self.db.execute(select(func.sum(GameSession.score))).scalar() or 0
            total_coins = self.db.execute(select(func.sum(GameSession.coins_collected))).scalar() or 0
            total_distance = self.db.execute(select(func.sum(GameSession.distance))).scalar() or 0.0
            best_score = self.db.execute(select(func.max(GameSession.score))).scalar() or 0
            
            average_score = total_score / total_games if total_games > 0 else 0.0
            
            return GameStats(
                total_games=total_games,
                total_score=total_score,
                total_coins=total_coins,
                average_score=average_score,
                best_score=best_score,
                total_distance=total_distance
            )
        except Exception as e:
            app_logger.error(f"Error getting game stats: {e}")
            return GameStats(
                total_games=0,
                total_score=0,
                total_coins=0,
                average_score=0.0,
                best_score=0,
                total_distance=0.0
            )