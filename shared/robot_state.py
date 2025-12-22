
from dataclasses import dataclass, field

@dataclass
class RobotState:
    x: int = 0
    y: int = 0
    battery: int = 100
    status: str = "IDLE"
    map_size: tuple[int, int] = (10, 10)
    obstacles: list[tuple[int, int]] = field(default_factory=list)
    current_path: list[tuple[int, int]] | None = None
    current_goal: tuple[int, int] | None = None
