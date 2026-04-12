def apply_constraint(state, sink, sources, **kwargs):
    addr = state.solver.eval(sink, cast_to=int)
    if state.project.loader.find_section_containing(addr) is not None:
        # Force an unsat error
        state.solver.add(False)
    return


def specify_sinks():
    maps = {
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

    return maps


def specify_sources():
    return {}
