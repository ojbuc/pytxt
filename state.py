from dataclasses import dataclass, field
from enums import Area


@dataclass
class GameState:
    current_position: Area = Area.LIVING_ROOM
    inventory: list = field(default_factory=list)
    action_log: list = field(default_factory=list)
    new_log_lines: int = 0
    shown_inventory_help: bool = False
    item_states: dict = field(default_factory=lambda: {"watering can": "empty"})
    safe_revealed: bool = False

