def specify_sources():
    return {"free": 1}


def specify_sinks():
    mem_sinks = {
        "memcpy": ["n", "i", "c"],
        "__memcpy_chk": ["n", "i", "c", "c"],
        "wmemcpy": ["n", "i", "c"],
        "__wmemcpy__chk": ["n", "i", "c", "c"],
        "mempcpy": ["n", "i", "c"],
        "__mempcpy_chk": ["n", "i", "c", "c"],
        "wmempcpy": ["n", "i", "c"],
        "__wmempcpy__chk": ["n", "i", "c", "c"],
        "memmove": ["o", "n", "c"],
        "__memmove_chk": ["o", "n", "c", "c"],
        "wmemmove": ["o", "n", "c"],
        "__wmemmove_chk": ["o", "n", "c", "c"],
    }
    str_sinks = {
        "strstr": ["n", "i"],
        "strtok_r": ["n", "i", "i"],
        "strpbrk": ["n", "i"],
        "strcmp": ["n", "i"],
        "strcat": ["n", "i"],
        "__strcat_chk": ["n", "i", "c"],
        "strncat": ["n", "i", "c"],
        "__strncat_chk": ["n", "i", "c", "c"],
        "strcpy": ["n", "i"],
        "__strcpy_chk": ["n", "i", "c"],
        "strncpy": ["n", "i", "c"],
        "__strncpy_chk": ["n", "i", "c"],
    }
    format_sinks = {
        "sprintf": ["n", "fmt"],
        "__sprintf_chk": ["n", "c", "c", "fmt"],
        "swprintf": ["n", "c", "fmt"],
        "__swprintf_chk": ["n", "c", "c", "c", "fmt"],
        "snprintf": ["n", "c", "fmt"],
        "__snprintf_chk": ["n", "c", "c", "c", "fmt"],
        "asprintf": ["n", "fmt"],
        "__asprintf_chk": ["n", "c", "fmt"],
        "vasprintf": ["n", "fmt"],
        "__vasprintf_chk": ["n", "c", "fmt"],
        "vaswprintf": ["n", "fmt"],
        "__vaswprintf_chk": ["n", "c", "fmt"],
    }
    return mem_sinks | str_sinks | format_sinks


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
