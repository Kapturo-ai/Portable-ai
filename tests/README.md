# Kit de vérification publique

Ce dossier contient le protocole à donner à un agent IA indépendant après la
publication du dépôt. Le but est d'obtenir des preuves reproductibles pour
`docs/compatibility-matrix.md`, et non de transformer une mention dans une
documentation fournisseur en promesse de compatibilité.

- [`compatibility-report-template.md`](compatibility-report-template.md) est le
  fichier Markdown à remplir et à retourner.
- Le rapport doit toujours être rattaché à un commit, une date, un système et
  une version d'agent.
- Un agent indisponible, non authentifié ou interdit par l'environnement doit
  être marqué `blocked` ou `unknown`, jamais `verified`.

## Prompt prêt à copier

Copier le texte ci-dessous dans l'agent qui doit vérifier le dépôt. Remplacer
`REPOSITORY_URL` uniquement si l'URL publique est différente.

```text
Tu es un testeur indépendant de compatibilité pour portable-ai.

Dépôt public à examiner : https://github.com/Kapturo-ai/Portable-ai
URL de référence éventuelle : REPOSITORY_URL

Mission :
1. Consulte le dépôt public et lis tests/README.md ainsi que
   tests/compatibility-report-template.md avant de tester.
2. Suis le protocole sans modifier le dépôt, sans commit, sans push, sans PR,
   sans publication et sans écrire dans le compte utilisateur ou dans un
   serveur distant.
3. Utilise la recherche web native pour vérifier la documentation officielle
   et l'état actuel de chaque intégration testée. Cite les URL officielles et
   la date de consultation. Ne remplace pas une preuve locale par une simple
   page de documentation.
4. Retourne le contenu complet d'un seul fichier nommé
   compatibility-report.md, en conservant la structure du template. Le
   rapport doit être en Markdown, prêt à être copié dans la matrice de
   compatibilité.

Règles de sécurité :
- Commence par inspecter les fichiers et les instructions avant toute
  exécution de code.
- Travaille dans un clone ou un répertoire temporaire isolé.
- N'installe aucun paquet, binaire, plugin ou serveur MCP. N'utilise pas de
  secret, de token, de fichier .env, de clé privée ou de connexion distante.
- N'exécute pas le code du dépôt pendant l'inspection. Après cette inspection,
  les tests explicitement listés dans tests/README.md peuvent être exécutés.
- Les tests --apply sont autorisés uniquement dans des répertoires temporaires
  et jetables ; ne les applique jamais dans le clone source.
- Si une étape nécessite une installation, une authentification, un accès
  payant, un MCP ou une permission non disponible, arrête cette étape et
  inscris précisément la raison dans le rapport.
- Ne demande et ne conserve aucun identifiant. Ne modifie pas les variables
  d'environnement et ne lis pas le répertoire personnel pour contourner une
  limitation.

Exigences de preuve :
- `documented` signifie seulement que la documentation officielle décrit le
  chemin ;
- `smoke-tested` signifie qu'une commande ou une découverte sans erreur a été
  exécutée dans l'environnement indiqué ;
- `verified` exige la découverte ou le chargement de la skill, le workflow de
  lecture seule et l'installation de projection dans un répertoire temporaire
  lorsque cette installation est possible ;
- `handoff` est le résultat normal d'une surface cloud sans installation locale
  testable ;
- `blocked` ou `unknown` doit expliquer ce qui manque.

Ne déduis jamais qu'une skill est chargée simplement parce que son fichier est
présent. Sépare dans le tableau le niveau déclaré par data/agents.json, le
niveau de preuve réellement obtenu et les limitations observées.
```

## Protocole reproductible

### 1. Préparer un clone isolé

Le testeur doit travailler sur une copie publique et conserver le SHA testé.
Il ne doit pas travailler dans son clone de développement personnel.

```bash
git clone --depth 1 https://github.com/Kapturo-ai/Portable-ai.git /tmp/portable-ai-public
cd /tmp/portable-ai-public
git rev-parse HEAD
python3 --version
```

Si le dépôt n'est pas encore public ou si Python 3 n'est pas disponible, le
rapport doit le signaler et s'arrêter avec `blocked`. Il ne faut pas demander
de jeton GitHub pour contourner ce résultat.

### 2. Inspection avant exécution

Ces commandes lisent le dépôt et produisent les éléments de preuve de base.
La sortie volumineuse peut être conservée dans le répertoire temporaire du
rapport, pas dans le dépôt.

```bash
REPO="$PWD"
OUT="$(mktemp -d)"

python3 scripts/portable-ai.py inspect "$REPO" --json > "$OUT/inspect.json"
python3 scripts/portable-ai.py list-agents --json > "$OUT/agents.json"
python3 scripts/portable-ai.py doctor "$REPO" --json > "$OUT/doctor.json"
```

