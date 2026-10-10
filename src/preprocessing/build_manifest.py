from pathlib import Path
import pandas as pd
import pydicom

data_dir = Path(r"C:\fyp-breast-cancer\data")
clinical = pd.read_excel(data_dir / "CMMD_clinicaldata_revision.xlsx")

records = []
for dcm_path in data_dir.glob("cmmd/*/*/*/*.dcm"):
    ds = pydicom.dcmread(dcm_path, stop_before_pixels=True)  # header only, faster
    records.append({
        "path": str(dcm_path),
        "ID1": ds.PatientID,
        "LeftRight": getattr(ds, "ImageLaterality", None),
        "ViewPosition": getattr(ds, "ViewPosition", None),
    })

images_df = pd.DataFrame(records)
print("Total DICOM files found:", len(images_df))

manifest = images_df.merge(clinical, on=["ID1", "LeftRight"], how="left")

# NEW 1: the merge must not duplicate images
assert len(manifest) == len(images_df), "Merge changed the number of rows - check for duplicate clinical rows"

# NEW 2: exclude images with no clinical row (unbiopsied breasts) - see docs/decisions.md D4
unlabelled = manifest["classification"].isna()
print(f"\nExcluding {unlabelled.sum()} images with no clinical data row (D4)")
manifest[unlabelled].to_csv(data_dir / "cmmd_excluded_unlabelled.csv", index=False)  # NEW 3: keep an audit list
manifest = manifest[~unlabelled].copy()
print("Images remaining:", len(manifest))
print("Breasts remaining:", manifest.groupby(["ID1", "LeftRight"]).ngroups)

print("\nLabel distribution (after exclusion):")
print(manifest["classification"].value_counts())

# NEW 4: known open issue - ViewPosition is empty in the DICOM headers
print("\nViewPosition values:", manifest["ViewPosition"].value_counts(dropna=False).to_dict())

manifest.to_csv(data_dir / "manifest.csv", index=False)
print("\nSaved to data/manifest.csv")