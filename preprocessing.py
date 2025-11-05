"""
preprocessing.py

Reads the raw SMS spam CSV (no header) and writes a cleaned CSV.

Assumptions:
- If input CSV has no header, first column is label (spam/ham), second column is message text.
- Default input: D:\test\HW3\sms_spam_no_header.csv
- Default output: D:\test\HW3\sms_spam_clean.csv

Usage:
    python preprocessing.py --input "D:\\test\\HW3\\sms_spam_no_header.csv" --output "D:\\test\\HW3\\sms_spam_clean.csv"
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from typing import Callable

import pandas as pd


def basic_clean(text: str) -> str:
    if pd.isna(text):
        return ""
    # to string
    text = str(text)
    text = text.lower()
    # replace numbers with token
    text = re.sub(r"\d+", " <NUM> ", text)
    # remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    # remove email addresses
    text = re.sub(r"\S+@\S+", " ", text)
    # remove punctuation (keep basic tokens and <NUM>)
    text = re.sub(r"[^\w\s<>]", " ", text)
    # collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_input(path: str) -> pd.DataFrame:
    # Try reading with header first, else fallback to no header
    try:
        df = pd.read_csv(path)
    except Exception:
        # fallback to no header, assume two columns: label, text
        df = pd.read_csv(path, header=None, encoding="utf-8", names=["label", "text"])
    # If only one column exists, attempt to split by comma
    if df.shape[1] == 1:
        col = df.columns[0]
        # try splitting into label,text
        parts = df[col].str.split(",", n=1, expand=True)
        if parts.shape[1] == 2:
            df = pd.DataFrame({"label": parts[0], "text": parts[1]})
    return df


def clean_df(df: pd.DataFrame, text_col: str = "text", label_col: str = "label") -> pd.DataFrame:
    # Ensure columns exist
    if label_col not in df.columns:
        raise KeyError(f"Label column '{label_col}' not found in dataframe")
    if text_col not in df.columns:
        raise KeyError(f"Text column '{text_col}' not found in dataframe")

    df = df[[label_col, text_col]].rename(columns={label_col: "label", text_col: "text"})
    # Normalize labels
    df["label"] = df["label"].astype(str).str.strip().str.lower().map(lambda s: "spam" if s.startswith("spam") or s == "1" else "ham")
    df["text_clean"] = df["text"].apply(basic_clean)
    # drop empty
    df = df.dropna(subset=["text_clean"]).loc[df["text_clean"].str.len() > 0]
    return df[["label", "text", "text_clean"]]


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=r"D:\\test\\HW3\\sms_spam_no_header.csv")
    parser.add_argument("--output", default=r"D:\\test\\HW3\\sms_spam_clean.csv")
    parser.add_argument("--text-col", default="text")
    parser.add_argument("--label-col", default="label")
    args = parser.parse_args(argv)

    if not os.path.exists(args.input):
        print(f"Input file not found: {args.input}")
        sys.exit(2)

    df = load_input(args.input)
    df_clean = clean_df(df, text_col=args.text_col, label_col=args.label_col)
    # Save
    out_dir = os.path.dirname(args.output)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    df_clean.to_csv(args.output, index=False, encoding="utf-8")
    print(f"Saved cleaned dataset to {args.output} (rows={len(df_clean)})")


if __name__ == "__main__":
    main()
