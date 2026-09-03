# Modèle de sécurité

## Principes

- L’inspection est lecture seule et ne lance pas le code du dépôt source.
- Le mode par défaut de `install` est un plan ; `--apply` est explicite.
- Les secrets, fichiers `.env`, clés privées et tokens sont exclus des sorties.
- Les configurations MCP utilisent des références de variables d’environnement ou des placeholders.
- Un package non vérifié n’est jamais considéré comme sûr parce qu’il vient de GitHub.
- Les commandes système sont affichées avant exécution lorsqu’une future version compilée les activera.

## Niveaux d’action

| Action | Défaut | Confirmation |
|---|---:|---:|
| Lire la structure et les manifestes | autorisée | non |
| Lire un fichier texte non secret | autorisée | non |
| Exécuter du code du dépôt inspecté | refusée | oui, hors inspection |
| Écrire un package de sortie | plan uniquement | oui avec `--apply` |
| Modifier un dossier utilisateur | plan uniquement | oui avec destination explicite |
| Installer un MCP | refusée | revue manuelle des outils |
| Utiliser un secret | refusée | configuration hors Git + confirmation |
| Push, publication ou action distante | refusée | confirmation séparée |

## Supply chain

Le catalogue et les packages doivent être hashés. Le registre statique doit être revu dans Git. La signature cryptographique, l’attestation de build et la gestion des secrets sont des évolutions nécessaires avant une marketplace qui installe automatiquement des extensions.
