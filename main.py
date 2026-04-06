import os
from data import (
        AREAS,
        ITEM_DESCRIPTIONS,
        WRONG_ITEM_RESPONSES,
        GENERIC_WRONG_ITEM_RESPONSE
)
from enums import Area, Item, Object, Status, Command, Used, Color
from state import GameState

LOG_MAX = 8

# Shorthand directions for faster movement between areas
DIRECTION_ALIASES = {
    "n": "north", "s": "south", "e": "east",
    "w": "west", "u": "up", "d": "down"
}


def clear_screen():
    os.system("clear")


def log(state, message):
    """Add a message to the action log, keeping only the last LOG_MAX lines."""
    for line in message.split("\n"):
        if line.strip():
            state.action_log.append(line)
            state.new_log_lines += 1
    while len(state.action_log) > LOG_MAX:
        state.action_log.pop(0)


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


def handle_inventory_command(state):
    if state.inventory:
        print("▶ You have: " + ", ".join(state.inventory))
        if not state.shown_inventory_help:
            print("▶ (You can examine items in your inventory)")
            state.shown_inventory_help = True
    else:
        print("▶ Your inventory is empty.")
    input("▶ Press Enter to continue: ")


def get_item_description(state, item_name):
    """ Get description for an item based on its current state. """
    if item_name in state.item_states:
        item_state = state.item_states[item_name]
        if isinstance(ITEM_DESCRIPTIONS[item_name], dict):
            return ITEM_DESCRIPTIONS[item_name][item_state]
    # Fallback to simple description or default
    item_desc = ITEM_DESCRIPTIONS.get(item_name)
    if isinstance(item_desc, dict):
        return item_desc.get("default", f"A {item_name}.")
    return item_desc or f"A {item_name}."


def handle_take_command(state, item_name):
    area_items = AREAS[state.current_position][Area.ITEMS]
    # Find the matching key (may be an Item enum)
    key_match = next((k for k in area_items if k == item_name), None)
    if key_match is not None:
        state.inventory.append(key_match)
        log(state,
            "▶ You take the "
            f"{key_match.value if hasattr(key_match, 'value') else key_match}."
        )
        del area_items[key_match]
    else:
        log(state, "▶ You can't take that.")


def show_object_not_found(state):
    log(state, "▶ You don't see that here.")


def is_visible(area, interactable_name):
    """ Check if an interactable object is visible to the player. """
    interactable = AREAS[area][Object.INTERACTABLES].get(interactable_name)
    return interactable and interactable.get(Object.VISIBLE, True)


def reveal_interactable(area, interactable_name):
    """ Make a hidden interactable object visible in the specified area. """
    if interactable_name in AREAS[area][Object.INTERACTABLES]:
        AREAS[area][Object.INTERACTABLES][interactable_name][
                Object.VISIBLE] = True


def _mark_as_used(obj, obj_name):
    """ Mark an object as used when appropriate. """
    if any([
        Object.GIVES_ITEM in obj
        or Object.ALSO_GIVES in obj
        or Object.BECOMES_ITEM in obj
        or obj_name == Object.CARL
        or Object.ENABLES_EXIT in obj
    ]):
        obj[Object.USED] = True


def _apply_state_changes(state, obj):
    """ Update item states (e.g. watering can empty/full). """
    if Object.CHANGES_ITEM_STATE in obj:
        for item, new_state in obj[Object.CHANGES_ITEM_STATE].items():
            if item in state.inventory:
                state.item_states[item] = new_state


def _apply_item_removals(obj, obj_name, inventory, result_parts):
    """ Handle removing items from inventory after use. """
    consumed_objects = {
        Object.CARL: "gave Carl the",
        Object.PEDESTAL: "placed the",
    }
    if obj_name not in consumed_objects:
        return
    required_item = obj[Object.REQUIRES_ITEM]
    if required_item and required_item in inventory:
        inventory.remove(required_item)
        verb = consumed_objects[obj_name]
        suffix = " on the pedestal" if obj_name == Object.PEDESTAL else ""
        result_parts.append(f"\n▶ (You {verb} {required_item.value}{suffix})")


