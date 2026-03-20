# Marketing Data Engineering Portfolio

Six years running paid marketing across B2B SaaS. I've built attribution models, scaled campaigns to 36x ROAS, automated reporting pipelines with CRM APIs, and worked across the full funnel from acquisition to retention. The marketing side isn't new to me.

What this repo is about: closing the last gap — owning the data infrastructure that most marketers outsource to analysts or engineers.

---

## The actual gap I'm closing

I've always been the person on the marketing team who goes further with data than expected. Built cohort models in spreadsheets when the BI tool wasn't flexible enough. Wrote Python scripts to pull campaign data when the native exports were insufficient. Designed attribution logic from scratch when the default last-click model was misleading leadership.

The missing piece was never understanding the problem — it was not having formal fluency in the tooling that data and engineering teams use. dbt, BigQuery, proper SQL modeling, production-grade pipelines. This project is where I'm building that.

---

## Background

Currently working at an AI SaaS startup in Germany. Previously: performance marketing across Google, LinkedIn, and Meta, with hands-on experience in:

- Multi-touch attribution and cohort tracking
- CRM workflow automation via APIs
- Campaign analytics and funnel modeling
- Growth experimentation frameworks

---

## Tech stack

| Layer | Tool |
|---|---|
| Analytics & modeling | SQL |
| Data warehouse | BigQuery |
| Transformation layer | dbt |
| Scripting & automation | Python |
| AI tooling | OpenAI API / Claude API |
| Workflow automation | n8n / Make |

---

## What I'm building

The project simulates a B2B SaaS marketing data stack — the kind used by companies with a dedicated data team. The difference is I'm building it myself, which means understanding every layer.

### Data layer

Simulated datasets modeled after real SaaS marketing:

- `google_ads_campaigns`
- `linkedin_ads_campaigns`
- `website_sessions`
- `signups`
- `subscriptions`

### SQL analytics models

Not just queries — structured models with proper grain, incremental logic, and reusable CTEs. The metrics: CAC, ROAS, funnel conversion, paid vs organic split, and attribution.

```sql
SELECT
  date,
  channel,
  campaign,
  SUM(spend)                             AS total_spend,
  SUM(clicks)                            AS total_clicks,
  SUM(signups)                           AS total_signups,
  SUM(spend) / NULLIF(SUM(clicks), 0)    AS cpc,
  SUM(spend) / NULLIF(SUM(signups), 0)   AS cpa,
  SUM(signups) / NULLIF(SUM(clicks), 0)  AS conversion_rate
FROM campaigns
GROUP BY 1, 2, 3;
```

### AI marketing tools

Built on top of the data layer — not standalone toys:

- Campaign performance summarizer (structured data → plain-English insight)
- Ad copy generator benchmarked against historical CTR patterns
- SEO content brief generator

### Dashboards

Self-serve reporting across CAC by channel, funnel performance, and campaign ROI — designed to replace the "can you pull this for me" requests.

---

## Project structure

```
marketing-data-engineering/
├── data/          # Simulated SaaS datasets
├── sql/           # Analytics models and queries
├── python/        # Scripts and AI tools
├── dashboards/    # Marketing dashboards
└── docs/          # Notes and write-ups
```

---

## Status

- [x] SaaS dataset simulation
- [x] Core SQL campaign analysis
- [ ] dbt models
- [ ] BigQuery integration
- [ ] Dashboards
- [ ] AI automation layer

---

## Connect

- Portfolio: [akshundogra.com](https://akshundogra.com/?utm_source=github&utm_term=marketing-analytics-engineering-readme)
- LinkedIn: [linkedin.com/in/akshundogra](https://www.linkedin.com/in/akshundogra)
- YouTube: [youtube.com/@akshundogra](https://www.youtube.com/@akshundogra)
