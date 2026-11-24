# ReqTrace – Workshop-Codebase «Agentic Engineering mit Claude Code»

> **Schulungsmaterial mit ausschliesslich synthetischen Daten.**
> ReqTrace ist **kein Medizinprodukt** und **nicht für den Produktivbetrieb** bestimmt.
> KI-generiert mit Claude Code und vom Workshop-Leiter geprüft – vor Weiterverwendung erneut prüfen.

ReqTrace ist eine kleine lokale App, die Anforderungen (REQ-xxx) eines **fiktiven Laborrührwerks RW-100** und daraus abgeleitete Testfälle (TC-xxx) verwaltet: Liste, Traceability-Matrix, Abdeckung, CSV-Import von Testergebnissen und eine minimale Weboberfläche.
Im Workshop erweitern wir die App Schritt für Schritt mit Claude Code.

## Voraussetzungen

| Werkzeug | Version | Prüfen mit | Pflicht |
|---|---|---|---|
| Python | ≥ 3.8 (getestet mit 3.8.2 und 3.11.0) | `python --version` (Windows ggf. `py --version`) | ja |
| Git | aktuell | `git --version` | ja |
| Claude Code | aktuell, angemeldet | `claude --version` | ja |
| C-Compiler (gcc) | beliebig, C99 | `gcc --version` | nur Übung 6 (sonst Review ohne Kompilieren) |
| pytest | optional | `python -m pytest --version` | nein |

Zur Laufzeit werden **keine** Pakete aus dem Internet benötigt (nur Python-Standardbibliothek).

## Setup (ca. 5 Minuten)

```bash
git clone <URL dieses Repositorys> reqtrace-workshop
cd reqtrace-workshop
python -m unittest
```

Erwartet: `Ran 21 tests ... OK`. Der Startzustand ist bereits committet: Damit sehen Sie jede Änderung von Claude Code mit `git diff` und können jederzeit zurück.

Als ZIP heruntergeladen (ohne Git)? Dann einmalig `git init`, `git add .` und `git commit -m "Startzustand Workshop"` ausführen.

## App starten

```bash
python -m reqtrace list                 # Anforderungen (APP-01)
python -m reqtrace list --status entwurf
python -m reqtrace show REQ-003
python -m reqtrace testcases            # Testfälle (APP-03)
python -m reqtrace trace                # Traceability-Matrix (APP-04)
python -m reqtrace coverage             # Abdeckung (APP-08)
python -m reqtrace serve                # Weboberfläche: http://127.0.0.1:8000/
```

`serve` mit Ctrl+C beenden. Port belegt? `python -m reqtrace serve --port 8010`.

## Tests

```bash
python -m unittest                       # alle Tests
python -m unittest tests.test_trace -v   # einzelnes Modul
python -m pytest -q                      # alternativ, falls pytest installiert ist
```

## Zurücksetzen

| Was | Befehl |
|---|---|
| Arbeitsdaten (`data/work/`) und Log | `python tools/reset_workshop.py` |
| Alle Code-Änderungen verwerfen | `git restore .` und neue Dateien mit `git clean -n` prüfen, dann `git clean -f` |
| Änderungen beiseitelegen | `git stash` |

## Struktur

```
reqtrace-workshop/
├── CLAUDE.md               Projektanweisungen für Claude Code
├── REQUIREMENTS.md         App-Anforderungen APP-01 … APP-11 (einige absichtlich unklar)
├── .claude/settings.json   Beispiel für Berechtigungsregeln (allow/deny)
├── reqtrace/               App-Code (Python, nur Standardbibliothek)
├── tests/                  unittest-Tests
├── data/seed/              synthetische Ausgangsdaten (RW-100)
├── data/sample_results.csv Beispiel-Import (löst den Fehler aus Übung 5 aus)
├── logs/                   synthetische Fehlermeldung für Übung 5
├── uebungen/UEBUNGEN.md    Übungsanleitungen 1–7 (+ Zusatzaufgaben)
├── c-review/               eigenständiges C-Beispiel für Code-Review (Übung 6)
├── qms/                    synthetische QMS-Dokumente (Übung 7)
├── cve-demo/               fiktives Advisory + SBOM (Demo «Sind wir betroffen?»)
├── support/                fiktive gelöste Supportfälle (Demo)
├── mcp-demo/               fiktives Ticketsystem als MCP-Server (Demo, eigener Ordner)
├── prototyp/               Ablage für Mockups (Zusatzaufgabe)
├── docs/                   Ablage für Ergebnisse
└── tools/reset_workshop.py Arbeitsdaten zurücksetzen
```

## Bekannte Eigenschaften (absichtlich)

- APP-05 (Abdeckungslücken) ist **noch nicht umgesetzt** → Übung 3.
- Der CSV-Import bricht bei `data/sample_results.csv` mit einem `KeyError` ab → Übung 5.
- `c-review/ringbuffer.c` enthält mehrere Fehler → Übung 6.
- Einige Anforderungen in `REQUIREMENTS.md` sind widersprüchlich oder unpräzise → Übung 2.

## Datenschutz und Sicherheit im Workshop

- Nur mit diesem Repository arbeiten. Keine echten Projekt-, Kunden-, Patienten-, Support- oder Personaldaten in Prompts kopieren.
- Keine Passwörter, Tokens oder Schlüssel in Prompts, Dateien oder Logs.
- Berechtigungsanfragen von Claude Code lesen, bevor Sie zustimmen.
