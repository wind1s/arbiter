def specify_sources():
    # Arbiter often works best with implicit sources (backtracking from sink).
    # However, if you want to enforce that data comes from network/files:
    return {"recv": 2, "read": 2, "fgets": 1, "fread": 1, "getenv": 0}


def specify_sinks():
    return {
        "open": ["n", "c"],
        "fopen": ["n", "p"],
        "openat": ["c", "n", "c"],
        "chdir": ["n"],
        "chroot": ["n"],
        "rmdir": ["n"],
        "unlink": ["n"],
    }


def apply_constraint(state, sink, sources, **kwargs):
    return
