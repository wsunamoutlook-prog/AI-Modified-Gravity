from __future__ import annotations

import inspect
import json
import random
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from ai_theory_lab.graph_agent_batch import (
    _async_slot_resume_state,
    _group_targets,
    _target_for_slot_group,
    _validate_async_slot_resume_configuration,
    run_batch_agent,
)
from ai_theory_lab.check_api_connections import FRONTIER6_SPECS, _call_anthropic
from ai_theory_lab.llm_agent import (
    _call_anthropic_messages,
    _choice_prompt,
    _openai_compatible_request_options,
    _parse_candidate_choice,
)
from ai_theory_lab.submit_final_runs import CHEAP5_RUNS, FRONTIER6_RUNS, _slurm_text
from ai_theory_lab.langsmith_live_monitor import _elapsed_hours
from ai_theory_lab.compare_benchmarks import _wall_seconds


ROOT = Path(__file__).resolve().parents[1]


class OpenOnlySchedulingTests(unittest.TestCase):
    def test_open_only_assigns_every_initial_target_to_unrestricted_open_search(self) -> None:
        targets = _group_targets(25, "open_only", 0.5, random.Random(7))

        self.assertEqual(len(targets), 25)
        self.assertEqual({target["group"] for target in targets}, {"open_search"})
        self.assertEqual({target["track"] for target in targets}, {None})

    def test_async_slot_replenishment_stays_open_only(self) -> None:
        target = _target_for_slot_group(
            group_mode="open_only",
            eh_track_fraction=0.5,
            submitted_by_group={"open_search": 113},
            rng=random.Random(11),
        )

        self.assertEqual(target, {"group": "open_search", "track": None, "scalar_config": None})

    def test_sector_split_remains_available_for_legacy_runs(self) -> None:
        targets = _group_targets(24, "sector_split", 0.5, random.Random(13))
        groups = [target["group"] for target in targets]

        self.assertEqual(groups.count("open_search"), 12)
        self.assertEqual(groups.count("non_eh"), 12)

    def test_open_only_is_the_programmatic_default(self) -> None:
        parameters = inspect.signature(run_batch_agent).parameters
        default = parameters["group_mode"].default
        self.assertEqual(default, "open_only")
        self.assertNotIn("non_eh_refine_parameter_samples", parameters)
        self.assertNotIn("non_eh_refine_chi2_threshold", parameters)
        self.assertFalse(parameters["resume"].default)


