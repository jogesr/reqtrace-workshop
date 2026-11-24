# Übungen – Agentic Engineering mit Claude Code

> Synthetisches Schulungsmaterial. KI-generiert mit Claude Code, vom Workshop-Leiter geprüft.
> Die Übungen bauen aufeinander auf. Wer einen Schritt nicht fertig bekommt, erhält vom Workshop-Leiter den Lösungsstand und macht mit dem nächsten Schritt weiter.

## Arbeitsregeln für alle Übungen

1. **Vor jeder Übung:** `git status` sauber? Sonst committen (`git add . && git commit -m "…"`) oder `git stash`.
2. **Prompts kopieren, dann bewusst anpassen** – die Prompts sind Ausgangspunkte, keine Zauberformeln.
3. **Berechtigungsanfragen lesen**, bevor Sie zustimmen. Im Zweifel ablehnen und nachfragen.
4. **Ergebnis prüfen:** `git diff`, Tests ausführen, Aussagen am Code oder Dokument nachprüfen.
5. **Nur synthetische Daten.** Keine echten Projekt- oder Personendaten in Prompts.

**Ohne Claude-Code-Lizenz?** Sie arbeiten im Tandem als Prüfer/in (Akzeptanzkriterien, Belege, Diff). Während Übung 3b–5 können Sie stattdessen Z4 (HW-Entwicklung) oder Z5 (Projektleitung) bearbeiten. Ü2, Ü6a, Ü7, Z4 und Z5 gehen auch im Claude-Chat mit Datei-Upload – aber nur, wenn Ihre IT das freigegeben hat, mit abgewähltem Modelltraining und nur mit diesen synthetischen Dateien. Im Chat statt `@datei` die Dateien hochladen und «Erstelle …» durch «Gib … aus» ersetzen.

Nützlich: `Shift+Tab` schaltet zwischen den Modi um (u.a. Plan Mode) · `@datei` bindet eine Datei ein · `/clear` startet einen frischen Kontext · `Esc Esc` bzw. `/rewind` springt zu einem früheren Stand zurück (ersetzt Git nicht).

---

## Übung 1 – Repository verstehen und Plan erstellen (25 min)

**Lernziel:** Ein unbekanntes Repository mit Claude Code erkunden, ohne etwas zu ändern, und Aussagen am Code belegen lassen.
**Startzustand:** frisch geklonter Startzustand, Tests grün.

1. `claude` im Ordner `reqtrace-workshop` starten. Mit `Shift+Tab` in den **Plan Mode** wechseln.
2. Prompt:

```text
Du arbeitest in einem Schulungs-Repository. Ändere in diesem Schritt KEINE Dateien.
Ziel: Ich will das Projekt verstehen, bevor wir es erweitern.
1. Fasse in höchstens 10 Punkten zusammen, was die App tut und wie sie aufgebaut ist
   (Module und Datenfluss von data/ bis zur CLI und Weboberfläche).
2. Erkläre, wie die Tests ausgeführt werden.
3. Vergleiche REQUIREMENTS.md mit dem Code: Welche APP-Anforderungen sind umgesetzt,
   welche nicht? Nenne für jede Aussage Datei und Funktion als Beleg.
4. Skizziere einen Plan mit höchstens 6 Schritten, wie APP-05 umgesetzt werden könnte.
Kennzeichne Vermutungen ausdrücklich als Vermutung.
```

3. Plan Mode verlassen und Tests ausführen lassen: `Führe die Tests aus und berichte das Ergebnis.`

**Akzeptanzkriterien**
- [ ] Zusammenfassung nennt die Module `models`, `storage`, `trace`, `importer`, `cli`, `server`.
- [ ] APP-05 wird als nicht umgesetzt erkannt, mit Beleg.
- [ ] Mindestens zwei Aussagen haben Sie selbst im Code nachgeprüft.
- [ ] `git status` zeigt keine Änderungen.

**Zusatz:** Fragen Sie: `Welche Teile des Codes würdest du als riskant für Änderungen einschätzen und warum?` – und prüfen Sie die Begründung.

---

## Übung 2 – Anforderungen prüfen (25 min)

**Lernziel:** Anforderungen KI-gestützt auf Eindeutigkeit, Vollständigkeit, Prüfbarkeit und Widersprüche analysieren und Befunde belegen.
**Startzustand:** wie nach Übung 1.

