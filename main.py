from src.extract import extract
from src.clean import clean
from src.transform import transform, transform_errors
from src.load import load

if __name__ == "__main__":
    df = clean(extract())
    load(transform(df), tab_name="daily_metrics")
    load(transform_errors(df), tab_name="error_analysis")