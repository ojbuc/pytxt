import subprocess

from data import AREAS
from enums import Area, AreaKey, Color, Item, Object, ObjectKey
from utils import (
    colorize, display_name, printc, resolve_description, substitute_player_name
)
from world import can_use_exit, is_used, is_visible


def display_interactables(state, current_position):
    interactables = AREAS[current_position].get(ObjectKey.INTERACTABLES, {})

    if not interactables:
        return

    visible_interactables = [
        name
        for name in AREAS[current_position][ObjectKey.INTERACTABLES]
        if is_visible(state, current_position, name)
    ]

    if not visible_interactables:
        return

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
        printc(f"  You can examine: {', '.join(examine_only)}", Color.MAGENTA)
    if use_only:
        printc(f"  You can use: {', '.join(use_only)}", Color.WHITE)


def display_area_information(state):
    clear_screen()

    # Show action log
    if state.action_log:
        printc("=" * 40, Color.BRIGHT_WHITE)
        for i, line in enumerate(state.action_log):
            if i >= len(state.action_log) - state.new_log_lines:
                print(f"{Color.BOLD_CYAN.value}{line}{Color.RESET.value}")
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
    exits = AREAS[state.current_position].get(AreaKey.EXITS, {})
    exit_reqs = AREAS[state.current_position].get(
        AreaKey.EXIT_REQUIREMENTS, {}
    )
    if exits:
        printc("  Exits:", Color.BRIGHT_RED)
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
    area_items = AREAS[state.current_position].get(AreaKey.ITEMS, {})
    if area_items:
        items = [display_name(item) for item in area_items.keys()]
        printc(f"  Items here: {', '.join(items)}", Color.BLUE)

    # Show interactables
    display_interactables(state, state.current_position)


def get_area_description(state, area):
    description = resolve_description(
        state, AREAS[area], AreaKey.DESCRIPTION_STATES, AreaKey.DESCRIPTION
    )
    return substitute_player_name(description, state)


def clear_screen():
    subprocess.run("clear")
