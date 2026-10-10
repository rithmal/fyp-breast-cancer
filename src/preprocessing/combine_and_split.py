from pathlib import Path
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold

data_dir = Path(r"C:\fyp-breast-cancer\data")
SEED = 42  # fixed so the split is the same every time you run it

# --- Load both datasets ---
cmmd = pd.read_csv(data_dir / "manifest.csv")
cbis = pd.read_csv(data_dir / "cbis_images.csv")

# --- Put both into the same columns ---
cmmd_std = pd.DataFrame({
    "source": "CMMD",
    "participant_id": cmmd["ID1"],
    "side": cmmd["LeftRight"],
    "image_path": cmmd["path"],
    "label": cmmd["classification"].map({"Benign": 0, "Malignant": 1}),
})
cbis_std = pd.DataFrame({
    "source": "CBIS",
    "participant_id": cbis["patient_id"],
    "side": cbis["side"],
    "image_path": cbis["image file path"],   # NOTE: must be matched to downloaded files later
    "label": cbis["label"],
})
df = pd.concat([cmmd_std, cbis_std], ignore_index=True)
print("Combined images:", len(df))                     # expect 6,847
assert df["label"].notna().all(), "Some images have no label"

# --- Split once: grouped by patient, stratified by source + label ---
strata = df["source"] + "_" + df["label"].astype(str)
groups = df["source"] + "_" + df["participant_id"].astype(str)

# Step A: hold out ~15% as test (1 fold out of 7 = ~14%)
sgkf = StratifiedGroupKFold(n_splits=7, shuffle=True, random_state=SEED)
trainval_idx, test_idx = next(sgkf.split(df, strata, groups))
df["split"] = "train"
df.loc[test_idx, "split"] = "test"

# Step B: from the rest, hold out ~15% of the total as validation (1 of 6 = ~17% of remainder)
rest = df[df["split"] == "train"]
sgkf2 = StratifiedGroupKFold(n_splits=6, shuffle=True, random_state=SEED)
_, val_rel = next(sgkf2.split(rest, strata[rest.index], groups[rest.index]))
df.loc[rest.index[val_rel], "split"] = "val"

# --- Checks ---
leak = df.groupby(groups)["split"].nunique()
assert (leak == 1).all(), f"{(leak > 1).sum()} patients appear in more than one split"
print("\nLeakage check passed: no patient in more than one split")

print("\nImages per split:")
print(df["split"].value_counts(normalize=True).round(3))
print("\nSplit x source x label:")
print(pd.crosstab([df["split"], df["source"]], df["label"], margins=True))

df.to_csv(data_dir / "combined_manifest.csv", index=False)
print("\nSaved data/combined_manifest.csv")