# Rapport de vérification de compatibilité — portable-ai

> **Statut : modèle à remplir.** Remplacer chaque valeur `TBD` par une preuve,
> `not tested` ou `blocked` avec une raison. Ne pas présenter ce modèle vierge
> comme un résultat de test.

## Identité du test

| Champ | Valeur |
|---|---|
| Dépôt | `https://github.com/Kapturo-ai/Portable-ai` |
| Commit testé | `TBD` |
| Date et fuseau | `TBD` |
| Testeur / agent évaluateur | `TBD` |
| Système et architecture | `TBD` |
| Réseau | `TBD` — préciser si aucun accès distant n'a été utilisé |
| Répertoire de travail | `TBD` — indiquer un chemin temporaire, jamais un secret |
| Modification du clone source | `none` attendu |

## Règle de lecture

Le **niveau déclaré** vient de `data/agents.json` et ne constitue pas une
preuve. La colonne **evidence** décrit uniquement ce qui a été observé pendant
ce test.

- `documented` : chemin décrit par une documentation officielle, sans test
  local suffisant ;
- `smoke-tested` : commande ou découverte sans erreur observée ;
- `verified` : découverte/chargement de la skill, workflow de lecture seule et
  projection d'installation vérifiés dans l'environnement indiqué ;
- `handoff` : surface cloud/conversationnelle transmise sans installation
  locale testable ;
- `blocked` : test empêché par un outil, une version, une permission ou un
  accès manquant ;
- `unknown` : preuve insuffisante ou résultat ambigu.

Un test de `portable-ai` réussi ne prouve pas à lui seul que l'hôte a chargé la
skill. Un hôte cloud ne doit pas être classé `verified` à partir d'un simple
fichier présent dans le dépôt.

## Tests de référence du converter

| Test | Commande ou observation | Code | Résultat | Preuve courte |
|---|---|---:|---|---|
| Inspection JSON sans exécution du dépôt | `python3 scripts/portable-ai.py inspect REPO --json` | `TBD` | `TBD` | `TBD` |
| Catalogue des agents | `python3 scripts/portable-ai.py list-agents --json` | `TBD` | `TBD` | `TBD` |
| Détection locale | `python3 scripts/portable-ai.py doctor REPO --json` | `TBD` | `TBD` | `TBD` |
| Suite de tests | `python3 -m unittest discover -s tests -p 'test_*.py'` | `TBD` | `TBD` | `TBD` |
| Validation de la source | `python3 scripts/portable-ai.py validate REPO` | `TBD` | `TBD` | `TBD` |
| Build hors du clone | `python3 scripts/portable-ai.py build REPO --out OUT --force` | `TBD` | `TBD` | `TBD` |
| Validation du package | `python3 scripts/portable-ai.py validate OUT/portable-ai` | `TBD` | `TBD` | `TBD` |
| Clone inchangé après les tests | `git -C REPO status --short` | `TBD` | `TBD` | `TBD` |

## Résultats par agent

`support_level` doit reprendre la valeur du catalogue au moment du test. Ne
pas la réécrire en fonction du résultat. Dans `limitations`, préciser les
contraintes de surface : local, cloud, sandbox, permissions, authentification,
réseau, MCP ou version.

| Agent | support_level | evidence | Découverte / chargement de skill | Workflow lecture seule | Projection / install temporaire | MCP | Version / environnement | Limitations et preuve |
|---|---|---|---|---|---|---|---|---|
| Arena Agent Mode (`arena-agent-mode`) | `handoff` | `TBD` | `TBD` | `TBD` | `handoff` ou `not applicable` | `TBD` | `TBD` | `TBD` |
| Claude.ai / Claude cloud (`claude-ai`) | `configured` | `TBD` | `TBD` | `TBD` | `handoff` ou `not applicable` | `TBD` | `TBD` | `TBD` |
| Claude Code (`claude-code`) | `native` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` |
| Hermes Agent (`hermes`) | `native` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` |
| OpenClaw (`openclaw`) | `native` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` |
| OpenCode (`opencode`) | `native` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` |
| Codex CLI / IDE (`codex`) | `native` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` |
| ChatGPT / ChatGPT Work (`chatgpt`) | `configured` | `TBD` | `TBD` | `TBD` | `handoff` ou `not applicable` | `TBD` | `TBD` | `TBD` |
| Mistral Vibe CLI (`mistral-vibe`) | `native` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` |
| Google Antigravity CLI / IDE (`antigravity`) | `native` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` |
| ZCode by Z.AI (`zcode`) | `native` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` |
| DeepSeek Harness / DSH (`dsh`) | `native` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` |
| Generic Agent Skills client (`generic-agent-skills`) | `core` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` | `TBD` |

