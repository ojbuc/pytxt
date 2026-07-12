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
        from enums import AreaKey, ObjectKey
        from world import reveal_interactable

        state = cls(current_position=area)
        state.inventory = list(Item)
        state.item_states[Item.WATERING_CAN] = ItemState.FULL
        state.safe_revealed = True

        for area_name, area_data in AREAS.items():
            # Remove items from the world so they can't be picked up again
            area_items = area_data.get(AreaKey.ITEMS, {})
            for item in list(area_items):
                if item in state.inventory:
                    del area_items[item]

            # Mark interactables as used so they can't be re-granted
            interactables = area_data.get(ObjectKey.INTERACTABLES, {})
            for obj_name, obj in interactables.items():
                granted = [
                        obj.get(ObjectKey.GIVES_ITEM),
                        obj.get(ObjectKey.ALSO_GIVES),
                        obj.get(ObjectKey.BECOMES_ITEM),
                ]
                if any(g in state.inventory for g in granted if g is not None):
                    state.object_used.add((area_name, obj_name))
                    if ObjectKey.REVEALS in obj:
                        reveal_interactable(
                                state, area_name, obj[ObjectKey.REVEALS]
                        )
        return state
