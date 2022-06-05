from sqlalchemy import BigInteger, Column, String
from sqlalchemy.dialects.postgresql import UUID

from bot.db.base import Base

class GamesHistoryEntry(Base):
    __tablename__ = "gameshistory"
    
    game_id = Column(UUID, primary_key=True)
    telegram_id = Column(BigInteger, nullable=False, index=True)
    opponent_name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    result = Column(String, nullable=False)