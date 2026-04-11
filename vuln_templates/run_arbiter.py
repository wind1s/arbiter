#!/usr/bin/env python
import json
import logging
import string
import sys
from argparse import ArgumentParser
from importlib import util
from itertools import groupby
from pathlib import Path

import angr

from arbiter.master_chief import sa_advanced, sa_recon, symbolic_execution

LOG_DIR = None
JSON_DIR = None
CALL_DEPTH = 1
STRICT_MODE = False
IDENTIFIER = None
LOG_LEVEL = logging.DEBUG
CALLER_LEVEL = -1

logging.getLogger("angr").setLevel(logging.WARNING)


def enable_logging(vd, target):
    vd = Path(vd).stem
    target = Path(target).stem

    loggers = ["sa_recon", "sa_advanced", "symbolic_execution"]
    for logger in loggers:
        log = logging.getLogger(f"arbiter.master_chief.{logger}")

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        if LOG_DIR is not None:
            handler = logging.FileHandler(f"{LOG_DIR}/arbiter_{vd}_{target}.log")
            handler.setFormatter(formatter)
            log.addHandler(handler)

        log.setLevel(LOG_LEVEL)


def save_results(reports):
    if not reports:
        logging.info("No reports generated.")
        return

    for r in reports:
        filepath = f"{JSON_DIR}/ArbiterReport_{hex(r.bbl)}.json"

        report_data = {
            "sink_bbl": hex(r.bbl),
            "function": hex(r.function),
            # Applying the sequence encoding here
            "bbl_history": {key: len(list(group)) for key, group in groupby(r.bbl_history)},
            "function_history": {key: len(list(group)) for key, group in groupby(r.function_history)},
        }

        with open(filepath, "w") as f:
            json.dump(report_data, f, indent=2)


def main(template, target):
    project = angr.Project(target, auto_load_libs=False)

    sink_map = template.specify_sinks()
    sa = sa_recon.SA_Recon(project, sinks=sink_map.keys(), maps=sink_map, json_dir=JSON_DIR)
    if IDENTIFIER is None:
        sa.analyze(ignore_funcs=BLACKLIST)
    else:
        sa.analyze_one(IDENTIFIER)

    sources = template.specify_sources()
    sb = sa_advanced.SA_Adv(
        sa,
        checkpoint=sources,
        require_dd=STRICT_MODE,
        call_depth=CALL_DEPTH,
        json_dir=JSON_DIR,
    )
    sb.analyze_all()

    constrain = template.apply_constraint
    se = symbolic_execution.SymExec(sb, constrain=constrain, require_dd=STRICT_MODE, json_dir=JSON_DIR)
    se.run_all()

    save_results(se.postprocessing(pred_level=CALLER_LEVEL))


if __name__ == "__main__":
    parser = ArgumentParser(description="Use Arbiter to run a template against a specific binary")
    parser.add_argument("-f", metavar="VD", type=str, help="The VD template to use", required=True)
    parser.add_argument(
        "-t",
        metavar="TARGET",
        type=str,
        help="The target binary to analyze",
        required=True,
    )
    parser.add_argument(
        "-i",
        metavar="ADDR",
        type=str,
        help="Specify a target function identifier (name|addr) to focus the analysis on",
        required=False,
        default="",
    )
    parser.add_argument(
        "-b",
        metavar="BLACKLIST",
        type=str,
        help="Specify a list of function identifiers (name|addr) to skip analysis",
        required=False,
        default=[],
        nargs="+",
    )
    parser.add_argument(
        "-r",
        metavar="LEVEL",
        type=int,
        help="Number of levels for Adaptive False Positive Reduction",
        required=False,
        default=-1,
    )
    parser.add_argument(
        "-l",
        metavar="LOG_DIR",
        type=str,
        help="Enable logging to LOG_DIR",
        required=False,
    )
    parser.add_argument(
        "-j",
        metavar="JSON_DIR",
        type=str,
        help="Enable verbose statistics dumps to JSON_DIR",
        required=False,
    )
    parser.add_argument(
        "-s",
        help="Enable strict mode (stricter static data-flow based filtering)",
        action="store_true",
        required=False,
    )

    args = parser.parse_args()

    vd = Path(args.f)
    target = Path(args.t)

    if vd.exists() is False:
        sys.stderr.write(f"Error: {vd} does not exist\n")
        sys.exit(-1)
    elif target.exists() is False:
        sys.stderr.write(f"Error: {target} does not exist\n")
        sys.exit(-1)

    try:
        spec = util.spec_from_file_location(vd.stem, vd.absolute().as_posix())
        template = util.module_from_spec(spec)
        spec.loader.exec_module(template)
    except Exception as e:
        sys.stderr.write(f"Error could not import VD {vd}: Error {e}\n")
        sys.exit(-1)

    if len(args.i) == 0:
        IDENTIFIER = None
    elif args.i.isdecimal():
        IDENTIFIER = int(args.i)
    elif args.i.startswith("0x") or all(c in string.hexdigits for c in args.i):
        IDENTIFIER = int(args.i, 16)
    else:
        IDENTIFIER = args.i

    BLACKLIST = args.b

    CALLER_LEVEL = args.r

    if args.l:
        Path(args.l).mkdir(parents=True, exist_ok=True)
        if Path(args.l).exists():
            LOG_DIR = Path(args.l).resolve().as_posix()
        else:
            sys.stderr.write(f"Directory {args.l} does not exist and we could not create it\n")
    enable_logging(vd, target)

    if args.j:
        Path(args.j).mkdir(parents=True, exist_ok=True)
        if Path(args.j).exists():
            JSON_DIR = Path(args.j).resolve().as_posix()
        else:
            sys.stderr.write(f"Directory {args.l} does not exist and we could not create it\n")

    if args.s:
        STRICT_MODE = True

    main(template, target)
