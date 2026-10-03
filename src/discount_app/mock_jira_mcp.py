"""Minimal stdio MCP server that serves a single mock JIRA ticket.

Lets the jira-bugfix demo run end-to-end without a real Jira instance.
Implements just enough of the MCP protocol (tools/list, tools/call) to back
the `get_issue` tool.

Usage:
    python3 mock_jira_mcp.py

Test with a JSON-RPC message on stdin:
    printf '%s' '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | python3 mock_jira_mcp.py
"""

import json
import sys
from pathlib import Path

TICKETS = {}

_ticket_path = Path(__file__).resolve().parents[2] / "PROJ-102.json"
if _ticket_path.exists():
    TICKETS[_ticket_path.stem] = json.loads(_ticket_path.read_text())

TOOLS = [
    {
        "name": "get_issue",
        "description": "Fetch a JIRA issue by its key (e.g. PROJ-102) as a JSON object.",
        "inputSchema": {
            "type": "object",
            "properties": {"key": {"type": "string"}},
            "required": ["key"],
        },
    }
]


def handle(msg):
    """Return the JSON-RPC result for one MCP request, or None for notifications."""
    method = msg.get("method")
    params = msg.get("params", {})

    if method == "initialize":
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "mock-jira", "version": "1.0.0"},
        }

    if method == "notifications/initialized":
        return None

    if method == "ping":
        return {}

    if method == "tools/list":
        return {"tools": TOOLS}

    if method == "tools/call":
        args = params.get("arguments", {})
        key = args.get("key", "").upper()
        ticket = TICKETS.get(key)
        if not ticket:
            return {
                "content": [{"type": "text", "text": f"issue {key} not found"}],
                "isError": True,
            }
        return {"content": [{"type": "text", "text": json.dumps(ticket)}]}

    raise ValueError(f"unsupported method: {method}")


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except ValueError:
            continue
        rid = msg.get("id")
        try:
            result = handle(msg)
        except ValueError as exc:
            if rid is None:
                continue
            response = {
                "jsonrpc": "2.0",
                "id": rid,
                "error": {"code": -32601, "message": str(exc)},
            }
        else:
            if rid is None:
                continue
            response = {"jsonrpc": "2.0", "id": rid, "result": result}
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()

