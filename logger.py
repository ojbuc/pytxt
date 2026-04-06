LOG_MAX = 8


def log(state, message):
    """Add a message to the action log, keeping only the last LOG_MAX lines."""
    for line in message.split("\n"):
        if line.strip():
            state.action_log.append(line)
            state.new_log_lines += 1
    while len(state.action_log) > LOG_MAX:
        state.action_log.pop(0)
