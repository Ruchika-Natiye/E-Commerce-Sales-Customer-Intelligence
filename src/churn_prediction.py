
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(
    ROOT / "data/processed/cleaned_sales.csv",
    parse_dates=["InvoiceDate"],
    dtype={"CustomerID": str}
)

last_date = df["InvoiceDate"].max()
cutoff = last_date - pd.Timedelta(days=90)

# Historical customer information
history = df[df["InvoiceDate"] <= cutoff]

# Final 90-day purchases
future = df[df["InvoiceDate"] > cutoff]

# Customer features
features = history.groupby("CustomerID").agg(
    Recency=("InvoiceDate",
             lambda x: (cutoff - x.max()).days),
    Frequency=("InvoiceNo", "nunique"),
    Monetary=("Revenue", "sum")
)

# Target variable
active_customers = set(future["CustomerID"])

features["Churn"] = (
    ~features.index.isin(active_customers)
).astype(int)

X = features[["Recency", "Frequency", "Monetary"]]
y = features["Churn"]

if y.nunique() < 2:
    raise ValueError("Churn target has only one class.")

# Split data
stratify = y if y.value_counts().min() >= 2 else None

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.25,
    random_state=42,
    stratify=stratify
)

# Train model
model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# Prediction
predictions = model.predict(X_test)

print(classification_report(
    y_test,
    predictions,
    zero_division=0
))

# Churn probability
features["ChurnProbability"] = (
    model.predict_proba(X)[:, 1]
)

features.to_csv(
    ROOT / "outputs/churn_risk.csv"
)

print("Churn prediction completed!")
