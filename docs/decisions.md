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

---

## Open (must decide before the manifest is final)

- [ ] O1. What is one sample: image, breast, or patient?
- [ ] O2. BENIGN_WITHOUT_CALLBACK -> benign, or exclude?
- [ ] O3. Label for an image whose abnormalities disagree
- [ ] O4. Full mammograms vs ROI crops
- [ ] O5. Image target ("~8k") - does the actual count support it?
- [ ] O6. Report metrics per source as well as combined?
