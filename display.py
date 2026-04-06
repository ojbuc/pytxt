import os
from data import AREAS
from enums import Area, Color, Object
from logger import log
from world import can_use_exit, is_visible


def display_interactables(current_position):
    if Object.INTERACTABLES not in AREAS[current_position]:
        return

    visible_interactables = [
        name
        for name in AREAS[current_position][Object.INTERACTABLES]
        if is_visible(current_position, name)
    ]

    if not visible_interactables:
        return
    # Categorize objects by available actions
    examine_only = []
    use_only = []
    both = []

    for name in visible_interactables:
        obj = AREAS[current_position][Object.INTERACTABLES][name]
        can_examine = True  # All objects can be examined
        can_use = obj.get(Object.CAN_INTERACT, False)
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
    print("  " + AREAS[state.current_position][Area.DESCRIPTION])
    # Show exits
    exits = AREAS[state.current_position][Area.EXITS]
    exit_reqs = AREAS[state.current_position].get(Area.EXIT_REQUIREMENTS, {})
    if exits:
        print("  Exits:")
        for direction, destination in exits.items():
            requirement = exit_reqs.get(direction, {})
            if Object.CONDITION in requirement:
                can_go, _ = can_use_exit(state.current_position, direction, [])
                if not can_go:
                    continue
            print(
                f"    ➜ {direction.value} - "
                f"{destination.value.replace('_', ' ')}"
            )
    # Show items
    if AREAS[state.current_position][Area.ITEMS]:
        items = list(AREAS[state.current_position][Area.ITEMS].keys())
        print(f"  Items here: {', '.join(items)}")
    # Show interactables
    display_interactables(state.current_position)


def show_object_not_found(state):
    log(state, "▶ You don't see that here.")


def clear_screen():
    os.system("clear")
