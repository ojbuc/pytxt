import subprocess

from data import AREAS
from enums import Area, AreaKey, Color, Command, Item, ObjectKey, Status
from interactions import (
    handle_examine_command,
    handle_take_command,
    handle_use_command,
)
from logger import debug_log, log, logc
from utils import (
    colorize,
    display_name,
    flash_quit_message,
    printc,
    resolve_name,
)
from world import (
    handle_movement,
    is_visible,
    mark_used,
    set_visible,
    sync_granted_item,
)


def _cmd_take(state, command):
    area_items = list(AREAS[state.current_position][AreaKey.ITEMS].keys())
    partial = command[5:]  # Remove "take "
    obj_name, hint = resolve_name(partial, area_items)
    if hint:
        log(state, hint)
    elif obj_name:
        handle_take_command(state, obj_name)
    else:  # Check if it exists somewhere in the world
        if partial in _build_world_names(items_only=True):
            log(state, f"▶ There's no {partial} here.")
        else:
            log(state, "▶ You can't take that.")
    return state.current_position


def _cmd_use(state, command):
    visible_interactables = [
        name
        for name in AREAS[state.current_position][ObjectKey.INTERACTABLES]
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
            log(state, f"▶ You can't use the {partial} from here.")
        else:
            logc(state, "▶ You can't use that.", Color.GREEN)
    return state.current_position


def _cmd_examine(state, command):
    visible_interactables = [
        name
        for name in AREAS[state.current_position][ObjectKey.INTERACTABLES]
        if is_visible(state, state.current_position, name)
    ]
    area_items = list(
        AREAS[state.current_position].get(AreaKey.ITEMS, {}).keys()
    )
    # Handle other commands
    partial = (
        command[8:] if command.startswith(Command.EXAMINE) else command[3:]
    )
    candidates = visible_interactables + area_items + state.inventory
    obj_name, hint = resolve_name(partial, candidates)
    if hint:
        log(state, hint)
    elif obj_name:
        handle_examine_command(state, obj_name)
    else:
        if partial in _build_world_names():
            logc(state, f"▶ There's no {partial} here.", Color.GREEN)
        else:
            logc(state, "▶ You can't examine that.", Color.BRIGHT_CYAN)
    return state.current_position


def _cmd_debug(state, command):
    remainder = command[6:].strip()  # Remove "debug "
    if not remainder:
        _debug_help(state)
        return state.current_position

    parts = remainder.split(maxsplit=1)
    action = parts[0]
    args = parts[1] if len(parts) > 1 else ""

    handlers = {
        "give": _debug_give,
        "add": _debug_give,
        "drop": _debug_drop,
        "goto": _debug_goto,
        "teleport": _debug_goto,
        "reveal": _debug_reveal,
        "hide": _debug_hide,
        "use": _debug_use,
        "unuse": _debug_unuse,
        "state": _debug_state,
        "list": _debug_list,
    }

    if action == "help":
        _debug_help(state)
        return state.current_position

    handler = handlers.get(action)
    if handler is None:
        debug_log(
            state,
            f"▶ [DEBUG] Unknown debug command '{action}'. "
            "Try 'debug help'.",
        )
        return state.current_position
    return handler(state, args)


def _debug_give(state, args):
    if not args:
        debug_log(state, "▶ [DEBUG] Usage: debug give <item|all>")
        return state.current_position

    if args.strip().lower() == "all":
        added = []
        for item in list(Item):
            if item not in state.inventory:
                state.inventory.append(item)
                sync_granted_item(state, item)
                added.append(item.value)
        if added:
            debug_log(state, f"▶ [DEBUG] Added: {', '.join(
                          display_name(a) for a in added)}")
        else:
            debug_log(state, "▶ [DEBUG] You already have every item.")
        return state.current_position

    item, hint = resolve_name(args, list(Item))
    if hint:
        log(state, hint)
    elif item:
        if item in state.inventory:
            debug_log(state, f"▶ [DEBUG] You already have '{item.value}'.")
        else:
            state.inventory.append(item)
            sync_granted_item(state, item)
            debug_log(state, f"▶ [DEBUG] Added '{item.value}' to inventory.")
    else:
        debug_log(state, f"▶ [DEBUG] No item matches '{args}'.")
    return state.current_position


def _debug_drop(state, args):
    if not args:
        debug_log(state, "▶ [DEBUG] Usage: debug drop <item>")
        return state.current_position
    item, hint = resolve_name(args, state.inventory)
    if hint:
        log(state, hint)
    elif item:
        state.inventory.remove(item)
        name = item.value if hasattr(item, "value") else item
        debug_log(state, f"▶ [DEBUG] Removed '{name}' from inventory.")
    else:
        debug_log(state, f"▶ [DEBUG] '{args}' is not in your inventory.")
    return state.current_position


