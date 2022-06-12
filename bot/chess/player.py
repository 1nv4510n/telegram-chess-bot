from uuid import UUID
from .enums import Colors, ChessStatus
from dataclasses import dataclass

@dataclass
class Player:
    id: int
    rating: float
    game_id: UUID
    color: Colors
    status: ChessStatus