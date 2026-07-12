from dataclasses import dataclass, field
from enums import Area, Item, ItemState


@dataclass
class GameState:
    action_log: list = field(default_factory=list)
    current_position: Area = Area.LIVING_ROOM
    full_history: list = field(default_factory=list)
    inventory: list = field(default_factory=list)
    item_states: dict = field(default_factory=lambda: 
                            {Item.WATERING_CAN: ItemState.EMPTY})
    new_log_lines: int = 0
    object_used: set = field(default_factory=set)
    object_visible: dict = field(default_factory=dict)
    safe_revealed: bool = False
    shown_inventory_help: bool = False

    @classmethod
    def debug_state(cls, area):
        """ Start in any area with every item, for manual testing. """
        from data import AREAS
        from enums import AreaKey

        state = cls(current_position=area)
        state.inventory = list(Item)
        state.item_states[Item.WATERING_CAN] = ItemState.FULL
        state.safe_revealed = True

        # Remove items from the world so they can't be picked up again
        for area_data in AREAS.values():
            area_items = area_data.get(AreaKey.ITEMS, {})
            for item in list(area_items):
                if item in state.inventory:
                    del area_items[item]
        return state
