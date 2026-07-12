import argparse

from commands import process_command
from display import display_area_information
from enums import Area, Status
from logger import log
from state import GameState
from world import update_dynamic_visibility


def _parse_args():
    parser = argparse.ArgumentParser(description="Text adventure game.")
    parser.add_argument(
            "--start",
            metavar="AREA",
            help=(
                "Start in a specific area with full inventory, for testing. "
                f"Choices: {', '.join(a.value for a in Area)}"
            ),
    )
    return parser.parse_args()


def _get_debug_state(raw_area):
    if not raw_area:
        return None

    normalized = raw_area.strip().lower()
    area = next((a for a in Area if a.value == normalized), None)
    state = GameState.debug_state(area)

    if area is None:
        valid = ", ".join(a.value for a in Area)
        log(
                state, 
                f"▶ [DEBUG] Unknown area '{raw_area}'. "
                f"Valid options: {valid}\n"
        )
        return None

    log(state, f"▶ [DEBUG] Starting in '{area.value}' with full inventory.\n")
    return state


def main():
    try:
        args = _parse_args()
        state = _get_debug_state(args.start) or GameState()

        while True:
            update_dynamic_visibility(state)
            display_area_information(state)

            command = input("▶ ").strip().lower()
            if not command:
                continue

            next_state = process_command(state, command)

            if next_state == Status.QUIT:
                break
            if next_state == Status.CONTINUE:
                continue

            assert isinstance(next_state, Area)
            state.current_position = next_state
            print()

    except KeyboardInterrupt:
        print("\n▶ The adventure ends abruptly!\n")


if __name__ == "__main__":
    main()
