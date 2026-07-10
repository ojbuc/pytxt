from data import AREAS
from enums import Area, AreaKey, Color, Item, Object, ObjectKey
from world import can_use_exit, is_used, is_visible

import subprocess


def display_interactables(state, current_position):
    if ObjectKey.INTERACTABLES not in AREAS[current_position]:
        return

    visible_interactables = [
        name
        for name in AREAS[current_position][ObjectKey.INTERACTABLES]
        if is_visible(state, current_position, name)
    ]

    if not visible_interactables:
        return
    # Categorize objects by available actions
    examine_only = []
    use_only = []
    both = []

    for name in visible_interactables:
        obj = AREAS[current_position][ObjectKey.INTERACTABLES][name]
        can_examine = True  # All objects can be examined
        can_use = obj.get(ObjectKey.CAN_INTERACT, False)
        obj_name = name.value if hasattr(name, 'value') else name

        if can_examine and can_use:
            both.append(obj_name)
        elif can_examine:
            examine_only.append(obj_name)
        elif can_use:
            use_only.append(obj_name)

    if both:
        print(f"  You can examine and use: {', '.join(both)}")
    if examine_only:
        print(f"  You can examine: {', '.join(examine_only)}")
    if use_only:
        print(f"  You can use: {', '.join(use_only)}")


def display_area_information(state):
    clear_screen()
    # Show action log
    if state.action_log:
        print("=" * 40)
        for i, line in enumerate(state.action_log):
            if i >= len(state.action_log) - state.new_log_lines:
                print(f"{Color.YELLOW.value}{line}{Color.RESET.value}")
            else:
                print(line)
    print("=" * 40)

    print("Current area:")
    print("  " + get_area_description(state, state.current_position))
    # Show exits
    exits = AREAS[state.current_position][AreaKey.EXITS]
    exit_reqs = AREAS[state.current_position].get(AreaKey.EXIT_REQUIREMENTS, {})
    if exits:
        print("  Exits:")
        for direction, destination in exits.items():
            requirement = exit_reqs.get(direction, {})
            if ObjectKey.CONDITION in requirement:
                can_go, _ = can_use_exit(state, state.current_position,
                                         direction, [])
                if not can_go:
                    continue
            print(
                f"    ➜ {direction.value} - "
                f"{destination.value.replace('_', ' ')}"
            )
    # Show items
    if AREAS[state.current_position][AreaKey.ITEMS]:
        items = list(AREAS[state.current_position][AreaKey.ITEMS].keys())
        print(f"  Items here: {', '.join(items)}")
    # Show interactables
    display_interactables(state, state.current_position)


def get_area_description(state, area):
    default = AREAS[area][AreaKey.DESCRIPTION]

    if area == Area.LIVING_ROOM and is_used(state, area, Object.ASHES):
        return AREAS[area][AreaKey.POST_ASHES_DESCRIPTION]

    if area == Area.YARD and Item.DOG_STATUE in state.inventory:
        return "A ground of fertile green and earthy browns."

    return default


def clear_screen():
    subprocess.run("clear")
