import pandas as pd

def clean(df):
    raw_rows = len(df)

    # Fix types
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["due_time"] = pd.to_datetime(df["due_time"], errors="coerce")
    df["submitted_time"] = pd.to_datetime(df["submitted_time"], errors="coerce")
    for col in ["tasks_assigned", "tasks_completed", "tasks_reviewed", "errors_found"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop rows with missing key fields and duplicate task IDs
    df = df.dropna(subset=["contributor_id", "date", "tasks_assigned", "tasks_completed"])
    df = df.drop_duplicates(subset="task_id")

    # Validation rules
    df = df[df["tasks_completed"] <= df["tasks_assigned"]]
    df = df[df["errors_found"] <= df["tasks_reviewed"]]

    # Derived column
    df["on_time"] = (df["submitted_time"] <= df["due_time"]).astype(int)

    print(f"Cleaned: {raw_rows} rows in, {len(df)} rows out, {raw_rows - len(df)} removed")
    return df

if __name__ == "__main__":
    from extract import extract
    print(clean(extract()).head())