from data import (
    AREAS,
    GENERIC_WRONG_ITEM_RESPONSE,
    ITEM_DESCRIPTIONS,
    WRONG_ITEM_RESPONSES,
)
from enums import AreaKey, Color, Item, Object, ObjectKey, Used
from logger import log, logc
from utils import (
    colorize, display_name, printc, resolve_description, resolve_name
)
from world import is_used, is_visible, mark_used, reveal_interactable


def handle_examine_command(state, obj_name):
    # Check inventory items first
    if obj_name in state.inventory:
        log(state, get_item_description(state, obj_name))
        return

    # Check area interactables
    if obj_name in AREAS[state.current_position].get(
        ObjectKey.INTERACTABLES, {}
    ):
        if is_visible(state, state.current_position, obj_name):
            obj = AREAS[state.current_position][ObjectKey.INTERACTABLES][
                obj_name
            ]

            hidden_item = obj.get(ObjectKey.HIDDEN_DESCRIPTION_ITEM)
            examine_with_item = False
            if hidden_item and hidden_item in state.inventory:
                examine_with_item = prompt_examine_method(state, hidden_item)

            if examine_with_item:
                logc(
                    state,
                    obj[ObjectKey.HIDDEN_DESCRIPTION],
                    Color.BRIGHT_MAGENTA,
                )
                return

            if (
                hidden_item
                and hidden_item in state.inventory
                and ObjectKey.PAINTED_EYE_TAKEN in obj
            ):
                log(state, obj[ObjectKey.PAINTED_EYE_TAKEN])

            log(state, get_object_description(state, obj))
            return

    # Check area items
    if obj_name in AREAS[state.current_position].get(AreaKey.ITEMS, {}):
        log(state, AREAS[state.current_position][AreaKey.ITEMS][obj_name])
        return

    logc(state, "▶ There's no items to examine here.", Color.GREEN)


def handle_use_command(state, obj_name, used_item=None):
    if obj_name not in AREAS[state.current_position].get(
        ObjectKey.INTERACTABLES, {}
    ):
        logc(state, "▶ You can't use that here.", Color.GREEN)
        return

    if not is_visible(state, state.current_position, obj_name):
        logc(state, "▶ You don't see that here.", Color.GREEN)
        return

    obj = AREAS[state.current_position][ObjectKey.INTERACTABLES][obj_name]

    if not obj.get(ObjectKey.CAN_INTERACT, False):
        logc(state, "▶ You can't use that.", Color.GREEN)
        return

    # If the object accepts items and none was specified, prompt the player
    if (
        used_item is None
        and state.inventory
        and ObjectKey.REQUIRES_ITEM in obj
        and not is_used(state, state.current_position, obj_name)
    ):
        used_item = prompt_item_selection(state.inventory)
        if used_item is None:
            logc(state, "▶ Never mind.", Color.GREEN)
            return

    was_used_before = is_used(state, state.current_position, obj_name)
    output = interact_with_object(state, obj_name, used_item=used_item)
    log(state, output)

    if (
        ObjectKey.REVEALS in obj
        and not was_used_before
        and is_used(state, state.current_position, obj_name)
    ):
        reveal_interactable(
            state, state.current_position, obj[ObjectKey.REVEALS]
        )


def prompt_examine_method(state, item_name):
    item_label = item_name.value if hasattr(item_name, "value") else item_name
    eyes_label = (
        f"{state.player_name}'s eyes" if state.player_name else "your own eyes"
    )
    printc(" Examine with what?", Color.GREEN)
    printc(f" 1: {eyes_label}", Color.BRIGHT_YELLOW)
    printc(f" 2: The {display_name(item_label)}", Color.BRIGHT_MAGENTA)

    while True:
        choice = input(colorize("▶ ", Color.GREEN)).strip().lower()
        if choice in ("1", "eyes", ""):
            return False
        if choice in ("2", item_label):
            return True
        printc(" Invalid choice.", Color.GREEN)


