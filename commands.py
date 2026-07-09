from data import AREAS
from enums import Area, Command, Object, Status
from interactions import (
        handle_examine_command, handle_take_command, handle_use_command
)
from logger import log
from utils import resolve_name
from world import handle_movement, is_visible

import subprocess


def _cmd_take(state, command):
    area_items = list(AREAS[state.current_position][Area.ITEMS].keys())
    partial = command[5:]  # Remove "take "
    obj_name, hint = resolve_name(partial, area_items)
    if hint:
        log(state, hint)
    elif obj_name:
        handle_take_command(state, obj_name)
    else: # Check if it exists somewhere in the world
        if partial in _build_world_names(items_only=True):
            log(state, f"▶ There's no {partial} here.")
        else:
            log(state, "▶ You can't take that.")
    return state.current_position


def _cmd_use(state, command):
    visible_interactables = [
        name for name in AREAS[state.current_position][Object.INTERACTABLES]
        if is_visible(state, state.current_position, name)
    ]
    remainder = command[4:]  # Remove "use "
    used_item = None
    # Parse "use <item> on <object>"
    if " on " in remainder:
        item_part, obj_part = remainder.split(" on ", 1)
        item_resolved, item_hint = resolve_name(item_part, state.inventory)
        if item_hint:
            log(state, item_hint)
            return state.current_position
        if not item_resolved:
            log(state, "▶ You don't have that item.")
            return state.current_position
        used_item = item_resolved
        partial = obj_part
    else:
        partial = remainder
    obj_name, hint = resolve_name(partial, visible_interactables)
    if hint:
        log(state, hint)
    elif obj_name:
        handle_use_command(state, obj_name, used_item=used_item)
    else:
        if partial in _build_world_names(interactables_only=True):
            log(state,
                f"▶ You can't use the {partial} from here."
            )
        else:
            log(state, "▶ You can't use that.")
    return state.current_position


def _cmd_examine(state, command):
    visible_interactables = [
        name for name in AREAS[state.current_position][Object.INTERACTABLES]
        if is_visible(state, state.current_position, name)
    ]
    area_items = list(AREAS[state.current_position][Area.ITEMS].keys())
    # Handle other commands
    partial = (
            command[8:] if command.startswith(Command.EXAMINE)
            else command[3:]
    )
    candidates = visible_interactables + area_items + state.inventory
    obj_name, hint = resolve_name(partial, candidates)
    if hint:
        log(state, hint)
    elif obj_name:
        handle_examine_command(state, obj_name)
    else:
        if partial in _build_world_names():
            log(state, f"▶ There's no {partial} here.")
        else:
            log(state, "▶ You can't examine that.")
    return state.current_position


COMMAND_DISPATCH = [
    (Command.EXAMINE, _cmd_examine),
    (Command.EX,      _cmd_examine),
    (Command.USE,     _cmd_use),
    (Command.TAKE,    _cmd_take),
]

DIRECTION_ALIASES = {
    "n": "north", "s": "south", "e": "east",
    "w": "west", "u": "up", "d": "down"
}

KNOWN_DIRECTIONS = (
    set(DIRECTION_ALIASES.values()) | set(DIRECTION_ALIASES.keys())
)


def _build_world_names(items_only=False, interactables_only=False):
    names = set()
    for area in AREAS.values():
        if not interactables_only:
            for item in area.get(Area.ITEMS, {}).keys():
                names.add(item.value if hasattr(item, 'value') else item)
        if not items_only:
            for obj in area.get(Object.INTERACTABLES, {}).keys():
                names.add(obj.value if hasattr(obj, 'value') else obj)
    return names


def parse_direction_attempt(command):
    parts = command.split()
    if not parts:
        return None
    first = DIRECTION_ALIASES.get(parts[0], parts[0])
    if len(parts) == 1 and first in KNOWN_DIRECTIONS:
        return first
    if len(parts) == 2 and parts[0] == "go":
        second = DIRECTION_ALIASES.get(parts[1], parts[1])
        if second in KNOWN_DIRECTIONS:
            return second
    return None


def process_command(state, command):
    state.new_log_lines = 0

    # Try movement first
    direction = parse_movement_command(state, command)
    if direction:
        return handle_movement(state, direction)


    result = None
    for prefix, handler in COMMAND_DISPATCH:
        if command.startswith(prefix):
            result = handler(state, command)
            break
    else:
        if command in (Command.INVENTORY, Command.INV):
            handle_inventory_command(state)
        elif command in Command.HISTORY:
            show_history(state)
        elif command in Command.HELP:
            show_help(state)
        elif command in (Command.QUIT, Command.EXIT):
            if handle_quit_command(state):
                return Status.QUIT
        else:
            direction_attempt = parse_direction_attempt(command)
            if direction_attempt:
                log(state,
                    f"▶ There's no exit {direction_attempt} from here."
                )
            else:
                log(state,
                    "▶ Invalid command, type 'help' for a list of commands."
                )
    return result if result is not None else Status.CONTINUE


def parse_movement_command(state, command):
    parts = command.split()
    if not parts:
        return None
    exits = AREAS[state.current_position][Area.EXITS]
    # Resolve alias first
    first = DIRECTION_ALIASES.get(parts[0], parts[0])
    # "n", "north", "go north"
    if len(parts) == 1 and first in exits:
        return first
    if len(parts) == 2 and parts[0] == "go":
        second = DIRECTION_ALIASES.get(parts[1], parts[1])
        if second in exits:
            return second
    # "living area" or "go living area" - match by destination name
    # Strip leading "go " if present
    dest_input = command[3:] if command.startswith("go ") else command
    for direction, destination in exits.items():
        if dest_input == destination:
            return direction
    return None


def handle_inventory_command(state):
    if state.inventory:
        items = ", ".join(
            i.value if hasattr(i, "value") else i for i in state.inventory
        )
        log(state, f"▶ You have: {items}")
        if not state.shown_inventory_help:
            log(state, "▶ (You can examine items in your inventory)")
            state.shown_inventory_help = True
    else:
        log(state, "▶ Your inventory is empty.")


def show_history(state):
    if not state.full_history:
        print("▶ There is no history yet.")
        input("▶ Press Enter to continue: ")
        return
    content = "\n".join(state.full_history)
    subprocess.run(
        ["less", "-R", "--prompt=History (q to quit, arrows to scroll)"],
        input=content,
        text=True
    )


def show_help(state):
    log(state, "\nAvailable commands:")
    log(state,
        "  • go <direction/location> OR <direction/location> - Go somewhere"
    )
    log(state, "  • examine OR ex <item/object/etc> - Examine the surroundings")
    log(state,
    "  • use <object> - Use something"
    )
    log(state, "  • use <item> on <object> - Use a specific item on an object")
    log(state, "  • take <item> - Pick up an item and add it to your inventory")
    log(state, "  • inventory OR inv - Show your inventory")
    log(state, "  • history - View full command history")
    log(state, "  • help - Show this help menu")
    log(state, "  • quit OR exit - End the game without saving progress)")


def handle_quit_command(state):
    while True:
        quit_confirm = (
                input("▶ Would you like to quit? (y/n): ").strip().lower()
        )
        if quit_confirm in ('y', 'yes'):
            print("▶ Ending the adventure...\n")
            return True
        if quit_confirm in ('n', 'no'):
            log(state, "▶ The adventure continues!\n")
            return False
        print("▶ Invalid input, please enter y/n.")
