SELECT
channel,
SUM(spend) AS total_spend,
SUM(clicks) AS total_clicks,
SUM(signups) AS total_signups
FROM saas_marketing_data
GROUP BY channel;

-- CAC by channel

SELECT
channel,
SUM(spend) AS total_spend,
SUM(signups) AS total_signups,
SUM(spend) / SUM(signups) AS cac
FROM saas_marketing_data
GROUP BY channel;

-- Excercises