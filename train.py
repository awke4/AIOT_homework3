"""
train.py

Train a Logistic Regression model on the cleaned SMS spam dataset.

Usage:
    python train.py --input "D:\\test\\HW3\\sms_spam_clean.csv" --models-dir ./models --test-size 0.2 --random-seed 42

Outputs:
- models/model.joblib
- models/vectorizer.joblib
"""
from __future__ import annotations

import argparse
import os
from dataclasses import dataclass

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split


@dataclass
class TrainConfig:
    input_csv: str
    models_dir: str
    test_size: float = 0.2
    seed: int = 42


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="utf-8")
    if "text_clean" not in df.columns:
        if "text" in df.columns:
            df["text_clean"] = df["text"].astype(str)
        else:
            raise KeyError("Input CSV must contain 'text_clean' or 'text' column")
    return df


def train_and_save(cfg: TrainConfig) -> None:
    df = load_data(cfg.input_csv)
    X = df["text_clean"].astype(str).values
    y = (df["label"] == "spam").astype(int).values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=cfg.test_size, random_state=cfg.seed, stratify=y)

    vectorizer = TfidfVectorizer(max_features=20000, ngram_range=(1, 2))
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    model = LogisticRegression(max_iter=1000, solver="saga")
    model.fit(X_train_vec, y_train)

    # Evaluate
    preds = model.predict(X_test_vec)
    probs = model.predict_proba(X_test_vec)[:, 1]
    print(classification_report(y_test, preds, digits=4))
    try:
        auc = roc_auc_score(y_test, probs)
        print(f"ROC AUC: {auc:.4f}")
    except Exception:
        pass

    # Save
    os.makedirs(cfg.models_dir, exist_ok=True)
    model_path = os.path.join(cfg.models_dir, "model.joblib")
    vec_path = os.path.join(cfg.models_dir, "vectorizer.joblib")
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vec_path)
    print(f"Saved model to {model_path}")
    print(f"Saved vectorizer to {vec_path}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=r"D:\\test\\HW3\\sms_spam_clean.csv")
    parser.add_argument("--models-dir", default="models")
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--random-seed", type=int, default=42)
    args = parser.parse_args(argv)
    cfg = TrainConfig(input_csv=args.input, models_dir=args.models_dir, test_size=args.test_size, seed=args.random_seed)
    train_and_save(cfg)


if __name__ == "__main__":
    main()
