## ADDED Requirements

### Requirement: Spam Classifier Pipeline
The system SHALL provide an end-to-end spam/hams classifier pipeline that includes data preprocessing, model training using Logistic Regression with TF-IDF features, evaluation (ROC, Precision-Recall), and a demo application exposing model predictions and visualizations.

#### Scenario: Preprocessing produces cleaned CSV
- **GIVEN** a raw CSV `sms_spam_no_header.csv` with label and text columns (possibly no header)
- **WHEN** `preprocessing.py` is run with the input path and output path
- **THEN** a cleaned CSV SHALL be written containing `label`, `text`, and `text_clean` columns

#### Scenario: Model training saves model and vectorizer
- **GIVEN** a cleaned CSV with `text_clean` and `label` columns
- **WHEN** `train.py` is executed
- **THEN** the system SHALL fit a `LogisticRegression` model with a TF-IDF vectorizer and write `models/model.joblib` and `models/vectorizer.joblib`

#### Scenario: Demo app provides visualizations and live inference
- **GIVEN** a trained model and a dataset
- **WHEN** the Streamlit app (`app.py`) is started and model + dataset are loaded
- **THEN** the app SHALL display class distribution, top tokens by class, ROC, Precision-Recall plots, threshold sweep, confusion matrix, and allow live inference (with spam/ham examples and custom text input)
