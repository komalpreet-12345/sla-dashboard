SELECT
    date(date) AS date,
    contributor_id,
    client,
    SUM(tasks_completed) AS throughput,
    ROUND(1.0 - SUM(errors_found) * 1.0 / NULLIF(SUM(tasks_reviewed), 0), 4) AS accuracy,
    ROUND(AVG(on_time), 4) AS sla_rate,
    CASE
        WHEN AVG(on_time) < 0.90
          OR 1.0 - SUM(errors_found) * 1.0 / NULLIF(SUM(tasks_reviewed), 0) < 0.95
        THEN 'At Risk'
        ELSE 'On Track'
    END AS sla_status
FROM deliveries
GROUP BY date(date), contributor_id, client
ORDER BY date, contributor_id;