from sqlalchemy import BigInteger, Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID

from bot.db.base import Base

class GamesHistoryEntry(Base):
    __tablename__ = "gameshistory"
    
    game_id = Column(UUID, primary_key=True)
    telegram_id = Column(BigInteger, nullable=False, index=True)
    opponent_name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    result = Column(String, nullable=False)
    
class PlayersEntry(Base):
    __tablename__ = "players"
    
    telegram_id = Column(BigInteger, nullable=False, unique=True, primary_key=True)
    searching = Column(Boolean, nullable=False)
    playing = Column(Boolean, nullable=False)
    game_id = Column(UUID, nullable=True)
    