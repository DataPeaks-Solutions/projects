-- DataPeaks Solutions | CDA SQL Track | Project: E-commerce Order Analysis
-- Deep-dive queries. Each block maps to a story beat for the video.
-- Techniques covered: JOINs, subqueries, CTEs, window functions, CASE, GROUP BY/HAVING.

-- Q1
SELECT
    SUM(oi.quantity * oi.unit_price_at_purchase
        * (1 - oi.discount_pct/100)) AS net_revenue
FROM order_items oi
JOIN orders o ON o.order_id = oi.order_id
WHERE o.order_status = 'Delivered';

-- Q2
SELECT p.category,
       SUM(oi.quantity * oi.unit_price_at_purchase
           * (1 - oi.discount_pct/100)) AS net_revenue
FROM order_items oi
JOIN orders o ON o.order_id = oi.order_id
JOIN products p ON p.product_id = oi.product_id
WHERE o.order_status = 'Delivered'
GROUP BY p.category
ORDER BY net_revenue DESC;

-- Q3 — Segment revenue with window function
SELECT c.customer_segment,
       COUNT(DISTINCT c.customer_id) AS customers,
       SUM(oi.quantity * oi.unit_price_at_purchase
           * (1 - oi.discount_pct/100)) AS net_revenue,
       100.0 * SUM(oi.quantity * oi.unit_price_at_purchase
           * (1 - oi.discount_pct/100))
           / SUM(SUM(oi.quantity * oi.unit_price_at_purchase
           * (1 - oi.discount_pct/100))) OVER () AS pct_of_total
FROM order_items oi
JOIN orders o ON o.order_id = oi.order_id
JOIN customers c ON c.customer_id = o.customer_id
WHERE o.order_status = 'Delivered'
GROUP BY c.customer_segment;
-- Expected: VIP 121 customers ~₹2.41Cr | Regular 423 customers ~₹2.40Cr

-- Q4 — Top 10 customers by lifetime value (RANK)
SELECT c.customer_name,
       SUM(oi.quantity * oi.unit_price_at_purchase
           * (1 - oi.discount_pct/100)) AS lifetime_value,
       RANK() OVER (ORDER BY SUM(oi.quantity * oi.unit_price_at_purchase
           * (1 - oi.discount_pct/100)) DESC) AS value_rank
FROM order_items oi
JOIN orders o ON o.order_id = oi.order_id
JOIN customers c ON c.customer_id = o.customer_id
WHERE o.order_status = 'Delivered'
GROUP BY c.customer_id, c.customer_name
ORDER BY value_rank
LIMIT 10;

-- Q5 — Cancellation/return % by category
SELECT p.category,
       COUNT(DISTINCT o.order_id) AS total_orders,
       100.0 * SUM(CASE WHEN o.order_status
            IN ('Cancelled','Returned') THEN 1 ELSE 0 END)
            / COUNT(DISTINCT o.order_id) AS bad_order_pct
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY bad_order_pct DESC;
-- Expected: Fashion 35.6%, Electronics 22.3%, Home & Kitchen 21.9%,
--           Sports & Fitness 20.7%, Beauty 20.0%

-- Q6 — Cancellation/return % by shipping city
SELECT c.city,
       COUNT(DISTINCT o.order_id) AS total_orders,
       100.0 * SUM(CASE WHEN o.order_status
            IN ('Cancelled','Returned') THEN 1 ELSE 0 END)
            / COUNT(DISTINCT o.order_id) AS bad_order_pct
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
GROUP BY c.city
ORDER BY bad_order_pct DESC;
-- Expected: Lucknow 32.1%, Nagpur 30.3%, Delhi 21.2%, Jaipur 18.6%, Chennai 17.3%

-- Q7 — Festive vs rest-of-year margin (CTE)
WITH item_margin AS (
  SELECT MONTH(o.order_date) AS mo,
         oi.quantity * oi.unit_price_at_purchase
             * (1 - oi.discount_pct/100) AS net_sale,
         oi.quantity * p.unit_cost AS cost
  FROM order_items oi
  JOIN orders o ON o.order_id = oi.order_id
  JOIN products p ON p.product_id = oi.product_id
  WHERE o.order_status = 'Delivered'
)
SELECT CASE WHEN mo IN (11,12) THEN 'Festive' ELSE 'Rest' END AS period,
       100.0 * SUM(net_sale - cost) / SUM(net_sale) AS margin_pct
FROM item_margin
GROUP BY period;
-- Expected: Festive 29.9%, Rest of year 35.4%

-- Q8 — Repeat-purchase rate
SELECT
    SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) AS repeat_customers,
    SUM(CASE WHEN order_count = 0 THEN 1 ELSE 0 END) AS never_converted,
    COUNT(*) AS total_customers,
    100.0 * SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) / COUNT(*) AS repeat_pct
FROM (
    SELECT c.customer_id,
           COUNT(DISTINCT o.order_id) AS order_count
    FROM customers c
    LEFT JOIN orders o ON o.customer_id = c.customer_id
        AND o.order_status = 'Delivered'
    GROUP BY c.customer_id
    )t;