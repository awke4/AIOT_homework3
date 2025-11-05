# Change: add-spam-classifier

## Why
Implement a complete spam/ham classifier pipeline for HW3 using Logistic Regression. This includes preprocessing, training, evaluation, a reproducible notebook, a Streamlit demo app, and a final report. The goal is to provide a reproducible end-to-end solution students can run locally and extend.

## What Changes
- ADDED: `preprocessing.py` to clean raw dataset and write a cleaned CSV.
- ADDED: `train.py` and `predict.py` for model training, evaluation, and CLI prediction.
- ADDED: `notebooks/spam_classifier.ipynb` containing the full pipeline with Traditional Chinese explanations per code cell.
- ADDED: `app.py` Streamlit application for interactive demos and live inference.
- ADDED: `report.md` documenting methodology and how OpenSpec was used.

**BREAKING:** None.

## Impact
- Affected specs: `ml` (new capability describing spam classifier pipeline)
- Affected code: top-level scripts and docs; no changes to existing services.
- Operational: Requires Python 3.10+, scikit-learn, pandas, joblib, and Streamlit for the demo. Dataset path is expected at `D:\test\HW3\sms_spam_no_header.csv` by default.
