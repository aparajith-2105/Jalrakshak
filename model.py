from pathlib import Path
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, f1_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

FEATURES = ["Soil_Type", "Soil_pH", "Soil_Moisture", "Organic_Carbon", "Electrical_Conductivity", "Temperature_C", "Humidity", "Rainfall_mm", "Sunlight_Hours", "Wind_Speed_kmh", "Crop_Type", "Crop_Growth_Stage", "Season", "Irrigation_Type", "Water_Source", "Field_Area_hectare", "Mulching_Used", "Previous_Irrigation_mm", "Region"]
CATEGORICAL = ["Soil_Type", "Crop_Type", "Crop_Growth_Stage", "Season", "Irrigation_Type", "Water_Source", "Mulching_Used", "Region"]
NUMERIC = [c for c in FEATURES if c not in CATEGORICAL]
TARGET = "Irrigation_Need"

def load_training_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = FEATURES + [TARGET]
    missing = sorted(set(required) - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    df = df[required].dropna(subset=[TARGET]).copy()
    df[TARGET] = df[TARGET].astype(str).str.strip().str.title()
    for col in CATEGORICAL:
        df[col] = df[col].fillna("Unknown").astype(str).str.strip()
    for col in NUMERIC:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

def train_model(df: pd.DataFrame):
    X, y = df[FEATURES], df[TARGET]
    if y.nunique() < 2:
        raise ValueError("At least two target classes are required for training.")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    preprocessor = ColumnTransformer([
        ("numeric", Pipeline([("imputer", SimpleImputer(strategy="median"))]), NUMERIC),
        ("categorical", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))]), CATEGORICAL),
    ])
    pipe = Pipeline([("features", preprocessor), ("classifier", RandomForestClassifier(n_estimators=180, min_samples_leaf=2, class_weight="balanced_subsample", random_state=42, n_jobs=-1))])
    pipe.fit(X_train, y_train)
    predicted = pipe.predict(X_test)
    report = classification_report(y_test, predicted, output_dict=True, zero_division=0)
    metrics = {"accuracy": accuracy_score(y_test, predicted), "macro_f1": f1_score(y_test, predicted, average="macro"), "report": report}
    return pipe, metrics, df, TARGET
