# HW3 — Spam/Ham Classifier (Logistic Regression)

This repository contains the HW3 implementation to build a spam/ham classifier using Logistic Regression.

Files added:
- `preprocessing.py` — cleans raw dataset and writes cleaned CSV
- `train.py` — trains logistic regression with TF-IDF and saves model
- `predict.py` — CLI for model prediction on single text or CSV
- `app.py` — Streamlit demo app for interactive exploration and live inference
- `requirements.txt` — Python dependencies
- `notebooks/spam_classifier.ipynb` — (skeleton) notebook for end-to-end pipeline
- `report.md` — final report describing methodology and OpenSpec usage

Quick start (Windows PowerShell):

```powershell
python -m pip install -r requirements.txt
# 1) Preprocess (adjust input path as needed)
python preprocessing.py --input "D:\\test\\HW3\\sms_spam_no_header.csv" --output "D:\\test\\HW3\\sms_spam_clean.csv"

# 2) Train
python train.py --input "D:\\test\\HW3\\sms_spam_clean.csv" --models-dir models

# 3) Predict single text
python predict.py --model-dir models --text "Free entry to win a prize"

# 4) Run Streamlit demo
streamlit run app.py
```

Notes:
- The dataset path used above is the path you provided. If you store datasets elsewhere, pass the correct path.
- The notebook includes Traditional Chinese markdown for each code cell's explanation; run it locally to execute the cells and generate visual outputs.
