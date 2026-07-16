import shutil

from enums import Color
from utils import colorize, substitute_player_name

LOG_MAX = max(10, shutil.get_terminal_size().lines - 15)


def log(state, message):
    message = substitute_player_name(message, state)
    for line in message.split("\n"):
        if line.strip():
            state.action_log.append(line)
            state.full_history.append(line)
            state.new_log_lines += 1
    while len(state.action_log) > LOG_MAX:
        state.action_log.pop(0)


def logc(state, text, color):
    log(state, colorize(text, color))


def debug_log(state, text):
    logc(state, text, Color.BRIGHT_GREEN)
