import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "bootstrap_evalsmith.py"


class BootstrapEvalSmithTests(unittest.TestCase):
    def run_script(self, target_dir: Path, *extra_args: str) -> subprocess.CompletedProcess[str]:
        command = [
            sys.executable,
            str(SCRIPT_PATH),
            str(target_dir),
            *extra_args,
        ]
        return subprocess.run(
            command,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )

    def test_bootstrap_creates_expected_layout(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            target_dir = Path(tmpdir) / "sample-repo"

            result = self.run_script(
                target_dir,
                "--feature-name",
                "Customer Support Copilot",
                "--workflow-type",
                "rag",
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)

            slug = "customer-support-copilot"
            expected_paths = [
                target_dir / "evals" / "workflows" / f"{slug}.md",
                target_dir / "evals" / "specs" / f"{slug}.yaml",
                target_dir / "evals" / "cases" / slug / "cases.jsonl",
                target_dir / "evals" / "rubrics" / f"{slug}.md",
                target_dir / "evals" / "components" / f"{slug}.yaml",
                target_dir / "evals" / "experiments" / slug / "ablation-plan.yaml",
                target_dir / "evals" / "forensics" / f"{slug}.md",
                target_dir / "evals" / "traces" / slug / ".gitkeep",
                target_dir / "evals" / "reports" / ".gitkeep",
                target_dir / "evals" / "runs" / ".gitkeep",
            ]

            for path in expected_paths:
                self.assertTrue(path.exists(), msg=f"expected {path} to exist")

            spec_text = (target_dir / "evals" / "specs" / f"{slug}.yaml").read_text()
            self.assertIn("feature_name: Customer Support Copilot", spec_text)
            self.assertIn("workflow_type: rag", spec_text)
            self.assertIn("trace_capture:", spec_text)
            self.assertIn("forensic_analysis:", spec_text)
            self.assertIn("component_inventory_file:", spec_text)

            components_text = (target_dir / "evals" / "components" / f"{slug}.yaml").read_text()
            self.assertIn("system_prompt_components:", components_text)
            self.assertIn("context_sources:", components_text)

            forensic_text = (target_dir / "evals" / "forensics" / f"{slug}.md").read_text()
            self.assertIn("Component Influence Ledger", forensic_text)
            self.assertIn("Counterfactual Or Ablation Evidence", forensic_text)

    def test_bootstrap_refuses_to_overwrite_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            target_dir = Path(tmpdir) / "sample-repo"

            first_run = self.run_script(
                target_dir,
                "--feature-name",
                "Structured Extractor",
                "--workflow-type",
                "structured-output",
            )
            self.assertEqual(first_run.returncode, 0, msg=first_run.stderr)

            second_run = self.run_script(
                target_dir,
                "--feature-name",
                "Structured Extractor",
                "--workflow-type",
                "structured-output",
            )

            self.assertNotEqual(second_run.returncode, 0)
            self.assertIn("already exist", second_run.stderr)


if __name__ == "__main__":
    unittest.main()
