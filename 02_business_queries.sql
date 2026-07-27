-- ============================================
-- Business Question Queries
-- Run these against the `clean_transactions` view
-- ============================================

USE retail_analytics;

-- 1. TOP 10 BEST-SELLING PRODUCTS BY REVENUE
SELECT
    stock_code,
    description,
    SUM(quantity) AS total_units_sold,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM clean_transactions
GROUP BY stock_code, description
ORDER BY total_revenue DESC
LIMIT 10;


-- 2. MONTHLY REVENUE TREND
SELECT
    DATE_FORMAT(invoice_date, '%Y-%m') AS month,
    ROUND(SUM(revenue), 2) AS monthly_revenue,
    COUNT(DISTINCT invoice_no) AS num_orders
FROM clean_transactions
GROUP BY month
ORDER BY month;


-- 3. REVENUE BY COUNTRY (TOP 10)
SELECT
    country,
    ROUND(SUM(revenue), 2) AS total_revenue,
    COUNT(DISTINCT customer_id) AS num_customers
FROM clean_transactions
GROUP BY country
ORDER BY total_revenue DESC
LIMIT 10;


-- 4. AVERAGE ORDER VALUE (AOV) BY MONTH
SELECT
    DATE_FORMAT(invoice_date, '%Y-%m') AS month,
    ROUND(SUM(revenue) / COUNT(DISTINCT invoice_no), 2) AS avg_order_value
FROM clean_transactions
GROUP BY month
ORDER BY month;


-- 5. CUSTOMER REPEAT PURCHASE RATE
-- (% of customers who ordered more than once)
SELECT
    ROUND(
        100.0 * SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS repeat_customer_pct
FROM (
    SELECT customer_id, COUNT(DISTINCT invoice_no) AS order_count
    FROM clean_transactions
    GROUP BY customer_id
) AS customer_orders;


-- 6. RFM COMPONENTS (Recency, Frequency, Monetary) — raw values
-- Used as input for the RFM segmentation done in Python later.
SELECT
    customer_id,
    DATEDIFF(
        (SELECT MAX(invoice_date) FROM clean_transactions),
        MAX(invoice_date)
    ) AS recency_days,
    COUNT(DISTINCT invoice_no) AS frequency,
    ROUND(SUM(revenue), 2) AS monetary
FROM clean_transactions
GROUP BY customer_id
ORDER BY monetary DESC;


-- 7. TOP PRODUCT CATEGORY PER COUNTRY (uses description as proxy for category)
-- Interview talking point: window functions (RANK) instead of subqueries
SELECT country, description, total_revenue
FROM (
    SELECT
        country,
        description,
        SUM(revenue) AS total_revenue,
        RANK() OVER (PARTITION BY country ORDER BY SUM(revenue) DESC) AS rnk
    FROM clean_transactions
    GROUP BY country, description
) ranked
WHERE rnk = 1
ORDER BY total_revenue DESC;
