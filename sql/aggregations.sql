
DROP VIEW IF EXISTS agg_orders_daily_revenue;
DROP VIEW IF EXISTS agg_orders_channel_revenue;
DROP VIEW IF EXISTS agg_orders_monthly_revenue;
DROP VIEW IF EXISTS agg_orders_taobao_revenue;
DROP VIEW IF EXISTS agg_orders_shopify_revenue;
DROP VIEW IF EXISTS agg_orders_payment_method_share;

-- Daily KPI & 7-Day Moving Average
CREATE VIEW agg_orders_daily_revenue AS
WITH daily_agg AS (
    SELECT 
        Order_Date, 
        ROUND(SUM(Revenue), 2) AS daily_revenue,
        COUNT(Order_ID) AS order_count 
    FROM orders
    WHERE 
        Order_Date BETWEEN '2024-01-01' AND '2025-12-31'                              
        AND Revenue IS NOT NULL                              
    GROUP BY Order_Date
)
SELECT 
    Order_Date, 
    daily_revenue,
    ROUND(AVG(daily_revenue) OVER (ORDER BY Order_Date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 2) AS revenue_7d_ma,
    order_count
FROM daily_agg;

-- Channel Revenue Contribution
CREATE VIEW agg_orders_channel_revenue AS
WITH channel_agg AS (
    SELECT 
        Channel,
        SUM(Revenue) AS total_revenue,
        COUNT(Order_ID) AS order_count
    FROM orders
    WHERE 
        Order_Date BETWEEN '2024-01-01' AND '2025-12-31'
        AND Revenue IS NOT NULL   
    GROUP BY Channel
)
SELECT 
    Channel, 
    total_revenue, 
    ROUND(total_revenue* 1.0 / SUM(total_revenue) OVER (), 4) AS share_pct, 
    order_count
FROM channel_agg;

-- Monthly Growth
CREATE VIEW agg_orders_monthly_revenue AS
WITH growth_agg AS (
    SELECT 
        strftime('%Y-%m', Order_Date) AS month, 
        ROUND(SUM(Revenue), 2) AS monthly_revenue,
        COUNT(Order_ID) AS order_count
    FROM orders
    WHERE 
        Order_Date BETWEEN '2024-01-01' AND '2025-12-31'
        AND Revenue IS NOT NULL 
    GROUP BY month
)
SELECT 
    month,
    monthly_revenue,
    ROUND((monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY month)) / NULLIF(LAG(monthly_revenue, 1) OVER (ORDER BY month), 0) * 100, 2) AS growth_pct,
    order_count
FROM growth_agg;

-- Taobao Revenue by Category
CREATE VIEW agg_orders_taobao_revenue AS
SELECT 
    Product_Category, 
    ROUND(SUM(Revenue), 2) AS total_revenue,
    COUNT(Order_ID) AS order_count
FROM orders
WHERE 
    Channel = 'Taobao'
    AND Order_Date BETWEEN '2024-01-01' AND '2025-12-31'
    AND Revenue IS NOT NULL         
GROUP BY Product_Category;

-- Shopify Revenue by City
CREATE VIEW agg_orders_shopify_revenue AS
SELECT 
    City, 
    ROUND(SUM(Revenue), 2) AS total_revenue,
    COUNT(Order_ID) AS order_count
FROM orders
WHERE 
    Channel = 'Shopify'
    AND Order_Date BETWEEN '2024-01-01' AND '2025-12-31'
    AND Revenue IS NOT NULL       
GROUP BY City;

-- POS Payment Method Share
CREATE VIEW agg_orders_payment_method_share AS
SELECT 
    Payment_Method, 
    ROUND(SUM(Revenue), 2) AS total_revenue,
    ROUND(100.0 * SUM(Revenue) / SUM(SUM(Revenue)) OVER (), 2) AS pct_within_pos,
    COUNT(Order_ID) AS order_count
FROM orders
WHERE 
    Channel = 'POS'
    AND Order_Date BETWEEN '2024-01-01' AND '2025-12-31'
    AND Revenue IS NOT NULL     
GROUP BY Payment_Method;

-- Channel By Day
CREATE VIEW agg_orders_daily_channel AS
SELECT 
    Order_Date,
    Channel,
    ROUND(SUM(Revenue), 2) AS total_revenue,
    COUNT(Order_ID) AS order_count
FROM orders
WHERE 
    Order_Date BETWEEN '2024-01-01' AND '2025-12-31'
    AND Revenue IS NOT NULL
GROUP BY Order_Date, Channel;