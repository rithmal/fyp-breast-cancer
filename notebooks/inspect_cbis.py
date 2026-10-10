from pathlib import Path
import pandas as pd

cbis_dir = Path(r"C:\fyp-breast-cancer\data\cbis-ddsm")

files = {
    "mass_train": "mass_case_description_train_set.csv",
    "mass_test":  "mass_case_description_test_set.csv",
    "calc_train": "calc_case_description_train_set.csv",
    "calc_test":  "calc_case_description_test_set.csv",
}

# Load each file and remember which file each row came from
frames = []
for name, filename in files.items():
    df = pd.read_csv(cbis_dir / filename)
    df["source_file"] = name
    print(f"{name}: {len(df)} rows")
    frames.append(df)

# Compare column names between a mass file and a calc file
mass_cols = set(frames[0].columns)
calc_cols = set(frames[2].columns)
print("\nColumns only in mass files:", mass_cols - calc_cols)
print("Columns only in calc files:", calc_cols - mass_cols)

# Fix the naming accident so both files use the same column name
for df in frames:
    df.rename(columns={"breast density": "breast_density"}, inplace=True)

cbis = pd.concat(frames, ignore_index=True)
print("\nCombined rows:", len(cbis))

print("\nPathology values (all files):")
print(cbis["pathology"].value_counts())

print("\nPathology by file:")
print(pd.crosstab(cbis["source_file"], cbis["pathology"]))

# Which split did each row come from?
cbis["split"] = cbis["source_file"].str.split("_").str[1]   # "train" or "test"

train_patients = set(cbis.loc[cbis["split"] == "train", "patient_id"])
test_patients  = set(cbis.loc[cbis["split"] == "test",  "patient_id"])
overlap = train_patients & test_patients

print("\nPatients in train:", len(train_patients))
print("Patients in test:", len(test_patients))
print("Patients in BOTH train and test:", len(overlap))
print("Examples:", sorted(overlap)[:10])

# D2 update: move leaky patients entirely into test (Option B)
rows_before = cbis["split"].value_counts().to_dict()
cbis.loc[cbis["patient_id"].isin(overlap), "split"] = "test"
rows_after = cbis["split"].value_counts().to_dict()

print("\nRows per split before:", rows_before)
print("Rows per split after: ", rows_after)

# Check the leak is gone
train_p = set(cbis.loc[cbis["split"] == "train", "patient_id"])
test_p  = set(cbis.loc[cbis["split"] == "test",  "patient_id"])
print("Patients in train:", len(train_p))
print("Patients in test:", len(test_p))
print("Patients in BOTH:", len(train_p & test_p))   # must be 0

label_map = {"MALIGNANT": 1, "BENIGN": 0, "BENIGN_WITHOUT_CALLBACK": 0}   # D5
cbis["label"] = cbis["pathology"].map(label_map)

print("\nImages with more than one lesion:",
      (cbis.groupby("image file path").size() > 1).sum())
print("Images where lesions have DIFFERENT labels:",
      (cbis.groupby("image file path")["label"].nunique() > 1).sum())

print("\nUnique images per split:")
print(cbis.groupby("split")["image file path"].nunique())

# D6: collapse lesion rows into one row per image.
# Image label = malignant (1) if ANY lesion on it is malignant -> max of labels.
cbis_images = (
    cbis.groupby("image file path")
        .agg(
            patient_id=("patient_id", "first"),
            side=("left or right breast", "first"),
            view=("image view", "first"),
            split=("split", "first"),
            label=("label", "max"),
            n_lesions=("label", "size"),
        )
        .reset_index()
)

print("\nImages after collapse:", len(cbis_images))          # expect 3,103
print("\nLabel balance per split (0 = benign, 1 = malignant):")
print(pd.crosstab(cbis_images["split"], cbis_images["label"], margins=True))

# Safety check: one image must never belong to two splits
assert cbis.groupby("image file path")["split"].nunique().max() == 1, "An image is in two splits!"

cbis_images.to_csv(r"C:\fyp-breast-cancer\data\cbis_images.csv", index=False)
print("Saved data/cbis_images.csv")