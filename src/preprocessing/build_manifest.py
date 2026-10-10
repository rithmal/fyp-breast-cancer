from pathlib import Path
import pydicom
import pandas as pd

data_dir = Path(r"C:\fyp-breast-cancer\data")
clinical = pd.read_excel(data_dir / "CMMD_clinicaldata_revision.xlsx")

records = []
for dcm_path in data_dir.glob("cmmd/*/*/*/*.dcm"):
    ds = pydicom.dcmread(dcm_path, stop_before_pixels=True)  # skip pixel data — we only need header tags here, much faster
    records.append({
        "path": str(dcm_path),
        "ID1": ds.PatientID,
        "LeftRight": getattr(ds, "ImageLaterality", None),
        "ViewPosition": getattr(ds, "ViewPosition", None),
    })

images_df = pd.DataFrame(records)
print("Total DICOM files found:", len(images_df))

manifest = images_df.merge(clinical, on=["ID1", "LeftRight"], how="left")

print("Images with no matching metadata row:", manifest["classification"].isna().sum())
print("\nLabel distribution across all images:")
print(manifest["classification"].value_counts(dropna=False))
print("\nSubtype distribution across all images:")
print(manifest["subtype"].value_counts(dropna=False))

manifest.to_csv(data_dir / "manifest.csv", index=False)
print("\nSaved to data/manifest.csv")