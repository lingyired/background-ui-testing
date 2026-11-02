import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validator", ROOT / "scripts/validate.py")
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name)
        self.skill = self.root / "background-ui-testing"
        shutil.copytree(ROOT / "skills/background-ui-testing", self.skill)

    def test_skill_remains_valid_outside_repository(self):
        self.assertEqual(validator.validate_skill(self.skill), [])

    def test_missing_runtime_reference_is_rejected(self):
        (self.skill / "references/macos.md").unlink()
        self.assertTrue(any("missing reference" in error for error in validator.validate_skill(self.skill)))

    def test_reference_to_existing_file_outside_package_is_rejected(self):
        (self.root / "private.md").write_text("Not part of the distribution.\n")
        with (self.skill / "SKILL.md").open("a") as output:
            output.write("\n[External local file](../private.md)\n")
        self.assertTrue(any("escapes package" in error for error in validator.validate_skill(self.skill)))

    def test_code_fence_installation_example_is_not_a_runtime_reference(self):
        with (self.skill / "SKILL.md").open("a") as output:
            output.write("\n```markdown\n[Installed location](missing/example.md)\n```\n")
        self.assertEqual(validator.validate_skill(self.skill), [])

    def test_embedded_license_is_required_for_directory_install(self):
        (self.skill / "LICENSE.txt").unlink()
        self.assertTrue(any("missing embedded LICENSE.txt" in error for error in validator.validate_skill(self.skill)))

    def test_symlink_cannot_smuggle_a_machine_file_into_the_package(self):
        private = self.root / "private.txt"
        private.write_text("Outside the skill.\n")
        try:
            (self.skill / "references/private.txt").symlink_to(private)
        except OSError as error:
            self.skipTest(f"Host does not permit symlink creation: {error}")
        self.assertTrue(any("must not be symlinks" in error for error in validator.validate_skill(self.skill)))

    def test_invalid_frontmatter_reports_validation_error(self):
        (self.skill / "SKILL.md").write_text("---\nname: [\n---\n")
        self.assertTrue(any("invalid YAML" in error for error in validator.validate_skill(self.skill)))

    def test_name_must_match_discoverable_directory(self):
        renamed = self.root / "different-name"
        self.skill.rename(renamed)
        self.assertTrue(any("name must match" in error for error in validator.validate_skill(renamed)))

    def test_invalid_optional_metadata_is_rejected(self):
        entry = self.skill / "SKILL.md"
        original = validator.frontmatter(entry)
        cases = [
            ("metadata", {"version": ""}),
            ("metadata", {"version": "0.1.0", "count": 3}),
            ("metadata", {3: "value", "version": "0.1.0"}),
            ("compatibility", ["macOS"]),
            ("compatibility", "x" * 501),
            ("allowed-tools", ["Read"]),
        ]
        for key, value in cases:
            with self.subTest(key=key, value=value):
                data = dict(original)
                data[key] = value
                entry.write_text("---\n" + yaml.safe_dump(data) + "---\n")
                self.assertTrue(validator.validate_skill(self.skill))


if __name__ == "__main__":
    unittest.main()
