from data import AREAS
from enums import Area, AreaKey, Color, Item, Path, Object, ObjectKey
from logger import log, logc
from utils import colorize, display_name, print_narration, printc


def update_dynamic_visibility(state):
    pos = state.current_position
    inv = state.inventory

    if pos == Area.LIVING_ROOM and Item.SHED_KEY in inv:
        # Make ashes invisible when player has shed key
        if all(
            k in AREAS[pos][ObjectKey.INTERACTABLES]
            for k in (Object.ASHES, Object.BUTTON, Object.FIREPLACE)
        ):
            set_visible(state, pos, Object.ASHES, False)

    if pos == Area.YARD and Item.SHOVEL in inv:
        # Make x mark visible when player has shovel
        if Object.X_MARK in AREAS[pos][ObjectKey.INTERACTABLES]:
            set_visible(state, pos, Object.X_MARK, True)

    if pos == Area.YARD and Item.DOG_STATUE in inv:
        # Make carl disappear when player has dog statue
        if Object.CARL in AREAS[pos][ObjectKey.INTERACTABLES]:
            set_visible(state, pos, Object.CARL, False)

    if pos == Area.GARDEN and state.safe_revealed and Item.UNTITLED_47 in inv:
        # Show magic plant in garden if safe has been revealed
        # and player has untitled #47
        if Object.MAGIC_PLANT in AREAS[pos][ObjectKey.INTERACTABLES]:
            set_visible(state, pos, Object.MAGIC_PLANT, True)


def handle_movement(state, direction):
    can_go, message = can_use_exit(
        state, state.current_position, direction, state.inventory
    )
    if not can_go:
        log(state, message)
        return state.current_position

    requirement = get_exit_requirement(state.current_position, direction)
    if not _confirm_exit(state, requirement):
        return state.current_position

    success_message = requirement.get(AreaKey.CONFIRM_SUCCESS_MESSAGE)
    if success_message:
        print_narration(success_message, state, color=Color.BRIGHT_CYAN)

    if state.current_position == Area.GARDEN and direction == Path.EAST:
        state.shed_unlocked = True

    next_area = AREAS[state.current_position][AreaKey.EXITS][direction]
    logc(
        state,
        f"▶ You go " f"{display_name(direction)}: {display_name(next_area)}",
        Color.BRIGHT_BLUE,
    )
    return next_area


def get_exit_requirement(area, direction):
    return AREAS[area].get(AreaKey.EXIT_REQUIREMENTS, {}).get(direction, {})


def _confirm_exit(state, requirement):
    """
    Some exits (like a one-way jump with no going back) need an explicit
    y/n confirmation before the player commits. Exits with no CONFIRM_PROMPT
    skip this entirely and proceed as normal.
    """
    raw_prompt = requirement.get(AreaKey.CONFIRM_PROMPT)
    if not raw_prompt:
        return True

    print_narration(raw_prompt, state, color=Color.BRIGHT_CYAN)

    question = colorize(
        requirement.get(AreaKey.CONFIRM_QUESTION, "▶ Proceed? (y/n): "),
        Color.GREEN,
    )
    while True:
        choice = input(question).strip().lower()
        if choice in ("y", "yes"):
            return True
        if choice in ("n", "no"):
            logc(
                state,
                requirement.get(
                    AreaKey.CONFIRM_DECLINE_MESSAGE, "▶ You decide against it."
                ),
                Color.GREEN,
            )
            return False
        printc(" Invalid input, please enter y/n.", Color.GREEN)


CONDITION_OBJECT_MAP = {
    Object.WATERED_PLANT: Object.MAGIC_PLANT,
    Object.STATUE_PLACED: Object.PEDESTAL,
}


def can_use_exit(state, current_position, direction, inventory):
    area = AREAS[current_position]
    if AreaKey.EXIT_REQUIREMENTS not in area:
        return True, None

    required = get_exit_requirement(current_position, direction)
    if not required:
        return True, None

    # Handle item requirements
    if AreaKey.ITEM in required and required[AreaKey.ITEM] not in inventory:
        return False, required[AreaKey.MESSAGE]

    # Handle condition requirements (like watered plant)
    if ObjectKey.CONDITION in required:
        condition = required[ObjectKey.CONDITION]
        check_object = CONDITION_OBJECT_MAP.get(condition, condition)
        if not is_used(state, current_position, check_object):
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
    interactable = AREAS[area].get(ObjectKey.INTERACTABLES, {}).get(obj_name)
    if not interactable:
        return False
    if ObjectKey.BECOMES_ITEM in interactable and is_used(
        state, area, obj_name
    ):
        return False
    return interactable and interactable.get(ObjectKey.VISIBLE, True)


def set_visible(state, area, obj_name, value):
    state.object_visible[(area, obj_name)] = value


def reveal_interactable(state, area, interactable_name):
    if interactable_name in AREAS[area].get(ObjectKey.INTERACTABLES, {}):
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
                reveal_interactable(state, area_name, obj[ObjectKey.REVEALS])