def _apply_item_grants(state, obj, obj_name, result_parts):
    """ Handle giving primary, secondary and painting-become items. """
    if obj.get(Object.USED, False):
        return

    if Object.GIVES_ITEM in obj:
        state.inventory.append(obj[Object.GIVES_ITEM])
        result_parts.append("\n▶ (You now have: "
                            f" {obj[Object.GIVES_ITEM].value})")

    if Object.ALSO_GIVES in obj:
        state.inventory.append(obj[Object.ALSO_GIVES])
        result_parts.append("\n▶ (You also found: "
                            f"{obj[Object.ALSO_GIVES].value})")

    if Object.BECOMES_ITEM in obj:
        state.inventory.append(obj[Object.BECOMES_ITEM])
        result_parts.append("\n▶ (You now have: "
                            f"{obj[Object.BECOMES_ITEM].value})")
        if obj_name == Object.LOOSE_PAINTING:
            state.safe_revealed = True
            for area in AREAS.values():
                if obj_name in area.get(Object.INTERACTABLES, {}):
                    del area[Object.INTERACTABLES][obj_name]
                    break


def apply_interaction_effects(state, obj, obj_name, success):
    """ Apply the effects of a successful interaction. """
    if not success:
        return ""

    result_parts = []

    _apply_item_grants(state, obj, obj_name, result_parts)
    _apply_item_removals(obj, obj_name, state.inventory, result_parts)
    _apply_state_changes(state, obj)
    _mark_as_used(obj, obj_name)

    return "".join(result_parts)


def get_wrong_item_response(obj_name, used_item):
    """ 
    Return the appropriate response when the wrong item is used on an object.
    """
    obj_responses = WRONG_ITEM_RESPONSES.get(obj_name)
    if obj_responses:
        if isinstance(obj_responses, dict):
            return obj_responses.get(used_item, GENERIC_WRONG_ITEM_RESPONSE)
        return obj_responses
    return GENERIC_WRONG_ITEM_RESPONSE



def handle_item_requirements(state, obj, obj_name=None, used_item=None):
    """ Handle object interaction requirements and return result message. """
    required_item = obj[Object.REQUIRES_ITEM]
    # If the player specified an item, test that item specifically
    if used_item is not None:
        if used_item != required_item:
            return get_wrong_item_response(obj_name, used_item), False
        # Correct item - fall through to state check below
        item_to_check = used_item
    else:
        # Legacy auto-check: look for the required item in inventory
        if required_item not in state.inventory:
            return obj[Object.INTERACTION_RESULT], False
        item_to_check = required_item
    # Check if item needs to be in specific state
    if Object.REQUIRES_ITEM_STATE in obj:
        required_state = obj[Object.REQUIRES_ITEM_STATE]
        current_state = state.item_state.get(item_to_check, "default")

        if current_state != required_state:
            return (
                obj.get(Object.FAILED_STATE_RESULT,
                obj[Object.INTERACTION_RESULT]),
                False,
            )
    # Item requirements met
    return obj.get(Object.SUCCESS_RESULT, obj[Object.INTERACTION_RESULT]), True


def get_used_message(obj_name):
    """ Get appropriate message for already used objects. """
    if Used.BUTTON in obj_name.lower():
        return "▶ The button has already been pressed."
    if Used.CARL in obj_name.lower():
        return (
            "▶ Carl is happily chewing his bone and gives you a contented wag."
        )
    if Used.DRAWER in obj_name.lower():
        return "▶ The drawer is already open and empty."
    if Used.PAINTING in obj_name.lower():
        return "▶ You've already taken the painting."
    if Used.PLANT in obj_name.lower():
        return (
            "▶ The magic plant has grown into a magnificent beanstalk. "
            "▶ It doesn't need any more water."
        )
    if Used.X_MARK in obj_name.lower():
        return "▶ You've already dug here. There's just a hole in the ground."
    return "▶ You've already used this."


def interact_with_object(state, obj_name, used_item=None):
    """ Handle interaction with objects. """
    obj = AREAS[state.current_position][Object.INTERACTABLES][obj_name]
    # Check if object has already been used
    if obj.get(Object.USED, False):
        return get_used_message(obj_name)
    # Handle objects with item requirements
    if Object.REQUIRES_ITEM in obj:
        result, success = handle_item_requirements(
               state, obj, obj_name=obj_name, used_item=used_item
        )
        effects = apply_interaction_effects(state, obj, obj_name, success)
        return result + effects
    # No item requirement - if player tried to use an item here, note it
    if used_item is not None:
        return get_wrong_item_response(obj_name, used_item)
    # No item requirement - normal interaction
    result = obj[Object.INTERACTION_RESULT]
    effects = apply_interaction_effects(state, obj, obj_name, True)
    return result + effects


