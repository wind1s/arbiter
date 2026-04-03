import claripy


def specify_sources():
    # Arbiter often works best with implicit sources (backtracking from sink).
    # However, if you want to enforce that data comes from network/files:
    return {"recv": 2, "read": 2, "fgets": 1, "fread": 1, "getenv": 0}


def specify_sinks():
    return {
        "open": ["n"],
        "fopen": ["n"],
        "openat": ["c", "n"],  # pathname is the 2nd argument
        "chdir": ["n"],
        "rmdir": ["n"],
        "unlink": ["n"],
    }


def apply_constraint(state, sink, sources, **kwargs):
    """
    Constraint: Can the symbolic filename contain the substring "../" or "..\\"?
    """
    if not sources:
        state.solver.add(False)
        return

    # Concrete Evaluation
    if not sink.symbolic:
        conc_bytes = state.solver.eval(sink, cast_to=bytes)
        if b"../" in conc_bytes or b"..\\" in conc_bytes:
            return  # Bug found (concrete)
        state.solver.add(False)
        return

    bits = sink.length
    found = False

    # Pre-create the bitvectors for our target traversal strings
    # This avoids endianness/integer mismatch issues
    dot_dot_slash = claripy.BVV(b"../")
    # Windows addition: dot_dot_back = claripy.BVV(b"..\\")

    # Iterate through the bitvector byte by byte (sliding window)
    # Stop at bits-24 because we need 3 bytes (24 bits) to match "../"
    for i in range(0, bits - 16, 8):
        # Extract 24 bits (3 bytes) at current offset
        chunk = sink[i + 23 : i]

        # Can this chunk be equal to "../" OR "..\"?
        # Windows addition: condition = claripy.Or(chunk == dot_dot_slash, chunk == dot_dot_back)
        condition = chunk == dot_dot_slash

        if state.solver.satisfiable(extra_constraints=[condition]):
            # Bug confirmed. Commit the constraint to the main state to trigger the alarm.
            state.solver.add(condition)
            found = True
            break

    if not found:
        state.solver.add(False)
