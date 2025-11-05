"""
predict.py

CLI for loading a saved model and vectorizer and predicting spam probability for a single text or for a CSV.

Usage examples:
    python predict.py --model-dir models --text "Free entry to win a prize"
    python predict.py --model-dir models --input-csv D:\\test\\HW3\\sms_spam_clean.csv --output-csv out_with_preds.csv
"""
from __future__ import annotations

import argparse
import os
from typing import Iterable

import joblib
import pandas as pd


def load_model(model_dir: str):
    model_path = os.path.join(model_dir, "model.joblib")
    vec_path = os.path.join(model_dir, "vectorizer.joblib")
    if not os.path.exists(model_path) or not os.path.exists(vec_path):
        raise FileNotFoundError(f"Model or vectorizer not found in {model_dir}")
    model = joblib.load(model_path)
    vectorizer = joblib.load(vec_path)
    return model, vectorizer


def predict_texts(model, vectorizer, texts: Iterable[str]):
    X = vectorizer.transform([t if t is not None else "" for t in texts])
    probs = model.predict_proba(X)[:, 1]
    preds = (probs >= 0.5).astype(int)
    return preds, probs


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-dir", default="models")
    parser.add_argument("--text", help="Single text to predict")
    parser.add_argument("--input-csv", help="CSV file with `text_clean` or `text` column")
    parser.add_argument("--output-csv", help="If set and input-csv provided, write results to this path")
    parser.add_argument("--threshold", type=float, default=0.5)
    args = parser.parse_args(argv)

    model, vectorizer = load_model(args.model_dir)

    if args.text:
        preds, probs = predict_texts(model, vectorizer, [args.text])
        label = "spam" if preds[0] == 1 else "ham"
        print(f"Text: {args.text}\nPrediction: {label} (p_spam={probs[0]:.4f})")
        return

    if args.input_csv:
        df = pd.read_csv(args.input_csv, encoding="utf-8")
        if "text_clean" in df.columns:
            texts = df["text_clean"].astype(str).tolist()
        elif "text" in df.columns:
            texts = df["text"].astype(str).tolist()
        else:
            raise KeyError("Input CSV must contain 'text_clean' or 'text' column")

        preds, probs = predict_texts(model, vectorizer, texts)
        df["pred_spam"] = preds
        df["p_spam"] = probs
        if args.output_csv:
            df.to_csv(args.output_csv, index=False, encoding="utf-8")
            print(f"Wrote predictions to {args.output_csv}")
        else:
            print(df[[c for c in ["text", "text_clean", "label"] if c in df.columns] + ["pred_spam", "p_spam"]].head(20))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
