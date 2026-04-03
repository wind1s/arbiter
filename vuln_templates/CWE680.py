def apply_constraint(state, sink, sources, **kwargs):
    if not sources:
        state.solver.add(False)
        return

    for x in sources:
        if x.length > sink.length:
            continue
        if x.length < sink.length:
            x = x.zero_extend(sink.length - x.length)

        # Update amount of bits to bound by according to lenght of x.
        # Clamp to range of 8..32 bits
        bit_bound = min(max(x.length, 8), 32)
        # Prevents Unrealistic Data Requirements from the paper.
        number_bound = (1 << bit_bound) - 1

        constraints = [sink > x, x < number_bound]

        # Test if it is possible to increment within bounds.
        if state.solver.satisfiable(extra_constraints=constraints):
            # Swap 'sink > x' for 'sink < x' to check for overflow.
            # If sink and be larger and smaller than source then we have a positive.
            constraints[0] = sink < x

            if state.solver.satisfiable(extra_constraints=constraints):
                # Bug confirmed! Commit the safe constraints to the main state.
                for c in constraints:
                    state.solver.add(c)
                return

        # Safely shrinks or can't overflow.
        # Kill the state explicitly so the solver drops it.
        state.solver.add(False)
        return


def specify_sinks():
    return {
        "malloc": ["n"],
        "calloc": ["n"],
        "realloc": ["p", "n"],
        "operator new": ["n"],
    }


def specify_sources():
    return {"atoi": 0, "rand": 0, "fscanf": 3}
