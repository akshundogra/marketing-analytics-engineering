with source as (
    select * from read_csv_auto('../data/linkedin_ads_campaigns.csv')
),

renamed as (
    select
        campaign_id,
        campaign_name,
        cast(date as date)  as date,
        spend               as spend,
        clicks              as clicks,
        impressions         as impressions,
        'LinkedIn Ads'      as channel
    from source
)

select * from renamed