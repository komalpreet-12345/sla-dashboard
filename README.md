# Automated Contributor Performance & SLA Dashboard

An automated pipeline that pulls delivery data from Google Sheets, cleans and
aggregates it with Python and SQL, and powers a two-page Looker Studio dashboard
for SLA and quality tracking.

> **Note:** The data is synthetic (50 simulated contributors, 3,000 records,
> Aug 28 to Oct 17, 2026). No real client data is used.

## Architecture

Google Sheet (raw_deliveries)
→ Python: extract (Sheets API) → clean and validate
→ SQL (SQLite): daily metrics + 7-day rolling error analysis
→ Google Sheet tabs: daily_metrics, error_analysis
→ Looker Studio dashboard
→ Windows Task Scheduler (daily refresh)

## What it does

- **Extract:** reads raw delivery logs through the Google Sheets API (gspread)
- **Clean:** fixes types, drops duplicates and blank keys, and removes rows where
  completed > assigned or errors > reviewed
- **Aggregate (SQL):** throughput, accuracy, on-time SLA rate and an
  On Track / At Risk status per contributor per day
- **Error analysis (SQL):** 7-day rolling error rate with window functions,
  flagging "High Error Rate" and "Rising Errors"
- **Dashboard:** Page 1 shows SLA overview (scorecards, throughput trend,
  contributor table with red highlighting). Page 2 shows quality analysis.

## Key findings

- Overall: 96.6% accuracy, 86.2% on-time SLA, 106,434 tasks delivered
- The error analysis consistently flagged five contributors: CONTR_023,
  CONTR_007, CONTR_036, CONTR_014 and CONTR_044. Four of them also rank among
  the lowest on SLA rate.

## Time saved

| Method | Time |
|---|---|
| Manual report in Google Sheets (timed once) | ~25 minutes |
| Automated pipeline (measured, 3,000 rows) | ~10.4 seconds |

That is a reduction of over 90% (99% for the refresh alone).

## Screenshots

(Add your dashboard screenshots here: page 1, page 2, and the Sheet tabs.)

## How to run

1. Create a Google Cloud project, enable the Sheets and Drive APIs, and create a
   service account. Save its key as `creds.json` (never commit this file).
2. Share your sheet with the service account's email as Editor.
3. `pip install -r requirements.txt`
4. `python main.py`

## Project structure

main.py, src/extract.py, src/clean.py, src/transform.py, src/load.py,
src/transform.sql, src/error_analysis.sql, run_pipeline.bat

## Limitations

- Data is simulated, and the refresh is a daily batch rather than true real-time.
- The scheduled run only works while the laptop is on.