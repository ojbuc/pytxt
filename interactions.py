from data import (
        AREAS,
        GENERIC_WRONG_ITEM_RESPONSE,
        ITEM_DESCRIPTIONS,
        WRONG_ITEM_RESPONSES
)
from display import show_object_not_found
from enums import Area, Object, Used
from logger import log
from utils import resolve_name
from world import is_visible, reveal_interactable


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
        current_state = state.item_states.get(item_to_check, "default")

        if current_state != required_state:
            return (
                obj.get(Object.FAILED_STATE_RESULT,
                obj[Object.INTERACTION_RESULT]),
                False,
            )
    # Item requirements met
    return obj.get(Object.SUCCESS_RESULT, obj[Object.INTERACTION_RESULT]), True


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
