SELECT
channel,
SUM(spend) AS total_spend,
SUM(clicks) AS total_clicks,
SUM(signups) AS total_signups
FROM saas_marketing_data
GROUP BY channel;