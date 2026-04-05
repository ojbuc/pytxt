from data import (
        AREAS, 
        ITEM_DEFINITIONS, 
        WRONG_ITEM_RESPONSES, 
        GENERIC_WRONG_ITEM_RESPONSE
)
from enums import Area, Item, Object, Status, Command, Color
import os

ACTION_LOG = []
LOG_MAX = 8
NEW_LOG_LINES = 0

# Global game state
SHOWN_INVENTORY_HELP = False

# Track item states
ITEM_STATES = {"watering can": "empty"}  # can be "empty" or "full"

# Track puzzle progress
SAFE_REVEALED = False

# Shorthand directions for faster movement between areas
DIRECTION_ALIASES = {
    "n": "north", "s": "south", "e": "east",
    "w": "west", "u": "up", "d": "down"
}


def clear_screen():
    os.system("clear")


def log(message):
    """Add a message to the action log, keeping only the last LOG_MAX lines."""
    global NEW_LOG_LINES
    for line in message.split("\n"):
        if line.strip():
            ACTION_LOG.append(line)
            NEW_LOG_LINES += 1
    while len(ACTION_LOG) > LOG_MAX:
        ACTION_LOG.pop(0)


def handle_quit_command():
    while True:
        quit_confirm = (
                input("▶ Would you like to quit? (y/n): ").strip().lower()
        )

        if quit_confirm in ('y', 'yes'): 
            print("▶ Ending the adventure...\n")
            return True
        elif quit_confirm in ('n', 'no'):
            log("▶ The adventure continues!\n")
            return False
        else:
            print("▶ Invalid input, please enter y/n.")


def show_help():
    log("\nAvailable commands:")
    log("  • go <direction> OR <direction> - Move in specified direction")
    log("  • examine OR ex <object> - Examine an object")
    log(
    "  • use <object> - Interact with an object (prompts for item if needed)"
    )
    log("  • use <item> on <object> - Use a specific item on an object")
    log("  • take <item> - Pick up an item and add it to your inventory")
    log("  • inventory OR inv - Show your inventory")
    log("  • help - Show this help menu")
    log("  • quit OR exit - End the game without saving progress")


def handle_inventory_command(inventory):
    global SHOWN_INVENTORY_HELP
    if inventory:
        print("▶ You have: " + ", ".join(inventory))
        if not SHOWN_INVENTORY_HELP:
            print("▶ (You can examine items in your inventory)")
            SHOWN_INVENTORY_HELP = True
    else:
        print("▶ Your inventory is empty.")
    input("▶ Press Enter to continue: ")


def get_item_description(item_name):
    """ Get description for an item based on its current state. """
    if item_name in ITEM_STATES:
        state = ITEM_STATES[item_name]
        if isinstance(ITEM_DEFINITIONS[item_name], dict):
            return ITEM_DEFINITIONS[item_name][state]

    # Fallback to simple description or default
    item_desc = ITEM_DEFINITIONS.get(item_name)
    if isinstance(item_desc, dict):
        return item_desc.get("default", f"A {item_name}.")
    return item_desc or f"A {item_name}."


def handle_take_command(item_name, current_position, inventory):
    area_items = AREAS[current_position][Area.ITEMS]
    # Find the matching key (may be an Item enum)
    key_match = next((k for k in area_items if k == item_name), None)
    if key_match is not None:
        inventory.append(key_match)
        log(f"▶ You take the "
            f"{key_match.value if hasattr(key_match, 'value') else key_match}."
        )
        del area_items[key_match]
    else:
        log("▶ You can't take that.")


def show_object_not_found():
    log("▶ You don't see that here.")


def is_visible(area, interactable_name):
    """ Check if an interactable object is visible to the player. """
    interactable = AREAS[area][Object.INTERACTABLES].get(interactable_name)
    return interactable and interactable.get(Object.VISIBLE, True)


def reveal_interactable(area, interactable_name):
    """ Make a hidden interactable object visible in the specified area. """
    if interactable_name in AREAS[area][Object.INTERACTABLES]:
        AREAS[area][Object.INTERACTABLES][interactable_name][
                Object.VISIBLE] = True


