# C-Review-Beispiel: Ringpuffer (Übung 6)

> Synthetisches, eigenständiges Beispiel. Enthält **absichtlich** Fehler. Nicht in echter Firmware verwenden.

Ein kleiner Ringpuffer für 16-Bit-Messwerte (z.B. Stromwerte eines fiktiven Antriebs) mit `rb_init`, `rb_push`, `rb_pop` und `rb_average`.

## Bauen und testen

```bash
cd c-review
gcc -std=c99 -Wall -Wextra -o test_rb ringbuffer.c test_ringbuffer.c
./test_rb
```

Optional (falls verfügbar):

```bash
gcc -std=c99 -Wall -Wextra -fanalyzer -c ringbuffer.c
cppcheck --enable=warning,style ringbuffer.c
```

Ohne C-Compiler: Review trotzdem durchführen, Befunde aber als «nicht durch Test belegt» kennzeichnen.

## Auftrag

Siehe `uebungen/UEBUNGEN.md`, Übung 6. Wichtig: Jeder Review-Befund ist zunächst eine **Hypothese**. Belegen oder widerlegen Sie ihn mit einem Test, einem Compiler-/Analysewerkzeug oder einer nachvollziehbaren Begründung.
