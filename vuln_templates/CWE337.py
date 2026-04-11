def apply_constraint(state, sink, sources, **kwargs):
    if not sources:
        state.solver.add(False)
        return

    match_found = False
    for rand_val in sources:
        constraint = sink == rand_val

        if state.solver.satisfiable(extra_constraints=constraint):
            state.solver.add(constraint)
            match_found = True
            break

    if not match_found:
        state.solver.add(False)


def specify_sinks():
    maps = {"srand": ["n"]}
    return maps


def specify_sources():
    checkpoints = {"time": 0}
    return checkpoints
