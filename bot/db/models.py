from sqlalchemy import BigInteger, Column, String, Boolean, Integer, Float
from sqlalchemy.dialects.postgresql import UUID

from bot.db.base import Base

class GamesHistoryEntry(Base):
    __tablename__ = "gameshistory"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(UUID)
    telegram_id = Column(BigInteger, nullable=False, index=True)
    opponent_name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    result = Column(String, nullable=False)
    
class PlayersEntry(Base):
    __tablename__ = "players"
    
    telegram_id = Column(BigInteger, nullable=False, unique=True, primary_key=True)
    rating = Column(Float, nullable=False)
    searching = Column(Boolean, nullable=False)
    playing = Column(Boolean, nullable=False)
    game_id = Column(UUID, nullable=True)
    