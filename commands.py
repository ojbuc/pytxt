from data import AREAS
from display import show_object_not_found
from enums import Area, Command, Object, Status
from interactions import (
        handle_examine_command,handle_take_command, handle_use_command
)
from logger import log
from utils import resolve_name
from world import handle_movement, is_visible


# Shorthand directions for faster movement between areas
DIRECTION_ALIASES = {
    "n": "north", "s": "south", "e": "east",
    "w": "west", "u": "up", "d": "down"
}


def process_command(state, command):
    """ Process a single command and return new area state. """
    state.new_log_lines = 0

    # Try movement first
    direction = parse_movement_command(state, command)
    if direction:
        return handle_movement(state, direction)

    if command.startswith(Command.EXAMINE) or command.startswith(Command.EX):
        return _cmd_examine(state, command)
    if command.startswith(Command.USE):
        return _cmd_use(state, command)
    if command.startswith(Command.TAKE):
        return _cmd_take(state, command)
    if command in (Command.INVENTORY, Command.INV):
        handle_inventory_command(state)
        return Status.CONTINUE
    if command in Command.HELP:
        show_help(state)
        return Status.CONTINUE
    if command in (Command.QUIT, Command.EXIT):
        return Status.QUIT if handle_quit_command(state) else Status.CONTINUE

    log(state, "▶ Invalid command, type 'help' for a list of commands.")
    return state.current_position


def _cmd_examine(state, command):
    visible_interactables = [
        name for name in AREAS[state.current_position][Object.INTERACTABLES]
        if is_visible(state.current_position, name)
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
        show_object_not_found(state)
    return state.current_position


def _cmd_use(state, command):
    visible_interactables = [
        name for name in AREAS[state.current_position][Object.INTERACTABLES]
        if is_visible(state.current_position, name)
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
        log(state, "▶ You can't interact with that.")
    return state.current_position


def _cmd_take(state, command):
    area_items = list(AREAS[state.current_position][Area.ITEMS].keys())
    partial = command[5:]  # Remove "take "
    obj_name, hint = resolve_name(partial, area_items)
    if hint:
        log(state, hint)
    elif obj_name:
        handle_take_command(state, obj_name)
    else:
        log(state, "▶ You can't take that.")
    return state.current_position


def parse_movement_command(state, command):
    """ Parse movement commands and return direction if valid. """
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
        print("▶ You have: " + ", ".join(state.inventory))
        if not state.shown_inventory_help:
            print("▶ (You can examine items in your inventory)")
            state.shown_inventory_help = True
    else:
        print("▶ Your inventory is empty.")
    input("▶ Press Enter to continue: ")


def show_help(state):
    log(state, "\nAvailable commands:")
    log(state,
        "  • go <direction> OR <direction> - Move in specified direction"
    )
    log(state, "  • examine OR ex <object> - Examine an object")
    log(state,
    "  • use <object> - Interact with an object (prompts for item if needed)"
    )
    log(state, "  • use <item> on <object> - Use a specific item on an object")
    log(state, "  • take <item> - Pick up an item and add it to your inventory")
    log(state, "  • inventory OR inv - Show your inventory")
    log(state, "  • help - Show this help menu")
    log(state, "  • quit OR exit - End the game without saving progress")


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
