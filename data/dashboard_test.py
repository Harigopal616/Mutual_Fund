import pandas as pd

df = pd.read_csv("data/transactions.csv")

df.columns = df.columns.str.replace("'", "", regex=False)

summary = (
    df.groupby("SCHEME")
      .agg({
          "AMOUNT": "sum",
          "UNITS": "sum"
      })
      .reset_index()
)

print(summary.head())