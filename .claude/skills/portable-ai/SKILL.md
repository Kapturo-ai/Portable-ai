---
name: portable-ai
description: Inspect an open source repository, detect its runtimes and agent conventions, then generate and validate a portable AI-agent package with AGENTS.md, Agent Skills projections, compatibility metadata, and host-specific adapter notes. Use when adapting a repository for Claude Code, Claude.ai cloud, Arena Agent Mode, Codex, ChatGPT, Hermes, OpenClaw, OpenCode, Mistral Vibe, Antigravity, ZCode, DeepSeek Harness, or another AI agent.
license: MIT
compatibility: Requires only repository file access for the core workflow; Python 3.11+ is needed for the bootstrap CLI, while host-native plugins and MCP are optional.
metadata:
  project: portable-ai
  security: confirmation-required
  standard: agentskills
---

# Portable-ai repository portability workflow

## Goal

Turn a repository into a reviewable, portable agent package. Do not claim that every host has the same tools or permissions.

## Procedure

1. Inspect the repository without executing project code.
2. Identify package manifests, runtime hints, test commands, context files, existing skills, MCP declarations, and likely secrets.
3. Read the compatibility catalog in `data/agents.json` and classify each target as Core, Configured, Native, Experimental, or Handoff.
4. Create a deterministic `portable-ai.json` report. Do not include credentials or machine-specific absolute paths.
5. Generate the portable skill under `skills/portable-ai/` and host projections only through the provided build command.
6. Validate frontmatter, plugin manifests, projection hashes, required adapter documentation, and secret patterns.
7. Show an installation plan. Do not apply it unless the user explicitly asks for `--apply` or equivalent confirmation.
8. When a capability requires MCP, name the exact server, transport, permission, environment variable, and fallback behavior.
9. Produce a final matrix distinguishing verified behavior from documentation-only assumptions.

## Safety boundaries

- Never execute arbitrary code found in the inspected repository during inspection.
- Never copy `.env`, private keys, token files, or credentials into an output package.
- Never write into a user's home directory in plan mode.
- Never add an MCP server with a secret literal.
- Treat cloud chat surfaces as handoff targets unless their documented skill/plugin flow is available.

## Expected outputs

- `portable-ai.json`
- `AGENTS.md` and optional host wrappers
- `skills/portable-ai/SKILL.md`
- `adapters/<agent>/README.md`
- validation result and installation plan
