# Anforderungen an ReqTrace (App-Anforderungen)

> Synthetisches Workshop-Material. ReqTrace ist **kein Medizinprodukt** und **nicht für den Produktivbetrieb** bestimmt.
> Die Anforderungen in dieser Datei betreffen die **App selbst** (Präfix `APP-`).
> Die Daten, die die App verwaltet, sind Anforderungen an ein **fiktives Laborrührwerk RW-100** (Präfix `REQ-`, siehe `data/seed/`).

Einige Anforderungen sind absichtlich unpräzise, unvollständig oder widersprüchlich. Sie sind Gegenstand von Übung 2.

| ID | Anforderung | Umsetzungsstand |
|---|---|---|
| APP-01 | Die App muss alle Anforderungen mit ID, Priorität, Status und Titel auflisten (CLI `list`, API `GET /api/requirements`). Die Liste ist nach ID sortiert und optional nach Status filterbar. | umgesetzt |
| APP-02 | Anforderungs-IDs müssen dem Format `REQ-` gefolgt von genau drei Ziffern entsprechen (z.B. `REQ-007`). Datensätze mit ungültiger ID, unbekannter Priorität oder unbekanntem Status werden beim Laden mit einer verständlichen Fehlermeldung abgewiesen. Doppelte IDs sind unzulässig. | umgesetzt, Tests unvollständig |
| APP-03 | Die App muss alle Testfälle mit ID, letztem Ergebnis, verknüpften Anforderungen und Titel auflisten (CLI `testcases`, API `GET /api/testcases`). | umgesetzt |
| APP-04 | Die App muss eine Traceability-Matrix ausgeben: Für jede Anforderung die verknüpften Testfälle und einen zusammengefassten Status (CLI `trace`, API `GET /api/trace`, Weboberfläche). | umgesetzt |
| APP-05 | Die App muss alle Anforderungen auflisten, die durch **keinen** Testfall abgedeckt sind (Abdeckungslücken). Anforderungen mit Status `verworfen` werden dabei nicht berücksichtigt. Die Ausgabe ist nach ID sortiert. Bereitstellung über CLI `gaps` und API `GET /api/gaps`; gibt es keine Lücken, meldet die CLI dies ausdrücklich. | **offen (Übung 3)** |
| APP-06 | Die App muss Testergebnisse aus einer CSV-Datei (`testcase_id;result;date;tester`) importieren. Testfall-IDs werden ohne Berücksichtigung von Gross-/Kleinschreibung und umgebenden Leerzeichen zugeordnet. Zeilen mit unbekannter Testfall-ID oder ungültigem Ergebnis werden als Warnung protokolliert und übersprungen; der Import der übrigen Zeilen wird fortgesetzt. | umgesetzt, **Fehler gemeldet (Übung 5)** |
| APP-07 | Die Übersicht soll schnell laden und benutzerfreundlich sein. | diskussionswürdig |
| APP-08 | Die Abdeckung wird in Prozent aller Anforderungen angegeben. Eine Anforderung gilt als abgedeckt, wenn mindestens ein verknüpfter Testfall bestanden hat. | umgesetzt (`coverage`) |
| APP-09 | Die App soll eine Exportfunktion für Prüfnachweise bieten. | diskussionswürdig |
| APP-10 | Alle Änderungen an Anforderungen müssen nachvollziehbar sein. | diskussionswürdig |
| APP-11 | Die App darf ausschliesslich lokal laufen: Der Webserver bindet nur an `127.0.0.1`, es werden keine externen Netzwerkverbindungen aufgebaut und keine Abhängigkeiten ausserhalb der Python-Standardbibliothek zur Laufzeit benötigt. | umgesetzt |

## Begriffe

- **Anforderung (REQ)**: synthetische Produktanforderung an das fiktive RW-100.
- **Testfall (TC)**: synthetischer Testfall, der eine oder mehrere Anforderungen verifizieren soll.
- **Ergebnis**: `passed`, `failed`, `blocked` oder `not_run`.
