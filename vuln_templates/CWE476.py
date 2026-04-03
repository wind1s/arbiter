def specify_sources():
    return {}


def specify_sinks():
    return {
        "printf": ["fmt", "n"],
        "wprintf": ["fmt", "n"],
        "memset": ["n", "c", "c"],
        "strcpy": ["n", "i"],
        "strlen": ["n"],
        "fprintf": ["n", "fmt"],
        "memcpy": ["o", "n", "c"],
        "strncpy": ["o", "n", "c"],
    }


def apply_constraint(state, sink, sources, **kwargs):
    """
    Constraint: Did the developer forget to check if the allocation
    returned NULL before passing the pointer into the sink?
    """
    if not sources:
        state.solver.add(False)
        return

    source_ptr = sources[0]

    # Hypothesis: Can the allocation pointer be NULL at this exact moment?
    # If the developer wrote `if (!ptr) exit(1);`, angr would have already
    # permanently added `source_ptr != 0` to the state. Therefore, testing
    # `source_ptr == 0` here would correctly return UNSAT.
    null_condition = source_ptr == 0

    # 2. Sandbox the check using extra_constraints (Must be a list!)
    if state.solver.satisfiable(extra_constraints=[null_condition]):
        # Bug confirmed! The execution path allows a NULL pointer to reach the sink.

        # Permanently commit the constraints to trigger the ARBITER alarm
        state.solver.add(null_condition)

        # We also enforce that the sink equals 0 to ensure the generated
        # concrete exploit (ArbiterReport) accurately reflects the crash state.
        state.solver.add(sink == 0)
    else:
        # The pointer was safely checked and cannot be NULL here. Safe path.
        state.solver.add(False)
