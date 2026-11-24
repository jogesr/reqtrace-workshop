# MCP-Demo: fiktives Ticketsystem «demo-tickets»

> **Alles synthetisch:** Tickets, Personen und Kommentare sind erfunden. Der Server läuft lokal,
> baut keine Netzwerkverbindung auf und braucht nur die Python-Standardbibliothek.

Die Demo zeigt in 3 Minuten, was MCP ist: Claude Code nutzt die Werkzeuge eines externen Systems –
hier ein nachgebautes Ticketsystem anstelle von Jira.

## Inhalt

| Datei | Zweck |
|---|---|
| `.mcp.json` | meldet den Server `demo-tickets` für Claude Code an (Projekt-Konfiguration) |
| `server.py` | MCP-Server (stdio) mit den Werkzeugen `list_tickets`, `get_ticket`, `add_comment` |
| `tickets.json` | vier fiktive Tickets mit Bezug zu den APP-Anforderungen |
| `kommentare.json` | entsteht beim ersten `add_comment`; zum Zurücksetzen löschen |

## Ablauf

1. **In diesem Ordner** starten (nur hier wird `.mcp.json` gelesen):

   ```bash
   cd mcp-demo
   claude
   ```

2. Beim Start fragt Claude Code, ob der Server aus `.mcp.json` verwendet werden darf → **freigeben**.
   Zeigen: Projekt-Server müssen bewusst erlaubt werden.
3. `/mcp` eingeben: Server `demo-tickets` ist verbunden, drei Werkzeuge.
4. Lesen:

   ```text
   Welche Tickets sind offen? Fasse DEMO-101 in zwei Sätzen zusammen.
   ```

   Claude fragt vor dem ersten Aufruf eines Werkzeugs nach Erlaubnis (`mcp__demo-tickets__…`).
5. Schreiben:

   ```text
   Schreibe in DEMO-101 einen Kommentar: Ursache vermutlich Gross-/Kleinschreibung der
   Testfall-IDs im Import, Fix mit Regressionstest folgt.
   ```

   Die Berechtigungsanfrage für `add_comment` lesen und bestätigen.
6. Ergebnis zeigen: `kommentare.json` öffnen – Autor ist **Ihr Windows-Benutzername**
   (`DEMO_TICKET_USER`), Text ist als «KI-unterstützt» gekennzeichnet.

## Botschaft

- MCP ist ein offener Standard: Ein Server stellt Werkzeuge bereit, Claude Code ruft sie auf.
- Jeder Aufruf läuft über die normalen Berechtigungen – lesen und schreiben getrennt bestätigen.
- Bei echten Systemen (z.B. Atlassian Rovo MCP Server) arbeitet Claude mit **Ihrem** Konto und
  **Ihren** Rechten; Änderungen erscheinen unter Ihrem Namen.

## Hinweise

- `python` muss im PATH sein (unter macOS/Linux ggf. in `.mcp.json` `python3` eintragen).
- Freigabe zurücksetzen (für einen erneuten Probelauf): `claude mcp reset-project-choices`.
- Server ohne Claude testen: `claude mcp list` im Ordner `mcp-demo` zeigt den Verbindungsstatus.
