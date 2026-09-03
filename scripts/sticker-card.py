#!/usr/bin/env python3
"""Dependency-free bootstrap CLI for repository portability cards.

The CLI deliberately inspects files without executing repository code.  It is a
reference implementation of the card format; the format is intended to remain
stable if this CLI is later replaced by a compiled Go or Rust binary.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import sys
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "data" / "agents.json"
SKIP_DIRS = {".git", ".hg", ".svn", "node_modules", ".venv", "venv", "target", "dist", "build", "__pycache__"}
MANIFEST_NAMES = {
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "pyproject.toml",
    "requirements.txt",
    "Pipfile",
    "poetry.lock",
    "go.mod",
    "go.sum",
    "Cargo.toml",
    "Cargo.lock",
    "Gemfile",
    "pom.xml",
    "build.gradle",
    "*.csproj",
    "composer.json",
    "Makefile",
}
COMMANDS = {
    "claude-code": ["claude"],
    "hermes": ["hermes"],
    "openclaw": ["openclaw"],
    "opencode": ["opencode"],
    "codex": ["codex"],
    "mistral-vibe": ["vibe"],
    "antigravity": ["agy"],
    "zcode": ["zcode"],
    "dsh": ["dsh"],
}
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bsk-(?:live|proj)-[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{20,}\b"),
]


def load_catalog() -> list[dict[str, Any]]:
    with CATALOG_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)["agents"]


def json_write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def text_write(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def iter_files(root: Path) -> Iterable[Path]:
    """Walk without following symlinks and without reading repository code."""
    for current, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(name for name in dirs if name not in SKIP_DIRS)
        for name in sorted(files):
            path = Path(current) / name
            if path.is_symlink() or not path.is_file():
                continue
            yield path


def relative_files(root: Path) -> list[str]:
    files: list[str] = []
    for path in iter_files(root):
        try:
            files.append(path.relative_to(root).as_posix())
        except ValueError:
            continue
    return files


def safe_name(value: str) -> str:
    result = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return result or "repository"


def inspect_repo(repo: Path) -> dict[str, Any]:
    repo = repo.resolve()
    if not repo.is_dir():
        raise ValueError(f"Repository path is not a directory: {repo}")

    files = relative_files(repo)
    file_set = set(files)
    manifests = sorted(
        path for path in files
        if Path(path).name in MANIFEST_NAMES or Path(path).suffix == ".csproj"
    )
    context_files = sorted(
        path for path in files
        if Path(path).name in {"AGENTS.md", "CLAUDE.md", "GEMINI.md", "CONTEXT.md"}
        or path.startswith(".claude/")
        or path.startswith(".agents/")
        or path.startswith(".vibe/")
    )
    agent_assets = sorted(
        path for path in files
        if path.startswith((".claude/skills/", ".agents/skills/", ".opencode/skills/", ".vibe/skills/"))
        or path.endswith(("plugin.json", "mcp.json", "mcp_config.json"))
    )

    runtimes: list[str] = []
    if {"package.json", "pnpm-lock.yaml", "yarn.lock", "package-lock.json"} & file_set:
        runtimes.append("node")
    if {"pyproject.toml", "requirements.txt", "Pipfile", "poetry.lock"} & file_set:
        runtimes.append("python")
    if "go.mod" in file_set:
        runtimes.append("go")
    if {"Cargo.toml", "Cargo.lock"} & file_set:
        runtimes.append("rust")
    if {"Gemfile"} & file_set:
        runtimes.append("ruby")
    if {"pom.xml", "build.gradle"} & file_set:
        runtimes.append("jvm")
    if "Makefile" in file_set or any(path.endswith((".sh", ".bash")) for path in files):
        runtimes.append("shell")
    if any(path.endswith((".csproj", ".sln")) for path in files):
        runtimes.append("dotnet")
    if not runtimes:
        runtimes.append("unknown")

    warnings: list[str] = []
    if "README.md" not in file_set and "README" not in file_set:
        warnings.append("No README file detected")
    if not manifests:
        warnings.append("No common package or build manifest detected")
    if not context_files:
        warnings.append("No agent context file detected")

    agents = {
        item["id"]: {
            "support_level": item["support_level"],
            "installable": item["installable"],
            "evidence": "catalogued",
        }
        for item in load_catalog()
    }
    return {
        "schema_version": "0.1.0",
        "source": {
            "name": repo.name,
            "path_kind": "local-repository",
            "readme": "README.md" in file_set or "README" in file_set,
            "git": (repo / ".git").exists(),
        },
        "runtimes": sorted(set(runtimes)),
        "package_manifests": manifests,
        "context_files": context_files,
        "existing_agent_assets": agent_assets,
        "agents": agents,
        "security": {
            "secrets_copied": False,
            "execution_during_inspection": False,
            "default_action": "confirm",
        },
        "warnings": warnings,
    }


def make_skill(source_name: str) -> str:
    return f"""---
