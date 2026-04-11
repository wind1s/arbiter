def specify_sources():
    return {"free": 1}


def specify_sinks():
    return {
        "memcpy": ["o", "n", "c"],
        "memset": ["n", "c", "c"],
        "memmove": ["n", "p", "c"],
        "realloc": ["n", "c"],
        # string functions
        "strcpy": ["n", "i"],
        "strlen": ["n"],
        "strdup": ["n"],
        "strncpy": ["o", "n", "c"],
        # print functions
        "printf": ["fmt", "n"],
        "__printf_chk": ["fmt", "n"],
        "fprintf": ["p", "fmt", "n"],
        "__fprintf_chk": ["c", "c", "n"],
        "sprintf": ["n", "fmt"],
        "__sprintf_chk": ["c", "c", "c", "n"],
        "snprintf": ["n", "c", "fmt"],
        "__snprintf_chk": ["c", "c", "c", "c", "n"],
        "wprintf": ["fmt", "n"],
        "vasprintf": ["n", "fmt"],
        "__dprintf_chk": ["c", "c", "n"],
        "__vasprintf_chk": ["c", "c", "n"],
        "__asprintf_chk": ["c", "c", "n"],
    }


def apply_constraint(state, sink, sources, **kwargs):
    # sources contains the list of pointers tracked from the source (first free)
    # sink is the pointer being freed at the sink (second free)
    if not sources:
        state.solver.add(False)
        return

    match_found = False
    for freed_ptr in sources:
        # Check if they can be the same address
        # We must verify satisfiability before enforcing it
        constraint = sink == freed_ptr

        if state.solver.satisfiable(extra_constraints=[constraint]):
            # Enforce the double free condition
            state.solver.add(constraint)
            match_found = True
            break

    if not match_found:
        state.solver.add(False)
