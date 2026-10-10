# Decisions Log

Every number and decision in the proposal should trace back to this file.
Write the reasoning in your own words. Add a source where one supports it.

---

## Verified facts

| Fact | Value | How verified | Date |
|---|---|---|---|
| CBIS mass_train rows | 1,318 | loaded CSV | 2026-10-10 |
| CBIS mass_test rows | 378 | loaded CSV | 2026-10-10 |
| CBIS calc_train rows | 1,546 | loaded CSV | 2026-10-10 |
| CBIS calc_test rows | 326 | loaded CSV | 2026-10-10 |
| CBIS rows total (one row = ? ) | 3,568 | sum of above | 2026-10-10 |
| CBIS unique full mammograms | TODO | | |
| CBIS unique participants | TODO (TCIA states 1,566) | | |
| CMMD patients (download) | 1,775 | NBIA download | 2026-09 |
| CMMD DICOM files (download) | 5,202 | NBIA download | 2026-09 |
| CMMD clinical spreadsheet rows | 1,872 (one row = ?) | loaded CMMD_clinicaldata_revision.xlsx | 2026-09 |
| CMMD images actually used | TODO (TCIA text says 3,728; why 5,202 on disk?) | | |
| CMMD benign / malignant | TODO | | |

---

## Decided

### D1. Combine CBIS-DDSM with CMMD
- Reasoning: TODO
- Known risks: film vs digital domain shift; label level differs (CBIS per abnormality, CMMD per breast)

### D2. Keep CBIS-DDSM official train/test split
- Reasoning: TODO
- Still to resolve: where the validation set comes from; whether any participant crosses train/test

### D3. Stratified split for CMMD, grouped by patient
- Stratify on: TODO (label only? label + finding type?)
- Reasoning: TODO

### D4. Exclude CMMD images with no clinical data row
- What: Drop the 1,458 DICOMs whose (PatientID, side) has no row in
  CMMD_clinicaldata_revision.xlsx. Audit list saved to data/cmmd_excluded_unlabelled.csv.
- Why: These images have no clinical data row, so the dataset provides no biopsy-confirmed label for them. Labelling them benign would treat “not biopsied” as equivalent to CMMD’s “Benign”, which means a biopsy-confirmed benign lesion, and would add unverified labels to a dataset chosen specifically because its ground truth is biopsy-confirmed.
- Evidence:
  - 3,744 images matched a clinical row = 1,872 rows x 2 views (exact).
  - Example: D2-0001 has a clinical row for L only; its R images are unmatched.
  - TCIA describes 3,728 biopsy-confirmed mammographies but lists 5,202 images;
    the extra images are not documented. Flowchart: inclusion = histologically
    confirmed breast, n=1,872. (TCIA CMMD page, DOI 10.7937/tcia.eqde-4b16)
- Consequence: CMMD = 3,744 images (2,632 malignant, 1,112 benign, ~70% malignant).
  Combined total with CBIS is below ~7,300, not "8k+".
- Limitation: model never sees normal (unbiopsied) breasts -> lesion classification,
  not screening.
- Still open: 16-image gap between 3,744 and TCIA's 3,728.
- ViewPosition is empty in all CMMD DICOM headers. Not needed: the model classifies single images, and the split is grouped by patient, so both views of a breast stay together.

### D5. Merge CBIS-DDSM BENIGN_WITHOUT_CALLBACK into benign
- What: Map pathology values to binary labels:
  MALIGNANT -> 1; BENIGN -> 0; BENIGN_WITHOUT_CALLBACK -> 0.
  Affects 682 of 3,568 abnormality rows (calc_train 474, calc_test 67,
  mass_train 104, mass_test 37).
- Why (DRAFT - check against my own understanding):
  Unlike the CMMD images excluded in D4, which have no clinical row and no
  recorded lesion, BENIGN_WITHOUT_CALLBACK rows describe a specific lesion
  that the dataset explicitly labels as benign. Merging them into benign
  [is common practice in prior CBIS-DDSM work - CITE 2-3 PAPERS].
- Evidence:
  - Pathology counts from the four case-description CSVs (inspect_cbis.py).
  - Definition of BENIGN_WITHOUT_CALLBACK: [VERIFY in Lee et al. 2017,
    DOI 10.1038/sdata.2017.177, or Heath et al. 2001 DDSM documentation].
- Risk: If these lesions were not biopsied, their labels rest on radiologist
  judgement rather than pathology -> possible label noise in the benign class,
  concentrated in calcification training cases.
- Mitigation: Sensitivity analysis - train with and without these rows and
  compare results.
- Still open: Image-level label when one image has abnormalities with
  different labels (O3).

### D2. Keep CBIS-DDSM official train/test split (modified)
- What: Use the official split, but move the 31 patients who appear in both
  train and test entirely into test (their train rows reassigned to test).
- Why: TODO (my own words)
- Evidence: 1,248 train + 349 test - 31 overlap = 1,566 unique patients
  (matches TCIA). Leak found with inspect_cbis.py.
- Consequence: Split is no longer identical to the official one -> direct
  comparison with papers using the official split is approximate.
  Rows: train [X] / test [Y] (fill in from output).
- Still open: validation set (carve from train BY PATIENT).

### D6. Image-level label for images with multiple lesions
- What: One row per full mammogram. Label = malignant if ANY lesion on the image
  is malignant (max of lesion labels).
- Why: TODO (my own words)
- Evidence: 293 images have >1 lesion; 17 have conflicting labels
  (inspect_cbis.py).
- Consequence: 17 images labelled malignant that also contain benign lesions.
  CBIS = 3,103 images (train 2,394 / test 709).
- Alternative considered: drop the 17 (Option B) - possible sensitivity check.
---

## Open (must decide before the manifest is final)

- [ ] O1. What is one sample: image, breast, or patient?
- [ ] O2. BENIGN_WITHOUT_CALLBACK -> benign, or exclude?
- [ ] O3. Label for an image whose abnormalities disagree
- [ ] O4. Full mammograms vs ROI crops
- [ ] O5. Image target ("~8k") - does the actual count support it?
- [ ] O6. Report metrics per source as well as combined?
