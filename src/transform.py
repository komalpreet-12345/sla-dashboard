import sqlite3
import pandas as pd

def transform(df, sql_path="src/transform.sql"):
    conn = sqlite3.connect(":memory:")
    df.to_sql("deliveries", conn, index=False, if_exists="replace")

    with open(sql_path) as f:
        query = f.read()

    result = pd.read_sql_query(query, conn)
    conn.close()
    print(f"Aggregated into {len(result)} daily contributor rows")
    return result

def transform_errors(df, sql_path="src/error_analysis.sql"):
    conn = sqlite3.connect(":memory:")
    df.to_sql("deliveries", conn, index=False, if_exists="replace")

    with open(sql_path) as f:
        query = f.read()

    result = pd.read_sql_query(query, conn)
    conn.close()
    print(f"Error analysis: {len(result)} rows, "
          f"{(result['quality_flag'] != 'OK').sum()} flagged")
    return result

if __name__ == "__main__":
    from extract import extract
    from clean import clean
    out = transform(clean(extract()))
    print(out.head())
    print(out["sla_status"].value_counts())