def specify_sources():
    # Source: The argument to the first free call.
    # Index 1 corresponds to the first argument in Arbiter's convention (0 is return val).
    return {"free": 1}


def specify_sinks():
    # Sink: The argument to the second free call.
    # 'n' maps to the first argument (similar to malloc in utils.py)
    return {"free": ["n"]}


def apply_constraint(state, sink, sources, **kwargs):
    """
    Constraint: Is the pointer at the second free EQUAL to the first?
    """
    # sources contains the list of pointers tracked from the source (first free)
    # sink is the pointer being freed at the sink (second free)

    match_found = False
    for freed_ptr in sources:
        # Check if they can be the same address
        # We must verify satisfiability before enforcing it
        s_check = state.copy()
        s_check.solver.add(sink == freed_ptr)

        if s_check.satisfiable():
            # Enforce the double free condition
            state.solver.add(sink == freed_ptr)
            match_found = True
            break

    if not match_found:
        state.solver.add(False)
