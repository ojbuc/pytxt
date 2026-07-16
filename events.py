from data import AREAS
from enums import Area, AreaKey, Color
from logger import log
from utils import colorize, print_narration


def _fall_through_void(state):
    print_narration(
        AREAS[Area.THE_VOID][AreaKey.DESCRIPTION],
        state,
        color=Color.BRIGHT_CYAN,
    )

    name = input(
        colorize(
            "  A voice, ancient and vast, asks for your name: ",
            Color.BRIGHT_CYAN,
        )
    ).strip()
    while not name:
        name = input(
            colorize(
                "  ...it asks again, more insistently: ", Color.BRIGHT_CYAN
            )
        ).strip()

    state.player_name = name
    log(state, f'▶ "{name}"... the entity repeats, tasting the word.')
    log(
        state,
        f"▶ {name} lands suddenly somewhere they've been before, but "
        "this time it's different, something isn't right.",
    )
    return Area.DEAD_ROOM


AREA_ENTRY_EVENTS = {
    Area.THE_VOID: _fall_through_void,
}
