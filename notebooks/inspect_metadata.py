import pandas as pd

df = pd.read_excel(r"C:\fyp-breast-cancer\data\CMMD_clinicaldata_revision.xlsx")

print("Shape:", df.shape)
print("Columns:", list(df.columns))
print(df.head())

print("\nClassification counts:")
print(df['classification'].value_counts(dropna=False))

print("\nSubtype counts (including missing):")
print(df['subtype'].value_counts(dropna=False))

print("\nCross-tab (confirms subtype is only missing for Benign):")
print(pd.crosstab(df['classification'], df['subtype'], dropna=False))

print("\nUnique patients:", df['ID1'].nunique())

dupe_check = df.groupby(['ID1', 'LeftRight']).size()
print(dupe_check[dupe_check > 1])