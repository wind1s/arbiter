def apply_constraint(state, sink, sources, **kwargs):
    if not sources:
        state.solver.add(False)
        return

    match_found = False
    for freed_ptr in sources:
        constraint = sink == freed_ptr

        if state.solver.satisfiable(extra_constraints=constraint):
            state.solver.add(constraint)
            match_found = True
            break

    if not match_found:
        state.solver.add(False)


def specify_sinks():
    return {"srand": ["n"]}


def specify_sources():
    return {"time": 0}