class AsyncSlotResumeTests(unittest.TestCase):
    def test_resume_recounts_completed_initial_attempts_and_advances_task_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            proposal_dir = root / "proposals"
            memory_dir = root / "memory"
            proposal_dir.mkdir()
            memory_dir.mkdir()
            attempts = [
                {
                    "loop_id": "task_000001_slot_01_lag_1",
                    "scheduler_task_id": "task_000001",
                    "validation_stage": "initial",
                    "proposal_group": "open_search",
                },
                {
                    "loop_id": "task_000002_slot_02_lag_1",
                    "scheduler_task_id": "task_000002",
                    "validation_stage": "initial",
                    "proposal_group": "open_search",
                },
                {
                    "loop_id": "task_000001_expanded_slot_01_lag_1",
                    "scheduler_task_id": "task_000001_expanded",
                    "validation_stage": "expanded",
                    "proposal_group": "open_search",
                },
                {
                    "loop_id": "task_000001_refine_slot_01_lag_1",
                    "scheduler_task_id": "task_000001_refine",
                    "validation_stage": "refine",
                    "proposal_group": "open_search",
                },
            ]
            (memory_dir / "attempt_history.jsonl").write_text(
                "\n".join(json.dumps(row) for row in attempts) + "\n{partial",
                encoding="utf-8",
            )
            events = [
                {
                    "event": "submitted",
                    "task_id": "task_000009",
                    "submitted_total": 5,
                    "recorded_total": 2,
                    "expanded_submitted_total": 2,
                    "refine_submitted_total": 1,
                    "failed_total": 3,
                }
            ]
            (proposal_dir / "scheduler_tasks.jsonl").write_text(
                "\n".join(json.dumps(row) for row in events),
                encoding="utf-8",
            )
            (proposal_dir / "task_000012_slot_08_lag_1.json").write_text("{}", encoding="utf-8")

            state = _async_slot_resume_state(
                proposal_dir=proposal_dir,
                memory_dir=memory_dir,
                group_names=["open_search"],
            )

        self.assertEqual(state["recorded_total"], 2)
        self.assertEqual(state["submitted_total"], 2)
        self.assertEqual(state["historical_submitted_total"], 5)
        self.assertEqual(state["expanded_recorded_total"], 1)
        self.assertEqual(state["expanded_submitted_total"], 2)
        self.assertEqual(state["refine_recorded_total"], 1)
        self.assertEqual(state["failed_total"], 3)
        self.assertEqual(state["task_sequence"], 12)
        self.assertEqual(state["recorded_by_group"], {"open_search": 2})

    def test_resume_rejects_interior_jsonl_corruption(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            proposal_dir = root / "proposals"
            memory_dir = root / "memory"
            proposal_dir.mkdir()
            memory_dir.mkdir()
            (memory_dir / "attempt_history.jsonl").write_text(
                '{"loop_id":"task_000001"}\n{broken\n{"loop_id":"task_000002"}\n',
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "Malformed JSONL record"):
                _async_slot_resume_state(
                    proposal_dir=proposal_dir,
                    memory_dir=memory_dir,
                    group_names=["open_search"],
                )

    def test_resume_rejects_changed_model_or_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            proposal_dir = Path(tmp)
            original = {
                "event": "scheduler_start",
                "target_attempts": 1000,
                "llm_provider": "openai_compatible",
                "llm_model": "qwen3.7-max",
                "llm_base_url": "https://example.test/v1/",
                "llm_api_key_env": "DASHSCOPE_API_KEY",
            }
            (proposal_dir / "scheduler_tasks.jsonl").write_text(
                json.dumps(original) + "\n",
                encoding="utf-8",
            )

            _validate_async_slot_resume_configuration(
                proposal_dir=proposal_dir,
                target_attempts=1000,
                llm_provider="openai_compatible",
                llm_model="qwen3.7-max",
                llm_base_url="https://example.test/v1",
                llm_api_key_env="DASHSCOPE_API_KEY",
            )
            with self.assertRaisesRegex(ValueError, "llm_model"):
                _validate_async_slot_resume_configuration(
                    proposal_dir=proposal_dir,
                    target_attempts=1000,
                    llm_provider="openai_compatible",
                    llm_model="qwen3.7-plus",
                    llm_base_url="https://example.test/v1",
                    llm_api_key_env="DASHSCOPE_API_KEY",
                )
            with self.assertRaisesRegex(ValueError, "target_attempts"):
                _validate_async_slot_resume_configuration(
                    proposal_dir=proposal_dir,
                    target_attempts=2000,
                    llm_provider="openai_compatible",
                    llm_model="qwen3.7-max",
                    llm_base_url="https://example.test/v1",
                    llm_api_key_env="DASHSCOPE_API_KEY",
                )

    def test_elapsed_time_excludes_resume_downtime(self) -> None:
        events = [
            {"event": "scheduler_start", "timestamp": "2026-07-24T00:00:00+00:00"},
            {"event": "recorded", "timestamp": "2026-07-24T01:00:00+00:00"},
            {"event": "scheduler_resume", "timestamp": "2026-07-24T03:00:00+00:00"},
            {"event": "recorded", "timestamp": "2026-07-24T05:00:00+00:00"},
        ]

        self.assertEqual(_elapsed_hours(events), 3.0)
        self.assertEqual(_wall_seconds(events, []), 3.0 * 3600.0)

    def test_completed_target_resume_finishes_without_duplicate_submission(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            proposal_dir = root / "ai_theory_lab" / "proposals" / "resume_complete"
            memory_dir = root / "ai_theory_lab" / "memory" / "resume_complete"
            proposal_dir.mkdir(parents=True)
            memory_dir.mkdir(parents=True)
            attempt = {
                "loop_id": "task_000004_slot_01_lag_1",
                "scheduler_task_id": "task_000004",
                "validation_stage": "initial",
                "proposal_group": "open_search",
                "theory": {"proposal_group": "open_search"},
            }
            (memory_dir / "attempt_history.jsonl").write_text(
                json.dumps(attempt) + "\n",
                encoding="utf-8",
            )

            with mock.patch("ai_theory_lab.graph_agent_batch.ROOT", root), mock.patch(
                "ai_theory_lab.graph_agent_batch._build_token_level_context",
                return_value={},
            ), mock.patch(
                "ai_theory_lab.graph_agent_batch._write_token_level_context_summary"
            ), mock.patch(
                "ai_theory_lab.graph_agent_batch.generate_report",
                return_value=root / "report",
            ):
                output = run_batch_agent(
                    waves=1,
                    batch_size=1,
                    seed=7,
                    run_name="resume_complete",
                    initial_parameter_samples=1000,
                    timeout_setup=1200,
                    proposal_mode="deterministic",
                    llm_fallback="skip",
                    llm_api_timeout=30,
                    use_token_context_cache=True,
                    n_workers=1,
                    scheduler="async_slots",
                    target_attempts=1,
                    slot_count=1,
                    slot_workers=1,
                    resume=True,
                )

            events = [
                json.loads(line)
                for line in (proposal_dir / "scheduler_tasks.jsonl").read_text(encoding="utf-8").splitlines()
            ]

        self.assertTrue(output["resume"])
        self.assertEqual([event["event"] for event in events], ["scheduler_resume", "scheduler_complete"])
        self.assertEqual(events[-1]["recorded_total"], 1)
        self.assertEqual(list(proposal_dir.glob("task_*.json")), [])


class SubmissionTemplateTests(unittest.TestCase):
    def test_generated_slurm_uses_open_only(self) -> None:
        text = _slurm_text(
            CHEAP5_RUNS[0],
            run_name="open_only_test",
            attempts=24,
            cpus=8,
            mem="32G",
            time_limit="01:00:00",
            run_label="test",
            group_mode="open_only",
        )

        self.assertIn("--group-mode open_only", text)
        self.assertNotIn("--group-mode sector_split", text)
        self.assertNotIn("--non-eh-refine", text)

    def test_generated_resume_slurm_uses_single_continuation(self) -> None:
        text = _slurm_text(
            FRONTIER6_RUNS[1],
            run_name="resume_test",
            attempts=1000,
            cpus=8,
            mem="32G",
            time_limit="96:00:00",
            run_label="resume",
            group_mode="open_only",
            resume=True,
        )

        self.assertIn("  --resume \\\n", text)
        self.assertNotIn("  --resume \\\\\n", text)

    def test_frontier6_models_match_api_preflight(self) -> None:
        submit_models = [run.model for run in FRONTIER6_RUNS]
        preflight_models = [spec.model for spec in FRONTIER6_SPECS]

        self.assertEqual(submit_models, preflight_models)
        self.assertEqual(
            submit_models,
            [
                "gpt-5.6-sol",
                "claude-sonnet-5",
                "gemini-3.6-flash",
                "qwen3.7-max",
                "deepseek-v4-pro",
                "kimi-k3",
            ],
        )

    def test_frontier6_slurm_templates_fail_fast_and_stay_open_only(self) -> None:
        for run in FRONTIER6_RUNS:
            with self.subTest(model=run.model):
                text = _slurm_text(
                    run,
                    run_name=f"frontier_test_{run.tag}",
                    attempts=24,
                    cpus=8,
                    mem="32G",
                    time_limit="01:00:00",
                    run_label="test",
                    group_mode="open_only",
                )
                self.assertIn("set -euo pipefail", text)
                self.assertIn(f"{run.key_env} is required", text)
                self.assertIn("--group-mode open_only", text)
                self.assertIn("--llm-fallback skip", text)

        kimi_text = _slurm_text(
            FRONTIER6_RUNS[-1],
            run_name="frontier_test_kimi",
            attempts=24,
            cpus=8,
            mem="32G",
            time_limit="01:00:00",
            run_label="test",
            group_mode="open_only",
        )
        self.assertIn('"${KIMI_MODEL:-kimi-k3}"', kimi_text)
        self.assertIn("MOONSHOT_API_KEY is required", kimi_text)
        self.assertIn('https://api.moonshot.ai/v1', kimi_text)
        self.assertNotIn("KIMI_BASE_URL is required", kimi_text)


class ApiPreflightTests(unittest.TestCase):
    def test_sonnet5_probe_disables_adaptive_thinking(self) -> None:
        response = mock.MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps(
            {"content": [{"type": "text", "text": "ok"}]}
        ).encode("utf-8")

        with mock.patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}), mock.patch(
            "urllib.request.urlopen", return_value=response
        ) as urlopen:
            text = _call_anthropic(FRONTIER6_SPECS[1], timeout=1.0)

        request = urlopen.call_args.args[0]
        body = json.loads(request.data.decode("utf-8"))
        self.assertEqual(text, "ok")
        self.assertEqual(body["model"], "claude-sonnet-5")
        self.assertEqual(body["thinking"], {"type": "disabled"})
        self.assertEqual(body["max_tokens"], 64)