`inspect` ne doit lancer aucun fichier du dépôt. `doctor` détecte les commandes
présentes avec une recherche de chemin ; il ne prouve ni authentification ni
capacité réelle de l'agent.

### 3. Tests de référence du converter

Après la revue de l'inspection, exécuter exactement les tests non destructifs
suivants :

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/portable-ai.py validate "$REPO"
python3 scripts/portable-ai.py build "$REPO" --out "$OUT" --force
python3 scripts/portable-ai.py validate "$OUT/portable-ai"
git -C "$REPO" status --short
```

Résultats attendus dans l'état actuel :

- la suite Python se termine avec un code nul ; le nombre de tests doit être
  reporté sans être figé dans le protocole ;
- la validation de la source et du package affiche `VALID` ;
- le build est effectué hors du clone, dans `OUT/portable-ai` ;
- `git status --short` ne montre aucune modification du clone source ;
- aucune dépendance n'est installée par ces commandes.

Le testeur doit relever les codes de retour, les erreurs et les versions, pas
seulement recopier le mot `VALID`.

### 4. Vérifier le plan et l'application dans un dossier temporaire

Le CLI ne teste pas le chargement interne de chaque produit ; il vérifie la
projection de skill et le comportement de sécurité de l'installateur. Pour
chaque agent installable du catalogue, exécuter d'abord le plan sans
`--apply`, puis éventuellement l'application dans un dossier temporaire :

```bash
PACKAGE="$OUT/portable-ai"
TARGET="$OUT/install-codex"

python3 scripts/portable-ai.py install "$PACKAGE" \
  --agent codex --scope project --target "$TARGET"
# Vérifier ici que le plan affiche PLAN ONLY et que TARGET n'existe pas.

python3 scripts/portable-ai.py install "$PACKAGE" \
  --agent codex --scope project --target "$TARGET" --apply
# Vérifier ici uniquement la projection attendue dans TARGET.
```

Répéter avec les identifiants de `data/agents.json` qui ont
`installable: true`. Utiliser le chemin indiqué dans le catalogue pour vérifier
la destination. Ne jamais appliquer le test dans le clone source ni dans le
répertoire personnel réel.

Pour `arena-agent-mode`, `claude-ai` et `chatgpt`, le résultat attendu est un
handoff sans création de `TARGET`. Cela ne prouve pas que l'interface cloud a
chargé la skill ; cette preuve doit être obtenue séparément dans cette
interface, si le testeur y a un accès autorisé.

### 5. Test de l'hôte réel, seulement s'il est déjà disponible

Cette étape est facultative et doit être exécutée uniquement si le binaire ou
l'interface est déjà disponible, sans installation ni authentification
supplémentaire. Le testeur doit enregistrer :

1. le nom exact de l'hôte, sa version et son système ;
2. le chemin de découverte réellement utilisé ;
3. une preuve observable du chargement de `SKILL.md` (sortie, journal ou
   indication UI) ;
4. une tâche de lecture seule qui lit `portable-ai.json`, identifie le runtime
   et explique le niveau de support sans modifier de fichier ;
5. le résultat du plan d'installation et, si autorisé, de l'application dans
   `OUT` ;
6. le fait que MCP n'a pas été activé, ou les détails d'un test MCP explicitement
   autorisé et réalisé sans secret.

Une simple commande `--version`, la présence d'un binaire ou la présence d'un
fichier dans un dossier ne suffit pas pour classer un hôte `verified`. Les
commandes spécifiques doivent venir de la documentation officielle consultée
et être reproduites telles quelles dans le rapport.

### 6. Finaliser le rapport

Partir de [`compatibility-report-template.md`](compatibility-report-template.md)
et remplacer tous les champs `TBD` par des valeurs ou par `not tested` avec une
raison. Le fichier final doit :

- contenir le commit exact et la date de test ;
- séparer `support_level` (catalogue) et `evidence` (test réellement observé) ;
- donner les commandes et un court extrait de résultat pour chaque preuve ;
- fournir les versions des hôtes et les limites locales/cloud/sandbox/MCP ;
- citer les pages officielles utilisées avec leur date de consultation ;
- ne pas inclure de secret, de sortie contenant un token ou de donnée privée ;
- conserver une ligne pour chaque agent du catalogue, même si elle vaut
  `blocked` ou `unknown`.

## Intégration dans la matrice

Le rapport retourné est une pièce de preuve datée. Après revue humaine :

1. conserver le rapport complet dans la discussion ou dans un artefact de
   test séparé ;
2. reporter uniquement les résultats vérifiés dans
   [`docs/compatibility-matrix.md`](../docs/compatibility-matrix.md) ;
3. ne pas remplacer le niveau déclaré du catalogue par une réussite ponctuelle
   sans indiquer la version et l'environnement ;
4. ajouter le lien vers les sources officielles et le commit testé ;
5. si un test échoue, documenter la limitation au lieu de supprimer la ligne.

Le template contient un bloc de tableau court prévu pour cette mise à jour.
