


def resolve_name(partial, candidates):
    """ Resolve a partial name to a full name from a list of candidates. """
    # Exact match first
    if partial in candidates:
        return partial, None
    # Substring matches
    matches = [c for c in candidates if partial in c]

    if len(matches) == 1:
        return matches[0], None
    if len(matches) > 1:
        return None, f"▶ Did you mean: {', '.join(matches)}?"
    # No match found
    return None, None
