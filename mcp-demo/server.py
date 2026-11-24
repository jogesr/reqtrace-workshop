#!/usr/bin/env python3
"""Demo-MCP-Server «demo-tickets» – ein FIKTIVES Ticketsystem für den Workshop.

Synthetisches Schulungsmaterial: keine echten Tickets, keine Netzwerkverbindung,
nur Python-Standardbibliothek. Kommuniziert per MCP über stdio (JSON-RPC 2.0,
eine Nachricht pro Zeile).

Werkzeuge:
  list_tickets  – Tickets auflisten (lesend)
  get_ticket    – ein Ticket mit Kommentaren anzeigen (lesend)
  add_comment   – Kommentar schreiben (schreibend) unter dem Konto aus
                  DEMO_TICKET_USER; gespeichert in kommentare.json

Zum Zurücksetzen der Demo: kommentare.json löschen.
"""
import datetime
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TICKETS = HERE / "tickets.json"
COMMENTS = HERE / "kommentare.json"
USER = os.environ.get("DEMO_TICKET_USER") or "workshop.teilnehmer"

TOOLS = [
    {
        "name": "list_tickets",
        "description": "Listet die Tickets des fiktiven Ticketsystems (Schlüssel, Status, Titel). "
                       "Optional nach Status filtern.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "enum": ["offen", "in Arbeit", "erledigt"],
                           "description": "Nur Tickets mit diesem Status"},
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "get_ticket",
        "description": "Liefert ein Ticket mit Beschreibung, Bezug zur Anforderung und allen Kommentaren.",
        "inputSchema": {
            "type": "object",
            "properties": {"key": {"type": "string", "description": "Ticket-Schlüssel, z.B. DEMO-101"}},
            "required": ["key"],
            "additionalProperties": False,
        },
    },
    {
        "name": "add_comment",
        "description": "SCHREIBENDE Aktion: Fügt einem Ticket einen Kommentar hinzu. Der Kommentar erscheint "
                       "unter dem Konto des angemeldeten Benutzers und wird als KI-unterstützt gekennzeichnet.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "key": {"type": "string", "description": "Ticket-Schlüssel, z.B. DEMO-101"},
                "text": {"type": "string", "description": "Kommentartext"},
            },
            "required": ["key", "text"],
            "additionalProperties": False,
        },
    },
]


def load_tickets():
    with open(TICKETS, encoding="utf-8") as f:
        return json.load(f)


def load_comments():
    if not COMMENTS.exists():
        return []
    with open(COMMENTS, encoding="utf-8") as f:
        return json.load(f)


def find(key):
    key = (key or "").strip().upper()
    for t in load_tickets():
        if t["key"] == key:
            return t
    return None


def tool_list_tickets(args):
    status = args.get("status")
    rows = [t for t in load_tickets() if not status or t["status"] == status]
    if not rows:
        return "Keine Tickets gefunden."
    return "\n".join(f"{t['key']} [{t['status']}] {t['titel']}" for t in rows)


def tool_get_ticket(args):
    t = find(args.get("key"))
    if not t:
        raise ValueError(f"Ticket {args.get('key')!r} nicht gefunden.")
    comments = t.get("kommentare", []) + [c for c in load_comments() if c["key"] == t["key"]]
    lines = [
        f"{t['key']} – {t['titel']}",
        f"Status: {t['status']} · Bezug: {t['bezug']} · Gemeldet von: {t['gemeldet_von']}",
        "",
        t["beschreibung"],
        "",
        "Kommentare:" if comments else "Kommentare: keine",
    ]
    for c in comments:
        lines.append(f"- {c['datum']} · {c['autor']}: {c['text']}")
    return "\n".join(lines)


def tool_add_comment(args):
    t = find(args.get("key"))
    if not t:
        raise ValueError(f"Ticket {args.get('key')!r} nicht gefunden.")
    text = (args.get("text") or "").strip()
    if not text:
        raise ValueError("Leerer Kommentar.")
    entry = {
        "key": t["key"],
        "datum": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "autor": USER,
        "text": "[KI-unterstützt, via Claude Code] " + text,
    }
    comments = load_comments()
    comments.append(entry)
    with open(COMMENTS, "w", encoding="utf-8") as f:
        json.dump(comments, f, ensure_ascii=False, indent=2)
    return f"Kommentar in {t['key']} gespeichert – Autor: {USER} (Datei: {COMMENTS.name})."


HANDLERS = {"list_tickets": tool_list_tickets, "get_ticket": tool_get_ticket, "add_comment": tool_add_comment}


def respond(mid, result=None, error=None):
    msg = {"jsonrpc": "2.0", "id": mid}
    if error is not None:
        msg["error"] = error
    else:
        msg["result"] = result
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()


def handle(msg):
    method = msg.get("method")
    mid = msg.get("id")
    params = msg.get("params") or {}
    if mid is None:  # Benachrichtigungen (z.B. notifications/initialized) brauchen keine Antwort
        return
    if method == "initialize":
        respond(mid, {
            "protocolVersion": params.get("protocolVersion", "2025-06-18"),
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "demo-tickets", "version": "1.0.0"},
            "instructions": "Fiktives Ticketsystem für die Workshop-Demo. Alle Daten sind synthetisch.",
        })
    elif method == "ping":
        respond(mid, {})
    elif method == "tools/list":
        respond(mid, {"tools": TOOLS})
    elif method == "tools/call":
        name = params.get("name")
        handler = HANDLERS.get(name)
        if handler is None:
            respond(mid, error={"code": -32602, "message": f"Unbekanntes Werkzeug: {name}"})
            return
        try:
            text = handler(params.get("arguments") or {})
            respond(mid, {"content": [{"type": "text", "text": text}], "isError": False})
        except Exception as exc:  # Fehler als Werkzeug-Ergebnis melden, damit Claude reagieren kann
            respond(mid, {"content": [{"type": "text", "text": f"Fehler: {exc}"}], "isError": True})
    else:
        respond(mid, error={"code": -32601, "message": f"Methode nicht unterstützt: {method}"})


def main():
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            respond(None, error={"code": -32700, "message": "Ungültiges JSON"})
            continue
        handle(msg)


if __name__ == "__main__":
    main()
