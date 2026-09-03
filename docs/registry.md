# Registre Git statique

Le premier registre de `portable-ai` est volontairement un dossier versionné plutôt qu’une API. Il peut être relu par GitHub, une CI ou une future interface sans ajouter de serveur ni de credentials.

## Contrat d’une entrée

```json
{
  "id": "publisher/package",
  "version": "0.1.0",
  "source": "https://…",
  "integrity_sha256": "…",
  "status": "draft|reviewed|verified|deprecated",
  "trust": "unverified|reviewed|verified",
  "tested_agents": [],
  "permissions": [],
  "review": {}
}
```

## Publication prévue

1. Générer le package avec une version déterminée.
2. Valider localement et en CI.
3. Calculer le hash de l’artefact exact.
4. Déclarer les agents, versions et scénarios smoke testés.
5. Faire relire le diff du registre.
6. Publier le package et l’entrée ensemble.

Le registre ne lance aucun script et ne fournit pas de secret. Une future marketplace pourra indexer `registry/index.json`, mais ne doit pas modifier le contrat de sécurité.
