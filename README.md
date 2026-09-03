# sticker-card

**Universal Agent Portability Kit**

`sticker-card` transforme un dépôt open source en package portable pour agents IA. Il inspecte un dépôt, détecte ses dépendances et ses conventions, produit une carte de compatibilité, génère les fichiers Agent Skills et prépare les adaptateurs propres à chaque hôte.

Le projet ne promet pas que tous les agents possèdent les mêmes capacités. Il distingue le cœur portable, les capacités optionnelles et les intégrations natives.

## Objectifs

- inspecter un dépôt sans l'exécuter ;
- produire une carte machine-readable (`sticker-card.json`) ;
- générer des skills `SKILL.md` conformes à Agent Skills ;
- préparer `AGENTS.md`, `CLAUDE.md` et les packages de plugin ;
- décrire les différences entre Arena, Claude, Codex, Hermes, OpenClaw, OpenCode, Mistral Vibe, Antigravity, ZCode et DSH ;
- valider les packages avant installation ;
- ne jamais installer, exécuter ou publier sans confirmation explicite ;
- fournir un registre Git statique et auditable à terme.

## État du prototype

Le dépôt démarre volontairement avec un package de référence et un CLI Python sans dépendance externe. Il sert de bootstrap testable dans les environnements où aucun compilateur Go/Rust n'est disponible. Le format de carte et les sorties générées restent indépendants du langage ; le CLI pourra être remplacé par un binaire Go ou Rust sans migration de format.

## Utilisation rapide

```bash
# Inspecter un dépôt
python3 scripts/sticker-card.py inspect /chemin/vers/repo

# Générer un package portable
python3 scripts/sticker-card.py build /chemin/vers/repo --out ./dist --force

# Valider un package généré
python3 scripts/sticker-card.py validate ./dist/nom-du-repo

# Voir les agents connus
python3 scripts/sticker-card.py list-agents

# Préparer une installation sans rien modifier
python3 scripts/sticker-card.py install ./dist/nom-du-repo --agent codex --scope project

# Appliquer après revue explicite
python3 scripts/sticker-card.py install ./dist/nom-du-repo --agent codex --scope project --apply

# Vérifier les outils disponibles localement
python3 scripts/sticker-card.py doctor .
```

`install` est en mode plan par défaut. `--apply` est obligatoire pour écrire dans un répertoire cible. Les surfaces cloud ou conversationnelles produisent un guide de transfert au lieu de modifier le système local.

## Structure du projet

```text
skills/                 source de vérité de la skill
.agents/skills/         projection compatible Codex/Gemini/OpenCode/OpenClaw
.claude/skills/         projection Claude Code
adapters/               notes d'adaptation par hôte
scripts/                CLI et outils sans dépendance externe
data/                   catalogue machine-readable des hôtes
docs/                   architecture, sécurité et compatibilité
tests/                  tests et fixtures
```

## Modèle de compatibilité

- **Core** : `AGENTS.md`, `SKILL.md`, JSON et Markdown, sans API ni runtime obligatoire.
- **Configured** : nécessite la configuration ou les permissions de l'hôte.
- **Native** : utilise le format plugin propre à l'hôte.
- **Experimental** : détecté mais non garanti par des tests de conformance.
- **Handoff** : surface cloud ou conversationnelle qui reçoit un package, un prompt ou un dépôt, sans installation locale directe.

## Sécurité

Le package ne contient pas de secrets. Les serveurs MCP sont optionnels et les configurations générées utilisent des placeholders. Consultez [`docs/security.md`](docs/security.md) avant d'activer une intégration qui peut exécuter du code, écrire des fichiers ou appeler une API distante.

## Standards et sources

- [Agent Skills specification](https://agentskills.io/specification)
- [Agent Plugins specification](https://github.com/agentplugins/agent-plugins-spec)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Documentation des surfaces](docs/sources.md)

## Licence

À définir avec le mainteneur avant une publication publique. Ne pas réutiliser automatiquement la licence du dépôt inspecté : le converter et le package généré peuvent avoir des licences différentes.