def prompt_item_selection(inventory, obj_name=None):
    if not inventory:
        return None

    target = f" with {display_name(obj_name)}" if obj_name else ""
    printc(f" Use what{target}?", Color.GREEN)
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
        printc(f" There's no {target} here.", Color.GREEN)


def interact_with_object(state, obj_name, used_item=None):
    obj = AREAS[state.current_position][ObjectKey.INTERACTABLES][obj_name]

    # Check if object has already been used
    if is_used(state, state.current_position, obj_name):
        return get_used_message(obj_name)

    # Check object-state precondition
    if ObjectKey.REQUIRES_OBJECT_USED in obj:
        required_obj = obj[ObjectKey.REQUIRES_OBJECT_USED]
        if not is_used(state, state.current_position, required_obj):
            return obj[ObjectKey.REQUIRES_OBJECT_USED_MESSAGE]

    # Handle objects with item requirements
    if ObjectKey.REQUIRES_ITEM in obj:
        result, success = handle_item_requirements(
            state, obj, obj_name=obj_name, used_item=used_item
        )
        effects = apply_interaction_effects(state, obj, obj_name, success)
        return result + effects

    # No item requirement - if player tried to use an item here, note it
    if used_item is not None:
        return get_wrong_item_response(obj_name, used_item)

    # No item requirement - normal interaction
    result = obj[ObjectKey.INTERACTION_RESULT]
    effects = apply_interaction_effects(state, obj, obj_name, True)
    return result + effects


USED_MESSAGES = {
    Used.BUTTON: "▶ The button has already been pressed.",
    Used.CARL: (
        "▶ Carl is happily chewing his bone and gives you a contented wag."
    ),
    Used.DRAWER: "▶ The drawer is empty.",
    Used.FIREPLACE: ("▶ You've already searched the fireplace."),
    Used.PLANT: (
        "▶ The magic plant has grown into a magnificent beanstalk. \n"
        "▶ It doesn't need any more water."
    ),
    Used.X_MARK: (
        "▶ You've already dug here. There's just a hole in the ground."
    ),
}


def get_used_message(obj_name):
    name = obj_name.lower()
    message = next(
        (msg for k, msg in USED_MESSAGES.items() if k in name),
        "▶ You've already used this.",
    )
    return message


def handle_item_requirements(state, obj, obj_name=None, used_item=None):
    required_item = obj[ObjectKey.REQUIRES_ITEM]

    # If the player specified an item, test that item specifically
    if used_item is not None:
        if used_item != required_item:
            return get_wrong_item_response(obj_name, used_item), False

        # Correct item - fall through to state check below
        item_to_check = used_item
    else:
        # Legacy auto-check: look for the required item in inventory
        if required_item not in state.inventory:
            return obj[ObjectKey.INTERACTION_RESULT], False
        item_to_check = required_item

    # Check if item needs to be in specific state
    if ObjectKey.REQUIRES_ITEM_STATE in obj:
        required_state = obj[ObjectKey.REQUIRES_ITEM_STATE]
        current_state = state.item_states.get(item_to_check, "default")

        if current_state != required_state:
            return (
                obj.get(
                    ObjectKey.FAILED_STATE_RESULT,
                    obj[ObjectKey.INTERACTION_RESULT],
                ),
                False,
            )

    # Item requirements met
    return (
        obj.get(ObjectKey.SUCCESS_RESULT, obj[ObjectKey.INTERACTION_RESULT]),
        True,
    )


def get_wrong_item_response(obj_name, used_item):
    obj_responses = WRONG_ITEM_RESPONSES.get(obj_name)
    if obj_responses:
        if isinstance(obj_responses, dict):
            return obj_responses.get(used_item, GENERIC_WRONG_ITEM_RESPONSE)
        return obj_responses
    return GENERIC_WRONG_ITEM_RESPONSE