def apply_interaction_effects(obj, obj_name, inventory, success):
    """ Apply the effects of a successful interaction. """
    global SAFE_REVEALED
    result_parts = []

    if not success:
        return ""

    # Give primary item
    if Object.GIVES_ITEM in obj and not obj.get(Object.USED, False):
        inventory.append(obj[Object.GIVES_ITEM])
        result_parts.append(
                f"\n▶ (You now have: {obj[Object.GIVES_ITEM].value})"
        )

    # Give secondary item
    if Object.ALSO_GIVES in obj and not obj.get(Object.USED, False):
        inventory.append(obj[Object.ALSO_GIVES])
        result_parts.append(
                f"\n▶ (You also found: {obj[Object.ALSO_GIVES].value})"
        )

    # Handle painting becoming an item
    if Object.BECOMES_ITEM in obj and not obj.get(Object.USED, False):
        inventory.append(obj[Object.BECOMES_ITEM])
        result_parts.append(
                f"\n▶ (You now have: {obj[Object.BECOMES_ITEM].value})"
        )
        if obj_name == Object.LOOSE_PAINTING:
            SAFE_REVEALED = True
            # Remove painting from interactables
            for area in AREAS.values():
                if obj_name in area.get(Object.INTERACTABLES, {}):
                    del area[Object.INTERACTABLES][obj_name]
                    break

    # Remove bone from inventory
    if obj_name == Object.CARL and Object.REQUIRES_ITEM in obj:
        required_item = obj[Object.REQUIRES_ITEM]
        if required_item in inventory:
            inventory.remove(required_item)
            result_parts.append(f"\n▶ (You gave Carl the "
                                f"{required_item.value})")

    # Remove dog statue from inventory
    if obj_name == Object.PEDESTAL and Object.REQUIRES_ITEM in obj:
        required_item = obj[Object.REQUIRES_ITEM]
        if required_item in inventory:
            inventory.remove(required_item)
            result_parts.append(f"\n▶ (You placed the {required_item.value} "
                                 "on the pedestal)")

    # Change item states
    if Object.CHANGES_ITEM_STATE in obj:
        for item, new_state in obj[Object.CHANGES_ITEM_STATE].items():
            if item in inventory:
                ITEM_STATES[item] = new_state

    # Mark as used if it gives items, becomes item, or is Carl
    if (
        Object.GIVES_ITEM in obj
        or Object.ALSO_GIVES in obj
        or Object.BECOMES_ITEM in obj
        or obj_name == Object.CARL
        or Object.ENABLES_EXIT in obj
    ):
        obj[Object.USED] = True

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



def handle_item_requirements(obj, inventory, obj_name=None, used_item=None):
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
        if required_item not in inventory:
            return obj[Object.INTERACTION_RESULT], False
        item_to_check = required_item

    # Check if item needs to be in specific state
    if Object.REQUIRES_ITEM_STATE in obj:
        required_state = obj[Object.REQUIRES_ITEM_STATE]
        current_state = ITEM_STATES.get(item_to_check, "default")

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
    if "drawer" in obj_name.lower():
        return "▶ The drawer is already open and empty."
    if "button" in obj_name.lower():
        return "▶ The button has already been pressed."
    if "x mark" in obj_name.lower():
        return "▶ You've already dug here. There's just a hole in the ground."
    if "carl" in obj_name.lower():
        return (
            "▶ Carl is happily chewing his bone and gives you a contented wag."
        )
    if "painting" in obj_name.lower():
        return "▶ You've already taken the painting."
    if "plant" in obj_name.lower():
        return (
            "▶ The magic plant has grown into a magnificent beanstalk. "
            "▶ It doesn't need any more water."
        )
    return "▶ You've already used this."


def interact_with_object(area_name, obj_name, inventory, used_item=None):
    """ Handle interaction with objects. """
    obj = AREAS[area_name][Object.INTERACTABLES][obj_name]

    # Check if object has already been used
    if obj.get(Object.USED, False):
        return get_used_message(obj_name)

    # Handle objects with item requirements
    if Object.REQUIRES_ITEM in obj:
        result, success = handle_item_requirements(
                obj, inventory, obj_name=obj_name, used_item=used_item
        )
        effects = apply_interaction_effects(obj, obj_name, inventory, success)
        return result + effects

    # No item requirement - if player tried to use an item here, note it
    if used_item is not None:
        return get_wrong_item_response(obj_name, used_item)

    # No item requirement - normal interaction
    result = obj[Object.INTERACTION_RESULT]
    effects = apply_interaction_effects(obj, obj_name, inventory, True)
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


