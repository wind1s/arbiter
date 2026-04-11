def apply_constraint(state, sink, sources, **kwargs):
    for x in sources:
        if x.length > sink.length:
            continue
        if x.length < sink.length:
            x = x.zero_extend(sink.length - x.length)

        # Update amount of bits to bound by according to lenght of x.
        # Clamp to range of 8..32 bits
        bit_bound = min(max(x.length, 8), 32)
        number_bound = (1 << bit_bound) - 1

        constraints = [sink > x, x < number_bound]

        # Use extra_constraints to test feasibility WITHOUT copying the state.
        # Prevents Unrealistic Data Requirements from the paper.
        can_grow = state.solver.satisfiable(extra_constraints=constraints)

        if can_grow:
            # Swap 'sink > x' for 'sink < x' to check for overflow
            constraints[0] = sink < x
            can_overflow = state.solver.satisfiable(extra_constraints=constraints)

            if can_overflow:
                # Bug confirmed! Commit the safe constraints to the main state.
                for c in constraints:
                    state.solver.add(c)
                return

        # Safely shrinks or can't overflow.
        # Kill the state explicitly so the solver drops it.
        state.solver.add(False)
        return


def specify_sinks():
    maps = {"malloc": ["n"], "calloc": ["n"], "realloc": ["c", "n"]}

    return maps


def specify_sources():
    return {}
