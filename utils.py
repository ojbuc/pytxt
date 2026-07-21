import time

from enums import Color


def _get_val(x):
    return x.value if hasattr(x, "value") else x


def display_name(x):
    name = x.value if hasattr(x, "value") else x
    return name.title()


def printc(text, color):
    print(colorize(text, color))


def colorize(text, color):
    """
    Wrap each line of text in the given Color, resetting at the end of every
    line, Coloring line-by-line keeps things correct even if the text contains
    embedded '\n's, since log() and the display loop both operate on individual
    lines.
    """
    return "\n".join(
        f"{color.value}{line}{Color.RESET.value}" for line in text.split("\n")
    )


def substitute_player_name(text, state):
    """
    Replace the literal '{name}' placeholder in any flavor/description text
    with the player's chosen name. Uses a plain string replace (not str.format)
    so any other stray '{' or '}' in flavor text is left alone rather than
    raising a KeyError.
    """
    return text.replace("{name}", state.player_name or "you")


def print_narration(text, state, color=None):
    """
    Print multi-line narration immediately, mid-command, before and input()
    prompt (a confirmation or a scripted event). This is deliberately NOT
    routed through log(): log() only becomes visible on the next screen redraw,
    this text needs to be visible *before* the player is asked to respond to
    something.
    """
    text = substitute_player_name(text, state)
    if color:
        text = colorize(text, color)
    for line in text.split("\n"):
        print(f"  {line}")


def resolve_description(state, data, states_key, default_key):
    for condition, key in data.get(states_key, []):
        if condition(state):
            return data[key]
    return data[default_key]


def resolve_name(partial, candidates):
    str_candidates = [_get_val(c) for c in candidates]
    key_map = {_get_val(c): c for c in candidates}
    partial = partial.strip().lower()

    if not partial:
        return None, None

    # Tier 0: exact full-string match
    if partial in str_candidates:
        return key_map[partial], None

    def _match(matches):
        if len(matches) == 1:
            return key_map[matches[0]], None
        if len(matches) > 1:
            titled_match = ", ".join(display_name(m) for m in matches)
            return None, f"▶ Did you mean: {titled_match}?"
        return None  # No matches at this tier, try the next one

    # Tier 1: partial matches one whole word in the candidate
    word_matches = [s for s in str_candidates if partial in s.split()]
    result = _match(word_matches)
    if result:
        return result

    # Tier 2: partial is a prefix of the candidate, or of one of its words
    prefix_matches = [
        s
        for s in str_candidates
        if s.startswith(partial)
        or any(w.startswith(partial) for w in s.split())
    ]
    result = _match(prefix_matches)
    if result:
        return result

    # No match found
    return None, None


def flash_quit_message(text, delay=0.06):
    frame_colors = [c for c in Color if c is not Color.RESET]
    spinner_frames = "|/-\\"
    print("\n\n\033[?25l", end="", flush=True)
    try:
        for i, color in enumerate(frame_colors):
            spinner = spinner_frames[i % len(spinner_frames)]
            print(
                f"\r{color.value}{spinner}{text} {spinner}{Color.RESET.value}",
                end="",
                flush=True,
            )
            time.sleep(delay)
    finally:
        print("\033[?25h", end="", flush=True)
    print()