## Preuves de commandes hôte

Pour chaque hôte réellement disponible, reproduire les commandes officielles
sans les remplacer par une supposition. Retirer les tokens et les données
privées des extraits.

### `TBD — agent-id`

- Version exacte : `TBD`
- Commande de découverte : `TBD`
- Preuve de chargement : `TBD`
- Tâche de lecture seule et résultat : `TBD`
- Commande de plan/install temporaire : `TBD`
- MCP : `not activated` ou décrire le test explicitement autorisé
- Limitation : `TBD`

## Sources officielles consultées

| Surface | URL officielle | Date de consultation | Ce que la source établit | Ce qu'elle ne prouve pas |
|---|---|---|---|---|
| Agent Skills | `https://agentskills.io/specification` | `TBD` | `TBD` | `TBD` |
| Arena Agent Mode | `TBD` | `TBD` | `TBD` | `TBD` |
| Claude | `TBD` | `TBD` | `TBD` | `TBD` |
| Codex / ChatGPT | `TBD` | `TBD` | `TBD` | `TBD` |
| Hermes | `TBD` | `TBD` | `TBD` | `TBD` |
| OpenClaw | `TBD` | `TBD` | `TBD` | `TBD` |
| OpenCode | `TBD` | `TBD` | `TBD` | `TBD` |
| Mistral Vibe | `TBD` | `TBD` | `TBD` | `TBD` |
| Antigravity | `TBD` | `TBD` | `TBD` | `TBD` |
| ZCode | `TBD` | `TBD` | `TBD` | `TBD` |
| DSH | `TBD` | `TBD` | `TBD` | `TBD` |

## Bloc prêt à reporter dans `docs/compatibility-matrix.md`

Ce bloc est volontairement compact. Ne le remplir qu'après revue du rapport
complet ci-dessus.

| Agent | Niveau déclaré | Preuve | Version / commit | Limitation principale |
|---|---|---|---|---|
| Arena Agent Mode | `handoff` | `TBD` | `TBD` | `TBD` |
| Claude.ai / Claude cloud | `configured` | `TBD` | `TBD` | `TBD` |
| Claude Code | `native` | `TBD` | `TBD` | `TBD` |
| Hermes Agent | `native` | `TBD` | `TBD` | `TBD` |
| OpenClaw | `native` | `TBD` | `TBD` | `TBD` |
| OpenCode | `native` | `TBD` | `TBD` | `TBD` |
| Codex CLI / IDE | `native` | `TBD` | `TBD` | `TBD` |
| ChatGPT / ChatGPT Work | `configured` | `TBD` | `TBD` | `TBD` |
| Mistral Vibe CLI | `native` | `TBD` | `TBD` | `TBD` |
| Google Antigravity CLI / IDE | `native` | `TBD` | `TBD` | `TBD` |
| ZCode by Z.AI | `native` | `TBD` | `TBD` | `TBD` |
| DeepSeek Harness / DSH | `native` | `TBD` | `TBD` | `TBD` |
| Generic Agent Skills client | `core` | `TBD` | `TBD` | `TBD` |

## Conclusion

- Décision globale : `TBD`
- Compatibilités réellement vérifiées : `TBD`
- Tests bloqués ou non réalisés : `TBD`
- Action recommandée dans la matrice : `TBD`
