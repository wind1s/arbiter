def specify_sources():
    # Arbiter often works best with implicit sources (backtracking from sink).
    # However, if you want to enforce that data comes from network/files:
    return {"recv": 1, "read": 1, "fgets": 0}


def specify_sinks():
    # 'i' usually denotes the input string/filename in Arbiter's utils
    return {
        "open": ["i"],
        "fopen": ["i"],
        "openat": ["i"],  # Extended
        "chdir": ["i"],  # Extended
        "rmdir": ["i"],  # Extended
        "unlink": ["i"],  # Extended
    }


def apply_constraint(state, sink, sources, **kwargs):
    """
    Constraint: Can the symbolic filename contain the substring "../"?
    """
    # 1. If the sinkession is not symbolic, we check concrete bytes
    if not sink.symbolic:
        # Evaluate to concrete bytes
        conc_bytes = state.solver.eval(sink, cast_to=bytes)
        if b"../" in conc_bytes or b"..\\" in conc_bytes:
            # Bug found (concrete)
            return
        state.solver.add(False)
        return

    # 2. Symbolic check: Sliding window for "../"
    # We create a new state to avoid polluting the main state during checks
    check_state = state.copy()

    # We look for the sequence 0x2E 0x2E 0x2F ('../')
    # Expression length in bits
    bits = sink.length
    found = False

    # Iterate through the bitvector byte by byte (sliding window)
    # We stop at bits-24 because we need 3 bytes
    for i in range(0, bits - 16, 8):
        # Extract 24 bits (3 bytes) at current offset
        # Note: slicing in Claripy is [high:low]
        chunk = sink[i + 23 : i]

        # Can this chunk be equal to "../" ?
        if check_state.solver.satisfiable(extra_constraints=[chunk == 0x2E2E2F]):
            state.solver.add(chunk == 0x2E2E2F)
            found = True
            break

    if not found:
        state.solver.add(False)
