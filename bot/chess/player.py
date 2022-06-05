from .enums import Colors
from dataclasses import dataclass

@dataclass
class Player:
    id: int
    color: Colors