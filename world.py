from data import AREAS
from enums import Area, Item, Object
from logger import log


def update_dynamic_visibility(state):
    """ Update visibility of objects that depend on inventory items. """
    pos = state.current_position
    inv = state.inventory

    if pos == Area.LIVING_ROOM and Item.SHED_KEY in inv:
        # Make ashes invisible when player has shed key
        if (
            all(k in AREAS[pos][Object.INTERACTABLES] for
                k in (Object.ASHES, Object.BUTTON, Object.FIREPLACE))
        ):
            AREAS[pos][Object.INTERACTABLES][
                  Object.ASHES][Object.VISIBLE] = False

    if pos == Area.YARD and Item.SHOVEL in inv:
        # Make x mark visible when player has shovel
        if Object.X_MARK in AREAS[pos][Object.INTERACTABLES]:
            AREAS[pos][Object.INTERACTABLES][Object.X_MARK][
                    Object.VISIBLE] = True

    if pos == Area.YARD and Item.DOG_STATUE in inv:
        # Make carl disappear when player has dog statue
        if Object.CARL in AREAS[pos][Object.INTERACTABLES]:
            AREAS[pos][Object.INTERACTABLES][ Object.CARL][
                    Object.VISIBLE] = False
            AREAS[pos][Area.DESCRIPTION
            ] = "A ground of fertile green and earthy browns."
    # Show magic plant in garden if safe has been revealed
    # and player has untitled #47
    if (
        pos == Area.GARDEN
        and state.safe_revealed
        and Item.UNTITLED_47 in inv
    ):
        if Object.MAGIC_PLANT in AREAS[pos][Object.INTERACTABLES]:
            AREAS[pos][Object.INTERACTABLES][
                  Object.MAGIC_PLANT][Object.VISIBLE] = True


def handle_movement(state, direction):
    can_go, message = can_use_exit(
            state.current_position, direction, state.inventory
    )
    if can_go:
        next_area = AREAS[state.current_position][Area.EXITS][direction]
        log(state, f"▶ You go {direction}: {next_area.value.replace('_', ' ')}")
        return next_area

    log(state, message)
    return state.current_position


def can_use_exit(current_position, direction, inventory):
    """ Check if player can use this exit. """
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
            plant_obj = area[Object.INTERACTABLES].get(Object.MAGIC_PLANT)
            if not plant_obj or not plant_obj.get(Object.USED, False):
                return False, required[Area.MESSAGE]

        if required[Object.CONDITION] == Object.STATUE_PLACED:
            pedestal_obj = area[Object.INTERACTABLES].get(Object.PEDESTAL)
            if not pedestal_obj or not pedestal_obj.get(Object.USED, False):
                return False, required[Area.MESSAGE]
    return True, None


def is_visible(area, interactable_name):
    """ Check if an interactable object is visible to the player. """
    interactable = AREAS[area][Object.INTERACTABLES].get(interactable_name)
    return interactable and interactable.get(Object.VISIBLE, True)


def reveal_interactable(area, interactable_name):
    """ Make a hidden interactable object visible in the specified area. """
    if interactable_name in AREAS[area][Object.INTERACTABLES]:
        AREAS[area][Object.INTERACTABLES][interactable_name][
                Object.VISIBLE] = True
