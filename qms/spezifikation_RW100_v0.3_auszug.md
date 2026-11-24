# Produktanforderungen RW-100 – Version 0.3 (Auszug)

> SYNTHETISCH – fiktives Produkt, nur für Schulungszwecke.

Dokument-ID: SPEC-RW100 · Version 0.3 · Stand 2026-10-01 · Status: in Prüfung

| ID | Titel | Text | Priorität | Status |
|---|---|---|---|---|
| REQ-001 | Drehzahlbereich | Die Solldrehzahl muss im Bereich 50 bis 2000 1/min in Schritten von 10 1/min einstellbar sein. | hoch | freigegeben |
| REQ-002 | Drehzahlgenauigkeit | Im stationären Betrieb darf die Ist-Drehzahl höchstens ±2 % von der Solldrehzahl abweichen. | hoch | freigegeben |
| REQ-003 | Stopp-Taste | Nach Betätigen der Stopp-Taste muss der Motor innerhalb von 1 s zum Stillstand kommen. | hoch | freigegeben |
| REQ-004 | Anzeige Ist-Drehzahl | Das Display muss die Ist-Drehzahl anzeigen und mindestens zweimal pro Sekunde aktualisieren. | mittel | freigegeben |
| REQ-005 | Timer | Ein Timer von 1 bis 999 min muss einstellbar sein. Nach Ablauf stoppt der Motor und ein akustisches Signal ertönt. | mittel | freigegeben |
| REQ-006 | Überlastabschaltung | Überschreitet der Motorstrom 1,5 A länger als 3 s, muss der Motor stoppen und der Fehlercode E-17 angezeigt werden. | hoch | freigegeben |
| REQ-007 | Sanftanlauf | Beim Start muss die Drehzahl mit höchstens 200 1/min pro Sekunde auf den Sollwert ansteigen. | mittel | freigegeben |
| REQ-008 | Fehlerprotokoll | Die letzten 50 Fehler müssen mit Zeitstempel gespeichert werden. | mittel | entwurf |
| REQ-009 | Bedienung mit Handschuhen | Das Gerät soll auch mit Handschuhen gut bedienbar sein. | niedrig | entwurf |
| REQ-010 | Datenexport | Messdaten sollen über USB als CSV exportiert werden können. | niedrig | entwurf |
| REQ-011 | Bluetooth-Fernsteuerung | Das Gerät soll per Bluetooth ferngesteuert werden können. | niedrig | verworfen |
| REQ-012 | Firmware-Update | Ein Firmware-Update über USB muss möglich sein; benutzerdefinierte Einstellungen bleiben dabei erhalten. | mittel | freigegeben |

Änderungshistorie: siehe Versionsverwaltung (in diesem Auszug nicht enthalten).
