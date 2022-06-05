from uuid import UUID
from .enums import Colors
from dataclasses import dataclass

@dataclass
class Player:
    id: int
    game_id: UUID
    color: Colors