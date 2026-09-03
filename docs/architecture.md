# Architecture

## Contrat principal

`portable-ai` est un convertisseur de dépôt, pas un nouveau runtime d’agent. Il produit une représentation déclarative et des sorties adaptées à l’environnement cible.

```text
repository
   │
   ├── inspect (lecture seule, aucune exécution)
   │       └── portable-ai.json
   │
   ├── build
   │       ├── Agent Skills
   │       ├── AGENTS.md / wrappers
   │       ├── Agent Plugins v1
   │       └── adaptateurs hôte
   │
   ├── validate
   │       ├── schéma et frontmatter
   │       ├── hashes des projections
   │       ├── manifestes
   │       └── scan de secrets
   │
   └── install --plan / --apply
           └── destination explicite et confirmation
```

## Source de vérité

Le package généré possède une skill canonique sous `skills/portable-ai/`. Les copies destinées à `.agents/skills/` et `.claude/skills/` sont des projections. Le validator vérifie qu’elles ont le même hash.

Les champs spécifiques à un fournisseur n’entrent pas dans `SKILL.md` lorsqu’ils changent la sémantique portable. Ils vont dans `adapters/<agent>/`, dans un manifest natif ou dans le catalogue.

## Flux de dépendances

1. **Core** : aucun serveur, aucune clé, aucune commande de projet exécutée.
2. **Local scripts** : dépendances détectées mais non installées automatiquement.
3. **MCP** : connexion déclarée mais activée seulement après revue des outils, du transport et des permissions.
4. **Native plugin** : package hôte séparé, versionné et testé indépendamment.

## Registre

Le premier registre sera un index Git statique :

```text
registry/
├── index.json
├── publishers/
├── packages/
└── compatibility/
```

Chaque entrée devra contenir le nom, la version, le hash du package, les hôtes testés, les versions testées, la liste des permissions et l’état de revue. Une future API peut indexer ce format sans le remplacer.
