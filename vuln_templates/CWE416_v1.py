def specify_sources():
    return {"free": 1}


def specify_sinks():
    mem_sinks = {
        "memcpy": ["o", "n", "c"],
        "__memcpy_chk": ["o", "n", "c", "c"],
        "wmemcpy": ["o", "n", "c"],
        "__wmemcpy__chk": ["o", "n", "c", "c"],
        "mempcpy": ["o", "n", "c"],
        "__mempcpy_chk": ["o", "n", "c", "c"],
        "wmempcpy": ["o", "n", "c"],
        "__wmempcpy__chk": ["o", "n", "c", "c"],
        "memmove": ["o", "n", "c"],
        "__memmove_chk": ["o", "n", "c", "c"],
        "wmemmove": ["o", "n", "c"],
        "__wmemmove_chk": ["o", "n", "c", "c"],
        "memset": ["n", "c", "c"],
        "__memset_chk": ["n", "c", "c", "c"],
        "wmemset": ["n", "c", "c"],
        "__wmemset_chk": ["n", "c", "c", "c"],
        "memchr": ["n", "c", "c"],
        "__memchr_chk": ["n", "c", "c", "c"],
    }
    str_sinks = {
        "strlen": ["n"],
        "strnlen": ["n", "c"],
        "wcslen": ["n"],
        "strdup": ["n"],
        "wcsdup": ["n"],
        "strndup": ["n", "c"],
        "strchr": ["n", "c"],
        "strrchr": ["n", "c"],
        "strtol": ["n", "i", "c"],
        "strtoul": ["n", "i", "c"],
        "strstr": ["i", "n"],
        "strtok": ["n", "i"],
        "strtok_r": ["i", "i", "n"],
        "strpbrk": ["i", "n"],
        "strcmp": ["i", "n"],
        "strcat": ["o", "n"],
        "__strcat_chk": ["o", "n", "c"],
        "strncat": ["o", "n", "c"],
        "__strncat_chk": ["o", "n", "c", "c"],
        "strcpy": ["o", "n"],
        "__strcpy_chk": ["o", "n", "c"],
        "strncpy": ["o", "n", "c"],
        "__strncpy_chk": ["o", "n", "c"],
    }
    format_sinks = {
        "printf": ["n"],
        "wprintf": ["n"],
        "fprintf": ["p", "n"],
        "__fprintf_chk": ["p", "c", "n"],
        "fwprintf": ["c", "n"],
        "__fwprintf_chk": ["p", "c", "n"],
        "dprintf": ["c", "n"],
        "__dprintf_chk": ["c", "c", "n"],
        "sprintf": ["o", "n"],
        "__sprintf_chk": ["o", "c", "c", "n"],
        "swprintf": ["o", "c", "n"],
        "__swprintf_chk": ["o", "c", "c", "c", "n"],
        "snprintf": ["o", "c", "n"],
        "__snprintf_chk": ["o", "c", "c", "c", "n"],
        "asprintf": ["o", "n"],
        "__asprintf_chk": ["o", "c", "n"],
        "vasprintf": ["o", "n"],
        "__vasprintf_chk": ["o", "c", "n"],
        "vaswprintf": ["o", "n"],
        "__vaswprintf_chk": ["o", "c", "n"],
        "syslog": ["c", "n"],
    }
    other_sinks = {
        "realloc": ["n", "c"],
        "atoi": ["n"],
        "atol": ["n"],
    }
    return mem_sinks | str_sinks | format_sinks | other_sinks


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