```text
Analysiere REQUIREMENTS.md als Requirements-Reviewer. Ändere keine bestehenden Dateien.
Prüfe jede Anforderung APP-01 bis APP-11 auf Eindeutigkeit, Vollständigkeit, Prüfbarkeit,
Widersprüche zu anderen Anforderungen und Abweichungen zum aktuellen Code.
Lege docs/offene-fragen.md an mit einer Tabelle:
ID | Kategorie | Befund | Beleg (Zitat oder Datei:Funktion) | Frage an Product Owner | Vorschlag für prüfbare Formulierung
Regeln: Erfinde keine neuen Anforderungen. Wenn eine Anforderung in Ordnung ist, sag das.
Begründe jeden Befund mit einem Zitat. Nenne zum Schluss die 3 wichtigsten offenen Fragen.
```

Danach Gegenprüfung: `Welche deiner Befunde sind am unsichersten und warum?`

**Akzeptanzkriterien**
- [ ] `docs/offene-fragen.md` existiert, jede Zeile hat einen Beleg.
- [ ] Der Widerspruch zwischen APP-05 und APP-08 (verworfene Anforderungen, Begriff «abgedeckt») ist erkannt.
- [ ] APP-07, APP-09, APP-10 sind als unpräzise bzw. unvollständig markiert.
- [ ] Sie haben mindestens einen Befund gefunden, dem Sie **nicht** zustimmen – und begründen können, warum.

**Zusatz:** Lassen Sie für APP-07 drei alternative, messbare Formulierungen vorschlagen und wählen Sie eine.

---

## Übung 3 – Feature APP-05 planen und umsetzen (3a: 10 min · 3b: 45 min Umsetzung + 15 min Diff-Review, Mittagspause dazwischen)

**Lernziel:** Ein kleines Feature mit Plan, Randbedingungen, Akzeptanzkriterien und Verifikation umsetzen lassen und den Diff kritisch reviewen.
**Startzustand:** Startzustand (+ ggf. `docs/offene-fragen.md`). Vorher committen.

**3a – Plan (Plan Mode):**

```text
Wir setzen APP-05 aus REQUIREMENTS.md um (Abdeckungslücken). Erstelle zuerst nur einen Plan,
ändere noch nichts.
Kontext: @REQUIREMENTS.md @reqtrace/trace.py @reqtrace/cli.py @reqtrace/server.py @tests/test_trace.py
Der Plan enthält: betroffene Dateien, neue Funktion(en) mit Signatur, Testfälle (Unit, CLI, API)
und offene Fragen.
```

**3b – Umsetzung** (nach Durchsicht des Plans):

```text
Setze den Plan für APP-05 um.
Ziel: Funktion find_gaps in reqtrace/trace.py, CLI-Befehl `gaps`, API GET /api/gaps
und ein Abschnitt «Abdeckungslücken» in reqtrace/static/index.html.
Randbedingungen:
- Nur Python-Standardbibliothek, bestehenden Stil beibehalten, keine anderen Funktionen umbauen.
- Anforderungen mit Status "verworfen" ignorieren, Ausgabe nach ID sortiert,
  die CLI meldet ausdrücklich, wenn es keine Lücken gibt.
Akzeptanzkriterien:
- `python -m reqtrace gaps` listet mit den Seed-Daten genau REQ-007 und REQ-010.
- GET /api/gaps liefert dieselben IDs als JSON.
- Neue Tests in tests/test_gaps.py (unittest, tests/helpers.py nutzen) decken ab: Lücke,
  verworfen, verknüpft aber nicht ausgeführt, Sortierung, Meldung «keine Lücken», CLI und API.
Verifikation: Führe `python -m unittest` aus und zeige das Ergebnis.
Zeige danach `git diff --stat` und fasse die Änderungen zusammen. Nicht committen.
```

**Review-Checkliste (selbst durchführen, nicht delegieren):**
- [ ] `git diff` gelesen: Nur die erwarteten Dateien geändert? Keine «Nebenbei-Umbauten»?
- [ ] `python -m reqtrace gaps` selbst ausgeführt; `python -m reqtrace serve` im Browser geprüft.
- [ ] Die Tests prüfen wirklich das Verhalten (nicht nur «läuft ohne Fehler»).
- [ ] Alle Tests grün – selbst ausgeführt, nicht nur der Aussage geglaubt.
- [ ] Danach committen: `git commit -am "APP-05: Abdeckungslücken"` (neue Dateien vorher mit `git add`).

