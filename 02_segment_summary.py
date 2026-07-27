"""
Quick summary script — run AFTER 01_rfm_analysis.py has generated
exports/rfm_segments.csv.

This pulls the real revenue/customer numbers per segment so you can
plug them straight into your README's "Insights & Recommendations"
section instead of using placeholder text.

Run from the same folder as your other scripts:
    python 02_segment_summary.py
"""

import pandas as pd

rfm = pd.read_csv("exports/rfm_segments.csv")

total_customers = len(rfm)
total_revenue = rfm["monetary"].sum()

summary = rfm.groupby("segment").agg(
    num_customers=("customer_id", "count"),
    total_revenue=("monetary", "sum"),
    avg_revenue_per_customer=("monetary", "mean"),
).round(2)

summary["pct_of_customers"] = (summary["num_customers"] / total_customers * 100).round(1)
summary["pct_of_revenue"] = (summary["total_revenue"] / total_revenue * 100).round(1)

# Reorder columns nicely and sort by revenue contribution
summary = summary[
    ["num_customers", "pct_of_customers", "total_revenue", "pct_of_revenue", "avg_revenue_per_customer"]
].sort_values("total_revenue", ascending=False)

print(f"Total customers: {total_customers:,}")
print(f"Total revenue (all segments): {total_revenue:,.2f}\n")
print(summary.to_string())

summary.to_csv("exports/segment_summary.csv")
print("\nSaved: exports/segment_summary.csv")

print("\n--- Ready-to-paste README bullets ---\n")
for seg, row in summary.iterrows():
    print(
        f"- **{seg}** ({row['pct_of_customers']}% of customers, "
        f"{int(row['num_customers'])} total) contributes "
        f"{row['pct_of_revenue']}% of total revenue "
        f"(avg {row['avg_revenue_per_customer']:.2f} per customer)."
    )
