# Discount App

A small Python project that demonstrates a currency-safe percentage discount calculation and a stdio mock Jira MCP server for issue `PROJ-102`.

## Project overview

The calculator accepts a price and discount percentage, validates both inputs, and returns a two-decimal currency string. It uses `Decimal` instead of binary floating point and rounds half up to the nearest cent. The MCP server exposes a single `get_issue` tool and reads its ticket fixture from `PROJ-102.json`.

## Repository layout

- `src/discount_app/discount.py` contains input conversion, validation, arithmetic, and currency rounding.
- `src/discount_app/mock_jira_mcp.py` implements the line-oriented stdio JSON-RPC mock server.
- `tests/test_discount.py` covers discount boundaries, rounding, and invalid inputs.
- `PROJ-102.json` stores the mock Jira issue served by the MCP tool.
- `discount.py` and `mock_jira_mcp.py` preserve the original flat-file entry points.
- `docs/INTERVIEW_GUIDE.md` contains a demo script and interview talking points.

## Requirements

Python 3.9 or newer. The application has no runtime dependencies. Pytest is needed only for the optional test extra.

## Install and run

```powershell
python -m pip install -e ".[test]"
python -m pytest
```

Calculate a discount from Python:

```python
from discount_app.discount import apply_discount

print(apply_discount("10.00", 50))  # 5.00
```

Start the mock Jira MCP server:

```powershell
python mock_jira_mcp.py
```

The server reads newline-delimited JSON-RPC messages from standard input and writes responses to standard output. It supports `initialize`, `notifications/initialized`, `ping`, `tools/list`, and `tools/call` for `get_issue`.

## Calculation rules

For price `P` and percentage `r`, the result is `P × (1 − r / 100)`, rounded to two decimal places with `ROUND_HALF_UP`. Prices must be finite and non-negative. Percentages must be finite and between 0 and 100 inclusive. Invalid inputs raise `ValueError`.

Examples:

| Price | Discount | Result |
| ---: | ---: | ---: |
| 10.00 | 0% | 10.00 |
| 10.00 | 50% | 5.00 |
| 9.99 | 10% | 8.99 |
| 9.99 | 100% | 0.00 |

## Current scope

The Jira server is a local demo fixture, not a production Jira integration. It serves the checked-in ticket only and implements the MCP methods needed by this demonstration. The calculator is a small library function without a command-line interface or web UI.

## Project notes

The repository's `KAN-board-update.md` records a previous run with 14 passing tests and notes that the correction was already present on `main` at that time. That status is historical; consult the current source and run the commands above for a fresh verification.
