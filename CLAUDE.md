# Instructions for Claude Code

## How to work with me
This is my Final Year Project. I must understand and defend every line of it.
- Explain your reasoning before or alongside any code you write.
- Do NOT make dataset or methodology decisions for me (label mapping, which
  rows to drop, split strategy, preprocessing choices). When a decision is
  needed, stop, explain the options and trade-offs, and ask me.
- Once I decide, record it in `docs/decisions.md` only with the reasoning I give.
- Flag data leakage risks, silent row drops, and unexplained count changes.
- Print row/image/participant counts after every transformation step.
- Never fabricate dataset facts. If unsure, say so and tell me how to check.

## Project
Binary benign vs malignant classification on mammography.
Datasets: CMMD (full-field digital, single vendor) + CBIS-DDSM (digitised film,
multiple scanners). See `docs/decisions.md` for decided and open items.

## Data rules
- Never commit data. Everything under `data/` is git-ignored (TCIA policy).
- Splits must be patient-level: no participant in more than one split.
- CBIS-DDSM `patient_id` (e.g. `P_00001`) is the true participant ID; the long
  DICOM IDs (e.g. `Calc-Test_P_00038_LEFT_CC`) are NOT participants.

## Repo layout
- `src/preprocessing/` manifest building and image preprocessing
- `src/models/` model definitions and training
- `src/evaluation/` metrics and analysis
- `notebooks/` exploration only
- Python env: `.venv` (Windows)
