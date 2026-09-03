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

## Protocole et preuve à ajouter

Le protocole reproductible, le prompt à donner à un agent indépendant et le
fichier Markdown à remplir sont dans [`tests/README.md`](../tests/README.md) et
[`tests/compatibility-report-template.md`](../tests/compatibility-report-template.md).

Pour chaque ligne, un test doit vérifier : découverte, chargement de la skill,
exécution du mode lecture seule, génération, validation et refus d’une
installation non confirmée. Les versions de l’agent et du système doivent être
enregistrées dans le rapport.

Le rapport doit distinguer le niveau déclaré (`core`, `configured`, `native`,
`handoff`) de la preuve obtenue (`documented`, `smoke-tested`, `verified`,
`handoff`, `blocked` ou `unknown`). Une documentation fournisseur seule ne
suffit pas à classer un hôte `verified`.
