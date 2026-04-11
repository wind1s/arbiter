import claripy

FUNCTIONS = {
    "setuid",
    "setreuid",
    "setresuid",
    "setpgid",
    "setregid",
    "setgid",
    "setresgid",
    "setsid",
    "fgets",
    "chdir",
    "mmap",
    "chown",
    "access",
    "chroot",
    "prctl",
}


def parse_functions(function_name="", constraint_val=0):
    default_constraints = {"error": constraint_val == -1, "success": constraint_val == 0}
    custom_constraints = {
        "setsid": {
            "error": constraint_val == -1,
            "success": claripy.SGE(constraint_val, 0),
        },
        "prctl": {
            "error": constraint_val == -1,
            "success": claripy.SGE(constraint_val, 0),
        },
        "mmap": {
            "error": constraint_val == -1,
            "success": constraint_val != -1,
        },
        "chown": {
            "error": constraint_val == -1,
            "success": constraint_val == 0,
        },
        "fgets": {
            "error": constraint_val == 0,
            "success": constraint_val != 0,
        },
    }

    if function_name in custom_constraints.keys():
        function_constraints = custom_constraints[function_name]
    else:
        function_constraints = default_constraints

    success_constraint = function_constraints["success"]
    error_constraint = function_constraints["error"]
    return (success_constraint, error_constraint)


def apply_constraint(state, sink, sources, **kwargs):
    """
    Constraint: Prove the developer forgot to check the return value
    by demonstrating the current execution path allows the value to be
    BOTH an error (-1) and a success (0).
    """
    if not sources:
        state.solver.add(False)
        return

    retval = sources[0]

    site = kwargs.get("site")
    callee_name = site.callee if site else ""

    success_constraint, error_constraint = parse_functions(function_name=callee_name, constraint_val=retval)

    found = False
    # Hypothesis A: Can the return value be an error on this path?
    if state.solver.satisfiable(extra_constraints=[error_constraint]):
        # Hypothesis B: Can it ALSO be a success on this exact same path?
        if state.solver.satisfiable(extra_constraints=[success_constraint]):
            # Bug confirmed: The path allows both, meaning no check exists!
            state.solver.add(error_constraint)
            found = True

    if not found:
        state.solver.add(False)


def specify_sinks():
    sinks = {}
    for func in FUNCTIONS:
        sinks[func] = ["r"]
    return sinks


def specify_sources():
    sources = {}
    for func in FUNCTIONS:
        sources[func] = 0
    return sources
