# CrossCore-Data 1.20.0

## Repository
Erstelle das öffentliche Repository `unhappyangel83/CrossCore-Data`. Lade den Inhalt des vorbereiteten Repository-ZIPs in den Stammordner.

## Secrets
Unter `Settings -> Secrets and variables -> Actions` anlegen:
- `BUNGIE_API_KEY`
- `WARGAMING_APPLICATION_ID`

## Wochenplan
- Montag 06:15 Europe/Berlin: WoT und WoWS.
- Mittwoch 06:15 Europe/Berlin: Destiny 2.
GitHub Actions verwendet IANA-Zeitzonen; die Workflows laufen auf dem Standardbranch.

## Erster Start
1. Actions aktivieren.
2. `Publish WoT and WoWS Data - Monday` manuell starten.
3. `Publish Destiny Data - Wednesday` manuell starten.
4. Release `data-latest` öffnen.
5. Prüfen, dass alle fünf Assets vorhanden sind.

## Release-Assets
```text
destiny_data_manifest.json
destiny_items.json.gz
wargaming_data_manifest.json
wot_catalog.json.gz
wows_catalog.json.gz
```

## Warum `gh release upload --clobber`
Jeder Workflow ersetzt nur seine eigenen Assets. Destiny darf WoT/WoWS nicht löschen und umgekehrt. Existiert das Release nicht, wird es einmalig angelegt.

## Beispiel für manuelle Ausführung
```text
GitHub -> Actions -> gewünschter Workflow -> Run workflow -> main -> Run workflow
```

## Fehlerdiagnose
- Secret fehlt: Workflow bricht vor dem Download ab.
- 401/403: API-Key/ID prüfen.
- 404 beim CrossCore-Download: Release-Tag und Dateiname prüfen.
- SHA-Fehler: Manifest und GZIP stammen nicht aus demselben Lauf.
- Zeitplan läuft nicht: Workflow muss im Defaultbranch liegen; öffentliche inaktive Repositories können Zeitpläne deaktivieren.

## Sicherheit
Keine Secrets in README, Issues, Logs, Artefakte oder Manifeste kopieren. Nur die GitHub-Actions-Secretverwaltung verwenden. Workflows minimal berechtigen: `contents: write` nur für Publisher, `contents: read` für Tests.

## Offizielle Quellen

- Microsoft Smart App Control: https://learn.microsoft.com/windows/apps/develop/smart-app-control/overview
- Microsoft Codesignierung für Smart App Control: https://learn.microsoft.com/windows/apps/develop/smart-app-control/code-signing-for-smart-app-control
- Microsoft Smart-App-Control-Test: https://learn.microsoft.com/windows/apps/develop/smart-app-control/test-your-app-with-smart-app-control
- GitHub Actions Workflow-Syntax: https://docs.github.com/actions/reference/workflows-and-actions/workflow-syntax
- Bungie API: https://github.com/Bungie-net/api
- Wargaming Developer Room: https://developers.wargaming.net/
- Warframe.market API: https://docs.warframe.market/

