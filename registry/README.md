# Static registry

Ce répertoire est le prototype d’un registre Git statique. Il catalogue des packages sans les exécuter.

Une entrée doit indiquer :

- une identité et une version ;
- la source et un hash SHA-256 avant publication ;
- les artefacts et agents réellement testés ;
- les permissions demandées ;
- un état de revue et de confiance.

Le registre ne doit pas devenir une autorité de confiance implicite. `auto_install` reste désactivé et les packages non vérifiés doivent être inspectés localement.
