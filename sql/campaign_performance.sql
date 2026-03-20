WITH ads AS (
    SELECT
        date,
        'Google Ads' AS channel,
        SUM(spend) AS total_spend,
        SUM(clicks) AS total_clicks
    FROM read_csv_auto('data/google_ads_campaigns.csv')
    GROUP BY 1,2

    UNION ALL

    SELECT
        date,
        'LinkedIn Ads' AS channel,
        SUM(spend) AS total_spend,
        SUM(clicks) AS total_clicks
    FROM read_csv_auto('data/linkedin_ads_campaigns.csv')
    GROUP BY 1,2
),

signups AS (
    SELECT
        date,
        channel,
        SUM(signups) AS total_signups
    FROM read_csv_auto('data/signups.csv')
    GROUP BY 1,2
),

subscriptions AS (
    SELECT
        date,
        channel,
        SUM(paid_users) AS total_paid_users,
        SUM(mrr) AS total_mrr
    FROM read_csv_auto('data/subscriptions.csv')
    GROUP BY 1,2
)

SELECT
    a.date,
    a.channel,
    a.total_spend,
    a.total_clicks,
    COALESCE(s.total_signups, 0) AS total_signups,
    COALESCE(sub.total_paid_users, 0) AS total_paid_users,
    COALESCE(sub.total_mrr, 0) AS total_mrr,

    a.total_spend / NULLIF(a.total_clicks, 0) AS cpc,
    a.total_spend / NULLIF(s.total_signups, 0) AS cac_signup,
    a.total_spend / NULLIF(sub.total_paid_users, 0) AS cac_paid,
    COALESCE(sub.total_mrr, 0) / NULLIF(a.total_spend, 0) AS roas

FROM ads a
LEFT JOIN signups s
    ON a.date = s.date AND a.channel = s.channel
LEFT JOIN subscriptions sub
    ON a.date = sub.date AND a.channel = sub.channel
ORDER BY 1,2;