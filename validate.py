"""
Static data-integrity checks for AREAS.

This walks the world data and cross-checks every reference (exits, reveals,
item grants/requirements, description-state keys, etc.) against what actually
exists, so a typo shows up as a startup warning instead of a runtime KeyError
three rooms later.

Usage:
    python validate.py  # Run standalone, prints report, exits 1 on error
    from validate import validate_world_data
    errors = validate_world_data() # Call it yourself, get a list of strings 
"""

from data import (
    AREAS,
    GENERIC_WRONG_ITEM_RESPONSE,
    ITEM_DESCRIPTIONS,
    WRONG_ITEM_RESPONSES,
)
from enums import Area, AreaKey, Item, Object, ObjectKey, Path


def _val(x):
    return x.value if hasattr(x, "value") else x


def validate_world_data():
    """Returns a list of human-readable error strings. Empty list = clean."""
    errors = []

    def err(area, msg):
        errors.append(f"[{_val(area)}] {msg}")

    # --- 1. Every Area enum member must have a populated entry -----------
    for area in Area:
        if area not in AREAS:
            errors.append(f"Area.{area.name} has no entry in AREAS.")

    for area, area_data in AREAS.items():
        if not isinstance(area, Area):
            errors.append(f"AREAS has a non-Area key: {area!r}")
            continue

        # -- 2. Every area needs the keys the rest of the code assumes ---
        if AreaKey.DESCRIPTION not in area_data:
            err(area, "Missing required AreaKey.DESCRIPTION.")
        for required_key in (AreaKey.EXITS, AreaKey.ITEMS,
                             ObjectKey.INTERACTABLES):
            if required_key not in area_data:
                err(area, f"Missing required key {required_key!r}.")

        exits = area_data.get(AreaKey.EXITS, {})
        interactables = area_data.get(ObjectKey.INTERACTABLES, {})
        area_items = area_data.get(AreaKey.ITEMS, {})

        # --- 3. Exit destinations must be real, populated areas -----------
        for direction, destination in exits.items():
            if not isinstance(direction, Path):
                err(area, f"Exit key {direction!r} is not a Path.")
            if destination not in AREAS:
                err(area, f"Exit {_val(direction)} -> "
                    f"{destination!r} is not a populated Area.")

        # --- 4. Area-level DESCRIPTION_STATES keys must exist -------------
        for cond, key in area_data.get(AreaKey.DESCRIPTION_STATES, []):
            if key not in area_data:
                err(area, f"DESCRIPTION_STATES references missing key "
                          f"{key!r}.")

        # --- 5. EXIT_REQUIREMENTS must line up with real exits/items ------
        exit_reqs = area_data.get(AreaKey.EXIT_REQUIREMENTS, {})
        for direction, requirement in exit_reqs.items():
            if direction not in exits:
                err(area, f"EXIT_REQUIREMENTS has direction"
                          f"{_val(direction)} with no matching exit.")
            if AreaKey.ITEM in requirement:
                if not isinstance(requirement[AreaKey.ITEM], Item):
                    err(area, f"EXIT_REQUIREMENTS[{_val(direction)}] "
                              f"ITEM {requirement[AreaKey.ITEM]!r} "
                              "is not a valid Item.")
            if ObjectKey.CONDITION in requirement:
                if not isinstance(requirement[ObjectKey.CONDITION], Object):
                    err(area, f"EXIT_REQUIREMENTS[{_val(direction)}] "
                              f"CONDITION {requirement[ObjectKey.CONDITION]!r}"
                              " is not a valid Object.")

        # --- 6. Interactables: cross-references within the same area -----
        for obj_name, obj in interactables.items():
            where = f"Interactable {_val(obj_name)!r}"

            if ObjectKey.REVEALS in obj:
                target = obj[ObjectKey.REVEALS]
                if target not in interactables:
                    err(area, f"{where} REVEALS {_val(target)!r}, which "
                              "is not an interactable in this area.")

            if ObjectKey.ENABLES_EXIT in obj:
                target = obj[ObjectKey.ENABLES_EXIT]
                if not isinstance(target, Path):
                    err(area, f"{where} ENABLES_EXIT {target!r} is not "
                              "a valid Path.")
                elif target not in exits:
                    err(area, f"{where} ENABLES_EXIT {_val(target)!r}, "
                        "but there is no such exit in this area.")

            if ObjectKey.REQUIRES_OBJECT_USED in obj:
                target = obj[ObjectKey.REQUIRES_OBJECT_USED]
                if target not in interactables:
                    err(area, f"{where} REQUIRES_OBJECT_USED "
                              f"{_val(target)!r}, which is not an "
                              "interactable in this area.")

            for key in (ObjectKey.GIVES_ITEM, ObjectKey.ALSO_GIVES,
                        ObjectKey.BECOMES_ITEM, ObjectKey.REQUIRES_ITEM,
                        ObjectKey.HIDDEN_DESCRIPTION_ITEM):
                if key in obj and not isinstance(obj[key], Item):
                    err(area, f"{where} {key.name} {obj[key]!r} is not "
                              "a valid Item.")

            if ObjectKey.CHANGES_ITEM_STATE in obj:
                for item in obj[ObjectKey.CHANGES_ITEM_STATE]:
                    if not isinstance(item, Item):
                        err(area, f"{where} CHANGES_ITEM_STATE key "
                                  f"{item!r} is not a valid Item.")

            if (
                ObjectKey.REQUIRES_ITEM_STATE in obj 
                and ObjectKey.REQUIRES_ITEM not in obj
            ):
                err(area, f"{where} has REQUIRES_ITEM_STATE but no "
                          "REQUIRES_ITEM to check the state of.")

            # DESCRIPTION_STATES keys must exist as sibling keys on obj
            for cond, key in obj.get(ObjectKey.DESCRIPTION_STATES, []):
                if key not in obj:
                    err(area, f"{where} DESCRIPTION_STATES references "
                              f"missing key {key!r}.")

            if ObjectKey.DESCRIPTION not in obj:
                err(area, f"{where} missing required DESCRIPTION.")

        # --- 7. Area item keys must be real Items -------------------------
        for item in area_items:
            if not isinstance(item, Item):
                err(area, f"ITEMS key {item!r} is not a valid Item.")

    # --- 8. Global lookup tables keyed by Item/Object --------------
    for item in ITEM_DESCRIPTIONS:
        if not isinstance(item, Item):
            errors.append(f"ITEM_DESCRIPTIONS has non-Item key {item!r}.")

    for obj_name, response in WRONG_ITEM_RESPONSES.items():
        if not isinstance(obj_name, Object):
            errors.append(
                f"WRONG_ITEM_RESPONSES has non-Object key {obj_name!r}."
            )
        if isinstance(response, dict):
            for item in response:
                if not isinstance(item, Item):
                    errors.append(
                        f"WRONG_ITEM_RESPONSES[{_val(obj_name)}] has "
                        f"non-Item key {item!r}."
                    )

    if not isinstance(GENERIC_WRONG_ITEM_RESPONSE, str):
        errors.append("GENERIC_WRONG_ITEM_RESPONSE is not a string.")
    return errors


def run_self_check(verbose=True):
    errors = validate_world_data()
    if not errors:
        if verbose:
            print(f"[DATA CHECK] OK - no issues found.")
        return True

    print(f"[DATA CHECK] {len(errors)} issue(s) found:")
    for e in errors:
        print(f"  - {e}")
    return False


def log_self_check(state):
    from logger import debug_log

    errors = validate_world_data()
    if not errors:
        debug_log(state, "▶ [DEBUG -> DATA CHECK]: OK, no issues found.")
        return True

    debug_log(state, f"▶ [DEBUG -> DATA CHECK]: {len(errors)} issue(s) found:")
    for e in errors:
        debug_log(state, f"▶ [DEBUG]  - {e}")
    return False


if __name__ == "__main__":
    import sys
    sys.exit(0 if run_self_check() else 1)