def handle_use_command(obj_name, current_position, inventory, used_item=None):
    if obj_name not in AREAS[current_position][Object.INTERACTABLES]:
        log("▶ You can't interact with that.")
        return

    if not is_visible(current_position, obj_name):
        show_object_not_found()
        return

    obj = AREAS[current_position][Object.INTERACTABLES][obj_name]

    # If the object accepts items and none was specified, prompt the player
    if used_item is None and inventory and obj.get(Object.REQUIRES_ITEM):
        used_item = prompt_item_selection(inventory)
        if used_item is None:
            log("▶ Never mind.")
            return

    # Capture reveals before interact_with_object marks obj as used
    reveals_target = (
            obj.get(Object.REVEALS) if not obj.get(Object.USED, False) else None
    )

    result = interact_with_object(
            current_position, obj_name, inventory, used_item=used_item
    )
    log(result)

    if reveals_target:
        reveal_interactable(current_position, reveals_target)

    # Handle reveals
    obj = AREAS[current_position][Object.INTERACTABLES].get(obj_name)
    if obj and Object.REVEALS in obj and not obj.get(Object.USED, False):
        reveal_interactable(current_position, obj[Object.REVEALS])
        obj[Object.USED] = True


def handle_examine_command(obj_name, current_position, inventory):
    """ Handle examine commands for objects and items. """
    # Check inventory items first
    if obj_name in inventory:
        log(get_item_description(obj_name))
        return

    # Check area interactables
    if obj_name in AREAS[current_position][Object.INTERACTABLES]:
        if is_visible(current_position, obj_name):
            obj = AREAS[current_position][Object.INTERACTABLES][obj_name]
            if obj_name == Object.FIREPLACE:
                interactables = AREAS[current_position][Object.INTERACTABLES]
                button = interactables.get(Object.BUTTON, {})
                ashes = interactables.get(Object.ASHES, {})
                if ashes.get(Object.USED):
                    log(obj[Object.POST_ASHES_DESCRIPTION])
                elif button.get(Object.USED):
                    log(obj[Object.POST_BUTTON_DESCRIPTION])
                elif obj.get(Object.USED) and Object.USED_DESCRIPTION in obj:
                    log(obj[Object.USED_DESCRIPTION])
                else:
                    log(obj[Object.DESCRIPTION])
            elif obj.get(Object.USED) and Object.USED_DESCRIPTION in obj:
                log(obj[Object.USED_DESCRIPTION])
            else:
                log(obj[Object.DESCRIPTION])
            return
        else:
            show_object_not_found()
            return
    # Check area items
    if obj_name in AREAS[current_position][Area.ITEMS]:
        log(AREAS[current_position][Area.ITEMS][obj_name])
        return

    show_object_not_found()


def resolve_name(partial, candidates):
    """ Resolve a partial name to a full name from a list of candidates. """
    # Exact match first
    if partial in candidates:
        return partial, None

    # Substring matches
    matches = [c for c in candidates if partial in c]

    if len(matches) == 1:
        return matches[0], None
    elif len(matches) > 1:
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


def handle_movement(direction, current_position, inventory):
    can_go, message = can_use_exit(current_position, direction, inventory)
    if can_go:
        next_area = AREAS[current_position][Area.EXITS][direction]
        log(f"▶ You go {direction}: {next_area.value.replace('_', ' ')}")
        return next_area

    log(message)
    return current_position


def parse_movement_command(command, current_position):
    """ Parse movement commands and return direction if valid. """
    parts = command.split()
    if not parts:
        return None
    exits = AREAS[current_position][Area.EXITS]

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


def process_command(command, current_position, inventory):
    """ Process a single command and return new area state. """
    global NEW_LOG_LINES
    NEW_LOG_LINES = 0

    # Try movement first
    direction = parse_movement_command(command, current_position)
    if direction:
        return handle_movement(direction, current_position, inventory)

    # Build candidate lists
    visible_interactables = [
        name for name in AREAS[current_position][Object.INTERACTABLES]
        if is_visible(current_position, name)
    ]
    area_items = list(AREAS[current_position][Area.ITEMS].keys())

    # Handle other commands
    if command.startswith(Command.EXAMINE) or command.startswith(Command.EX):
        # Remove "examine " or "ex "
        partial = (
                command[8:] if command.startswith(Command.EXAMINE) 
                else command[3:]
        )
        candidates = visible_interactables + area_items + inventory
        obj_name, hint = resolve_name(partial, candidates)
        if hint:
            log(hint)
        elif obj_name:
            handle_examine_command(obj_name, current_position, inventory)
        else:
            show_object_not_found()

    elif command.startswith(Command.USE):
        remainder = command[4:]  # Remove "use "
        used_item = None

        # Parse "use <item> on <object>"
        if " on " in remainder:
            item_part, obj_part = remainder.split(" on ", 1)
            item_resolved, item_hint = resolve_name(item_part, inventory)
            if item_hint:
                log(item_hint)
                return current_position
            if not item_resolved:
                log("▶ You don't have that item.")
                return current_position
            used_item = item_resolved
            partial = obj_part
        else:
            partial = remainder

        candidates = visible_interactables
        obj_name, hint = resolve_name(partial, candidates)
        if hint:
            log(hint)
        elif obj_name:
            handle_use_command(
                    obj_name, current_position, inventory, used_item=used_item
            )
        else:
            log("▶ You can't interact with that.")

    elif command.startswith(Command.TAKE):
        partial = command[5:]  # Remove "take "
        candidates = area_items
        obj_name, hint = resolve_name(partial, candidates)
        if hint:
            log(hint)
        elif obj_name:
            handle_take_command(obj_name, current_position, inventory)
        else:
            log("▶ You can't take that.")

    elif command in (Command.INVENTORY, Command.INV):
        handle_inventory_command(inventory)
        return Status.CONTINUE
    elif command == Command.HELP:
        show_help()
        return Status.CONTINUE
    elif command == Command.QUIT or command == Command.EXIT:
        if handle_quit_command():
            return Status.QUIT
        return Status.CONTINUE
    else:
        log("▶ Invalid command, type 'help' for a list of commands.")

    return current_position


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


