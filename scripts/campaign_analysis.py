import duckdb

con = duckdb.connect()

query = """
SELECT 
    platform,
    campaign,
    SUM(impressions) as impressions,
    SUM(clicks) as clicks,
    SUM(cost) as cost,
    SUM(conversions) as conversions
FROM 'data/marketing_campaign_data.csv'
GROUP BY platform, campaign
"""

result = con.execute(query).fetchdf()

print(result)