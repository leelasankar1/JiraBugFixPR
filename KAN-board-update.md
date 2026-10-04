# KAN Board Update

## Current Jira statuses

- **KAN-1** — Done
- **KAN-2** — In Progress
- **KAN-4** — Done

## KAN-4 resolution

KAN-4 reported that a 50% discount on `10.00` increased the price to `15.00`. The discount calculation in `src/discount_app/discount.py` uses `1 - percent / 100`, so `apply_discount("10.00", 50)` returns `5.00`.

The implementation is already present on `main`. This PR contains documentation updates only and does not change the calculator code.

## Prior verification

A previous run recorded 14 passing tests. No tests were run for this documentation-only update.

## Pull request history

PR #1 containing the README documentation update has been merged to `main`.
