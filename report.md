# HW3 Report — Spam/Ham Classifier (Logistic Regression)

Summary
-------
This project implements a simple end-to-end spam/ham classification pipeline using Logistic Regression and TF-IDF features. The repo was organized and scaffolded using the OpenSpec workflow: a change proposal (`openspec/changes/add-spam-classifier`) describes the feature and tasks.

What I implemented
------------------
- `preprocessing.py` — cleans the raw CSV (handles no-header files, basic token normalization, URL/email removal, number replacement).
- `train.py` — trains a `LogisticRegression` model (saga solver) on TF-IDF features and saves the model and vectorizer.
- `predict.py` — CLI to predict a single message or batch CSV; writes probabilities and predicted label.
- `app.py` — Streamlit app with dataset load, model load, class distribution, top tokens by class, ROC/PR plots, threshold sweep, and live inference buttons.
- `notebooks/spam_classifier.ipynb` — notebook skeleton to be executed locally (includes Traditional Chinese markdown explanation cells per requirement).

How OpenSpec was used
---------------------
I created an OpenSpec change `add-spam-classifier` under `openspec/changes/` with `proposal.md` and `tasks.md`. This documents the why/what/impact and provides a concrete checklist for implementation. Follow the OpenSpec validation and review steps before merging into `main`.

Reproducibility
---------------
1) Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

2) Preprocess:

```powershell
python preprocessing.py --input "D:\\test\\HW3\\sms_spam_no_header.csv" --output "D:\\test\\HW3\\sms_spam_clean.csv"
```

3) Train:

```powershell
python train.py --input "D:\\test\\HW3\\sms_spam_clean.csv" --models-dir models
```

4) Run demo:

```powershell
streamlit run app.py
```

Notes and next steps
--------------------
- The notebook should be executed locally to generate the figures required in Phase 3 (I can run it in this environment if you want and if the data is present in the workspace).
- Add tests for preprocessing and model training in `tests/` to validate behavior automatically.
- Optionally, add a Docker compose that runs Streamlit and provides a small sample dataset for reviewers.