def display_area_information(current_position):
    clear_screen()

    # Show action log
    if ACTION_LOG:
        print("=" * 40)
        for i, line in enumerate(ACTION_LOG):
            if i >= len(ACTION_LOG) - NEW_LOG_LINES:
                print(f"{Color.YELLOW.value}{line}{Color.RESET.value}")
            else:
                print(line)
    print("=" * 40)

    print("Current area:")
    print("  " + AREAS[current_position][Area.DESCRIPTION])

    # Show exits
    exits = AREAS[current_position][Area.EXITS]
    exit_reqs = AREAS[current_position].get(Area.EXIT_REQUIREMENTS, {})
    if exits:
        print("  Exits:")
        for direction, destination in exits.items():
            requirement = exit_reqs.get(direction, {})
            if Object.CONDITION in requirement:
                can_go, _ = can_use_exit(current_position, direction, [])
                if not can_go:
                    continue
            print(
                f"    ➜ {direction.value} - "
                f"{destination.value.replace('_', ' ')}"
            )
    # Show items
    if AREAS[current_position][Area.ITEMS]:
        items = list(AREAS[current_position][Area.ITEMS].keys())
        print(f"  Items here: {', '.join(items)}")
    # Show interactables
    display_interactables(current_position)


def update_dynamic_visibility(current_position, inventory):
    """ Update visibility of objects that depend on inventory items. """
    if current_position == Area.LIVING_ROOM and Item.SHED_KEY in inventory:
        # Make ashes invisible when player has shed key
        if (
            all(k in AREAS[current_position][Object.INTERACTABLES] for 
                k in (Object.ASHES, Object.BUTTON, Object.FIREPLACE))
        ):
            AREAS[current_position][Object.INTERACTABLES][
                  Object.ASHES][Object.VISIBLE] = False

    if current_position == Area.YARD and Item.SHOVEL in inventory:
        # Make x mark visible when player has shovel
        if Object.X_MARK in AREAS[current_position][Object.INTERACTABLES]:
            AREAS[current_position][Object.INTERACTABLES][Object.X_MARK][
                  Object.VISIBLE] = True

    if current_position == Area.YARD and Item.DOG_STATUE in inventory:
        # Make carl disappear when player has dog statue
        if Object.CARL in AREAS[current_position][Object.INTERACTABLES]:
            AREAS[current_position][Object.INTERACTABLES][
                  Object.CARL][Object.VISIBLE] = False
            AREAS[current_position][
                  Area.DESCRIPTION
            ] = "A ground of fertile green and earthy browns."

    # Show magic plant in garden if safe has been revealed 
    # and player has untitled #47
    if (
        current_position == Area.GARDEN
        and SAFE_REVEALED
        and Item.UNTITLED_47 in inventory
    ):
        if Object.MAGIC_PLANT in AREAS[current_position][Object.INTERACTABLES]:
            AREAS[current_position][Object.INTERACTABLES][
                  Object.MAGIC_PLANT][Object.VISIBLE] = True


def main():
    try:
        current_position = Area.LIVING_ROOM
        inventory = []

        while True:
            # Update dynamic visibility based on current inventory
            update_dynamic_visibility(current_position, inventory)

            # Display area information
            display_area_information(current_position)

            # Get and process command
            command = input("▶ ").strip().lower()
            if not command:
                continue
            new_position = process_command(command, current_position, inventory)

            if new_position == Status.QUIT:
                break

            if new_position == Status.CONTINUE:
                continue

            current_position = new_position
            print()

    except KeyboardInterrupt:
        print("\n▶ The adventure ends abruptly!\n")


if __name__ == "__main__":
    main()
