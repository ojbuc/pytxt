import argparse
import sys

from commands import process_command
from display import display_area_information
from enums import Area, Color, Status
from events import AREA_ENTRY_EVENTS
from logger import debug_log
from state import GameState
from utils import colorize, flash_quit_message, printc
from world import update_dynamic_visibility


def _parse_args():
    parser = argparse.ArgumentParser(description="Text Adventure game.")
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
        valid = "\n".join(f"  - {a.value}" for a in Area)
        printc(
            f" [DEBUG] Unknown area '{raw_area}'. "
            f"Valid options:\n{valid}\n",
            Color.BRIGHT_GREEN,
        )
        sys.exit(1)

    state = GameState.debug_state(area)
    debug_log(
        state, f"▶ [DEBUG] Starting in '{area.value}' with debug mode enabled."
    )
    return state


def main():
    state = None
    try:
        args = _parse_args()
        state = _get_debug_state(args.debug) or GameState()

        while True:
            update_dynamic_visibility(state)
            display_area_information(state)

            command = input(colorize("▶ ", Color.GREEN)).strip().lower()
            if not command:
                continue

            next_state = process_command(state, command)

            if next_state == Status.QUIT:
                break
            if next_state == Status.CONTINUE:
                continue

            assert isinstance(next_state, Area)
            state.current_position = next_state

            entry_event = AREA_ENTRY_EVENTS.get(state.current_position)
            if entry_event:
                state.current_position = entry_event(state)
            print()

    except BrokenPipeError:
        pass
    except EOFError:
        flash_quit_message(" End of file (and adventure)!")
    except KeyboardInterrupt:
        flash_quit_message(" The adventure has been interrupted!")
    except Exception as e:
        if state is not None and state.debug_mode:
            raise
        flash_quit_message(
            " Whoops! Something went awfully wrong... ABORTING."
        )
        printc(f" ({type(e).__name__}: {e})", Color.BRIGHT_RED)


if __name__ == "__main__":
    main()
