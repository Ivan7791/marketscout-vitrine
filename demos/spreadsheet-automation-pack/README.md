# Spreadsheet Automation Pack — demo

This is a small offline demo for recurring sales/reporting workflows.

It takes a CSV export of orders, calculates revenue and profit by channel, flags non-paid orders and low-margin rows, then writes:

- `sample_report.md`
- `sample_report.json`

This is a concept/demo asset. A real client version needs their exact exports, formulas, columns, and reporting rules.

## Run

```bash
python build_report.py
```
