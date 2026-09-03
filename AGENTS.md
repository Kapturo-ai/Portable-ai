# AGENTS.md

## Mission

Ce dépôt construit `portable-ai`, un kit qui inspecte des dépôts open source et génère des packages portables pour agents IA.

## Règles universelles

- Garder le cœur sans dépendance tierce obligatoire.
- Respecter Agent Skills : un skill est un dossier avec un `SKILL.md` contenant `name` et `description`.
- Maintenir `skills/portable-ai/SKILL.md` comme source de vérité ; les copies sous `.agents/skills/` et `.claude/skills/` sont des projections générées.
- Ne jamais mettre de clé API, token, certificat privé ou secret dans Git.
- Ne jamais lancer une installation, une commande distante, un push ou une action destructive sans confirmation explicite.
- Ne pas présenter une capacité comme compatible sans la classer et indiquer la preuve de test.
- Les formats propriétaires restent dans `adapters/` ; ne pas polluer le cœur portable avec des champs vendor-specific.
- Toute modification du catalogue d’agents doit mettre à jour `docs/compatibility-matrix.md` et les tests.

## Vérifications

```bash
python3 scripts/portable-ai.py validate .
python3 -m unittest discover -s tests -p 'test_*.py'
```

## Workflow

1. Inspecter et documenter avant de modifier.
2. Implémenter le cœur et les sorties déterministes.
3. Valider les manifestes et rechercher les secrets.
4. Tester le mode plan d'installation.
5. Ne tester `--apply` que dans un répertoire temporaire.
6. Mettre à jour la matrice de compatibilité et la documentation des sources.
