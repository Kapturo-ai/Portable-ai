# CLI de référence

Le bootstrap actuel est `scripts/sticker-card.py` et ne dépend d’aucun package Python externe.

## Commandes

### `inspect [REPO]`

Lecture seule. Détecte manifestes, runtimes, fichiers de contexte et assets d’agents. Ne lance ni les tests ni les scripts du dépôt.

### `build [REPO] --out DIR [--force]`

Génère un package autonome sous `DIR/<nom-du-repo>/` avec carte, skill canonique, projections, manifestes et notes d’adaptateurs.

### `validate [PATH]`

Valide le dépôt de référence ou un package généré. Vérifie le frontmatter, les trois projections de skill, les hashes, les manifestes, les adaptateurs et des motifs de secrets à haute confiance.

### `doctor [REPO]`

Détecte les commandes disponibles sans les exécuter. Une commande présente ne signifie pas que l’agent est authentifié ou que ses capacités sont autorisées.

### `install PACKAGE --agent ID [--scope project|user] [--target PATH]`

Affiche toujours un plan. Seul `--apply` autorise la copie de la skill portable, et aucune dépendance n’est installée. Les surfaces cloud donnent un handoff.

## Évolution vers un binaire

Le contrat de fichier est indépendant de Python. Une future version Go ou Rust peut reprendre les commandes et les sorties JSON ; le bootstrap restera utile pour prototyper et valider la spécification.
