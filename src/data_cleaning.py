
import pandas as pd
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
file_path = ROOT / "data" / "raw" / "Online Retail.xlsx"
df = pd.read_excel(file_path)
# Remove duplicate records
df = df.drop_duplicates()
# Handle missing values
df = df.dropna(subset=[
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
    "CustomerID",
    "Country"])

# Convert data types
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["CustomerID"] = df["CustomerID"].astype(int).astype(str)
df["InvoiceNo"] = df["InvoiceNo"].astype(str)

# Identify cancellations and returns
cancelled= (df["InvoiceNo"].str.startswith("C") |(df["Quantity"] < 0))
returns = df[cancelled].copy()

# Keep valid sales
sales = df[(~cancelled) &(df["Quantity"] > 0) &(df["UnitPrice"] > 0)].copy()

# Calculate revenue
sales["Revenue"] = (sales["Quantity"] * sales["UnitPrice"])

# Save files
output = ROOT / "data" / "processed"
output.mkdir(parents=True, exist_ok=True)
sales.to_csv(output / "cleaned_sales.csv", index=False)
returns.to_csv(output / "cancellations_returns_review.csv", index=False)
print("Data cleaning completed!")
print("Total rows:", len(sales))
print("Total Revenue:", sales["Revenue"].sum())