name: sticker-card
description: Inspect and adapt the {source_name} repository for portable AI-agent use. Detect runtimes and conventions, generate compatibility metadata and host projections, then validate everything before installation. Use for repository portability, Agent Skills, Claude Code, Codex, ChatGPT, Hermes, OpenClaw, OpenCode, Mistral Vibe, Antigravity, ZCode, DSH, or Arena handoff tasks.
license: MIT
compatibility: Core mode requires only file access; optional scripts, MCP servers and native plugins require their host-specific setup.
metadata:
  project: sticker-card
  source_repository: {safe_name(source_name)}
  security: confirmation-required
---

# Portable repository adaptation

## Rules

1. Inspect before execution. Do not run project code during repository inspection.
2. Read `sticker-card.json` and classify each target using its support level.
3. Keep `AGENTS.md` as project context and keep this skill focused on the repeatable workflow.
4. Generate host files only through the converter; never hand-edit generated projections.
5. Do not copy `.env`, private keys, tokens or machine-specific credentials.
6. Show an installation plan before writing to a user or project destination.
7. Require explicit confirmation for execution, external writes, MCP activation, push or publication.

## Outputs

Produce a deterministic card, a portable `SKILL.md`, host adapter notes and a validation report. If the target is a cloud or conversation surface, provide a handoff instead of pretending to install local files.
"""


def adapter_text(agent: dict[str, Any], source_name: str) -> str:
    project = agent.get("project_skill_path") or "handoff only"
    user = agent.get("user_skill_path") or "not applicable"
    native = agent.get("native_package") or "none documented"
    mcp = agent.get("mcp") or "none"
    if agent["kind"] == "cloud-handoff":
        action = "Use the generated package, connect the repository or import the skill through the product UI. Do not attempt a local filesystem install."
    else:
        action = f"Default project destination: `{project}/sticker-card/`. The CLI prints a plan and requires `--apply` before copying."
    return f"""# {agent['label']}

- **Support level**: `{agent['support_level']}`
- **Project skill path**: `{project}`
- **User skill path**: `{user}`
- **Native package surface**: `{native}`
- **MCP surface**: `{mcp}`
- **Installable locally**: `{str(agent['installable']).lower()}`

## Adapter note

{agent['notes']}

## Safe workflow

1. Review `sticker-card.json` and this adapter note.
2. Review the host's permissions and trust prompt.
3. Use `sticker-card install ... --agent {agent['id']}` to print a plan.
4. Apply only after explicit confirmation with `--apply` and an explicit destination when needed.

{action}