def _debug_goto(state, args):
    if not args:
        debug_log(state, "▶ [DEBUG] Usage: debug goto <area>")
        return state.current_position
    area, hint = resolve_name(args, list(Area))
    if hint:
        log(state, hint)
        return state.current_position
    if not area:
        debug_log(state, f"▶ [DEBUG] No area matches '{args}'.")
        return state.current_position
    debug_log(state, f"▶ [DEBUG] Teleporting to '{area.value}'.")
    return area


def _debug_set_visibility(state, args, value):
    if not args:
        verb = "reveal" if value else "hide"
        debug_log(state, f"▶ [DEBUG] Usage: debug {verb} <object>")
        return state.current_position
    interactables = AREAS[state.current_position][ObjectKey.INTERACTABLES]
    obj_name, hint = resolve_name(args, list(interactables.keys()))
    if hint:
        log(state, hint)
    elif obj_name:
        set_visible(state, state.current_position, obj_name, value)
        name = obj_name.value if hasattr(obj_name, "value") else obj_name
        verb = "Revealed" if value else "Hid"
        debug_log(state, f"▶ [DEBUG] {verb} '{name}'.")
    else:
        debug_log(state, f"▶ [DEBUG] No object matches '{args}' here.")
    return state.current_position


def _debug_reveal(state, args):
    return _debug_set_visibility(state, args, True)


def _debug_hide(state, args):
    return _debug_set_visibility(state, args, False)


def _debug_set_used(state, args, used):
    if not args:
        verb = "use" if used else "unuse"
        debug_log(state, f"▶ [DEBUG] Usage: debug {verb} <object>")
        return state.current_position
    interactables = AREAS[state.current_position][ObjectKey.INTERACTABLES]
    obj_name, hint = resolve_name(args, list(interactables.keys()))
    if hint:
        log(state, hint)
        return state.current_position
    if not obj_name:
        debug_log(state, f"▶ [DEBUG] No object matches '{args}' here.")
        return state.current_position
    name = obj_name.value if hasattr(obj_name, "value") else obj_name
    if used:
        mark_used(state, state.current_position, obj_name)
        debug_log(state, f"▶ [DEBUG] Marked '{name}' as used.")
    else:
        state.object_used.discard((state.current_position, obj_name))
        debug_log(state, f"▶ [DEBUG] Marked '{name}' as unused.")
    return state.current_position


def _debug_use(state, args):
    return _debug_set_used(state, args, True)


def _debug_unuse(state, args):
    return _debug_set_used(state, args, False)


def _debug_state(state, args):
    parts = args.split()
    if len(parts) < 2:
        debug_log(state, f"▶ [DEBUG] Usage: debug state <item> <state>")
        return state.current_position
    *item_parts, new_state = parts
    item_query = " ".join(item_parts)
    item, hint = resolve_name(item_query, list(Item))
    if hint:
        log(state, hint)
        return state.current_position
    if not item:
        debug_log(state, f"▶ [DEBUG] No item matches '{item_query}'.")
        return state.current_position
    state.item_states[item] = new_state
    debug_log(state, f"▶ [DEBUG] Set '{item.value}' state to '{new_state}'.")
    return state.current_position


def _debug_list(state, args):
    target = args.strip().lower()
    if target in ("item", "items"):
        names = ", ".join(display_name(i) for i in Item)
        debug_log(state, f"▶ [DEBUG] Items: {names}")
    elif target in ("area", "areas"):
        names = ", ".join(display_name(a) for a in Area)
        debug_log(state, f"▶ [DEBUG] Areas: {names}")
    elif target in ("object", "objects", "interactable", "interactables"):
        interactables = AREAS[state.current_position][ObjectKey.INTERACTABLES]
        names = ", ".join(display_name(n) for n in interactables) or "(none)"
        debug_log(state, f"▶ [DEBUG] Objects here: {names}")
    else:
        debug_log(state, "▶ [DEBUG] Usage: debug list <items|areas|objects>")
    return state.current_position


def _debug_help(state):
    debug_log(state, "\n[DEBUG] Debug commands:")
    debug_log(state, "  debug give <item|all>\t\t\t- Add item(s) to inventory")
    debug_log(state, "  debug drop <item>\t\t\t- Remove item from inventory")
    debug_log(state, "  debug goto <area>\t\t\t- Teleport to an area")
    debug_log(state, "  debug reveal <object>\t\t\t- Reveal object here")
    debug_log(state, "  debug hide <object>\t\t\t- Hide object here")
    debug_log(state, "  debug use <object>\t\t\t- Mark object as used")
    debug_log(state, "  debug unuse <object>\t\t\t- Mark object as unused")
    debug_log(state, "  debug state <item> <state>\t\t- Set an item's state")
    debug_log(state, "  debug list <items|areas|objects>\t- List valid names")


