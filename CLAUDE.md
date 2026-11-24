# CLAUDE.md – Projektanweisungen für ReqTrace (Workshop)

Dieses Repository ist Schulungsmaterial. Es enthält ausschliesslich **synthetische Daten**.
Keine echten Kunden-, Patienten-, Support- oder Firmendaten hinzufügen. Keine Geheimnisse, Tokens oder Passwörter in Dateien, Prompts oder Logs.

## Projekt in Kürze
- ReqTrace verwaltet synthetische Anforderungen (REQ-xxx) eines fiktiven Laborrührwerks und daraus abgeleitete Testfälle (TC-xxx).
- App-Anforderungen stehen in `REQUIREMENTS.md` (APP-xx). Bei Unklarheiten dort nachsehen und offene Fragen benennen statt raten.
- Stack: Python ≥ 3.8, nur Standardbibliothek zur Laufzeit (APP-11). Keine neuen Abhängigkeiten ohne Rückfrage.

## Struktur
- `reqtrace/models.py` Datenmodelle und Validierung
- `reqtrace/storage.py` JSON laden/speichern (`data/work/`, erzeugt aus `data/seed/`)
- `reqtrace/trace.py` Traceability und Abdeckung
- `reqtrace/importer.py` CSV-Import von Testergebnissen
- `reqtrace/cli.py` Kommandozeile, `reqtrace/server.py` + `reqtrace/static/index.html` lokale Weboberfläche
- `tests/` unittest-basierte Tests (laufen auch mit pytest)
- `qms/`, `c-review/`, `hardware/`, `cve-demo/`, `support/`, `mcp-demo/` Übungs- und Demomaterial – nicht Teil der App

## Befehle
- Tests: `python -m unittest` (alternativ `python -m pytest -q`)
- Einzelner Test: `python -m unittest tests.test_trace -v`
- App: `python -m reqtrace list | trace | coverage | serve`
- Daten zurücksetzen: `python tools/reset_workshop.py`

## Arbeitsweise
- Vor Änderungen kurz planen: betroffene Dateien, Vorgehen, Testidee. Bei grösseren Änderungen erst den Plan zeigen.
- Kleine, nachvollziehbare Schritte. Keine Umbauten ausserhalb des Auftrags.
- Jede Verhaltensänderung mit Test absichern; Tests im Stil der bestehenden Tests (`unittest.TestCase`, `tests/helpers.py` nutzen).
- Nach Änderungen die Tests ausführen und das Ergebnis ehrlich berichten (auch Fehlschläge).
- Annahmen ausdrücklich als Annahme kennzeichnen. Anforderungs-IDs (APP-xx, REQ-xxx) in Tests und Commit-Nachrichten referenzieren.
- `data/seed/` nur ändern, wenn der Auftrag das ausdrücklich verlangt.
- Keine Git-Commits oder Pushes ohne ausdrückliche Aufforderung.

## Grenzen
- Keine Netzwerkzugriffe, keine Installation von Paketen ohne Rückfrage.
- Bei QMS-Material: Nachweise zuordnen und Lücken markieren, aber **keine Konformitäts- oder Freigabeaussagen** treffen. Freigaben erfolgen durch Menschen im regulären Prozess.
