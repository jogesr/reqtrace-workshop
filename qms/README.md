# QMS-/Nachweisübung (Übung 7)

> **Synthetisches Material.** Fiktives Produkt «RW-100 Laborrührwerk». Kein Medizinprodukt, keine echten Dokumente, keine echten Personen.
> Die Übung zeigt, wie KI beim **Zuordnen von Nachweisen** und beim **Sichtbarmachen von Lücken** unterstützen kann.
> Sie ersetzt keinen QM-Prozess und liefert **keine Konformitäts- oder Freigabeaussage**.

## Dateien

| Datei | Inhalt |
|---|---|
| `spezifikation_RW100_v0.2_auszug.md` | Ältere Fassung der Produktanforderungen (Auszug) |
| `spezifikation_RW100_v0.3_auszug.md` | Aktuelle Fassung (entspricht `data/seed/requirements.json`) |
| `testplan_RW100_v0.3.md` | Testplan: welche Testfälle welche Anforderungen verifizieren sollen |
| `testbericht_RW100_2026-10.md` | Testbericht mit Ergebnissen – enthält absichtlich Lücken und Ungereimtheiten |
| `nachweis-matrix_vorlage.md` | Vorlage für die Nachweis-Matrix, die in der Übung befüllt wird |

## Markierungsregeln (verbindlich für die Übung)

| Markierung | Bedeutung |
|---|---|
| `[NACHWEIS: Dokument §Abschnitt]` | Konkrete Fundstelle, die von einem Menschen nachgeprüft werden kann |
| `[FEHLT]` | Kein Nachweis in den vorliegenden Dokumenten gefunden |
| `[UNKLAR]` | Widerspruch oder mehrdeutige Angabe zwischen Dokumenten |
| `[ZU PRÜFEN DURCH FACHPERSON]` | Bewertung erfordert fachliche Beurteilung |

Verboten sind Formulierungen wie «konform», «erfüllt die Norm», «freigegeben» oder «Nachweis vollständig», solange kein Mensch dies im regulären Prozess festgestellt hat.
