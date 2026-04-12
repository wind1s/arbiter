def specify_sources():
    """Track network input, standard input, and environment variables."""
    return {
        "recv": 2,
        "__recv_chk": 2,
        "recvfrom": 2,
        "__recvfrom_chk": 2,
        "read": 2,
        "__read_chk": 2,
        "fread": 1,
        "gets": 0,
        "fgets": 1,
        "getenv": 0,
        "secure_getenv": 0,
        "__fgets_chk": 1,
        "__fgets_u_chk": 1,
        "fwgets": 1,
        "__fwgets_chk": 1,
        "__fwgets_u_chk": 1,
    }


def specify_sinks():
    """
    Track strings passed to command execution APIs.
    'n' represents the 1st argument (the command or executable path).
    """
    return {"system": ["n"], "popen": ["n", "p"], "execlp": ["p", "p", "c", "n"], "execl": ["p", "p", "c", "n"]}


def apply_constraint(state, sink, sources, **kwargs):
    return
