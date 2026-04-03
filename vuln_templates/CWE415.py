def specify_sources():
    return {"free": 1}


def specify_sinks():
    return {"free": ["n"]}


def apply_constraint(state, sink, sources, **kwargs):
    """
    Constraint: Is the pointer at the second free EQUAL to the first?
    """
    if not sources:
        state.solver.add(False)
        return

    # sources contains the list of pointers tracked from the source (first free)
    # sink is the pointer being freed at the sink (second free)
    match_found = False

    for freed_ptr in sources:
        # Check if they can be the same address
        # We must verify satisfiability before enforcing it
        constraint = sink == freed_ptr

        if state.solver.satisfiable(extra_constraints=constraint):
            # Enforce the double free condition
            state.solver.add(constraint)
            match_found = True
            break

    if not match_found:
        state.solver.add(False)
