-- Campaign performance summary by date, channel, and campaign
-- Includes CPC, CPA, and conversion rate
Select
    date,
    channel,
    campaign,
    Sum(spend) As total_spend,
    Sum(clicks) As total_clicks,
    Sum(signups) As total_signups,

    -- KPIs
    Sum(spend) / Sum(clicks) As cpc,
    Sum(spend) / Sum(signups) As cpa,
    Sum(signups)* 1.0 / Sum(clicks) As conversion_rate

From saas_marketing_data
Group by 1,2,3
Order by Date;
