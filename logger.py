LOG_MAX = 10


def log(state, message):
    for line in message.split("\n"):
        if line.strip():
            state.action_log.append(line)
            state.full_history.append(line)
            state.new_log_lines += 1
    while len(state.action_log) > LOG_MAX:
        state.action_log.pop(0)
