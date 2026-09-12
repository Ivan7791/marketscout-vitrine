import csv
import json
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent
INPUT = BASE / "sample_orders.csv"
OUT_MD = BASE / "sample_report.md"
OUT_JSON = BASE / "sample_report.json"

rows = []
with INPUT.open(newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        row["revenue"] = float(row["revenue"])
        row["cost"] = float(row["cost"])
        row["profit"] = row["revenue"] - row["cost"]
        rows.append(row)

by_channel = defaultdict(lambda: {"orders": 0, "revenue": 0.0, "profit": 0.0})
flags = []
for row in rows:
    channel = row["channel"]
    by_channel[channel]["orders"] += 1
    by_channel[channel]["revenue"] += row["revenue"]
    by_channel[channel]["profit"] += row["profit"]
    if row["status"] != "paid":
        flags.append({"order_id": row["order_id"], "status": row["status"], "reason": "needs follow-up"})
    if row["profit"] / row["revenue"] < 0.6:
        flags.append({"order_id": row["order_id"], "status": row["status"], "reason": "margin below 60%"})

summary = {
    "total_orders": len(rows),
    "total_revenue": round(sum(r["revenue"] for r in rows), 2),
    "total_profit": round(sum(r["profit"] for r in rows), 2),
    "by_channel": {k: {kk: round(vv, 2) if isinstance(vv, float) else vv for kk, vv in v.items()} for k, v in by_channel.items()},
    "flags": flags,
}

lines = [
    "# Sample Sales Operations Report",
    "",
    f"Total orders: **{summary['total_orders']}**",
    f"Total revenue: **${summary['total_revenue']:,.2f}**",
    f"Estimated profit: **${summary['total_profit']:,.2f}**",
    "",
    "## Revenue by channel",
    "",
    "| Channel | Orders | Revenue | Profit |",
    "|---|---:|---:|---:|",
]
for channel, data in sorted(summary["by_channel"].items()):
    lines.append(f"| {channel} | {data['orders']} | ${data['revenue']:,.2f} | ${data['profit']:,.2f} |")
lines += ["", "## Follow-up flags", ""]
if flags:
    for flag in flags:
        lines.append(f"- Order {flag['order_id']}: {flag['reason']} ({flag['status']}).")
else:
    lines.append("No follow-up flags.")

OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(f"Wrote {OUT_MD}")
print(f"Wrote {OUT_JSON}")
