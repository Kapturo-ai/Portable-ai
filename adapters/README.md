# Adaptateurs

Chaque dossier décrit la projection d’un package vers un hôte. Un adaptateur ne doit pas recopier toute la skill portable : il documente seulement les chemins, manifestes, permissions et limites propres à l’hôte.

Les adaptateurs cloud/conversationnels produisent un handoff. Ils ne prétendent pas pouvoir modifier la machine locale.

Les adaptateurs natifs sont générés par `scripts/portable-ai.py build` et validés comme des artefacts séparés.
