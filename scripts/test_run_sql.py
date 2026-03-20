import duckdb

con = duckdb.connect()

files = [
    "data/google_ads_campaigns.csv",
    "data/linkedin_ads_campaigns.csv",
    "data/signups.csv",
    "data/subscriptions.csv"
]

for file in files:
    print(f"\n--- {file} ---")
    df = con.execute(f"SELECT * FROM read_csv_auto('{file}') LIMIT 5").fetchdf()
    print("Columns:", list(df.columns))
    print(df)