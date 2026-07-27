

import pandas as pd
from sqlalchemy import create_engine

# ---- CONFIG: update these to match your local MySQL setup ----
DB_CONFIG = {
    "user": "root",
    "password": "oyemysqlterapasswordle456",
    "host": "localhost",
    "port": 3306,
    "database": "retail_analytics",
}

DATA_PATH = "data/Online Retail.xlsx"

def main():
    print("Reading Excel file...")
    df = pd.read_excel(DATA_PATH)

    # Rename columns to match our SQL schema (snake_case)
    df = df.rename(columns={
        "InvoiceNo": "invoice_no",
        "StockCode": "stock_code",
        "Description": "description",
        "Quantity": "quantity",
        "InvoiceDate": "invoice_date",
        "UnitPrice": "unit_price",
        "CustomerID": "customer_id",
        "Country": "country",
    })

    print(f"Loaded {len(df):,} rows.")

    # Build MySQL connection string
    conn_str = (
        f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )
    engine = create_engine(conn_str)

    print("Writing to MySQL (this can take a minute for 540k+ rows)...")
    df.to_sql(
        "transactions",
        con=engine,
        if_exists="append",   # table already created by 01_schema.sql
        index=False,
        chunksize=5000,
    )

    print("Done. Data loaded into retail_analytics.transactions")

if __name__ == "__main__":
    main()
