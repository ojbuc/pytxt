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
