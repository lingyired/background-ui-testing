"""Validate repository packaging without GUI access or network requests."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml


def frontmatter(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---" or "---" not in lines[1:]:
        raise ValueError(f"{path}: missing YAML frontmatter")
    end = lines.index("---", 1)
    try:
        data = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError as error:
        raise ValueError(f"{path}: invalid YAML: {error}") from error
    if not isinstance(data, dict):
        raise ValueError(f"{path}: frontmatter must be a mapping")
    return data


def local_links(path: Path):
    fenced = False
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if fenced:
            continue
        for target in re.findall(r"!?\[[^\]]*\]\(([^)\s]+)\)", line):
            url = urlsplit(target.strip("<>"))
            if not url.scheme and not url.netloc and url.path:
                yield number, unquote(url.path)


def validate_links(path: Path, boundary: Path) -> list[str]:
    errors = []
    boundary = boundary.resolve()
    for number, target in local_links(path):
        resolved = (path.parent / target).resolve()
        if not resolved.is_relative_to(boundary):
            errors.append(f"{path}:{number}: reference escapes package: {target}")
        elif not resolved.exists():
            errors.append(f"{path}:{number}: missing reference: {target}")
    return errors


def validate_skill(skill: Path) -> list[str]:
    errors = []
    entry = skill / "SKILL.md"
    if not entry.is_file():
        return [f"{entry}: missing skill entrypoint"]
    try:
        data = frontmatter(entry)
    except ValueError as error:
        return [str(error)]
    name = data.get("name")
    if not isinstance(name, str) or not re.fullmatch(
        r"[a-z0-9]+(?:-[a-z0-9]+)*", name
    ) or len(name) > 64 or name != skill.name:
        errors.append(f"{entry}: name must match its folder and naming convention")
    description = data.get("description")
    if not isinstance(description, str) or not 1 <= len(description.strip()) <= 1024:
        errors.append(f"{entry}: description must contain 1..1024 characters")
    if data.get("license") != "Apache-2.0":
        errors.append(f"{entry}: this package must declare Apache-2.0")
    metadata = data.get("metadata")
    if not isinstance(metadata, dict) or any(
        not isinstance(key, str) or not isinstance(value, str)
        for key, value in metadata.items()
    ):
        errors.append(f"{entry}: metadata must map string keys to string values")
    if not isinstance(metadata, dict) or not isinstance(metadata.get("version"), str) or not metadata["version"].strip():
        errors.append(f"{entry}: metadata.version must be a nonempty string")
    if "compatibility" in data and (
        not isinstance(data["compatibility"], str)
        or not 1 <= len(data["compatibility"].strip()) <= 500
    ):
        errors.append(f"{entry}: compatibility must contain 1..500 characters")
    if "allowed-tools" in data and not isinstance(data["allowed-tools"], str):
        errors.append(f"{entry}: allowed-tools must be a space-delimited string")
    if len(entry.read_text(encoding="utf-8").splitlines()) >= 500:
        errors.append(f"{entry}: move detailed guidance into references")
    for filename in ("LICENSE.txt", "NOTICE"):
        if not (skill / filename).is_file():
            errors.append(f"{skill}: missing embedded {filename}")
    for path in skill.rglob("*"):
        if path.is_symlink():
            errors.append(f"{path}: installable files must not be symlinks")
        elif path.is_file() and path.suffix == ".md":
            errors.extend(validate_links(path, skill))
    interface_path = skill / "agents/openai.yaml"
    if interface_path.exists():
        try:
            config = yaml.safe_load(interface_path.read_text(encoding="utf-8"))
            interface = config.get("interface", {}) if isinstance(config, dict) else {}
            short = interface.get("short_description")
            prompt = interface.get("default_prompt")
            if not isinstance(short, str) or not 25 <= len(short) <= 64:
                errors.append(f"{interface_path}: short_description must be 25..64 characters")
            if not isinstance(prompt, str) or f"${name}" not in prompt:
                errors.append(f"{interface_path}: default_prompt must mention ${name}")
        except (yaml.YAMLError, AttributeError) as error:
            errors.append(f"{interface_path}: invalid interface: {error}")
    return errors


def validate_repo(root: Path) -> list[str]:
    errors = []
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    if not skills:
        errors.append(f"{root}: no discoverable skills/*/SKILL.md")
    for entry in skills:
        errors.extend(validate_skill(entry.parent))
    for path in root.glob("*.md"):
        errors.extend(validate_links(path, root))
    for section in ("examples", "evals"):
        for path in (root / section).glob("*.md"):
            errors.extend(validate_links(path, root))
    for filename in ("LICENSE", "NOTICE", "README.md", "CONTRIBUTING.md"):
        if not (root / filename).is_file():
            errors.append(f"{root}: missing repository {filename}")
    scenarios_path = root / "evals/scenarios.yaml"
    try:
        data = yaml.safe_load(scenarios_path.read_text(encoding="utf-8"))
        scenarios = data.get("scenarios", []) if isinstance(data, dict) else []
        if not isinstance(scenarios, list):
            return errors + [f"{scenarios_path}: scenarios must be a list"]
        seen = set()
        for scenario in scenarios:
            identity = scenario.get("id") if isinstance(scenario, dict) else None
            if not isinstance(identity, str) or identity in seen:
                errors.append(f"{scenarios_path}: missing or duplicate scenario id")
            if isinstance(identity, str):
                seen.add(identity)
            for key in ("prompt", "must", "must_not"):
                value = scenario.get(key) if isinstance(scenario, dict) else None
                valid = isinstance(value, str) and bool(value.strip()) if key == "prompt" else (
                    isinstance(value, list)
                    and bool(value)
                    and all(isinstance(item, str) and item.strip() for item in value)
                )
                if not valid:
                    errors.append(f"{scenarios_path}: {identity}: invalid {key}")
        if not scenarios:
            errors.append(f"{scenarios_path}: no decision scenarios")
    except (OSError, yaml.YAMLError) as error:
        errors.append(f"{scenarios_path}: {error}")
    return errors


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    errors = validate_repo(root)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("PASS: skill metadata, portable resources, local links, notices, and decision fixtures")
    print("Scope: static packaging only; no live UI or provider compatibility tested")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
