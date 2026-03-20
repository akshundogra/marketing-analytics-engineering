import duckdb

con = duckdb.connect()

# create a table from your CSV
con.execute("""
CREATE OR REPLACE TABLE saas_marketing_data AS
SELECT * FROM read_csv_auto('data/saas_marketing_data.csv')
""")

# run your SQL file
query = open("sql/campaign_performance.sql").read()

result = con.execute(query).fetchdf()

print(result)