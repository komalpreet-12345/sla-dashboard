from src.extract import extract
from src.clean import clean
from src.transform import transform_errors

res = transform_errors(clean(extract()))
print(res["quality_flag"].value_counts())

flagged = res[res["quality_flag"] != "OK"]
print(flagged.groupby("contributor_id").size().sort_values(ascending=False).head(10))