**Zusatz:** `Ergänze eine Option --priority für den Befehl gaps.` – zuerst Akzeptanzkriterien selbst formulieren.

---

## Übung 4 – Tests aus Anforderungen ableiten (22 min)

**Lernziel:** Systematisch (Äquivalenzklassen, Grenzwerte) Unit- und Integrationstests aus einer Anforderung ableiten und Abweichungen richtig einordnen.
**Startzustand:** nach Übung 3 (oder Lösungsstand Ü3).

```text
Leite aus APP-02 in REQUIREMENTS.md systematisch Testfälle ab.
1. Erstelle zuerst eine Testentwurfstabelle (Äquivalenzklassen und Grenzwerte: gültige und
   ungültige IDs, Priorität, Status, Duplikate, Fehlermeldung, Verhalten der CLI bei Datenfehlern).
   Gib zu jedem Testfall an, welchen Satz aus APP-02 er prüft.
2. Warte auf mein OK, bevor du Code schreibst.
3. Implementiere die Tests in tests/test_app02_validation.py (unittest, tests/helpers.py nutzen).
   Ändere keinen Produktivcode.
4. Führe die Tests aus. Wenn ein Test fehlschlägt: Passe nicht den Test an, sondern berichte,
   ob Code oder Anforderung abweicht.
```

**Akzeptanzkriterien**
- [ ] Testentwurf enthält gültige Grenzwerte (`REQ-000`, `REQ-999`) und mehrere ungültige Klassen (Kleinschreibung, zu wenige/viele Ziffern, Leerzeichen, falsches Präfix).
- [ ] Mindestens ein Integrationstest (Laden aus Datei oder CLI-Exit-Code 2).
- [ ] Jeder Test referenziert APP-02.
- [ ] Alle Tests grün, Produktivcode unverändert (`git diff reqtrace/` leer).

**Zusatz:** Welche Sätze aus APP-02 sind **nicht** testbar formuliert? («verständliche Fehlermeldung»)

---

## Übung 5 – Fehlersuche mit Log und Stacktrace (17 min)

**Lernziel:** Einen gemeldeten Fehler reproduzieren, die Ursache belegen, zuerst einen fehlschlagenden Test schreiben und minimal korrigieren.
**Startzustand:** nach Übung 4. Vorher `python tools/reset_workshop.py`.

```text
Im Testlabor bricht der Import von Testergebnissen ab. Fehlermeldung, Logauszug und Stacktrace:
@logs/testlabor_import_2026-11-02.log
1. Reproduziere den Fehler mit `python -m reqtrace import-results data/sample_results.csv`.
2. Ermittle die Ursache. Prüfe auch, welche weiteren Zeilen in data/sample_results.csv
   problematisch sind, und vergleiche das Verhalten mit APP-06.
3. Schreibe zuerst Regressionstests in tests/test_importer.py, die vor dem Fix fehlschlagen.
   Zeige mir den Fehlschlag.
4. Behebe den Fehler minimal in reqtrace/importer.py gemäss APP-06.
5. Führe alle Tests aus. Erkläre, warum nach dem Absturz auch Ergebnisse früherer Zeilen fehlten.
Ändere data/sample_results.csv nicht.
```

**Akzeptanzkriterien**
- [ ] Ursache benannt: IDs werden nicht normalisiert, unbekannte IDs führen zu `KeyError` statt Warnung.
- [ ] Tests schlugen vor dem Fix nachweislich fehl.
- [ ] Nach dem Fix: `python tools/reset_workshop.py` und Import liefert `5 Testfälle aktualisiert, 1 Zeilen übersprungen`.
- [ ] Erklärung: Gespeichert wird erst am Ende, der Absturz verhindert das Speichern.

**Zusatz:** Soll ein Import «alles oder nichts» sein? Notieren Sie das als offene Frage zu APP-06.

---

## Übung 6 – Code-Review eines C-Moduls (20 min)

**Lernziel:** KI-Review-Befunde als Hypothesen behandeln und mit Tests oder Werkzeugen bestätigen oder widerlegen.
**Startzustand:** Ordner `c-review/` (unabhängig von der App).

**6a – Review (nichts ändern):**

