from dataclasses import dataclass, field

from enums import Area, Item, ItemState


@dataclass
class GameState:
    action_log: list = field(default_factory=list)
    current_position: Area = Area.LIVING_ROOM
    debug_mode: bool = False
    full_history: list = field(default_factory=list)
    inventory: list = field(default_factory=list)
    item_states: dict = field(
        default_factory=lambda: {Item.WATERING_CAN: ItemState.EMPTY}
    )
    new_log_lines: int = 0
    object_used: set = field(default_factory=set)
    object_visible: dict = field(default_factory=dict)
    player_name: str = ""
    safe_revealed: bool = False
    shed_unlocked: bool = False
    shown_inventory_help: bool = False

    @classmethod
    def debug_state(cls, area):
        """Start in any area with debug mode enabled, for manual testing."""
        return cls(current_position=area, debug_mode=True)
