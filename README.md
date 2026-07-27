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
*(Fill this in after running the analysis — this section matters most
in interviews. 3-5 bullet points translating findings into business
actions, e.g. "Target 'At Risk' segment with a win-back email campaign,
representing X% of customers and $Y in historical revenue.")*