def prompt_item_selection(inventory):
    """
    Prompt the player to pick an item from their inventory.
    Returns the chosen item name, or None if cancelled.
    """
    if not inventory:
        return None

    print("▶ Use what?")
    for i, item in enumerate(inventory, 1):
        print(f"  {i}: {item.value if hasattr(item, 'value') else item}")
    print("  0: cancel")

    while True:
        choice = input("▶ ").strip().lower()
        if choice in ("0", "cancel", ""):
            return None
        # Accept number
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(inventory):
                return inventory[idx]
        # Accept item name or partial name
        resolved, hint = resolve_name(choice, inventory)
        if hint:
            print(hint)
            continue
        if resolved:
            return resolved
        print("▶ Invalid choice.")


def handle_use_command(state, obj_name, used_item=None):
    if obj_name not in AREAS[state.current_position][Object.INTERACTABLES]:
        log(state, "▶ You can't interact with that.")
        return

    if not is_visible(state.current_position, obj_name):
        show_object_not_found(state)
        return

    obj = AREAS[state.current_position][Object.INTERACTABLES][obj_name]
    # If the object accepts items and none was specified, prompt the player
    if used_item is None and state.inventory and obj.get(Object.REQUIRES_ITEM):
        used_item = prompt_item_selection(state.inventory)
        if used_item is None:
            log(state, "▶ Never mind.")
            return
    # Capture reveals before the interaction marks object as used
    reveals_target = (
            obj.get(Object.REVEALS) if not obj.get(Object.USED, False) else None
    )

    output = interact_with_object(state, obj_name, used_item=used_item)
    log(state, output)

    if reveals_target:
        reveal_interactable(state.current_position, reveals_target)
    # Handle reveals
    obj = AREAS[state.current_position][Object.INTERACTABLES].get(obj_name)
    if obj and Object.REVEALS in obj and not obj.get(Object.USED, False):
        reveal_interactable(state.current_position, obj[Object.REVEALS])
        obj[Object.USED] = True


def handle_examine_command(state, obj_name):
    """ Handle examine commands for objects and items. """
    # Check inventory items first
    if obj_name in state.inventory:
        log(state, get_item_description(state, obj_name))
        return
    # Check area interactables
    if obj_name in AREAS[state.current_position][Object.INTERACTABLES]:
        if is_visible(state.current_position, obj_name):
            obj = AREAS[state.current_position][Object.INTERACTABLES][obj_name]
            if obj_name == Object.FIREPLACE:
                interactables = AREAS[state.current_position][
                                      Object.INTERACTABLES]
                button = interactables.get(Object.BUTTON, {})
                ashes = interactables.get(Object.ASHES, {})
                if ashes.get(Object.USED):
                    log(state, obj[Object.POST_ASHES_DESCRIPTION])
                elif button.get(Object.USED):
                    log(state, obj[Object.POST_BUTTON_DESCRIPTION])
                elif obj.get(Object.USED) and Object.USED_DESCRIPTION in obj:
                    log(state, obj[Object.USED_DESCRIPTION])
                else:
                    log(state, obj[Object.DESCRIPTION])
            elif obj.get(Object.USED) and Object.USED_DESCRIPTION in obj:
                log(state, obj[Object.USED_DESCRIPTION])
            else:
                log(state, obj[Object.DESCRIPTION])
            return
        show_object_not_found(state)
        return
    # Check area items
    if obj_name in AREAS[state.current_position][Area.ITEMS]:
        log(state, AREAS[state.current_position][Area.ITEMS][obj_name])
        return
    show_object_not_found(state)


def resolve_name(partial, candidates):
    """ Resolve a partial name to a full name from a list of candidates. """
    # Exact match first
    if partial in candidates:
        return partial, None
    # Substring matches
    matches = [c for c in candidates if partial in c]

    if len(matches) == 1:
        return matches[0], None
    if len(matches) > 1:
        return None, f"▶ Did you mean: {', '.join(matches)}?"
    # No match found
    return None, None


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


def main():
    try:
        state = GameState()

        while True:
            update_dynamic_visibility(state)
            display_area_information(state)

            command = input("▶ ").strip().lower()
            if not command:
                continue

            output = process_command(state, command)

            if output == Status.QUIT:
                break
            if output == Status.CONTINUE:
                continue

            assert isinstance(output, Area)
            state.current_position = output
            print()

    except KeyboardInterrupt:
        print("\n▶ The adventure ends abruptly!\n")


if __name__ == "__main__":
    main()