COMMAND_DISPATCH = [
    (Command.EXAMINE, _cmd_examine),
    (Command.EX, _cmd_examine),
    (Command.USE, _cmd_use),
    (Command.TAKE, _cmd_take),
]

DIRECTION_ALIASES = {
    "n": "north",
    "s": "south",
    "e": "east",
    "w": "west",
    "u": "up",
    "d": "down",
}

KNOWN_DIRECTIONS = set(DIRECTION_ALIASES.values()) | set(
    DIRECTION_ALIASES.keys()
)


def _build_world_names(items_only=False, interactables_only=False):
    names = set()
    for area in AREAS.values():
        if not interactables_only:
            for item in area.get(AreaKey.ITEMS, {}).keys():
                names.add(item.value if hasattr(item, "value") else item)
        if not items_only:
            for obj in area.get(ObjectKey.INTERACTABLES, {}).keys():
                names.add(obj.value if hasattr(obj, "value") else obj)
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
    logc(state, f"> {command}", Color.BRIGHT_BLACK)

    # Debug commands are handled first and only run in debug mode
    if command == "debug" or command.startswith(Command.DEBUG):
        if not state.debug_mode:
            log(
                state, "▶ Invalid command, type 'help' for a list of commands."
            )
            return Status.CONTINUE
        return _cmd_debug(state, command)

    # Try movement
    direction = parse_movement_command(state, command)
    if direction:
        return handle_movement(state, direction)

    for prefix, handler in COMMAND_DISPATCH:
        if command.startswith(prefix):
            return handler(state, command) or Status.CONTINUE

    if command in (Command.INVENTORY, Command.INV):
        handle_inventory_command(state)
    elif command == Command.HISTORY:
        show_history(state)
    elif command == Command.HELP:
        show_help(state)
    elif command in (Command.ABANDON):
        if handle_quit_command(state):
            return Status.QUIT
        else:
            direction_attempt = parse_direction_attempt(command)
            if direction_attempt:
                log(state, f"▶ There's no exit {direction_attempt} from here.")
            else:
                log(
                    state,
                    "▶ Invalid command, type 'help' for a list of commands.",
                )
    return Status.CONTINUE


def parse_movement_command(state, command):
    parts = command.split()
    if not parts:
        return None
    exits = AREAS[state.current_position][AreaKey.EXITS]
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
        items = ", ".join(display_name(i) for i in state.inventory)
        logc(state, f"▶ You have: {items}", Color.GREEN)
        if not state.shown_inventory_help:
            logc(state, "▶ (You can examine items in your inventory)", 
                        Color.GREEN)
            state.shown_inventory_help = True
    else:
        logc(state, "▶ Your inventory is empty.", Color.GREEN)


def show_history(state):
    if not state.full_history:
        printc(" There is no history yet.", Color.GREEN)
        input(colorize(" Press Enter to continue: ", Color.GREEN))
        return
    content = "\n".join(state.full_history)
    subprocess.run(
        ["less", "-R", "--prompt=History (q to quit, arrows to scroll)"],
        input=content,
        text=True,
    )


def show_help(state):
    logc(state, "\nAvailable commands:", Color.GREEN)
    logc(
        state,
        "  • go <direction/location> OR <direction/location>\t- Go somewhere",
        Color.GREEN,
    )
    logc(
        state,
        "  • examine OR ex <item/object/etc>\t\t\t- Examine the surroundings",
        Color.GREEN,
    )
    logc(state, "  • use <object>\t\t\t\t\t- Use something", Color.GREEN)
    logc(
        state,
        "  • use <item> on <object>\t\t\t\t- Use a specific item on an object",
        Color.GREEN,
    )
    logc(
        state,
        "  • take <item>\t\t\t\t\t\t- Pick up an item and add it to your "
        "inventory",
        Color.GREEN,
    )
    logc(
        state,
        "  • inventory OR inv\t\t\t\t\t- Show your inventory",
        Color.GREEN,
    )
    logc(
        state,
        "  • history\t\t\t\t\t\t- View full command history",
        Color.GREEN,
    )
    logc(state, "  • help\t\t\t\t\t\t- Show this help menu", Color.GREEN)
    logc(
        state,
        "  • abandon\t\t\t\t\t\t- End the game (without saving progress)",
        Color.GREEN,
    )


def handle_quit_command(state):
    while True:
        quit_confirm = (
            input(
                colorize(
                    " Would you like to quit? (y/n): ", Color.BRIGHT_GREEN
                )
            )
            .strip()
            .lower()
        )
        if quit_confirm in ("y", "yes"):
            flash_quit_message(" Ending the adventure!")
            return Status.QUIT
        if quit_confirm in ("n", "no"):
            logc(state, "▶ The adventure continues!\n", Color.BRIGHT_GREEN)
            return False
        printc(" Invalid input, please enter y/n.", Color.GREEN)
