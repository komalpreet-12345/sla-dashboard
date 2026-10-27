WITH daily AS (
    SELECT date(date) AS date, contributor_id,
           SUM(errors_found) AS errors,
           SUM(tasks_reviewed) AS reviewed
    FROM deliveries
    GROUP BY date(date), contributor_id
),
rolling AS (
    SELECT date, contributor_id,
        SUM(errors) OVER (PARTITION BY contributor_id ORDER BY date
                          ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS errors_7d,
        SUM(reviewed) OVER (PARTITION BY contributor_id ORDER BY date
                          ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS reviewed_7d
    FROM daily
),
rates AS (
    SELECT date, contributor_id, errors_7d, reviewed_7d,
           ROUND(errors_7d * 1.0 / NULLIF(reviewed_7d, 0), 4) AS error_rate_7d
    FROM rolling
),
compared AS (
    SELECT *,
           LAG(error_rate_7d, 7) OVER (PARTITION BY contributor_id ORDER BY date) AS prev_error_rate_7d
    FROM rates
)
SELECT date, contributor_id, errors_7d, reviewed_7d, error_rate_7d, prev_error_rate_7d,
        CASE
        WHEN reviewed_7d < 100 THEN 'OK'
        WHEN error_rate_7d > 0.05 THEN 'High Error Rate'
        WHEN error_rate_7d - prev_error_rate_7d > 0.03 THEN 'Rising Errors'
        ELSE 'OK'
    END AS quality_flag
FROM compared
ORDER BY date, contributor_id;