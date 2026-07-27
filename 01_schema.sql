-- ============================================
-- E-commerce Sales Analytics — Schema Setup
-- Dataset: UCI Online Retail
-- ============================================

CREATE DATABASE IF NOT EXISTS retail_analytics;
USE retail_analytics;

-- Raw transactions table (loaded directly from CSV via Python)
CREATE TABLE IF NOT EXISTS transactions (
    invoice_no      VARCHAR(20),
    stock_code      VARCHAR(20),
    description     VARCHAR(255),
    quantity        INT,
    invoice_date    DATETIME,
    unit_price      DECIMAL(10, 2),
    customer_id     INT,
    country         VARCHAR(100)
);

-- Index the columns we'll filter/join on most — speeds up the
-- aggregation queries below and gives you something concrete
-- to talk about re: indexing in interviews.
CREATE INDEX idx_customer_id ON transactions(customer_id);
CREATE INDEX idx_invoice_date ON transactions(invoice_date);
CREATE INDEX idx_country ON transactions(country);

-- A cleaned view: removes cancelled orders (InvoiceNo starting with 'C'),
-- null customer IDs, and non-positive quantities/prices.
CREATE OR REPLACE VIEW clean_transactions AS
SELECT
    invoice_no,
    stock_code,
    description,
    quantity,
    invoice_date,
    unit_price,
    customer_id,
    country,
    (quantity * unit_price) AS revenue
FROM transactions
WHERE customer_id IS NOT NULL
  AND quantity > 0
  AND unit_price > 0
  AND invoice_no NOT LIKE 'C%';
