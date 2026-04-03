def specify_sources():
    # Source argument that is tracked: index 0 is return value, index 1,2,3 etc is arguments.
    return {"malloc": 0, "realloc": 1}


def specify_sinks():
    # Use these chars to describe the sinks parameters.
    # ARgument to track: n (only supply on per sink)
    # Pointer argument: p
    # Input buffer argument: i
    # Output buffer argument: o
    # Format string: fmt
    # Constant/int argument: c (can be used to pad arguments to correct position)
    # "ret" ["r"]: track return value of source.
    return {
        # Track the 1st argument (size)
        "malloc": ["n"],
        # Track the 2nd argument (size). 'p' pads the 1st arg.
        "realloc": ["p", "n"],
        # Track the 3rd argument (size). 'o' and 'i' pad the 1st/2nd args.
        "memcpy": ["o", "i", "n"],
        # Track the 1st arg (format string)
        "printf": ["n"],
        # Track the 1st arg (output string).
        "fprintf": ["n", "fmt"],
        # Track the return instruction of the function
        "ret": ["r"],
    }


def apply_constraint(state, sink, sources, **kwargs):
    """
    Constraint: ...
    """
    # sources is the list of return values from the source (malloc)
    # sink is the argument used at the sink
    # Prefer state.solver.satisfiable over copying state.

    if not sources:
        state.solver.add(False)
        return
