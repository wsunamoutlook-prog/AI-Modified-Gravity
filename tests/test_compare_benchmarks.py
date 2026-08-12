from __future__ import annotations

import unittest

from ai_theory_lab.compare_benchmarks import _proposal_stats_from_events


class ProposalStatsFromEventsTests(unittest.TestCase):
    def test_uses_unique_initial_submissions_only(self) -> None:
        events = [
            {
                "event": "submitted",
                "task_id": "task_000001",
                "validation_stage": "initial",
                "llm_provider": "openai_compatible",
                "llm_model": "model-a",
                "proposal_mode": "llm",
                "llm_latency_sec": 2.0,
            },
            {
                "event": "submitted",
                "task_id": "task_000001",
                "validation_stage": "initial",
                "llm_provider": "openai_compatible",
                "llm_model": "model-a",
                "proposal_mode": "llm",
                "llm_latency_sec": 99.0,
            },
            {
                "event": "expanded_submitted",
                "task_id": "task_000001_expanded",
                "validation_stage": "expanded",
                "llm_provider": "openai_compatible",
                "llm_model": "model-a",
                "llm_latency_sec": 3.0,
            },
            {
                "event": "submitted",
                "task_id": "task_000002",
                "validation_stage": "initial",
                "llm_provider": "openai_compatible",
                "llm_model": "model-a",
                "proposal_mode": "llm",
                "llm_latency_sec": 4.0,
            },
        ]

        stats = _proposal_stats_from_events(
            events,
            proposal_json_count=7,
            debug_file_count=1,
        )

        self.assertIsNotNone(stats)
        assert stats is not None
        self.assertEqual(stats["proposal_stats_source"], "scheduler_tasks.jsonl")
        self.assertEqual(stats["proposal_json_count"], 7)
        self.assertEqual(stats["llm_successful_proposal_count"], 2)
        self.assertIsNone(stats["llm_api_call_count"])
        self.assertEqual(stats["llm_model"], "model-a")
        self.assertEqual(stats["mean_llm_latency_sec"], 3.0)
        self.assertEqual(stats["median_llm_latency_sec"], 3.0)
        self.assertIsNone(stats["llm_retry_attempt_count"])
        self.assertFalse(stats["llm_retry_stats_available"])
        self.assertIsNone(stats["llm_total_tokens"])

    def test_returns_none_without_initial_submission_events(self) -> None:
        stats = _proposal_stats_from_events(
            [{"event": "scheduler_start", "llm_model": "model-a"}],
            proposal_json_count=0,
            debug_file_count=0,
        )
        self.assertIsNone(stats)


if __name__ == "__main__":
    unittest.main()
