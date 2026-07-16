import subprocess

from data import AREAS
from enums import Area, AreaKey, Color, Item, Object, ObjectKey
from utils import colorize, display_name, printc, substitute_player_name
from world import can_use_exit, is_used, is_visible


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
        obj_name = display_name(name)

        if can_examine and can_use:
            both.append(obj_name)
        elif can_examine:
            examine_only.append(obj_name)
        elif can_use:
            use_only.append(obj_name)

    if both:
        printc(f"  You can examine and use: {', '.join(both)}", Color.YELLOW)
    if examine_only:
        printc(f"  You can examine: {', '.join(examine_only)}", Color.YELLOW)
    if use_only:
        printc(f"  You can use: {', '.join(use_only)}", Color.YELLOW)


def display_area_information(state):
    clear_screen()
    # Show action log
    if state.action_log:
        printc("=" * 40, Color.BRIGHT_WHITE)
        for i, line in enumerate(state.action_log):
            if i >= len(state.action_log) - state.new_log_lines:
                print(f"{Color.BRIGHT_YELLOW.value}{line}{Color.RESET.value}")
            else:
                print(line)
    printc("=" * 40, Color.BRIGHT_WHITE)

    printc(
        f"Current area ({display_name(state.current_position.value)}):",
        Color.BRIGHT_BLUE,
    )
    description = colorize(
        get_area_description(state, state.current_position), Color.BRIGHT_CYAN
    )
    for line in description.split("\n"):
        print(f"  {line}")
    # Show exits
    exits = AREAS[state.current_position][AreaKey.EXITS]
    exit_reqs = AREAS[state.current_position].get(
        AreaKey.EXIT_REQUIREMENTS, {}
    )
    if exits:
        printc("  Exits:", Color.BRIGHT_MAGENTA)
        for direction, destination in exits.items():
            requirement = exit_reqs.get(direction, {})
            if ObjectKey.CONDITION in requirement:
                can_go, _ = can_use_exit(
                    state, state.current_position, direction, []
                )
                if not can_go:
                    continue
            printc(f"    ➜ {display_name(direction.value)} - " f"{display_name(
                destination.value.replace('_', ' '))}", Color.BRIGHT_RED)
    # Show items
    if AREAS[state.current_position][AreaKey.ITEMS]:
        items = [
            display_name(item)
            for item in AREAS[state.current_position][AreaKey.ITEMS].keys()
        ]
        printc(f"  Items here: {', '.join(items)}", Color.BLUE)
    # Show interactables
    display_interactables(state, state.current_position)


def get_area_description(state, area):
    if area == Area.LIVING_ROOM and is_used(state, area, Object.ASHES):
        return AREAS[area][AreaKey.POST_ASHES_DESCRIPTION]
    elif area == Area.YARD and Item.DOG_STATUE in state.inventory:
        return "A ground of fertile green and earthy browns."
    else:
        description = AREAS[area][AreaKey.DESCRIPTION]
    return substitute_player_name(description, state)


def clear_screen():
    subprocess.run("clear")
