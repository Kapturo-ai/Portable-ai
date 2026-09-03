# Matrice de compatibilité initiale

`documented` ne signifie pas `verified`. La première matrice décrit les chemins visés ; les tests de smoke feront évoluer la preuve.

| Agent | Core | Skill path | Plugin/MCP natif | Surface | Niveau initial |
|---|---|---|---|---|---|
| Arena Agent Mode | oui | handoff | non documenté | cloud | handoff |
| Claude.ai / cloud | oui | `.claude/skills` ou compte | connectors | cloud | configured |
| Claude Code | oui | `.claude/skills` | `.claude-plugin`, `.mcp.json` | local | native |
| Hermes | oui | `.agents/skills` | plugin Python, MCP | local | native |
| OpenClaw | oui | `skills`, `.agents/skills` | plugin natif / bundle | local | native |
| OpenCode | oui | `.opencode`, `.claude`, `.agents` | `opencode.json`, plugins | local | native |
| Codex | oui | `.agents/skills` | `.codex-plugin`, MCP | local/cloud desktop | native |
| ChatGPT Work | oui | plugin/skill | apps, remote MCP | cloud | configured |
| Mistral Vibe | oui | `.vibe`, `.agents` | agents TOML, MCP | local | native |
| Antigravity | oui | `.agents/skills` | `plugin.json`, `mcp_config.json` | local/IDE | native |
| ZCode | oui | `.zcode`, `.agents` | plugin, MCP | local/IDE | native |
| DSH | oui | `.agents/skills` | dsh bundle/plugin | local | native |
| Agent Skills générique | oui | `.agents/skills` | Agent Plugins v1 si supporté | variable | core |

## Preuve à ajouter

Pour chaque ligne, un test doit vérifier : découverte, chargement de la skill, exécution du mode lecture seule, génération, validation et refus d’une installation non confirmée. Les versions de l’agent et du système doivent être enregistrées dans le rapport.
