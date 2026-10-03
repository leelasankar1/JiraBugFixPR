# Discount App

Small Python project containing a percentage discount calculator and a mock
stdio JIRA MCP server for the `PROJ-102` demo.

## Structure

- `src/discount_app/discount.py` — discount calculation and validation.
- `src/discount_app/mock_jira_mcp.py` — mock JIRA MCP server.
- `tests/test_discount.py` — calculator regression tests.
- `discount.py` and `mock_jira_mcp.py` — compatibility entry points for the
  original flat-file layout.

## Install and run

```powershell
python -m pip install -e ".[test]"
python -m pytest
python mock_jira_mcp.py
```

`apply_discount(price, percent)` returns a two-decimal string. For example,
`apply_discount("10.00", 50)` returns `"5.00"`. Discounts reduce the price by
multiplying by `1 - percent / 100`; a 0% discount leaves the price unchanged,
and a 100% discount returns `"0.00"`.
"# JiraBugFixPR" 