The portable skill remains the source of behavior. This file documents only host-specific paths, permissions and limitations.
"""


def build_package(repo: Path, out_dir: Path, force: bool = False) -> Path:
    repo = repo.resolve()
    card = inspect_repo(repo)
    package = out_dir.resolve() / safe_name(repo.name)
    if package.exists():
        if not force:
            raise ValueError(f"Output already exists: {package} (use --force to replace it)")
        shutil.rmtree(package)
    package.mkdir(parents=True)

    json_write(package / "sticker-card.json", card)
    json_write(package / "compatibility.json", {"schema_version": "0.1.0", "agents": load_catalog()})
    json_write(
        package / "plugin.json",
        {
            "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
            "name": "sticker-card",
            "version": "0.1.0",
            "description": f"Portable agent adaptation package for {repo.name}.",
        },
    )
    json_write(
        package / ".claude-plugin" / "plugin.json",
        {
            "name": "sticker-card",
            "version": "0.1.0",
            "description": "Portable repository adaptation workflow for Claude Code.",
            "skills": "./skills/",
        },
    )
    json_write(
        package / ".codex-plugin" / "plugin.json",
        {
            "name": "sticker-card",
            "version": "0.1.0",
            "description": "Portable repository adaptation workflow for Codex and ChatGPT.",
            "skills": "./skills/",
        },
    )

    skill = make_skill(repo.name)
    text_write(package / "skills" / "sticker-card" / "SKILL.md", skill)
    text_write(package / ".agents" / "skills" / "sticker-card" / "SKILL.md", skill)
    text_write(package / ".claude" / "skills" / "sticker-card" / "SKILL.md", skill)
    text_write(
        package / "AGENTS.md",
        f"""# AGENTS.md

This package adapts the `{repo.name}` repository for AI-agent portability.

- Read `sticker-card.json` before selecting an adapter.
- Use the portable skill under `skills/sticker-card/`.
- Treat `.agents/skills/` and `.claude/skills/` as generated projections.
- Do not execute source code during inspection.
- Do not copy secrets or apply an install without explicit confirmation.
- Validate with `python3 scripts/sticker-card.py validate .` when the bootstrap CLI is available.
""",
    )
    text_write(package / "CLAUDE.md", "@AGENTS.md\n\nClaude-specific additions belong in the Claude adapter documentation.\n")
    text_write(package / "GEMINI.md", "@AGENTS.md\n\nUse .agents/skills for the portable skill projection.\n")
    for agent in load_catalog():
        text_write(package / "adapters" / agent["id"] / "README.md", adapter_text(agent, repo.name))
    text_write(
        package / "README.md",
        f"""# Portable package: {repo.name}

Generated by `sticker-card` without executing the source repository.

- Read `sticker-card.json` for the deterministic inspection card.
- Read `compatibility.json` for the host catalog.
- Read `adapters/` for host-specific instructions.
- Run the validator before any install.
- Use `--apply` only after reviewing the plan.

