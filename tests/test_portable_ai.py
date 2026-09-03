from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "portable-ai.py"


def run_cli(*args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )


class PortableAITests(unittest.TestCase):
    def test_public_compatibility_test_kit_is_present(self) -> None:
        instructions = ROOT / "tests" / "README.md"
        template = ROOT / "tests" / "compatibility-report-template.md"
        self.assertTrue(instructions.is_file())
        self.assertTrue(template.is_file())
        instruction_text = instructions.read_text(encoding="utf-8")
        template_text = template.read_text(encoding="utf-8")
        self.assertIn("Prompt prêt à copier", instruction_text)
        self.assertIn("portable-ai-public", instruction_text)
        self.assertIn("Bloc prêt à reporter", template_text)
        self.assertIn("generic-agent-skills", template_text)
        self.assertIn("TBD", template_text)

    def test_source_is_valid(self) -> None:
        result = run_cli("validate", ".")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("VALID", result.stdout)

    def test_inspection_does_not_execute_source(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            (repo / "README.md").write_text("# fixture\n", encoding="utf-8")
            (repo / "setup.py").write_text(
                "raise RuntimeError('inspection executed this file')\n", encoding="utf-8"
            )
            result = run_cli("inspect", str(repo), "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn("inspection executed", result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["source"]["name"], repo.name)

    def test_build_validate_and_plan_install(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "source-repo"
            output = Path(directory) / "out"
            repo.mkdir()
            (repo / "README.md").write_text("# source\n", encoding="utf-8")
            (repo / "package.json").write_text('{"name":"source-repo"}\n', encoding="utf-8")

            build = run_cli("build", str(repo), "--out", str(output))
            self.assertEqual(build.returncode, 0, build.stdout + build.stderr)
            package = output / "source-repo"
            validate = run_cli("validate", str(package))
            self.assertEqual(validate.returncode, 0, validate.stdout + validate.stderr)

            target = Path(directory) / "target"
            target.mkdir()
            plan = run_cli(
                "install",
                str(package),
                "--agent",
                "codex",
                "--scope",
                "project",
                "--target",
                str(target),
            )
            self.assertEqual(plan.returncode, 0, plan.stdout + plan.stderr)
            self.assertIn("PLAN ONLY", plan.stdout)
            self.assertFalse((target / ".agents").exists())

            apply = run_cli(
                "install",
                str(package),
                "--agent",
                "codex",
                "--scope",
                "project",
                "--target",
                str(target),
                "--apply",
            )
            self.assertEqual(apply.returncode, 0, apply.stdout + apply.stderr)
            self.assertTrue((target / ".agents/skills/portable-ai/SKILL.md").is_file())

    def test_handoff_never_writes_local_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory) / "package"
            package.mkdir()
            # A valid generated package is easiest to obtain from this repository.
            output = Path(directory) / "out"
            build = run_cli("build", ".", "--out", str(output))
            self.assertEqual(build.returncode, 0, build.stdout + build.stderr)
            package = output / "portable-ai"
            target = Path(directory) / "target"
            result = run_cli(
                "install",
                str(package),
                "--agent",
                "arena-agent-mode",
                "--scope",
                "project",
                "--target",
                str(target),
                "--apply",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Handoff required", result.stdout)
            self.assertFalse(target.exists())

    def test_possible_private_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "repo"
            output = Path(directory) / "out"
            repo.mkdir()
            (repo / "README.md").write_text("# source\n", encoding="utf-8")
            build = run_cli("build", str(repo), "--out", str(output))
            self.assertEqual(build.returncode, 0, build.stdout + build.stderr)
            package = output / "repo"
            (package / "leak.txt").write_text(
                "-----BEGIN " + "PRIVATE KEY-----\nnot-a-real-key\n", encoding="utf-8"
            )
            validate = run_cli("validate", str(package))
            self.assertNotEqual(validate.returncode, 0)
            self.assertIn("Possible secret", validate.stdout)


if __name__ == "__main__":
    unittest.main()
