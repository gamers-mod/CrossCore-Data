# Wargaming application_id - World of Tanks und World of Warships

## Zweck
Eine einzige Herausgeber-`application_id` kann für die öffentlichen WoT- und WoWS-Enzyklopädieabfragen des Projekts verwendet werden. Endanwender benötigen keine ID.

## Einrichtung
1. Wargaming Developer Room öffnen und anmelden.
2. Neue Anwendung `CrossCore Data Publisher` registrieren.
3. Anwendungstyp passend zum GitHub-Publisher wählen; die Anfragen kommen von GitHub-Runnern und nicht von Endanwendern.
4. `application_id` kopieren.
5. GitHub Secret `WARGAMING_APPLICATION_ID` anlegen.
6. Montagsworkflow manuell testen.

## Endpunkte
```text
https://api.worldoftanks.eu/wot/encyclopedia/vehicles/
https://api.worldofwarships.eu/wows/encyclopedia/ships/
```
Parameterbeispiel:
```text
application_id=<Secret>&language=de&limit=100&page_no=1
```
Der Publisher lädt DE und EN seitenweise, verknüpft über `tank_id` beziehungsweise `ship_id` und erzeugt GZIP plus SHA-256-Manifest.

## Fehler
- `APPLICATION_NOT_FOUND`: ID falsch oder Anwendung nicht aktiv.
- Rate limit: nicht unnötig manuell wiederholen; Wochenplan beibehalten.
- Leere Seiten: API-Status und Region prüfen.

## Sicherheit
Die `application_id` nicht in Endanwender-Builds einbetten. Obwohl sie nicht wie ein Passwort behandelt werden sollte, bleibt der registrierte Herausgeber für ihre Nutzung verantwortlich.

## Offizielle Quellen

- Microsoft Smart App Control: https://learn.microsoft.com/windows/apps/develop/smart-app-control/overview
- Microsoft Codesignierung für Smart App Control: https://learn.microsoft.com/windows/apps/develop/smart-app-control/code-signing-for-smart-app-control
- Microsoft Smart-App-Control-Test: https://learn.microsoft.com/windows/apps/develop/smart-app-control/test-your-app-with-smart-app-control
- GitHub Actions Workflow-Syntax: https://docs.github.com/actions/reference/workflows-and-actions/workflow-syntax
- Bungie API: https://github.com/Bungie-net/api
- Wargaming Developer Room: https://developers.wargaming.net/
- Warframe.market API: https://docs.warframe.market/

