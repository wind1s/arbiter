def apply_constraint(state, sink, sources, **kwargs):
    addr = state.solver.eval(sink, cast_to=int)
    if state.project.loader.find_section_containing(addr) is not None:
        # Force an unsat error
        state.solver.add(False)
    return


def specify_sinks():
    maps = {
        "printf": ["n"],
        "fprintf": ["c", "n"],
        "dprintf": ["c", "n"],
        "sprintf": ["c", "n"],
        "vasprintf": ["c", "n"],
        "snprintf": ["c", "c", "n"],
        "fprintf_chk": ["c", "c", "n"],
        "dprintf_chk": ["c", "c", "n"],
        "sprintf_chk": ["c", "c", "c", "n"],
        "vasprintf_chk": ["c", "c", "n"],
        "asprintf_chk": ["c", "c", "n"],
        "snprintf_chk": ["c", "c", "c", "c", "n"],
    }

    return maps


def specify_sources():
    return {}
