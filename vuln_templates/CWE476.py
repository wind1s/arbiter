def specify_sources():
    # Source: Return value (index 0) of allocation functions
    return {"malloc": 0, "calloc": 0, "realloc": 0}


def specify_sinks():
    # Sinks: Functions that crash on NULL arguments
    # 'o' = dest (arg 1), 'i' = source (arg 2), 'fmt' = format string
    return {
        "memset": ["o"],
        "memcpy": ["o", "i"],  # Check both dest and src
        "strcpy": ["o", "i"],
        "strlen": ["i"],  # Extended: often crashes on NULL
        "fprintf": ["fmt"],  # Extended: NULL format string crash
    }


def apply_constraint(state, sink, sources, **kwargs):
    """
    Constraint: Can the pointer be NULL at the sink, originating from a NULL allocation?
    """
    # sources is the list of return values from the source (malloc)
    # sink is the argument used at the sink

    if not sources:
        state.solver.add(False)
        return

    # 1. Force the SOURCE (malloc return) to be NULL.
    # Arbiter's under-constrained execution allows this.
    source_ptr = sources[0]

    s_check = state.copy()
    s_check.solver.add(source_ptr == 0)

    if not s_check.satisfiable():
        # If malloc CANNOT return NULL (e.g. constraints added by specific allocator models),
        # then this specific bug path is impossible.
        state.solver.add(False)
        return

    # 2. Force the SINK (usage) to be NULL.
    # If the program had a check `if (!ptr) return;`, this path would be unsat
    # because the path predicate would contain `ptr != 0`.
    state.solver.add(sink == 0)

    # 3. Link Source and Sink
    # We implicitly trust Arbiter's DDA to link them, but explicitly:
    # ensuring the sink sinkession derives from the source being 0.
    state.solver.add(source_ptr == 0)
