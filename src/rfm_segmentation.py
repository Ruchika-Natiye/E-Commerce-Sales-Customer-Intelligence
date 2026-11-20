
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(
    ROOT / "data/processed/cleaned_sales.csv",
    parse_dates=["InvoiceDate"],
    dtype={"CustomerID": str}
)

# Snapshot date
snapshot = df["InvoiceDate"].max() + pd.Timedelta(days=1)

# Calculate RFM
rfm = df.groupby("CustomerID").agg(
    Recency=("InvoiceDate",
             lambda x: (snapshot - x.max()).days),

    Frequency=("InvoiceNo", "nunique"),

    Monetary=("Revenue", "sum")
)

# Calculate scores
rfm["R"] = pd.qcut(
    rfm["Recency"].rank(method="first"),
    4,
    labels=[4, 3, 2, 1]
).astype(int)

rfm["F"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    4,
    labels=[1, 2, 3, 4]
).astype(int)

rfm["M"] = pd.qcut(
    rfm["Monetary"].rank(method="first"),
    4,
    labels=[1, 2, 3, 4]
).astype(int)

rfm["RFM_Score"] = (
    rfm[["R", "F", "M"]]
    .astype(str)
    .agg("".join, axis=1)
)

# Customer segmentation
rfm["Segment"] = "Regular"

rfm.loc[
    (rfm["R"] >= 3) &
    (rfm["F"] >= 3) &
    (rfm["M"] >= 3),
    "Segment"
] = "Champions"

rfm.loc[
    (rfm["R"] >= 3) &
    (rfm["F"] <= 2),
    "Segment"
] = "Recent Customers"

rfm.loc[
    (rfm["R"] <= 2) &
    (rfm["F"] >= 3),
    "Segment"
] = "At Risk / Loyal"

rfm.loc[
    (rfm["R"] == 1) &
    (rfm["F"] == 1),
    "Segment"
] = "Hibernating"

# Export
rfm.to_csv(ROOT / "outputs/rfm_segments.csv")

print(rfm.head())
print(rfm["Segment"].value_counts())
print("RFM analysis completed!")

