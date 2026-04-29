import pandas as pd

COLUMNS = ["A1","A2","A3","A4","A5","A6","A7","A8",
           "A9","A10","A11","A12","A13","A14","A15","A16"]

df = pd.read_csv("credit_approval/crx.data", header=None, names=COLUMNS, na_values="?")
df.to_csv("credit_approval/credit_approval.csv", index=False)
print(f"Saved {len(df)} rows to credit_approval/credit_approval.csv")