class ProposalApiTests(unittest.TestCase):
    def test_candidate_choice_protocol_keeps_rationale_for_run_compatibility(self) -> None:
        _system, user, schema = _choice_prompt([], {})

        self.assertIn("rationale", user["output_schema"])
        self.assertEqual(schema["required"], ["candidate_index", "rationale"])

    def test_production_anthropic_call_disables_thinking(self) -> None:
        response = mock.MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps(
            {"content": [{"type": "text", "text": "{\"candidate_index\": 2}"}]}
        ).encode("utf-8")

        with mock.patch("urllib.request.urlopen", return_value=response) as urlopen:
            text, _ = _call_anthropic_messages(
                system="system",
                user={"candidates": []},
                model="claude-sonnet-5",
                base_url=None,
                api_key="test-key",
                api_timeout=1.0,
                max_output_tokens=64,
            )

        request = urlopen.call_args.args[0]
        body = json.loads(request.data.decode("utf-8"))
        self.assertEqual(text, '{"candidate_index": 2}')
        self.assertEqual(body["thinking"], {"type": "disabled"})

    def test_provider_options_reduce_reasoning_for_short_choice(self) -> None:
        ali = _openai_compatible_request_options(
            model="deepseek-v4-pro",
            base_url="https://workspace.aliyuncs.com/compatible-mode/v1",
            max_output_tokens=1800,
        )
        gemini = _openai_compatible_request_options(
            model="gemini-3.6-flash",
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            max_output_tokens=1800,
        )
        kimi = _openai_compatible_request_options(
            model="kimi-k3",
            base_url="https://api.moonshot.ai/v1",
            max_output_tokens=1800,
        )

        self.assertEqual(ali["extra_body"], {"enable_thinking": False})
        self.assertEqual(gemini["reasoning_effort"], "low")
        self.assertEqual(kimi["reasoning_effort"], "low")
        self.assertEqual(kimi["max_completion_tokens"], 1800)

    def test_truncated_rationale_preserves_explicit_candidate_index(self) -> None:
        choice = _parse_candidate_choice('{"candidate_index": 7, "rationale": "unterminated')

        self.assertEqual(choice["candidate_index"], 7)
        self.assertTrue(choice["parse_recovered"])


class DocumentationConsistencyTests(unittest.TestCase):
    def test_current_run_guides_document_open_only_default(self) -> None:
        paths = [
            ROOT / "AGENTS.md",
            ROOT / "ai_theory_lab" / "proposal_schema.md",
            ROOT / "ai_theory_lab" / "cold_start_loop.md",
        ]

        for path in paths:
            with self.subTest(path=path):
                text = path.read_text(encoding="utf-8")
                self.assertIn("open_only", text)

    def test_cold_start_guide_does_not_restore_even_sector_default(self) -> None:
        text = (ROOT / "ai_theory_lab" / "cold_start_loop.md").read_text(encoding="utf-8")

        self.assertNotIn("proposal sectors are split evenly", text)
        self.assertIn("no budget is reserved for a dedicated `non_eh`", text)

    def test_guides_do_not_restore_non_eh_specific_refinement(self) -> None:
        for path in [ROOT / "AGENTS.md", ROOT / "ai_theory_lab" / "proposal_schema.md"]:
            with self.subTest(path=path):
                text = path.read_text(encoding="utf-8")
                self.assertNotIn("non-EH 10000-sample", text)
                self.assertNotIn("opportunistic non-EH 10000", text)


if __name__ == "__main__":
    unittest.main()
