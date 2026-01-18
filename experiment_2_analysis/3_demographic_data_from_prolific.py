import pandas as pd

prolific_demographic_file_location = '/Users/ed/Documents/prolific_demographic_export_682c8b96d3e552401090b0e3.csv'

df = pd.read_csv(prolific_demographic_file_location)
print(df.head())
df = df[~df["Completion code"].isna()]
print(len(df))
df["Age"] = df["Age"].astype("float32")
print(df["Age"].agg(["mean", "std", "min", "max"]))