```text
Führe ein Code-Review von @c-review/ringbuffer.c und @c-review/ringbuffer.h durch.
Kontext: Messwertpuffer auf einem Mikrocontroller, C99, keine dynamische Speicherverwaltung.
Ausgabe als Tabelle: Nr | Zeile | Befund | Schwere (hoch/mittel/niedrig) |
Wie belegbar (Test, Werkzeug, Begründung) | Korrekturvorschlag.
Trenne klar zwischen sicheren Fehlern, möglichen Problemen und Stilfragen. Ändere noch nichts.
```

**6b – Belegen und korrigieren:**

```text
Belege die Befunde mit Schwere "hoch": Ergänze c-review/test_ringbuffer.c um Tests, die mit dem
aktuellen Code fehlschlagen. Kompiliere im Ordner c-review mit
`gcc -std=c99 -Wall -Wextra -o test_rb ringbuffer.c test_ringbuffer.c` und führe ./test_rb aus.
Berichte, welche Befunde bestätigt, widerlegt oder nicht testbar sind.
Korrigiere danach ringbuffer.c minimal und führe die Tests erneut aus.
```

**Akzeptanzkriterien**
- [ ] Off-by-one in `rb_push` (Kapazität und Index-Umlauf) durch fehlschlagenden Test belegt.
- [ ] Überlauf der Summe in `rb_average` belegt.
- [ ] Division durch null und `strcpy`-Überlauf erkannt.
- [ ] Mindestens ein KI-Befund ist als Stilfrage oder Falsch-Positiv eingeordnet.
- [ ] Nach der Korrektur: `Alle Tests bestanden.`

**Ohne gcc:** nur 6a durchführen und Befunde als «nicht durch Test belegt» kennzeichnen.
**Zusatz:** `gcc -fanalyzer -c ringbuffer.c` – was findet das Werkzeug, was nicht?

---

## Übung 7 – QMS: Nachweise zuordnen, Lücken markieren (12 min)

**Lernziel:** Nachweise aus mehreren Dokumenten zuordnen, Widersprüche und fehlende Evidenz transparent markieren – ohne Konformitätsaussage.
**Startzustand:** Ordner `qms/`.

```text
Unterstütze mich beim Erstellen einer Nachweis-Matrix.
Material: @qms/README.md @qms/spezifikation_RW100_v0.3_auszug.md @qms/testplan_RW100_v0.3.md
@qms/testbericht_RW100_2026-10.md
1. Erstelle qms/nachweis-matrix_entwurf.md nach der Vorlage qms/nachweis-matrix_vorlage.md:
   für REQ-001 bis REQ-012 geplanter Testfall, Ergebnis, Fundstelle (Dokument und Abschnitt)
   und offene Punkte.
2. Liste dokumentübergreifende Ungereimtheiten (Versionen, Unterschriften, Kalibrierung,
   Testfälle ohne Plan …).
3. Vergleiche spezifikation_RW100_v0.2_auszug.md mit v0.3 und prüfe, ob der Testbericht gegen
   die richtige Version bewertet.
Regeln: Verwende ausschliesslich die Markierungen aus qms/README.md. Erfinde keine Nachweise,
Dokumentnummern oder Personen. Keine Aussagen wie «konform», «erfüllt» oder «freigegeben».
Wenn etwas fehlt, schreibe [FEHLT].
```

**Akzeptanzkriterien**
- [ ] Alle 12 Anforderungen in der Matrix, jede Fundstelle nachprüfbar.
- [ ] Erkannt: Firmware-Version 1.2.1 vs. 1.3.0, TC-011 ohne Plan, fehlende Kalibrierung Strommesszange, fehlende Unterschrift, fehlende AB-Nummer zu TC-003.
- [ ] Erkannt: TC-002 «bestanden» mit 2,4 % bei ±2 % gemäss v0.3.
- [ ] Keine Konformitäts- oder Freigabeaussage im Text.
- [ ] Mindestens drei Fundstellen selbst nachgeprüft.

---

## Zusatzaufgaben für Schnelle

**Z1 – Mockup:**

```text
Erstelle prototyp/gaps-dashboard.html: einen klickbaren, statischen HTML-Mockup in einer Datei
(kein externes CSS/JS, keine Netzwerkzugriffe) für ein Dashboard «Abdeckungslücken» mit
Filter nach Priorität, Liste der Lücken und Detailansicht. Verwende die Daten aus data/seed/
statisch eingebettet. Zeige sichtbar den Hinweis «Mockup – nicht funktional».
```

