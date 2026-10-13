"""Prepare an isolated supplementary search, then launch it explicitly.

Preparation copies source and likelihood inputs only. No archived search results,
learned priors, or solver caches are used. The physics stages are unchanged.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys

from .ablation_policy import patch_batch

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = ("ai_theory_lab", "gr_grammar_masker_v3_2", "eom_v5_2", "builder_v5_2", "solver_v5_2")
ENTRIES = ("GR_grammar_masker_v3.2.py", "EOM v5.2.py", "Builder v5.2.py", "Solver v5.2.py")
DATA = ("data/SN data/DES-Dovekie_HD.csv", "data/SN data/STAT+SYS.npz",
        "data/BAO data/desi_gaussian_bao_ALL_GCcomb_mean.txt",
        "data/BAO data/desi_gaussian_bao_ALL_GCcomb_cov.txt")
MODES = ("random", "memory-off", "memory-on", "mock")


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def runtime_env(protocol, directory):
    # Inherited stage overrides could silently change the data or protocol.
    allowed = ("PATH", "HOME", "USER", "TMPDIR", "SYSTEMROOT", "LANG", "LC_ALL",
               "SSL_CERT_FILE", "SSL_CERT_DIR", "REQUESTS_CA_BUNDLE",
               "HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY")
    env = {key: os.environ[key] for key in allowed if key in os.environ}
    work = directory / "workspace"
    env.update(PYTHONUNBUFFERED="1", PYTHONPATH=str(work), MPLCONFIGDIR=str(directory / "matplotlib-cache"),
               AGENT_MIN_OPERATOR_TERMS="1", AGENT_MAX_OPERATOR_TERMS="8",
               AGENT_OPERATOR_COUNT_FIXED_PROB="0.05", SOLVER_IDENTIFIABILITY_MODE="off",
               LANGSMITH_TRACING="false", SOLVER_PARALLEL="1", N_WORKERS=str(protocol["workers"]))
    for name in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
        env[name] = "1"
    if protocol["mode"] != "random":
        key = protocol["api_key_env"]
        if key in os.environ:
            env[key] = os.environ[key]
    if protocol["mode"] in ("random", "memory-off"):
        env["REAL_ABLATION_MODE"] = "uniform" if protocol["mode"] == "random" else "llm_no_memory"
    if protocol["mode"] == "mock":
        env.update(SN_DIR=str(directory / "MOCK_DATA_001/SN"), BAO_DIR=str(directory / "MOCK_DATA_001/BAO"))
    else:
        env.update(SN_DIR=str(work / "data/SN data"), BAO_DIR=str(work / "data/BAO data"))
    return env


def search_command(p):
    command = [sys.executable, "-m", "ai_theory_lab.graph_agent_batch",
               "--waves", str(math.ceil(p["parents"] / 24)), "--batch-size", "24",
               "--target-attempts", str(p["parents"]), "--run-name", p["run_name"],
               "--initial-parameter-samples", "1000", "--expanded-parameter-samples", "3000",
               "--expanded-chi2-threshold", "2000", "--refine-parameter-samples", "5000",
               "--refine-chi2-threshold", "1638", "--n-workers", str(p["workers"]),
               "--scheduler", "async_slots", "--slot-count", str(p["workers"]), "--slot-workers", "1",
               "--group-mode", "open_only", "--diversity-strength", "0.0", "--timeout-setup", "1200",
               "--seed", str(p["search_seed"]), "--pretty"]
    if p["mode"] == "random":
        command += ["--proposal-mode", "deterministic"]
    else:
        command += ["--proposal-mode", "llm", "--llm-provider", p["provider"],
                    "--llm-model", p["model"], "--llm-api-key-env", p["api_key_env"], "--llm-fallback", "skip"]
        if p.get("base_url"):
            command += ["--llm-base-url", p["base_url"]]
    return command


def prepare(args, root=ROOT):
    directory = args.output_dir.expanduser().resolve()
    if args.parents < 1 or args.workers < 1:
        raise ValueError("Parents and workers must be positive")
    if args.mode == "mock" and not directory.name.startswith("MOCK_"):
        raise ValueError("Mock search directory must be named MOCK_*")
    if args.mode != "mock" and any(part.startswith("MOCK_") or part == "mock_experiments" for part in directory.parts):
        raise ValueError("Real-data searches must stay outside mock directories")
    for protected in (*PACKAGES, "data", "reproduction"):
        if directory.is_relative_to(root / protected):
            raise ValueError("Use an output directory outside source and data directories")
    directory.mkdir(parents=True, exist_ok=False)
    work = directory / "workspace"
    sources = [root / name for name in ENTRIES + DATA]
    for name in PACKAGES:
        sources.extend(sorted((root / name).glob("*.py")))
    original_hashes = {}
    for source in sources:
        relative = source.relative_to(root)
        dest = work / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, dest)
        original_hashes[str(relative)] = sha256(source)
    if args.mode in ("random", "memory-off"):
        batch = work / "ai_theory_lab/graph_agent_batch.py"
        batch.write_text(patch_batch(batch.read_text()))
        shutil.copyfile(root / "reproduction/ablation_policy.py", work / "ai_theory_lab/ablation_policy.py")
    prefix = "MOCK" if args.mode == "mock" else "REAL"
    protocol = dict(release="v5.6", mode=args.mode, dataset_kind="MOCK_SYNTHETIC" if args.mode == "mock" else "REAL_OBSERVATION",
                    parents=args.parents, workers=args.workers, search_seed=args.seed, mock_seed=args.mock_seed,
                    run_name=f"{prefix}_{args.mode.replace('-', '_')}_{args.parents}",
                    provider=args.provider, model=args.model, api_key_env=args.api_key_env, base_url=args.base_url,
                    prepared_utc=datetime.now(timezone.utc).isoformat(), source_sha256=original_hashes,
                    scope="Rerun with v5.6 source; not a frozen historical benchmark implementation.")
    if args.mode == "mock":
        # Data creation/refit is local numerical work; no API calls or theory search.
        command = [sys.executable, "-m", "ai_theory_lab.lcdm_mock", "--sn-dir", str(work / "data/SN data"),
                   "--bao-dir", str(work / "data/BAO data"), "--output-dir", str(directory / "MOCK_DATA_001"),
                   "--seed", str(args.mock_seed)]
        subprocess.run(command, cwd=work, env=runtime_env(protocol, directory), check=True)
        protocol["mock_reference"] = "MOCK_DATA_001/MOCK_LCDM_reference.json"
        protocol["global_p_value_calibrated"] = False
    files = list(work.rglob("*.py")) + [work / name for name in DATA]
    if args.mode == "mock":
        files += [p for p in (directory / "MOCK_DATA_001").rglob("*") if p.is_file() and "__pycache__" not in p.parts]
    protocol["snapshot_sha256"] = {str(path.relative_to(directory)): sha256(path) for path in files}
    (directory / "protocol.json").write_text(json.dumps(protocol, indent=2) + "\n")
    (directory / "README.txt").write_text(
        f"{protocol['dataset_kind']} — {args.mode}, {args.parents} parent proposals.\n"
        "Source, data and all search outputs are isolated in this directory.\n"
        "Preparation has not started a theory search. Run explicitly with reproduction.search run.\n"
        + ("MOCK / SYNTHETIC — NOT REAL OBSERVATIONS. Use the refitted mock reference only.\n" if args.mode == "mock" else ""))
    print(f"Prepared {protocol['dataset_kind']}: {directory}")
    return protocol


def run(directory):
    directory = directory.expanduser().resolve()
    p = json.loads((directory / "protocol.json").read_text())
    for relative, expected in p["snapshot_sha256"].items():
        if sha256(directory / relative) != expected:
            raise ValueError(f"Snapshot changed: {relative}")
    env = runtime_env(p, directory)
    if p["mode"] != "random" and not env.get(p["api_key_env"]):
        raise ValueError(f"Set {p['api_key_env']} before starting this LLM search")
    # Do not silently overwrite or restart a paid search. A failed run is retained
    # for inspection; prepare a new directory for a new experiment.
    status_path = directory / "search_status.json"
    with status_path.open("x") as handle:
        json.dump({"dataset_kind": p["dataset_kind"], "status": "RUNNING"}, handle)
    command = search_command(p)
    print(f"Starting {p['dataset_kind']}: {p['parents']} parents; log: {directory / 'console.log'}", flush=True)
    try:
        with (directory / "console.log").open("x") as log:
            log.write(p["dataset_kind"] + "\n")
            log.flush()
            result = subprocess.run(command, cwd=directory / "workspace", env=env, stdout=log, stderr=subprocess.STDOUT)
        status = {"dataset_kind": p["dataset_kind"], "status": "EXITED", "exit_code": result.returncode,
                  "command": command, "finished_utc": datetime.now(timezone.utc).isoformat()}
    except BaseException:
        status_path.write_text(json.dumps({"dataset_kind": p["dataset_kind"], "status": "INTERRUPTED_OR_FAILED"}) + "\n")
        raise
    status_path.write_text(json.dumps(status, indent=2) + "\n")
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prep = commands.add_parser("prepare", help="Copy clean inputs; generate/refit data for mock mode; no theory search")
    prep.add_argument("--mode", choices=MODES, required=True)
    prep.add_argument("--parents", type=int, required=True)
    prep.add_argument("--output-dir", type=Path, required=True)
    prep.add_argument("--workers", type=int, default=8)
    prep.add_argument("--seed", type=int, default=20260607)
    prep.add_argument("--mock-seed", type=int, default=20260908)
    prep.add_argument("--provider", choices=("openai", "anthropic", "openai_compatible"), default="openai")
    prep.add_argument("--model", default="gpt-5.6-sol")
    prep.add_argument("--api-key-env", default="OPENAI_API_KEY")
    prep.add_argument("--base-url")
    launch = commands.add_parser("run", help="Launch the prepared search; LLM modes incur API charges")
    launch.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "prepare":
        prepare(args)
        return 0
    return run(args.output_dir)


if __name__ == "__main__":
    raise SystemExit(main())
