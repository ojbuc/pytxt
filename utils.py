def _get_val(x):
    return x.value if hasattr(x, "value") else x


def resolve_name(partial, candidates):
    str_candidates = [_get_val(c) for c in candidates]
    key_map = {_get_val(c): c for c in candidates}

    # Exact match first
    if partial in str_candidates:
        return key_map[partial], None

    # Substring matches
    matches = [s for s in str_candidates if partial in s]
    if len(matches) == 1:
        return key_map[matches[0]], None
    if len(matches) > 1:
        return None, f"▶ Did you mean: {', '.join(matches)}?"
    # No match found
    return None, None
