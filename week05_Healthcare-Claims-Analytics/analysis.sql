-- =====================================================================
-- DataPeaks Solutions | CDA SQL Project 2: Healthcare Claims Query Deep-Dive
-- Dataset: 40,000 claims · 150 providers · 8 payers
-- Author: Arshiya Kauser | DataPeaks Solutions
-- =====================================================================

USE datapeaks_healthcare_claims;

-- ---------------------------------------------------------------------
-- 1. DENIAL RATES BY PAYER & SPECIALTY (JOINs)
-- ---------------------------------------------------------------------
SELECT
    pay.payer_name,
    pr.specialty,
    COUNT(*) AS total_claims,
    SUM(CASE WHEN c.status = 'DENIED' THEN 1 ELSE 0 END) AS denied_claims,
    ROUND(
        SUM(CASE WHEN c.status = 'DENIED' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2
    ) AS denial_rate_pct
FROM claims c
JOIN providers pr ON c.provider_id = pr.provider_id
JOIN payers pay ON c.payer_id = pay.payer_id
GROUP BY pay.payer_name, pr.specialty
ORDER BY denial_rate_pct DESC;


-- ---------------------------------------------------------------------
-- 2. TOP PROVIDERS RANKED (Window Functions)
-- ---------------------------------------------------------------------
SELECT
    provider_id,
    provider_name,
    total_billed,
    RANK() OVER (ORDER BY total_billed DESC) AS billing_rank
FROM (
    SELECT
        pr.provider_id,
        pr.provider_name,
        SUM(c.billed_amount) AS total_billed
    FROM claims c
    JOIN providers pr ON c.provider_id = pr.provider_id
    GROUP BY pr.provider_id, pr.provider_name
) provider_totals
ORDER BY billing_rank
LIMIT 20;


-- ---------------------------------------------------------------------
-- 3. HIGH-RISK CLAIMS FLAGGED (CASE WHEN)
-- ---------------------------------------------------------------------
SELECT
    claim_id,
    provider_id,
    billed_amount,
    status,
    CASE
        WHEN status = 'DENIED' AND billed_amount > 5000 THEN 'HIGH RISK'
        WHEN status = 'DENIED' AND billed_amount BETWEEN 1000 AND 5000 THEN 'MEDIUM RISK'
        WHEN status = 'DENIED' THEN 'LOW RISK'
        ELSE 'NOT DENIED'
    END AS risk_flag
FROM claims
ORDER BY billed_amount DESC;


-- ---------------------------------------------------------------------
-- 4. RUNNING PAYER PAYOUTS (CTEs + Window Functions)
-- ---------------------------------------------------------------------
WITH monthly_payouts AS (
    SELECT
        payer_id,
        DATE_FORMAT(claim_date, '%Y-%m') AS claim_month,
        SUM(allowed_amount) AS monthly_total
    FROM claims
    WHERE status = 'PAID'
    GROUP BY payer_id, DATE_FORMAT(claim_date, '%Y-%m')
)
SELECT
    payer_id,
    claim_month,
    monthly_total,
    SUM(monthly_total) OVER (
        PARTITION BY payer_id ORDER BY claim_month
    ) AS running_total
FROM monthly_payouts
ORDER BY payer_id, claim_month;


-- ---------------------------------------------------------------------
-- 5. OUTLIER PROVIDERS (GROUP BY + HAVING)
-- ---------------------------------------------------------------------
SELECT
    pr.provider_id,
    pr.provider_name,
    COUNT(*) AS denial_count,
    SUM(c.billed_amount) AS total_lost
FROM claims c
JOIN providers pr ON c.provider_id = pr.provider_id
WHERE c.status = 'DENIED'
GROUP BY pr.provider_id, pr.provider_name
HAVING COUNT(*) > 50
ORDER BY total_lost DESC;


-- ---------------------------------------------------------------------
-- 6. OVERALL SUMMARY STATS
-- ---------------------------------------------------------------------
SELECT
    COUNT(*) AS total_claims,
    COUNT(DISTINCT patient_id) AS total_patients,
    COUNT(DISTINCT provider_id) AS total_providers,
    COUNT(DISTINCT payer_id) AS total_payers,
    SUM(billed_amount) AS total_billed,
    SUM(CASE WHEN status = 'DENIED' THEN 1 ELSE 0 END) AS total_denied
FROM claims;


-- ---------------------------------------------------------------------
-- BONUS: TOP DENIAL REASONS
-- ---------------------------------------------------------------------
SELECT
    denial_reason,
    COUNT(*) AS occurrences,
    SUM(billed_amount) AS total_billed_lost
FROM claims
WHERE status = 'DENIED' AND denial_reason IS NOT NULL
GROUP BY denial_reason
ORDER BY occurrences DESC;


-- ---------------------------------------------------------------------
-- BONUS: DIAGNOSIS CATEGORY COST BREAKDOWN
-- ---------------------------------------------------------------------
SELECT
    d.category,
    COUNT(*) AS claim_count,
    SUM(c.billed_amount) AS total_billed,
    ROUND(AVG(c.billed_amount), 2) AS avg_billed
FROM claims c
JOIN diagnoses d ON c.diagnosis_id = d.diagnosis_id
GROUP BY d.category
ORDER BY total_billed DESC;
