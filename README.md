# E-commerce Sales & Customer Behavior Analytics

A Data Analytics project using SQL, Python, and Power BI to analyze
customer purchasing behavior in an online retail dataset — including
RFM customer segmentation, cohort retention analysis, and an
interactive sales dashboard.

## Dataset
[UCI Online Retail Dataset](https://archive.ics.uci.edu/dataset/352/online+retail)
— ~540,000 transactions from a UK-based online retailer (Dec 2010 – Dec 2011).

## Tech Stack
- **MySQL** — data storage, cleaning (via views), business-question queries
- **Python (pandas, SQLAlchemy)** — RFM segmentation, cohort retention analysis
- **Power BI** — interactive dashboard

## Project Structure
```
ecommerce-analytics/
├── data/                     # place "Online Retail.xlsx" here
├── sql/
│   ├── 01_schema.sql         # DB schema + cleaned view
│   └── 02_business_queries.sql
├── notebooks/
│   ├── 00_load_data.py       # loads Excel -> MySQL
│   └── 01_rfm_analysis.py    # RFM segmentation + cohort analysis
└── exports/                  # CSVs + charts generated for Power BI
```

## How to Run

1. **Set up MySQL:**
   - Open MySQL Workbench, run `sql/01_schema.sql`

2. **Load the data:**
   - Download the dataset, place it in `/data`
   - Update DB credentials in `notebooks/00_load_data.py`
   - `pip install pandas sqlalchemy pymysql openpyxl --break-system-packages`
   - Run `python 00_load_data.py`

3. **Explore business questions:**
   - Run queries in `sql/02_business_queries.sql` in MySQL Workbench

4. **Run RFM + cohort analysis:**
   - `pip install matplotlib seaborn --break-system-packages`
   - Run `python 01_rfm_analysis.py`
   - Outputs land in `/exports`: `rfm_segments.csv`, `cohort_retention.csv`, and charts

5. **Build the Power BI dashboard:**
   - Import `exports/rfm_segments.csv` and connect Power BI directly to MySQL
     for the live transaction data (or import `02_business_queries.sql`
     results as CSVs)
   - Build visuals: revenue trend line, top products bar chart, country
     map/bar, RFM segment pie chart, cohort retention heatmap

## Key Business Questions Answered
- Which products/categories drive the most revenue?
- How does revenue trend month over month?
- Which countries are the biggest markets?
- What % of customers are repeat buyers?
- Which customers are "Champions" vs "At Risk" vs "Lost" (RFM segments)?
- How well does the business retain customers over time (cohort analysis)?

## Insights & Recommendations

- **Champions (29.2% of customers, 1,268 total) drive 76.8% of total
  revenue** (avg ₹5,397.51 per customer) — a heavily concentrated
  revenue base. Recommend a dedicated loyalty/VIP program and
  proactive relationship management for this segment, since losing
  even a small % of Champions would have an outsized revenue impact.

- **Loyal Customers (19.4%, 843 customers)** contribute 11.8% of
  revenue (avg ₹1,249.62/customer) — solid, consistent buyers with
  room to grow. Recommend upsell/cross-sell campaigns to move them
  toward Champion-level spend.

- **Potential Loyalists (21.6%, 936 customers)** contribute 7.3% of
  revenue (avg ₹699.06/customer). Recommend nurture campaigns
  (personalized recommendations, loyalty program invites) to convert
  them into higher-value segments.

- **At Risk (22.8%, 988 customers)** — a large segment (nearly a
  quarter of all customers) contributing only 3.5% of revenue
  (avg ₹313.92/customer), signaling declining engagement. Recommend a
  targeted win-back campaign (discount codes, re-engagement emails)
  before they churn into "Lost."

- **Lost (7.0%, 303 customers)** contribute just 0.6% of revenue
  (avg ₹163.22/customer) — recommend only low-cost reactivation
  attempts here, since ROI is lowest in this segment; budget is better
  spent retaining At Risk and growing Potential Loyalists.

- **Key business takeaway:** Revenue is highly concentrated — the top
  ~29% of customers generate over 3 out of every 4 revenue dollars.
  This suggests customer retention and Champion-tier relationship
  management should be prioritized over broad acquisition spend.