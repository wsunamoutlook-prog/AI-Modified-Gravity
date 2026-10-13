"""Release checks for isolated searches; no API calls or theory searches."""
import ast
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import types
import unittest
import sys
from unittest.mock import patch
from reproduction import search

ROOT = Path(__file__).resolve().parents[1]

def policy_module():
    spec = importlib.util.spec_from_file_location("ablation_test_package.ablation_policy", ROOT / "reproduction/ablation_policy.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class RealAblationTests(unittest.TestCase):
    def test_memory_off_removes_all_feedback_without_mutating_logs(self):
        policy = policy_module()
        source = {"total_attempts": 23, "by_family": [{"aic": 10}], "agent_loop": {"joint_prior": "secret"}}
        for arm in ("uniform", "llm_no_memory"):
            with patch.dict(os.environ, REAL_ABLATION_MODE=arm):
                self.assertEqual(policy.learning_feedback(source), {})
        with patch.dict(os.environ, REAL_ABLATION_MODE="adaptive"):
            self.assertIs(policy.learning_feedback(source), source)
        self.assertEqual(source["total_attempts"], 23)

    def test_all_three_sampling_stages_receive_scrubbed_feedback(self):
        policy = policy_module()
        source = (ROOT / "ai_theory_lab/graph_agent_batch.py").read_text()
        revised = policy.patch_batch(source)
        tree = ast.parse(revised)
        functions = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
        proposal = ast.unparse(functions["_generate_slot_entry"])
        scheduler = ast.unparse(functions["_run_async_slot_scheduler"])
        self.assertIn("learning_feedback(raw_summary)", proposal)
        self.assertIn("_under_duplicate_limit(entry, raw_summary)", proposal)
        self.assertIn("expanded_summary = learning_feedback(_load_summary(memory_dir))", scheduler)
        self.assertIn("refine_summary = learning_feedback(_load_summary(memory_dir))", scheduler)
        self.assertIn("final_summary = _load_summary(memory_dir)", revised)
        self.assertEqual((ROOT / "ai_theory_lab/graph_agent_batch.py").read_text(), source)
        with self.assertRaises(ValueError):
            policy.patch_batch(revised)

    def test_non_llm_selectors_do_not_call_api_and_uniform_ignores_rewards(self):
        policy = policy_module()
        package = types.ModuleType("ablation_test_package")
        package.__path__ = []
        cold = types.ModuleType("ablation_test_package.cold_start_runner")
        cold.DIRECT_MIN_OPERATOR_TERMS, cold.DIRECT_MAX_OPERATOR_TERMS = 1, 2
        cold._candidate_allowed_for_scalar_config = lambda c, s: True
        cold._candidate_sort_key = lambda c: c
        cold._potential_options_for_scalar_config = lambda s: [{"phi1": "quadratic", "phi2": None}]
        cold._entry_skeleton = lambda **k: {**k, "_candidate_objects": k["candidates"]}
        cold._direct_entry = lambda **k: {**k, "operators": k["candidates"]}
        cold.theory_track_from_operators = lambda x: "test_fixture"
        llm = types.ModuleType("ablation_test_package.llm_agent")
        llm._generate_candidate_entries = lambda *a, **k: [
            {"scalar_config": "phi1_only", "potential_types": {}, "_candidate_objects": ["first"], "local_number": 1},
            {"scalar_config": "phi1_only", "potential_types": {}, "_candidate_objects": ["second"], "local_number": 2}]
        llm._call_llm_for_choice = lambda **k: self.fail("Non-LLM selector called an API")
        modules = {package.__name__: package, cold.__name__: cold, llm.__name__: llm}
        kwargs = {"context": {"tensors": {}, "masker": types.SimpleNamespace(all_candidates=["A", "B", "R"])},
                  "seed": 17, "scalar_config": "phi1_only", "rng": None, "summary": {"best_aic": -999}}
        with patch.dict(sys.modules, modules):
            with patch.dict(os.environ, REAL_ABLATION_MODE="adaptive"):
                selected = policy.choose_entry(**kwargs)
                self.assertEqual(selected["operators"], ["first"])
                self.assertIsNone(selected["llm_provider"])
            with patch.dict(os.environ, REAL_ABLATION_MODE="uniform"):
                first = policy.choose_entry(**kwargs)
                second = policy.choose_entry(**{**kwargs, "summary": {"best_aic": 999}})
                self.assertEqual(first, second)
                self.assertFalse(first["baseline_control"])

    def arguments(self, directory, mode="random"):
        return types.SimpleNamespace(output_dir=directory, mode=mode, parents=2, workers=1,
            seed=20260607, mock_seed=20260908, provider="openai", model="test-model",
            api_key_env="OPENAI_API_KEY", base_url=None)

    def test_isolated_snapshot_is_clean_and_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp) / "random"
            original = (ROOT / "ai_theory_lab/graph_agent_batch.py").read_bytes()
            p = search.prepare(self.arguments(directory))
            work = directory / "workspace"
            self.assertFalse((work / "ai_theory_lab/memory").exists())
            self.assertFalse((work / "ai_theory_lab/cache").exists())
            self.assertFalse((work / "solver_result").exists())
            self.assertEqual((ROOT / "ai_theory_lab/graph_agent_batch.py").read_bytes(), original)
            self.assertIn("learning_feedback(raw_summary)", (work / "ai_theory_lab/graph_agent_batch.py").read_text())
            self.assertEqual(search.sha256(work / search.DATA[0]), search.sha256(ROOT / search.DATA[0]))
            with self.assertRaises(FileExistsError):
                search.prepare(self.arguments(directory))
            with patch.dict(os.environ, OPENAI_API_KEY="TEST_ONLY", SN_DIR="/MOCK/SN", PYTHONPATH="/old/memory"):
                env = search.runtime_env(p, directory)
            self.assertNotIn("OPENAI_API_KEY", env)
            self.assertEqual(env["SN_DIR"], str(work / "data/SN data"))
            self.assertEqual(env["REAL_ABLATION_MODE"], "uniform")
            self.assertIn("deterministic", search.search_command(p))
            (work / search.DATA[0]).write_text("changed")
            with self.assertRaisesRegex(ValueError, "Snapshot changed"):
                search.run(directory)
            self.assertFalse((directory / "search_status.json").exists())

    def test_real_mock_destinations_cannot_be_confused(self):
        with tempfile.TemporaryDirectory() as tmp:
            for dirname, mode in (("MOCK_bad", "random"), ("real_bad", "mock")):
                with self.assertRaises(ValueError):
                    search.prepare(self.arguments(Path(tmp) / dirname, mode))
            p = dict(mode="mock", workers=8, api_key_env="OPENAI_API_KEY")
            env = search.runtime_env(p, Path(tmp) / "MOCK_unit")
            self.assertTrue(env["SN_DIR"].endswith("MOCK_DATA_001/SN"))
            self.assertTrue(env["BAO_DIR"].endswith("MOCK_DATA_001/BAO"))

    def test_memory_on_preserves_original_source_and_requires_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp) / "memory_on"
            search.prepare(self.arguments(directory, "memory-on"))
            self.assertEqual(search.sha256(directory / "workspace/ai_theory_lab/graph_agent_batch.py"),
                             search.sha256(ROOT / "ai_theory_lab/graph_agent_batch.py"))
            with patch.dict(os.environ, {}, clear=True):
                with self.assertRaisesRegex(ValueError, "OPENAI_API_KEY"):
                    search.run(directory)
            self.assertFalse((directory / "search_status.json").exists())

if __name__ == "__main__":
    unittest.main()
