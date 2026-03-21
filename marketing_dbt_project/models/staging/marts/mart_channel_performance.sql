with google as (
    select * from {{ ref('stg_google_ads') }}
),

linkedin as (
    select * from {{ ref('stg_linkedin_ads') }}
),

all_channels as (
    select * from google
    union all
    select * from linkedin
),

aggregated as (
    select
        date,
        channel,
        sum(spend)       as total_spend,
        sum(clicks)      as total_clicks,
        sum(impressions) as total_impressions,

        round(sum(spend) / nullif(sum(clicks), 0), 2)       as cpc,
        round(sum(clicks) / nullif(sum(impressions), 0), 4) as ctr
    from all_channels
    group by 1, 2
)

select * from aggregated
order by date, channel