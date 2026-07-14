import pandas as pd

df = pd.read_csv(
    "data/anagrafiche/gi_comuni.csv",
    sep=";"
)

print(df.columns)
print(df.head())