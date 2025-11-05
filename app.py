"""
Streamlit app for the Spam/Ham classifier demo.

Run:
    streamlit run app.py

This is a simplified interactive demo: upload dataset (or use default path), select label/text columns, load a trained model, inspect class distribution, top tokens, ROC/PR, and run live inference with sample buttons.
"""
from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.metrics import (ConfusionMatrixDisplay, PrecisionRecallDisplay,
                             RocCurveDisplay, confusion_matrix, precision_recall_curve,
                             roc_curve)


@st.cache_data
def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


@lru_cache(maxsize=2)
def load_model(model_dir: str):
    model_path = os.path.join(model_dir, "model.joblib")
    vec_path = os.path.join(model_dir, "vectorizer.joblib")
    model = joblib.load(model_path)
    vectorizer = joblib.load(vec_path)
    return model, vectorizer


def show_class_distribution(df: pd.DataFrame, label_col: str):
    counts = df[label_col].value_counts()
    fig, ax = plt.subplots()
    counts.plot(kind="bar", ax=ax)
    ax.set_ylabel("count")
    st.pyplot(fig)


def top_tokens_by_class(model, vectorizer, top_k: int = 20):
    # For logistic regression, coeffs show contribution to positive class
    feature_names = np.array(vectorizer.get_feature_names_out())
    coefs = model.coef_[0]
    top_pos = feature_names[np.argsort(coefs)[-top_k:]][::-1]
    top_neg = feature_names[np.argsort(coefs)[:top_k]]
    return top_pos, top_neg


