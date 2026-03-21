import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

# ── Config ─────────────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="muted")
OUTPUT_DIR = "outputs/charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Load data via DuckDB ────────────────────────────────────
con = duckdb.connect()

df = con.execute("""
WITH ads AS (
    SELECT date, 'Google Ads' AS channel,
           SUM(spend) AS total_spend, SUM(clicks) AS total_clicks
    FROM read_csv_auto('data/google_ads_campaigns.csv')
    GROUP BY 1,2
    UNION ALL
    SELECT date, 'LinkedIn Ads' AS channel,
           SUM(spend) AS total_spend, SUM(clicks) AS total_clicks
    FROM read_csv_auto('data/linkedin_ads_campaigns.csv')
    GROUP BY 1,2
),
signups AS (
    SELECT date, channel, SUM(signups) AS total_signups
    FROM read_csv_auto('data/signups.csv')
    GROUP BY 1,2
),
subscriptions AS (
    SELECT date, channel,
           SUM(paid_users) AS total_paid_users,
           SUM(mrr) AS total_mrr
    FROM read_csv_auto('data/subscriptions.csv')
    GROUP BY 1,2
)
SELECT
    a.date, a.channel,
    a.total_spend, a.total_clicks,
    COALESCE(s.total_signups, 0)     AS total_signups,
    COALESCE(sub.total_paid_users, 0) AS total_paid_users,
    COALESCE(sub.total_mrr, 0)        AS total_mrr,
    a.total_spend / NULLIF(a.total_clicks, 0)          AS cpc,
    a.total_spend / NULLIF(s.total_signups, 0)         AS cac_signup,
    a.total_spend / NULLIF(sub.total_paid_users, 0)    AS cac_paid,
    COALESCE(sub.total_mrr, 0) / NULLIF(a.total_spend, 0) AS roas
FROM ads a
LEFT JOIN signups s     ON a.date = s.date AND a.channel = s.channel
LEFT JOIN subscriptions sub ON a.date = sub.date AND a.channel = sub.channel
ORDER BY 1,2
""").fetchdf()

print("✅ Data loaded. Columns:", df.columns.tolist())
print(df)

# ── Chart 1: Total Spend by Channel ────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))
channel_spend = df.groupby("channel")["total_spend"].sum().sort_values(ascending=False)
bars = ax.bar(channel_spend.index, channel_spend.values, color=sns.color_palette("muted"))
ax.set_title("Total Spend by Channel", fontsize=14, fontweight="bold")
ax.set_xlabel("Channel")
ax.set_ylabel("Total Spend (€)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"€{x:,.0f}"))
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
            f"€{bar.get_height():,.0f}", ha="center", va="bottom", fontsize=9)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/spend_by_channel.png", dpi=150)
plt.close()
print("✅ Chart 1 saved")

# ── Chart 2: CAC by Channel ─────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))
channel_cac = df.groupby("channel")["cac_paid"].mean().dropna().sort_values()
bars = ax.barh(channel_cac.index, channel_cac.values, color=sns.color_palette("muted"))
ax.set_title("Average CAC (Cost per Paid User) by Channel", fontsize=14, fontweight="bold")
ax.set_xlabel("CAC (€)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"€{x:,.0f}"))
for bar in bars:
    width = bar.get_width()
    ax.text(width + 1, bar.get_y() + bar.get_height()/2,
            f"€{width:,.0f}", va="center", fontsize=9)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/cac_by_channel.png", dpi=150)
plt.close()
print("✅ Chart 2 saved")

# ── Chart 3: ROAS by Channel ────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))
channel_roas = df.groupby("channel")["roas"].mean().sort_values(ascending=False)
bars = ax.bar(channel_roas.index, channel_roas.values, color=sns.color_palette("Set2"))
ax.axhline(y=1, color="red", linestyle="--", linewidth=1, label="Break-even (ROAS = 1)")
ax.set_title("Average ROAS by Channel", fontsize=14, fontweight="bold")
ax.set_xlabel("Channel")
ax.set_ylabel("ROAS (MRR / Spend)")
ax.legend()
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
            f"{bar.get_height():.2f}x", ha="center", va="bottom", fontsize=9)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/roas_by_channel.png", dpi=150)
plt.close()
print("✅ Chart 3 saved")

# ── Chart 4: Funnel — Signups vs Paid Users by Channel ──────
fig, ax = plt.subplots(figsize=(9, 5))
funnel = df.groupby("channel")[["total_signups", "total_paid_users"]].sum().reset_index()
x = range(len(funnel))
width = 0.35
ax.bar([i - width/2 for i in x], funnel["total_signups"],  width, label="Signups",    color="#4C72B0")
ax.bar([i + width/2 for i in x], funnel["total_paid_users"], width, label="Paid Users", color="#DD8452")
ax.set_title("Funnel: Signups vs Paid Users by Channel", fontsize=14, fontweight="bold")
ax.set_xlabel("Channel")
ax.set_ylabel("Count")
ax.set_xticks(list(x))
ax.set_xticklabels(funnel["channel"])
ax.legend()
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/funnel_by_channel.png", dpi=150)
plt.close()
print("✅ Chart 4 saved")

print("\n🎉 All charts saved to outputs/charts/")