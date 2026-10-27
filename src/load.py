import gspread
import pandas as pd

def load(result, sheet_name="raw_deliveries", tab_name="daily_metrics"):
    gc = gspread.service_account(filename="creds.json")
    sh = gc.open(sheet_name)

    try:
        ws = sh.worksheet(tab_name)
        ws.clear()
    except gspread.exceptions.WorksheetNotFound:
        ws = sh.add_worksheet(title=tab_name, rows=len(result) + 10, cols=len(result.columns))

    out = result.copy()
    out["date"] = out["date"].astype(str)
    out = out.fillna("")   # Sheets can't store NaN

    values = [out.columns.tolist()] + out.values.tolist()
    ws.update(values=values, range_name="A1")
    print(f"Wrote {len(out)} rows to tab '{tab_name}'")

if __name__ == "__main__":
    from extract import extract
    from clean import clean
    from transform import transform
    load(transform(clean(extract())))