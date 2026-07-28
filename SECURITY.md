# Security

Secrets ausschließlich als GitHub Actions Repository Secrets speichern:
- BUNGIE_API_KEY
- WARGAMING_APPLICATION_ID

Bei Offenlegung sofort beim Anbieter ersetzen. Keine Secrets in Logs, Issues, Manifeste oder Releases schreiben. Workflows erhalten nur die minimal erforderlichen Berechtigungen.
