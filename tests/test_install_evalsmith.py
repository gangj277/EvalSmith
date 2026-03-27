import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALL_SCRIPT = REPO_ROOT / "scripts" / "install_evalsmith.py"
CANONICAL_SKILL_DIR = REPO_ROOT / "skills" / "evalsmith"


class InstallEvalSmithTests(unittest.TestCase):
    def run_install(self, *args: str) -> subprocess.CompletedProcess[str]:
        command = [sys.executable, str(INSTALL_SCRIPT), *args]
        return subprocess.run(
            command,
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
        )

    def test_canonical_skill_directory_exists(self) -> None:
        self.assertTrue(CANONICAL_SKILL_DIR.exists(), msg="expected skills/evalsmith to exist")
        self.assertTrue((CANONICAL_SKILL_DIR / "SKILL.md").exists(), msg="expected packaged skill SKILL.md")
        self.assertTrue((CANONICAL_SKILL_DIR / "agents" / "openai.yaml").exists())
        self.assertTrue((CANONICAL_SKILL_DIR / "references").exists())
        self.assertTrue((CANONICAL_SKILL_DIR / "scripts" / "bootstrap_evalsmith.py").exists())

    def test_installs_to_codex_destination(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = self.run_install(
                "--target",
                "codex",
                "--dest-base",
                tmpdir,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            installed = Path(tmpdir) / ".codex" / "skills" / "evalsmith"
            self.assertTrue((installed / "SKILL.md").exists())
            self.assertTrue((installed / "agents" / "openai.yaml").exists())

    def test_installs_to_claude_destination(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = self.run_install(
                "--target",
                "claude",
                "--dest-base",
                tmpdir,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            installed = Path(tmpdir) / ".claude" / "skills" / "evalsmith"
            self.assertTrue((installed / "SKILL.md").exists())
            self.assertTrue((installed / "references" / "forensic-analysis.md").exists())

    def test_refuses_to_overwrite_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            first = self.run_install("--target", "codex", "--dest-base", tmpdir)
            self.assertEqual(first.returncode, 0, msg=first.stderr)

            second = self.run_install("--target", "codex", "--dest-base", tmpdir)
            self.assertNotEqual(second.returncode, 0)
            self.assertIn("already exists", second.stderr)


if __name__ == "__main__":
    unittest.main()
