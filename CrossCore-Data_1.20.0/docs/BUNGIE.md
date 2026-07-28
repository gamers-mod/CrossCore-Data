# Bungie-API-Key - vollständige Anleitung

## Zweck
Der Bungie-Key wird nur im GitHub-Datenpublisher verwendet. Endanwender benötigen keinen Key.

## Einrichtung
1. Bungie.net-Konto anmelden.
2. Bungie Application Portal öffnen.
3. Neue Anwendung `CrossCore Data Publisher` anlegen.
4. Website/Redirect nur entsprechend dem Portal ausfüllen; für reine Manifest-Lesezugriffe ist im CrossCore-Publisher kein OAuth-Benutzerlogin erforderlich.
5. API-Key kopieren.
6. GitHub Secret `BUNGIE_API_KEY` anlegen.
7. Destiny-Workflow manuell starten.

## Verwendung
Der Publisher sendet den Schlüssel im HTTP-Header `X-API-Key`, fragt `/Platform/Destiny2/Manifest/` ab und lädt die deutschen und englischen `DestinyInventoryItemDefinition`-Komponenten.

```http
GET /Platform/Destiny2/Manifest/
X-API-Key: <GitHub-Secret>
```

## Fehler
- 401/403: Key falsch, deaktiviert oder nicht übernommen.
- Definition fehlt: Bungie-Manifeststruktur oder Sprache temporär nicht verfügbar.
- Timeout: Workflow erneut ausführen; bestehendes Release bleibt unverändert.

## Sicherheit
Key niemals in CrossCore, JSON, Screenshot oder Issue eintragen. Bei Veröffentlichung sofort im Bungie-Portal ersetzen.

## Offizielle Quellen

- Microsoft Smart App Control: https://learn.microsoft.com/windows/apps/develop/smart-app-control/overview
- Microsoft Codesignierung für Smart App Control: https://learn.microsoft.com/windows/apps/develop/smart-app-control/code-signing-for-smart-app-control
- Microsoft Smart-App-Control-Test: https://learn.microsoft.com/windows/apps/develop/smart-app-control/test-your-app-with-smart-app-control
- GitHub Actions Workflow-Syntax: https://docs.github.com/actions/reference/workflows-and-actions/workflow-syntax
- Bungie API: https://github.com/Bungie-net/api
- Wargaming Developer Room: https://developers.wargaming.net/
- Warframe.market API: https://docs.warframe.market/