**Z2 – Supportwissen:**

```text
Lies @support/neue_anfrage.md und die gelösten Fälle in support/tickets/. Finde die ähnlichsten
Fälle (mit Begründung), liste fehlende Angaben auf und erstelle einen Antwortentwurf in
support/antwortentwurf.md. Kennzeichne jede Aussage, die nicht durch einen Ticket-Text belegt ist,
als unsicher.
```

**Z3 – Sind wir betroffen? (CVE/VEX):**

```text
Ein Scanner meldet für @cve-demo/sbom.cdx.json, dass demotinycsv 1.4.2 von
@cve-demo/advisory_DEMO-ADV-2026-0001.md betroffen ist.
Prüfe service_a, service_b und service_c einzeln: Wird read_rows_with_formulas erreicht – auch
indirekt, dynamisch oder konfigurationsabhängig? Wer kontrolliert die Eingabedaten?
Schlage je Service einen VEX-Status vor (not_affected mit Begründung, affected,
under_investigation), mit Beleg (Datei:Zeile) und offenen Fragen. Triff keine endgültige Entscheidung.
```

---

## Zusatzaufgaben für HW-Entwicklung und Projektleitung

Beide Aufgaben funktionieren mit Claude Code, im Chat mit Datei-Upload (nur mit IT-Freigabe) oder als Papier-Review. Dauer je 20–40 min, unabhängig von der App.

**Z4 – Hardware: Spezifikation, Firmware und Netzliste abgleichen** (Ordner `hardware/`)

```text
Gleiche drei Quellen zur Steuerplatine RW-100 ab:
@hardware/schnittstellen-spec_RW100.md @hardware/rw100_pins.h @hardware/netzliste_RW100.csv
Bezug zu den Produktanforderungen: @qms/spezifikation_RW100_v0.3_auszug.md
1. Erstelle hardware/befunde.md mit einer Tabelle: Nr | Signal/Grösse | Spezifikation | Header |
   Netzliste | Befund | Fundstellen (Datei und Zeile/Abschnitt) | Markierung | mögliche Folge (REQ-xxx).
2. Prüfe Pinbelegung, aktive Pegel, Frequenzen, Grenzwerte (rechne Herleitungen nach) und
   fehlende Signale.
3. Verwende nur die Markierungen aus hardware/README.md. Wenn unklar ist, welche Quelle stimmt,
   markiere [UNKLAR] und entscheide nicht selbst.
Ändere keine der drei Quelldateien.
```

**Akzeptanzkriterien**
- [ ] Jeder Befund hat mindestens zwei Fundstellen.
- [ ] Mindestens ein Grenzwert ist von Hand nachgerechnet.
- [ ] Widersprüche ohne klare Referenz sind als [UNKLAR] markiert, nicht «korrigiert».
- [ ] Mindestens drei Befunde selbst in den Dateien nachgeprüft – auch, ob ein Befund falsch ist.

**Z5 – Projektleitung: Statusnotiz mit Belegen** (Ordner `qms/`)

```text
Erstelle eine einseitige Statusnotiz zur Verifikation RW-100 für die Projektleitung in
qms/statusnotiz_entwurf.md.
Material: @qms/README.md @qms/spezifikation_RW100_v0.3_auszug.md @qms/testplan_RW100_v0.3.md
@qms/testbericht_RW100_2026-10.md
Inhalt: Kurzfassung (3–4 Sätze), Fortschritt in Zahlen (geplant, durchgeführt, bestanden,
nicht bestanden, blockiert, offen), Top-5-Risiken mit Beleg und vorgeschlagenem nächstem Schritt,
Abschnitt «Was diese Notiz nicht aussagt».
Regeln: Jede Zahl und jede Aussage mit Fundstelle. Verwende nur die Markierungen aus qms/README.md.
Erfinde keine Personen, Termine oder Dokumentnummern – fehlt etwas, schreibe [FEHLT].
Keine Aussagen wie «konform», «erfüllt», «freigegeben» und keine Ampel «grün».
```

**Akzeptanzkriterien**
- [ ] Zahlen selbst nachgezählt (Testplan und Testbericht).
- [ ] Nicht bestandene und blockierte Tests sowie die Firmware-Versionen sind erwähnt.
- [ ] Keine erfundenen Verantwortlichen oder Termine.
- [ ] Keine Freigabe- oder Konformitätsaussage.
