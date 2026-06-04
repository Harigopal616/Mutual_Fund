import pandas as pd

df = pd.read_csv("data/transactions.csv")

df.columns = df.columns.str.replace("'", "", regex=False)

print(df[[
    'INV_NAME',
    'PAN',
    'SCHEME',
    'TRADDATE',
    'PURPRICE',
    'UNITS',
    'AMOUNT'
]].head())