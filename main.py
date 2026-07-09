from commands import process_command
from display import display_area_information
from enums import Area, Status
from state import GameState
from world import update_dynamic_visibility


def main():
    try:
        state = GameState()

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