The generated package intentionally does not include project secrets or a required MCP server.
""",
    )
    return package


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md must start with YAML frontmatter")
    try:
        end = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValueError("SKILL.md frontmatter is not closed") from exc
    values: dict[str, str] = {}
    for line in lines[1:end]:
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.+)$", line)
        if match:
            values[match.group(1)] = match.group(2).strip().strip("'\"")
    if not values.get("name") or not values.get("description"):
        raise ValueError("SKILL.md frontmatter requires name and description")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", values["name"]):
        raise ValueError("SKILL.md name must be lowercase kebab-case")
    if len(values["name"]) > 64 or len(values["description"]) > 1024:
        raise ValueError("SKILL.md name or description exceeds the Agent Skills limit")
    return values


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def find_secrets(root: Path) -> list[str]:
    findings: list[str] = []
    for path in iter_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                findings.append(path.relative_to(root).as_posix())
                break
    return sorted(set(findings))


def validate_package(path: Path) -> list[str]:
    path = path.resolve()
    errors: list[str] = []
    if not path.is_dir():
        return [f"Not a directory: {path}"]

    card_path = path / "sticker-card.json"
    if card_path.exists():
        try:
            card = json.loads(card_path.read_text(encoding="utf-8"))
            for key in ("schema_version", "source", "runtimes", "package_manifests", "agents", "security"):
                if key not in card:
                    errors.append(f"sticker-card.json missing key: {key}")
            if card.get("security", {}).get("secrets_copied") is not False:
                errors.append("security.secrets_copied must be false")
            if card.get("security", {}).get("execution_during_inspection") is not False:
                errors.append("security.execution_during_inspection must be false")
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"Invalid sticker-card.json: {exc}")

    skill_paths = [
        path / "skills" / "sticker-card" / "SKILL.md",
        path / ".agents" / "skills" / "sticker-card" / "SKILL.md",
        path / ".claude" / "skills" / "sticker-card" / "SKILL.md",
    ]
    hashes: list[str] = []
    for skill_path in skill_paths:
        if not skill_path.is_file():
            errors.append(f"Missing skill projection: {skill_path.relative_to(path)}")
            continue
        try:
            parse_frontmatter(skill_path.read_text(encoding="utf-8"))
            hashes.append(file_hash(skill_path))
        except (OSError, ValueError) as exc:
            errors.append(f"Invalid {skill_path.relative_to(path)}: {exc}")
    if hashes and len(set(hashes)) != 1:
        errors.append("Skill projections have different hashes")

    for manifest in (path / "plugin.json", path / ".claude-plugin" / "plugin.json", path / ".codex-plugin" / "plugin.json"):
        if not manifest.is_file():
            errors.append(f"Missing plugin manifest: {manifest.relative_to(path)}")
            continue
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
            if not data.get("name"):
                errors.append(f"Plugin manifest has no name: {manifest.relative_to(path)}")
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"Invalid plugin manifest {manifest.relative_to(path)}: {exc}")

    if card_path.exists():
        try:
            catalog = json.loads((path / "compatibility.json").read_text(encoding="utf-8"))["agents"]
            for agent in catalog:
                adapter = path / "adapters" / agent["id"] / "README.md"
                if not adapter.is_file():
                    errors.append(f"Missing adapter documentation: adapters/{agent['id']}/README.md")
        except (OSError, KeyError, json.JSONDecodeError) as exc:
            errors.append(f"Invalid compatibility.json: {exc}")

    for finding in find_secrets(path):
        errors.append(f"Possible secret detected: {finding}")
    return errors


def print_plan(package: Path, agent: dict[str, Any], scope: str, target: Path, apply: bool, force: bool) -> int:
    if agent["kind"] == "cloud-handoff" or not agent.get("installable"):
        print(f"Handoff required for {agent['label']}; no local filesystem installation will be attempted.")
        print(f"Review: {package / 'adapters' / agent['id'] / 'README.md'}")
        return 0

    if scope == "project":
        relative = agent.get("project_skill_path")
        destination = target / relative / "sticker-card"
    else:
        relative = (agent.get("user_skill_path") or "").replace("~/", "")
        if not relative:
            print(f"{agent['label']} has no documented user-level skill path; use project scope or handoff.", file=sys.stderr)
            return 2
        destination = target / relative / "sticker-card"

    source = package / "skills" / "sticker-card"
    print(f"Agent:       {agent['label']} ({agent['id']})")
    print(f"Scope:       {scope}")
    print(f"Source:      {source}")
    print(f"Destination: {destination}")
    print(f"Files:       {len(list(iter_files(source)))}")
    print(f"Mode:        {'APPLY' if apply else 'PLAN ONLY'}")
    if destination.exists() and not force:
        print("Result:      blocked because destination exists; add --force after review", file=sys.stderr)
        return 2
    if not apply:
        print("No files changed. Re-run with --apply after explicit review.")
        return 0
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination, dirs_exist_ok=force)
    print("Applied:     portable skill copied; no dependency installation or command execution performed.")
    return 0


def command_inspect(args: argparse.Namespace) -> int:
    try:
        report = inspect_repo(Path(args.repo))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"Repository: {report['source']['name']}")
        print(f"Runtimes:   {', '.join(report['runtimes'])}")
        print(f"Manifests:  {len(report['package_manifests'])}")
        print(f"Contexts:   {len(report['context_files'])}")
        print(f"Agent assets:{len(report['existing_agent_assets'])}")
        for warning in report["warnings"]:
            print(f"Warning:    {warning}")
    return 0


def command_build(args: argparse.Namespace) -> int:
    try:
        package = build_package(Path(args.repo), Path(args.out), args.force)
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(f"Built: {package}")
    print("Next:  validate the package before installation.")
    return 0


def command_validate(args: argparse.Namespace) -> int:
    errors = validate_package(Path(args.path))
    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        return 1
    print("VALID")
    return 0


def command_list_agents(args: argparse.Namespace) -> int:
    catalog = load_catalog()
    if args.json:
        print(json.dumps(catalog, indent=2, ensure_ascii=False))
        return 0
    for agent in catalog:
        print(f"{agent['id']:<24} {agent['support_level']:<12} {agent['label']}")
    return 0


def command_doctor(args: argparse.Namespace) -> int:
    report = inspect_repo(Path(args.repo))
    tools = sorted({command for commands in COMMANDS.values() for command in commands} | {"git", "python3", "node", "npm", "uv", "bun", "pnpm"})
    installed = {tool: shutil.which(tool) for tool in tools}
    result = {
        "platform": platform.platform(),
        "python": sys.version.split()[0],
        "runtimes_detected": report["runtimes"],
        "commands": installed,
        "agents": {
            agent["id"]: {"detected": any(installed.get(command) for command in COMMANDS.get(agent["id"], []))}
            for agent in load_catalog()
        },
    }
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Platform: {result['platform']}")
        print(f"Python:   {result['python']}")
        print(f"Runtimes: {', '.join(result['runtimes_detected'])}")
        print("Detected agent commands:")
        for agent_id, data in result["agents"].items():
            print(f"  {agent_id:<24} {'yes' if data['detected'] else 'no'}")
        print("No dependency was installed and no command was executed.")
    return 0


def command_install(args: argparse.Namespace) -> int:
    catalog = {agent["id"]: agent for agent in load_catalog()}
    if args.agent not in catalog:
        print(f"Unknown agent: {args.agent}. Use list-agents.", file=sys.stderr)
        return 2
    package = Path(args.package).resolve()
    errors = validate_package(package)
    if errors:
        print("Refusing to install an invalid package:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    target = Path(args.target).resolve() if args.target else (Path.cwd().resolve() if args.scope == "project" else Path.home().resolve())
    return print_plan(package, catalog[args.agent], args.scope, target, args.apply, args.force)


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="sticker-card", description="Inspect and adapt repositories for portable AI agents.")
    sub = root.add_subparsers(dest="command", required=True)

    inspect_parser = sub.add_parser("inspect", help="Read-only repository inspection")
    inspect_parser.add_argument("repo", nargs="?", default=".")
    inspect_parser.add_argument("--json", action="store_true")
    inspect_parser.set_defaults(function=command_inspect)

    build_parser = sub.add_parser("build", help="Generate a portable package")
    build_parser.add_argument("repo", nargs="?", default=".")
    build_parser.add_argument("--out", default="./dist")
    build_parser.add_argument("--force", action="store_true")
    build_parser.set_defaults(function=command_build)

    validate_parser = sub.add_parser("validate", help="Validate source or generated package")
    validate_parser.add_argument("path", nargs="?", default=".")
    validate_parser.set_defaults(function=command_validate)

    list_parser = sub.add_parser("list-agents", help="List catalogued agents")
    list_parser.add_argument("--json", action="store_true")
    list_parser.set_defaults(function=command_list_agents)

    doctor_parser = sub.add_parser("doctor", help="Detect optional local tools without executing them")
    doctor_parser.add_argument("repo", nargs="?", default=".")
    doctor_parser.add_argument("--json", action="store_true")
    doctor_parser.set_defaults(function=command_doctor)

    install_parser = sub.add_parser("install", help="Plan or apply a skill projection")
    install_parser.add_argument("package")
    install_parser.add_argument("--agent", required=True)
    install_parser.add_argument("--scope", choices=("project", "user"), default="project")
    install_parser.add_argument("--target", help="Explicit project root or synthetic home directory")
    install_parser.add_argument("--apply", action="store_true", help="Apply the reviewed plan")
    install_parser.add_argument("--force", action="store_true", help="Replace an existing skill destination")
    install_parser.set_defaults(function=command_install)
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    return int(args.function(args))


if __name__ == "__main__":
    raise SystemExit(main())
