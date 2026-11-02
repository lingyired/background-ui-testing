"""Exercise the documented installer in an owned temporary project."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

from validate import validate_skill


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    npx = shutil.which("npx")
    if not npx:
        raise SystemExit("Node.js 22.20+ and npx are required for the installation check")
    with tempfile.TemporaryDirectory(prefix="background-ui-testing-install-") as folder:
        target = Path(folder)
        subprocess.run(
            ["git", "init", "-b", "main", str(target)],
            check=True, capture_output=True, text=True,
        )
        result = subprocess.run(
            [
                npx, "--yes", "skills@1.7.4", "add", str(root),
                "--skill", "background-ui-testing", "--agent", "codex",
                "--yes", "--copy",
            ],
            cwd=target, capture_output=True, text=True, timeout=120,
        )
        if result.returncode:
            raise SystemExit(result.stdout + result.stderr)
        installed = target / ".agents/skills/background-ui-testing"
        errors = validate_skill(installed)
        if errors:
            raise SystemExit("\n".join(errors))
        source = root / "skills/background-ui-testing"
        expected = {
            path.relative_to(source): path.read_bytes()
            for path in source.rglob("*") if path.is_file()
        }
        actual = {
            path.relative_to(installed): path.read_bytes()
            for path in installed.rglob("*") if path.is_file()
        }
        if actual != expected:
            raise SystemExit("Installation did not preserve the complete skill package")
        print(f"PASS: Skills CLI 1.7.4 installed all {len(actual)} files in an isolated project")
    print("Owned temporary project removed; existing skill installations preserved")


if __name__ == "__main__":
    main()