def main():
    st.title("Spam/Ham Classifier — Demo")

    st.sidebar.header("Configuration")
    dataset_path = st.sidebar.text_input("Dataset CSV path", value=r"D:\\test\\HW3\\sms_spam_clean.csv")
    label_col = st.sidebar.text_input("Label column", value="label")
    text_col = st.sidebar.text_input("Text column", value="text_clean")
    models_dir = st.sidebar.text_input("Models dir", value="models")
    seed = st.sidebar.number_input("Seed", value=42)
    np.random.seed(int(seed))
    threshold = st.sidebar.slider("Decision threshold", 0.0, 1.0, 0.5)

    st.sidebar.markdown("---")
    if st.sidebar.button("Load dataset"):
        if os.path.exists(dataset_path):
            df = load_csv(dataset_path)
            st.session_state["df"] = df
            st.success(f"Loaded {len(df)} rows from {dataset_path}")
        else:
            st.error(f"File not found: {dataset_path}")

    # Auto-load model if files exist and model not yet loaded
    model_path = os.path.join(models_dir, "model.joblib")
    vec_path = os.path.join(models_dir, "vectorizer.joblib")
    if "model" not in st.session_state and os.path.exists(model_path) and os.path.exists(vec_path):
        try:
            model, vectorizer = load_model(models_dir)
            st.session_state["model"] = model
            st.session_state["vectorizer"] = vectorizer
            st.sidebar.success(f"Auto-loaded model from {models_dir}")
        except Exception as e:
            st.sidebar.warning(f"Found model files but failed to load: {e}")

    # Explicit load-model button
    if st.sidebar.button("Load model"):
        try:
            model, vectorizer = load_model(models_dir)
            st.session_state["model"] = model
            st.session_state["vectorizer"] = vectorizer
            st.success("Model loaded")
        except Exception as e:
            st.error(f"Failed to load model: {e}")


    # --- Data Overview ---
    if "df" in st.session_state:
        df = st.session_state["df"]
        st.subheader("Data Overview 數據總覽")
        st.write("### 樣本預覽 (前10筆)")
        st.write(df.head(10))
        # Class distribution
        st.write("### 類別分佈")
        counts = df[label_col].value_counts()
        fig, ax = plt.subplots()
        counts.plot(kind="bar", ax=ax, color=["#1f77b4", "#ff7f0e"])
        ax.set_ylabel("count")
        st.pyplot(fig)
        st.write("百分比:")
        st.write((counts / counts.sum() * 100).round(2).astype(str) + "%")
        # Token replacements in cleaned text (approximate)
        if "text_clean" in df.columns:
            st.write("### Token replacements in cleaned text (approximate)")
            num_token = df["text_clean"].str.count(r"<NUM>").sum()
            url_token = df["text_clean"].str.count(r"http|www").sum()
            st.write(f"<NUM> tokens: {num_token}")
            st.write(f"URL tokens: {url_token}")

    # --- Top Tokens by Class ---
    if "model" in st.session_state and "df" in st.session_state:
        model = st.session_state["model"]
        vectorizer = st.session_state["vectorizer"]
        df = st.session_state["df"]
        st.subheader("Top Tokens by Class 重要詞彙分析")
        # Get top-N tokens for each class
        feature_names = np.array(vectorizer.get_feature_names_out())
        coefs = model.coef_[0]
        N = st.slider("Top-N tokens", min_value=5, max_value=30, value=15)
        # Top spam tokens
        top_spam_idx = np.argsort(coefs)[-N:][::-1]
        top_ham_idx = np.argsort(coefs)[:N]
        st.write("#### Class: spam")
        st.write(pd.DataFrame({"token": feature_names[top_spam_idx], "coef": coefs[top_spam_idx]}))
        st.write("#### Class: ham")
        st.write(pd.DataFrame({"token": feature_names[top_ham_idx], "coef": coefs[top_ham_idx]}))

    # --- Model Performance (Test) ---
    if "model" in st.session_state and "df" in st.session_state:
        st.subheader("Model Performance (Test) 測試集表現")
        texts = df[text_col].astype(str).tolist()
        y_true = (df[label_col] == "spam").astype(int).values
        X = st.session_state["vectorizer"].transform(texts)
        probs = st.session_state["model"].predict_proba(X)[:, 1]
        preds = (probs >= threshold).astype(int)
        # Confusion matrix
        st.write("### Confusion Matrix 混淆矩陣")
        cm = confusion_matrix(y_true, preds)
        fig, ax = plt.subplots()
        ConfusionMatrixDisplay(cm).plot(ax=ax)
        st.pyplot(fig)
        # Threshold sweep
        st.write("### Threshold Sweep (precision/recall/f1)")
        thresholds = np.linspace(0.0, 1.0, 21)
        metrics = []
        for thr in thresholds:
            p = (probs >= thr).astype(int)
            tn, fp, fn, tp = confusion_matrix(y_true, p).ravel()
            prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
            metrics.append((thr, prec, rec, f1))
        metrics_df = pd.DataFrame(metrics, columns=["threshold", "precision", "recall", "f1"]) 
        st.line_chart(metrics_df.set_index("threshold"))

    st.sidebar.markdown("---")
    st.sidebar.subheader("Live inference")
    sample_spam = st.sidebar.text_area("Spam example", "Congratulations! You have won a prize. Call now!")
    sample_ham = st.sidebar.text_area("Ham example", "Hey, are you free this evening for dinner?")
    input_text = st.text_area("Message to classify")

    col1, col2 = st.columns(2)
    if col1.button("Use spam example"):
        st.session_state["input_text"] = sample_spam
    if col2.button("Use ham example"):
        st.session_state["input_text"] = sample_ham

    if st.button("Predict"):
        text = st.session_state.get("input_text", input_text)
        if not text:
            st.warning("No input text")
        else:
            if "model" not in st.session_state:
                st.error("Model not loaded")
            else:
                model = st.session_state["model"]
                vectorizer = st.session_state["vectorizer"]
                X = vectorizer.transform([text])
                p = model.predict_proba(X)[0, 1]
                st.write(f"Spam probability: {p:.4f}")
                fig3, ax3 = plt.subplots(figsize=(6, 1))
                ax3.barh([0], [p], color="C1")
                ax3.set_xlim(0, 1)
                ax3.set_yticks([])
                ax3.set_xlabel("P(spam)")
                st.pyplot(fig3)


if __name__ == "__main__":
    main()
