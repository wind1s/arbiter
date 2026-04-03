def specify_sources():
    """Track network input, standard input, and environment variables."""
    return {"recv": 2, "read": 2, "fgets": 1, "getenv": 0}


def specify_sinks():
    """
    Track strings passed to command execution APIs.
    'n' represents the 1st argument (the command or executable path).
    """
    return {"system": ["n"], "popen": ["n", "p"], "execlp": ["p", "p", "c", "n"], "execl": ["p", "p", "c", "n"]}


def apply_constraint(state, sink, sources, **kwargs):
    pass
