from dataclasses import dataclass, field
from typing import Optional

@dataclass
class RobotState:
    x: int = 0
    y: int = 0
    battery: int = 100
    status: str = "IDLE"
    map_size: tuple[int, int] = (10, 10)
    obstacles: list[tuple[int, int]] = field(default_factory=list)
    current_path: Optional[list[tuple[int, int]]] = None
    current_goal: Optional[tuple[int, int]] = None
