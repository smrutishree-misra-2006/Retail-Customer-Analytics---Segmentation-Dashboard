"""
RFM (Recency, Frequency, Monetary) Customer Segmentation
+ Cohort Retention Analysis

This pulls cleaned data straight from MySQL (via the clean_transactions
view) so all the cleaning logic lives in one place (SQL), not duplicated
in Python.

Run: pip install pandas sqlalchemy pymysql matplotlib seaborn --break-system-packages

NOTE: This version assumes a FLAT folder structure — i.e. this script,
the "exports" folder, etc. all live in the same top-level project folder
(not inside a separate "notebooks" subfolder). Make sure an "exports"
folder exists next to this script before running:
    mkdir exports
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

DB_CONFIG = {
    "user": "root",
    "password": "oyemysqlterapasswordle456",
    "host": "localhost",
    "port": 3306,
    "database": "retail_analytics",
}

conn_str = (
    f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)
engine = create_engine(conn_str)


# ---------------------------------------------------------
# 1. Load cleaned data
# ---------------------------------------------------------
df = pd.read_sql("SELECT * FROM clean_transactions", con=engine)
df["invoice_date"] = pd.to_datetime(df["invoice_date"])
print(f"Loaded {len(df):,} clean transaction rows.")


# ---------------------------------------------------------
# 2. RFM Analysis
# ---------------------------------------------------------
snapshot_date = df["invoice_date"].max() + pd.Timedelta(days=1)

rfm = df.groupby("customer_id").agg(
    recency=("invoice_date", lambda x: (snapshot_date - x.max()).days),
    frequency=("invoice_no", "nunique"),
    monetary=("revenue", "sum"),
).reset_index()

# Score each dimension 1-4 using quartiles (4 = best)
rfm["r_score"] = pd.qcut(rfm["recency"], 4, labels=[4, 3, 2, 1]).astype(int)
rfm["f_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 4, labels=[1, 2, 3, 4]).astype(int)
rfm["m_score"] = pd.qcut(rfm["monetary"], 4, labels=[1, 2, 3, 4]).astype(int)

rfm["rfm_score"] = rfm["r_score"] + rfm["f_score"] + rfm["m_score"]

def segment_customer(score):
    if score >= 10:
        return "Champions"
    elif score >= 8:
        return "Loyal Customers"
    elif score >= 6:
        return "Potential Loyalists"
    elif score >= 4:
        return "At Risk"
    else:
        return "Lost"

rfm["segment"] = rfm["rfm_score"].apply(segment_customer)

print("\nCustomer segment distribution:")
print(rfm["segment"].value_counts())

# Save for Power BI import
rfm.to_csv("exports/rfm_segments.csv", index=False)
print("\nSaved: exports/rfm_segments.csv")


# ---------------------------------------------------------
# 3. Segment visualization (quick sanity check plot)
# ---------------------------------------------------------
plt.figure(figsize=(8, 5))
sns.countplot(data=rfm, y="segment", order=rfm["segment"].value_counts().index)
plt.title("Customer Segments (RFM Analysis)")
plt.xlabel("Number of Customers")
plt.tight_layout()
plt.savefig("exports/rfm_segment_distribution.png")
print("Saved: exports/rfm_segment_distribution.png")


# ---------------------------------------------------------
# 4. Cohort Retention Analysis
# ---------------------------------------------------------
df["order_month"] = df["invoice_date"].dt.to_period("M")
df["cohort_month"] = df.groupby("customer_id")["invoice_date"].transform("min").dt.to_period("M")

df["cohort_index"] = (
    (df["order_month"].dt.year - df["cohort_month"].dt.year) * 12
    + (df["order_month"].dt.month - df["cohort_month"].dt.month)
)

cohort_data = df.groupby(["cohort_month", "cohort_index"])["customer_id"].nunique().reset_index()
cohort_pivot = cohort_data.pivot(index="cohort_month", columns="cohort_index", values="customer_id")

cohort_size = cohort_pivot.iloc[:, 0]
retention = cohort_pivot.divide(cohort_size, axis=0).round(3) * 100

retention.to_csv("exports/cohort_retention.csv")
print("Saved: exports/cohort_retention.csv")

plt.figure(figsize=(12, 8))
sns.heatmap(retention, annot=True, fmt=".0f", cmap="Blues", cbar_kws={"label": "Retention %"})
plt.title("Monthly Cohort Retention Heatmap")
plt.xlabel("Months Since First Purchase")
plt.ylabel("Cohort Month")
plt.tight_layout()
plt.savefig("exports/cohort_retention_heatmap.png")
print("Saved: exports/cohort_retention_heatmap.png")

print("\nAll done. CSVs in exports/ are ready to import into Power BI.")
