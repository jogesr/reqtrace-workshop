# Hardware-Abgleich (Zusatzaufgabe Z4)

> **Synthetisches Material.** Fiktives Produkt «RW-100 Laborrührwerk», fiktiver Mikrocontroller, fiktive Bauteile. Kein Medizinprodukt, keine echten Schaltpläne.
> Die Aufgabe zeigt, wie KI beim **Abgleich von Spezifikation, Firmware und Schaltung** helfen kann. Sie ersetzt kein Design-Review.

## Dateien

| Datei | Inhalt |
|---|---|
| `schnittstellen-spec_RW100.md` | Schnittstellen-Spezifikation der Steuerplatine (Pinbelegung, Pegel, Grenzwerte) |
| `rw100_pins.h` | Firmware-Header mit Pinbelegung und Grenzwerten (C99) |
| `netzliste_RW100.csv` | Auszug aus der Netzliste der Steuerplatine (Semikolon-getrennt) |

Bezug zu den Produktanforderungen: `../qms/spezifikation_RW100_v0.3_auszug.md` (REQ-xxx).

## Markierungen für die Befundliste

| Markierung | Bedeutung |
|---|---|
| `[BESTÄTIGT: Datei Zeile/Abschnitt]` | Abweichung an mindestens zwei Stellen nachgeprüft |
| `[WIDERLEGT]` | Vermuteter Befund trifft nicht zu (mit Begründung) |
| `[UNKLAR]` | Widerspruch, aber unklar, welche Quelle stimmt – Klärung durch Fachperson |
| `[NICHT PRÜFBAR]` | Aus diesen Dokumenten nicht zu beurteilen |