def _mark_as_used(obj, obj_name, state):
    if (
        ObjectKey.GIVES_ITEM in obj
        or ObjectKey.ALSO_GIVES in obj
        or ObjectKey.BECOMES_ITEM in obj
        or ObjectKey.REVEALS in obj
        or obj.get(ObjectKey.CONSUMES_ITEM, False)
        or ObjectKey.ENABLES_EXIT in obj
    ):
        mark_used(state, state.current_position, obj_name)


def _apply_state_changes(state, obj):
    if ObjectKey.CHANGES_ITEM_STATE in obj:
        for item, new_state in obj[ObjectKey.CHANGES_ITEM_STATE].items():
            if item in state.inventory:
                state.item_states[item] = new_state


def _apply_item_removals(obj, obj_name, inventory, result_parts):
    if not obj.get(ObjectKey.CONSUMES_ITEM, False):
        return
    required_item = obj.get(ObjectKey.REQUIRES_ITEM)
    if required_item and required_item in inventory:
        inventory.remove(required_item)
        verb = obj.get(ObjectKey.CONSUME_MESSAGE, "used")
        suffix = obj.get(ObjectKey.CONSUME_SUFFIX, "")
        result_parts.append(
            f"\n▶ (You {verb} {display_name(required_item)}{suffix})"
        )


def _apply_item_grants(state, obj, obj_name, result_parts):
    if is_used(state, state.current_position, obj_name):
        return

    if ObjectKey.GIVES_ITEM in obj:
        state.inventory.append(obj[ObjectKey.GIVES_ITEM])
        result_parts.append(
            colorize(
                "\n▶ (You now have: "
                f"{display_name(obj[ObjectKey.GIVES_ITEM].value)})",
                Color.GREEN,
            )
        )

    if ObjectKey.ALSO_GIVES in obj:
        state.inventory.append(obj[ObjectKey.ALSO_GIVES])
        result_parts.append(
            colorize(
                "\n▶ (You also found: "
                f"{display_name(obj[ObjectKey.ALSO_GIVES].value)})",
                Color.GREEN,
            )
        )

    if ObjectKey.BECOMES_ITEM in obj:
        state.inventory.append(obj[ObjectKey.BECOMES_ITEM])
        result_parts.append(
            colorize(
                "\n▶ (You now have: "
                f"{display_name(obj[ObjectKey.BECOMES_ITEM].value)})",
                Color.GREEN,
            )
        )
        if obj_name == Object.LOOSE_PAINTING:
            state.safe_revealed = True


def apply_interaction_effects(state, obj, obj_name, success):
    if not success:
        return ""

    result_parts = []
    _apply_item_grants(state, obj, obj_name, result_parts)
    _apply_item_removals(obj, obj_name, state.inventory, result_parts)
    _apply_state_changes(state, obj)
    _mark_as_used(obj, obj_name, state)
    return "".join(result_parts)


def handle_take_command(state, item_name):
    area_items = AREAS[state.current_position].get(AreaKey.ITEMS, {})
    # Find the matching key (may be an Item enum)
    key_match = next((k for k in area_items if k == item_name), None)
    if key_match is not None:
        state.inventory.append(key_match)
        log(state, f"▶ You take the {display_name(key_match)}.")
        del area_items[key_match]
    else:
        logc(state, "▶ You can't take that.", Color.GREEN)


def get_item_description(state, item_name):
    if item_name in state.item_states:
        item_state = state.item_states[item_name]
        if isinstance(ITEM_DESCRIPTIONS[item_name], dict):
            return ITEM_DESCRIPTIONS[item_name][item_state]

    # Fallback to simple description or default
    item_desc = ITEM_DESCRIPTIONS.get(item_name)
    if isinstance(item_desc, dict):
        return item_desc.get("default", f"A {item_name}.")
    return item_desc or f"A {item_name}."


def get_object_description(state, obj):
    return resolve_description(
        state, obj, ObjectKey.DESCRIPTION_STATES, ObjectKey.DESCRIPTION
    )
