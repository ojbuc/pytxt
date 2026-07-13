import argparse
import sys

from commands import process_command
from display import display_area_information
from enums import Area, Status
from logger import log
from state import GameState
from world import update_dynamic_visibility


def _parse_args():
    parser = argparse.ArgumentParser(description="Text adventure game.")
    parser.add_argument(
            "--debug",
            metavar="AREA",
            help=(
                "Start in a specific area with debug mode enabled, for testing."
                f" Choices: {', '.join(a.value for a in Area)}"
            ),
    )
    return parser.parse_args()


def _get_debug_state(raw_area):
    if not raw_area:
        return None

    normalized = raw_area.strip().lower()
    area = next((a for a in Area if a.value == normalized), None)

    if area is None:
        valid = ", ".join(a.value for a in Area)
        print(f"▶ [DEBUG] Unknown area '{raw_area}'. Valid options: {valid}\n")
        sys.exit(1)

    state = GameState.debug_state(area)
    log(
            state,
            f"▶ [DEBUG] Starting in '{area.value}' with debug mode enabled.\n"
    )
    return state


def main():
    try:
        args = _parse_args()
        state = _get_debug_state(args.debug) or GameState()

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
