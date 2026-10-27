import gspread
import pandas as pd

def extract():
    gc = gspread.service_account(filename="creds.json")
    ws = gc.open("raw_deliveries").worksheet("data")
    return pd.DataFrame(ws.get_all_records())

if __name__ == "__main__":
    print(extract().head())