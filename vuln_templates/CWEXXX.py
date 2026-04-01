def specify_sources():
    # Source: Return value (index 0) of allocation functions
    return {"malloc": 0}


def specify_sinks():
    """
    Sinks: Functions that crash on NULL arguments
    """
    return {"strlen": ["n"]}


def apply_constraint(state, sink, sources, **kwargs):
    """
    Constraint: ...
    """
    # sources is the list of return values from the source (malloc)
    # sink is the argument used at the sink

    if not sources:
        state.solver.add(False)
        return


def save_results(reports):
    for r in reports:
        with open(f"./logs/ArbiterReport_{hex(r.bbl)}", "w") as f:
            f.write("BBL:\n")
            f.write(f"{hex(r.bbl)}\n")

            f.write("\nTriggering Input (State):\n")
            if r.triggering_state:
                for k, v in r.triggering_state.items():
                    f.write(f"{k}: {v}\n")
            else:
                f.write("No specific input constraints found.\n")

            f.write("\nFunction:\n")
            f.write(f"{hex(r.function)}\n")

            f.write("\nBBL History:\n")
            # r.bbl_history is a list of strings
            f.write("\n".join(r.bbl_history))

            f.write("\n\nFunction History:\n")
            # r.function_history is a list of string
            f.write("\n".join(r.function_history))
