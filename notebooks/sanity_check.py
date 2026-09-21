import pydicom
import matplotlib.pyplot as plt

dcm_path = r"C:\fyp-breast-cancer\data\cmmd\D1-0001\2010-07-18-79377\1-70244\608a073d-14ef-455b-be5d-f73f553b97f0.dcm"

ds = pydicom.dcmread(dcm_path)

print("Patient ID:", ds.PatientID)
print("Modality:", ds.Modality)               # should be "MG" for mammography
print("Laterality:", getattr(ds, "ImageLaterality", "not found"))   # L or R
print("View position:", getattr(ds, "ViewPosition", "not found"))  # CC or MLO
print("Image shape:", ds.pixel_array.shape)

plt.imshow(ds.pixel_array, cmap="gray")
plt.title(f"{ds.PatientID} - {getattr(ds, 'ImageLaterality', '?')} {getattr(ds, 'ViewPosition', '?')}")
plt.axis("off")
plt.show()