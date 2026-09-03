# Sources web et hypothèses de compatibilité

Recherche effectuée avec `web_search` natif le 3 septembre 2026. Les pages et fonctionnalités des agents évoluent rapidement ; les adaptateurs doivent être vérifiés par version.

## Standards

- [Agent Skills specification](https://agentskills.io/specification) — format `SKILL.md`, frontmatter, progressive disclosure et répertoires optionnels.
- [Agent Plugins specification v1.0.0](https://github.com/agentplugins/agent-plugins-spec/blob/main/spec/1.0.0.md) — packaging portable de skills et MCP.
- [Agent Plugins future considerations](https://github.com/agentplugins/agent-plugins-spec/blob/main/FUTURE_CONSIDERATIONS.md) — limites actuelles sur confiance, permissions, provenance et secrets.

## Surfaces

- [Arena Agent Mode](https://help.arena.ai/articles/5432423882-how-to-use-agent-mode) — web search, Bash/sandbox, fichiers et flux GitHub.
- [Claude Code skills](https://code.claude.com/docs/en/skills) — skills locales, account skills et sessions cloud.
- [Claude Code extension overview](https://code.claude.com/docs/en/features-overview) — skills, hooks, MCP, subagents et plugins.
- [Codex skills](https://developers.openai.com/codex/skills) — Agent Skills, `.agents/skills`, `agents/openai.yaml`.
- [Codex plugin packaging](https://developers.openai.com/codex/plugins/build/) — `.codex-plugin/plugin.json`, skills, MCP et assets.
- [ChatGPT plugins](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt-and-codex) — plugins, apps, skills et contrôles de workspace.
- [Hermes plugins](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins) — plugins Python, skills et bundles portables.
- [Hermes MCP](https://hermes-agent.nousresearch.com/docs/reference/mcp-config-reference) — serveurs stdio/HTTP et politique de confiance.
- [OpenClaw skills](https://docs.openclaw.ai/tools/skills) — priorité workspace, `.agents/skills` et skills personnels.
- [OpenClaw plugin bundles](https://docs.openclaw.ai/plugins/bundles) — bundles Agent Plugins, Codex, Claude et format natif.
- [OpenCode skills](https://opencode.ai/docs/skills) — chemins `.opencode/skills`, `.claude/skills` et `.agents/skills`.
- [OpenCode MCP](https://opencode.ai/docs/mcp-servers/) — serveurs locaux et distants.
- [Mistral Vibe skills](https://docs.mistral.ai/vibe/code/cli/skills) — Agent Skills, `.vibe/skills`, `.agents/skills` et permissions.
- [Mistral Vibe agents](https://docs.mistral.ai/vibe/code/cli/agents) — agents TOML et `AGENTS.md`.
- [Antigravity plugins et skills](https://antigravity.google/docs/cli/plugins/) — `plugin.json`, rules, hooks, agents et skills.
- [Antigravity MCP](https://antigravity.google/docs/mcp/) — `mcp_config.json`, stdio et serveurs distants.
- [ZCode skills](https://zcode.z.ai/en/docs/skill) — `~/.zcode/skills`, import externe et plugin skill layout.
- [ZCode MCP](https://zcode.z.ai/en/docs/mcp-services) — MCP natif et fallback `.agents/mcp.json`.
- [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) — architecture orientée plugins et dépôt DSH officiel.

## Règle de preuve

Une documentation fournisseur prouve qu’un chemin ou une fonctionnalité est documenté, pas que chaque version locale fonctionne. La matrice doit donc distinguer :

- `documented` : mentionné dans la documentation ;
- `smoke-tested` : vérifié dans un environnement local ou CI ;
- `verified` : testé avec installation, chargement et workflow ;
- `handoff` : transmis à une surface cloud/conversationnelle ;
- `unknown` : aucune preuve suffisante.
