from data import AREAS
from enums import Area, Item, Object
from logger import log


def update_dynamic_visibility(state):
    pos = state.current_position
    inv = state.inventory

    if pos == Area.LIVING_ROOM and Item.SHED_KEY in inv:
        # Make ashes invisible when player has shed key
        if all(k in AREAS[pos][Object.INTERACTABLES] for
               k in (Object.ASHES, Object.BUTTON, Object.FIREPLACE)):
            set_visible(state, pos, Object.ASHES, False)

    if pos == Area.YARD and Item.SHOVEL in inv:
        # Make x mark visible when player has shovel
        if Object.X_MARK in AREAS[pos][Object.INTERACTABLES]:
            set_visible(state, pos, Object.X_MARK, True)

    if pos == Area.YARD and Item.DOG_STATUE in inv:
        # Make carl disappear when player has dog statue
        if Object.CARL in AREAS[pos][Object.INTERACTABLES]:
            set_visible(state, pos, Object.CARL, False)

    # Show magic plant in garden if safe has been revealed
    # and player has untitled #47
    if (pos == Area.GARDEN and state.safe_revealed
            and Item.UNTITLED_47 in inv):
        if Object.MAGIC_PLANT in AREAS[pos][Object.INTERACTABLES]:
            set_visible(state, pos, Object.MAGIC_PLANT, True)


def handle_movement(state, direction):
    can_go, message = can_use_exit(state, state.current_position, 
                                   direction, state.inventory)
    if can_go:
        next_area = AREAS[state.current_position][Area.EXITS][direction]
        log(state, f"▶ You go "
                   f"{direction}: {next_area.value.replace('_', ' ')}")
        return next_area

    log(state, message)
    return state.current_position


def can_use_exit(state, current_position, direction, inventory):
    area = AREAS[current_position]
    if Area.EXIT_REQUIREMENTS not in area:
        return True, None

    required = area[Area.EXIT_REQUIREMENTS].get(direction)
    if not required:
        return True, None

    # Handle item requirements
    if Area.ITEM in required and required[Area.ITEM] not in inventory:
        return False, required[Area.MESSAGE]

    # Handle condition requirements (like watered plant)
    if Object.CONDITION in required:
        if required[Object.CONDITION] == Object.WATERED_PLANT:
            if not is_used(state, current_position, Object.MAGIC_PLANT):
                return False, required[Area.MESSAGE]

        if required[Object.CONDITION] == Object.STATUE_PLACED:
            if not is_used(state, current_position, Object.PEDESTAL):
                return False, required[Area.MESSAGE]
    return True, None


def is_used(state, area, obj_name):
    return (area, obj_name) in state.object_used


def mark_used(state, area, obj_name):
    state.object_used.add((area, obj_name))


def is_visible(state, area, obj_name):
    key = (area, obj_name)
    if key in state.object_visible:
        return state.object_visible[key]
    interactable = AREAS[area][Object.INTERACTABLES].get(obj_name)
    return interactable and interactable.get(Object.VISIBLE, True)


def set_visible(state, area, obj_name, value):
    state.object_visible[(area, obj_name)] = value


def reveal_interactable(state, area, interactable_name):
    if interactable_name in AREAS[area][Object.INTERACTABLES]:
        set_visible(state, area, interactable_name, True)
