"""Fixed-prior and no-memory controls, applied only to isolated source snapshots."""
from __future__ import annotations

import os
import random

MODES = ("adaptive", "uniform", "llm_no_memory")


def mode():
    value = os.environ.get("REAL_ABLATION_MODE", "")
    if value not in MODES:
        raise ValueError("An explicit REAL_ABLATION_MODE is required")
    return value


def learning_feedback(summary):
    # Result logging is unchanged. Only policy inputs are removed. Mechanical
    # duplicate limits are checked independently using the original summary.
    return summary if mode() == "adaptive" else {}


def choose_entry(**kwargs):
    selected_mode = mode()
    if selected_mode == "llm_no_memory":
        return None  # Use the original LLM path with the scrubbed summary.
    from . import cold_start_runner as cold

    context, seed = kwargs["context"], kwargs["seed"]
    scalar_config = kwargs.get("scalar_config")
    if selected_mode == "adaptive":
        from .llm_agent import _generate_candidate_entries
        # Same candidate construction and pre-ranking as the LLM arm. Replace
        # only the final API selection by taking the first pre-ranked entry.
        candidates = _generate_candidate_entries(
            context, kwargs["summary"], kwargs["rng"], seed,
            track=kwargs.get("track"), scalar_config=scalar_config,
            required_operator_substring=kwargs.get("required_operator_substring"),
            required_operator_contains_curvature=kwargs.get("required_operator_contains_curvature", False),
        )
        if not candidates:
            raise RuntimeError("No legal candidate for the non-LLM adaptive arm")
        selected = dict(candidates[0])
    else:
        # Hierarchical uniform prior, not uniform over physical equivalence
        # classes: scalar family, term count, potential and operator subset.
        rng = random.Random(seed)
        if kwargs.get("track") not in (None, "mixed") or kwargs.get("required_operator_substring") or kwargs.get("required_operator_contains_curvature"):
            raise ValueError("Uniform baseline requires the unrestricted open-only lane")
        scalar_config = scalar_config or rng.choice(("none", "phi1_only", "phi2_only", "both"))
        allowed = sorted(
            [candidate for candidate in context["masker"].all_candidates
             if cold._candidate_allowed_for_scalar_config(candidate, scalar_config)],
            key=cold._candidate_sort_key,
        )
        if not allowed:
            raise RuntimeError("No legal operators for sampled scalar family")
        count = rng.randint(cold.DIRECT_MIN_OPERATOR_TERMS,
                            min(cold.DIRECT_MAX_OPERATOR_TERMS, len(allowed)))
        selected = cold._entry_skeleton(
            scalar_config=scalar_config,
            potential_types=rng.choice(cold._potential_options_for_scalar_config(scalar_config)),
            candidates=rng.sample(allowed, count), local_number=1,
        )
        selected.update(target_operator_count=count, baseline_control=False)
    entry = cold._direct_entry(
        tensors=context["tensors"], scalar_config=selected["scalar_config"],
        potential_types=dict(selected["potential_types"]),
        candidates=selected["_candidate_objects"], local_number=selected["local_number"],
    )
    entry.update(
        proposal_mode="non_llm_" + selected_mode,
        target_operator_count=selected.get("target_operator_count"),
        baseline_control=bool(selected.get("baseline_control", False)),
        theory_track=cold.theory_track_from_operators(entry["operators"]),
        ablation_mode=selected_mode, llm_provider=None, llm_model=None,
    )
    if scalar_config:
        entry["proposal_scalar_constraint"] = scalar_config
    return entry


def patch_batch(source):
    """Apply audited, exact outer-loop hooks; fail on an unexpected source."""
    replacements = [
        ('    if proposal_mode == "llm":\n        try:\n',
         '    from .ablation_policy import choose_entry\n'
         '    intervention = choose_entry(**locals())\n'
         '    if intervention is not None:\n'
         '        return intervention\n'
         '    if proposal_mode == "llm":\n        try:\n'),
        ('    summary = _summary_with_diversity(raw_summary, diversity_strength)\n',
         '    from .ablation_policy import learning_feedback\n'
         '    summary = _summary_with_diversity(learning_feedback(raw_summary), diversity_strength)\n'),
        ('        family = _entry_family_key(target_group, entry)\n        if family in reserved_families:\n',
         '        from .cold_start_runner import _under_duplicate_limit\n'
         '        if not _under_duplicate_limit(entry, raw_summary):\n'
         '            continue\n'
         '        family = _entry_family_key(target_group, entry)\n        if family in reserved_families:\n'),
        ('                        expanded_summary = _load_summary(memory_dir)\n',
         '                        from .ablation_policy import learning_feedback\n'
         '                        expanded_summary = learning_feedback(_load_summary(memory_dir))\n'),
        ('                        refine_summary = _load_summary(memory_dir)\n',
         '                        from .ablation_policy import learning_feedback\n'
         '                        refine_summary = learning_feedback(_load_summary(memory_dir))\n'),
    ]
    for old, new in replacements:
        if source.count(old) != 1:
            raise ValueError("Unexpected batch source at intervention: " + old.strip())
        source = source.replace(old, new)
    # Avoid attributing deterministic control jobs to an API provider in their
    # scheduler and final summaries. Restrict this to functions with that arg.
    for function_name, next_function in (("_run_async_slot_scheduler", "run_batch_agent"), ("run_batch_agent", "main")):
        start = source.index("def " + function_name + "(")
        end = source.index("\ndef " + next_function + "(", start)
        part = source[start:end]
        for field in ("llm_provider", "llm_model", "llm_base_url", "llm_api_key_env"):
            part = part.replace('"' + field + '": ' + field + ',',
                                '"' + field + '": ' + field + ' if proposal_mode == "llm" else None,')
        source = source[:start] + part + source[end:]
    return source
