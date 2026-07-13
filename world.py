from data import AREAS
from enums import Area, AreaKey, Item, Object, ObjectKey
from logger import log


def update_dynamic_visibility(state):
    pos = state.current_position
    inv = state.inventory

    if pos == Area.LIVING_ROOM and Item.SHED_KEY in inv:
        # Make ashes invisible when player has shed key
        if all(k in AREAS[pos][ObjectKey.INTERACTABLES] for
               k in (Object.ASHES, Object.BUTTON, Object.FIREPLACE)):
            set_visible(state, pos, Object.ASHES, False)

    if pos == Area.YARD and Item.SHOVEL in inv:
        # Make x mark visible when player has shovel
        if Object.X_MARK in AREAS[pos][ObjectKey.INTERACTABLES]:
            set_visible(state, pos, Object.X_MARK, True)

    if pos == Area.YARD and Item.DOG_STATUE in inv:
        # Make carl disappear when player has dog statue
        if Object.CARL in AREAS[pos][ObjectKey.INTERACTABLES]:
            set_visible(state, pos, Object.CARL, False)

    # Show magic plant in garden if safe has been revealed
    # and player has untitled #47
    if (pos == Area.GARDEN and state.safe_revealed
            and Item.UNTITLED_47 in inv):
        if Object.MAGIC_PLANT in AREAS[pos][ObjectKey.INTERACTABLES]:
            set_visible(state, pos, Object.MAGIC_PLANT, True)


def handle_movement(state, direction):
    can_go, message = can_use_exit(state, state.current_position, 
                                   direction, state.inventory)
    if can_go:
        next_area = AREAS[state.current_position][AreaKey.EXITS][direction]
        log(state, f"▶ You go "
                   f"{direction}: {next_area.value.replace('_', ' ')}")
        return next_area

    log(state, message)
    return state.current_position


def can_use_exit(state, current_position, direction, inventory):
    area = AREAS[current_position]
    if AreaKey.EXIT_REQUIREMENTS not in area:
        return True, None

    required = area[AreaKey.EXIT_REQUIREMENTS].get(direction)
    if not required:
        return True, None

    # Handle item requirements
    if AreaKey.ITEM in required and required[AreaKey.ITEM] not in inventory:
        return False, required[AreaKey.MESSAGE]

    # Handle condition requirements (like watered plant)
    if ObjectKey.CONDITION in required:
        if required[ObjectKey.CONDITION] == Object.WATERED_PLANT:
            if not is_used(state, current_position, Object.MAGIC_PLANT):
                return False, required[AreaKey.MESSAGE]

        if required[ObjectKey.CONDITION] == Object.STATUE_PLACED:
            if not is_used(state, current_position, Object.PEDESTAL):
                return False, required[AreaKey.MESSAGE]
    return True, None


def is_used(state, area, obj_name):
    return (area, obj_name) in state.object_used


def mark_used(state, area, obj_name):
    state.object_used.add((area, obj_name))


def is_visible(state, area, obj_name):
    key = (area, obj_name)
    if key in state.object_visible:
        return state.object_visible[key]
    interactable = AREAS[area][ObjectKey.INTERACTABLES].get(obj_name)
    if not interactable:
        return False
    if (ObjectKey.BECOMES_ITEM in interactable 
        and is_used(state, area, obj_name)):
        return False
    return interactable and interactable.get(ObjectKey.VISIBLE, True)


def set_visible(state, area, obj_name, value):
    state.object_visible[(area, obj_name)] = value


def reveal_interactable(state, area, interactable_name):
    if interactable_name in AREAS[area][ObjectKey.INTERACTABLES]:
        set_visible(state, area, interactable_name, True)


def sync_granted_item(state, item):
    """
    Make the world consistent with 'item' being in inventory, for cases where
    it was added outside the normal interaction flow (debug tooling or a 
    fresh debug_state()):
        - remove it from any area's pickup pool, so it can't be taken twice
        - mark used any interactable that grants it, so 'use' can't re-grant
        it and reveal whatever that interactable would have revealed
    """
    for area_name, area_data in AREAS.items():
            area_items = area_data.get(AreaKey.ITEMS, {})
            if item in area_items:
                del area_items[item]

            interactables = area_data.get(ObjectKey.INTERACTABLES, {})
            for obj_name, obj in interactables.items():
                granted = [
                    obj.get(ObjectKey.GIVES_ITEM),
                    obj.get(ObjectKey.ALSO_GIVES),
                    obj.get(ObjectKey.BECOMES_ITEM),
                ]
                if item in granted:
                    mark_used(state, area_name, obj_name) 
                if ObjectKey.REVEALS in obj:
                    reveal_interactable(
                            state, area_name, obj[ObjectKey.REVEALS]
                    )
