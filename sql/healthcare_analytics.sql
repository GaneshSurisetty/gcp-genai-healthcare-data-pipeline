
-- BigQuery healthcare analytics
-- Replace PROJECT_ID with your GCP project ID.
-- Requires a populated encounter table.

SELECT
    encounter_type,
    COUNT(*) AS total_encounters,
    ROUND(SUM(claim_amount), 2) AS total_claim_amount,
    ROUND(AVG(claim_amount), 2) AS avg_claim_amount
FROM `PROJECT_ID.healthcare_analytics.patient_encounters`
WHERE claim_amount >= 0
  AND encounter_id IS NOT NULL
  AND patient_id IS NOT NULL
GROUP BY encounter_type
ORDER BY total_encounters DESC;
