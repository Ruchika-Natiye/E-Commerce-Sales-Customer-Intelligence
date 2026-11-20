
# E-COMMERCE SALES & CUSTOMER INTELLIGENCE
# SALES ANALYSIS AND EXPLORATORY DATA ANALYSIS


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ==========================================================
# 1. PROJECT PATHS
# ==========================================================

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "cleaned_sales.csv"
OUTPUT_PATH = ROOT / "outputs"
CHART_PATH = OUTPUT_PATH / "charts"

CHART_PATH.mkdir(parents=True, exist_ok=True)

# ==========================================================
# 2. LOAD DATASET
# ==========================================================

df = pd.read_csv(
    DATA_PATH,
    parse_dates=["InvoiceDate"],
    dtype={"CustomerID": str})

print("\n========== DATASET INFORMATION ==========\n")

print(df.head())

print("\nDataset Shape:", df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Records:", df.duplicated().sum())

# ==========================================================
# 3. DATA PREPARATION
# ==========================================================

# Calculate revenue if it does not exist
if "Revenue" not in df.columns:

    df["Revenue"] = ( df["Quantity"] * df["UnitPrice"])

# Extract date features
df["Year"] = df["InvoiceDate"].dt.year

df["Month"] = df["InvoiceDate"].dt.month

df["MonthName"] = df["InvoiceDate"].dt.month_name()

df["YearMonth"] = (df["InvoiceDate"].dt.to_period("M").astype(str))

df["Day"] = df["InvoiceDate"].dt.day

df["Weekday"] = df["InvoiceDate"].dt.day_name()

# Calculate order value
order_values = df.groupby("InvoiceNo")["Revenue"].sum()

# ==========================================================
# 4. KEY PERFORMANCE INDICATORS (KPIs)
# ==========================================================

total_revenue = df["Revenue"].sum()

total_orders = df["InvoiceNo"].nunique()

total_customers = df["CustomerID"].nunique()

total_products = df["StockCode"].nunique()

total_quantity = df["Quantity"].sum()

average_order_value = order_values.mean()

average_revenue_per_customer = (total_revenue / total_customers)

print("\n========== BUSINESS KPIs ==========\n")

print(f"Total Revenue: £{total_revenue:,.2f}")

print(f"Total Orders: {total_orders:,}")

print(f"Total Customers: {total_customers:,}")

print(f"Total Products: {total_products:,}")

print(f"Total Quantity Sold: {total_quantity:,}")

print(f"Average Order Value: £{average_order_value:,.2f}")

print(f"Average Revenue Per Customer: £{average_revenue_per_customer:,.2f}")

# ==========================================================
# 5. MONTHLY REVENUE ANALYSIS
# ==========================================================

monthly_sales = (
    df.groupby("YearMonth")["Revenue"]
    .sum()
    .reset_index())

monthly_sales.columns = ["Month","Revenue"]

# Calculate month-on-month growth
monthly_sales["Growth_Percentage"] = (monthly_sales["Revenue"].pct_change() * 100)

print("\n========== MONTHLY SALES ==========\n")

print(monthly_sales)

# Monthly revenue chart
plt.figure(figsize=(13, 6))

sns.lineplot(
    data=monthly_sales,
    x="Month",
    y="Revenue",
    marker="o",
    linewidth=2)

plt.title(
    "Monthly Revenue Analysis",
    fontsize=16,
    fontweight="bold")

plt.xlabel("Month")

plt.ylabel("Revenue (£)")

plt.xticks(rotation=45)

plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(CHART_PATH / "monthly_revenue.png",dpi=300)

plt.show()

# ==========================================================
# 6. MONTHLY SALES GROWTH
# ==========================================================

plt.figure(figsize=(13, 6))

sns.barplot(
    data=monthly_sales,
    x="Month",
    y="Growth_Percentage"
)

plt.title(
    "Month-on-Month Revenue Growth",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Month")

plt.ylabel("Growth (%)")

plt.axhline(
    y=0,
    linestyle="--",
    color="black"
)

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    CHART_PATH / "monthly_sales_growth.png",
    dpi=300
)

plt.show()

# ==========================================================
# 7. TOP 10 BEST-SELLING PRODUCTS BY REVENUE
# ==========================================================

top_products = (
    df.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

print("\n========== TOP 10 PRODUCTS ==========\n")

print(top_products)

plt.figure(figsize=(12, 7))

sns.barplot(
    data=top_products,
    x="Revenue",
    y="Description"
)

plt.title(
    "Top 10 Products by Revenue",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Revenue (£)")

plt.ylabel("Product")

plt.tight_layout()

plt.savefig(
    CHART_PATH / "top_products.png",
    dpi=300
)

plt.show()

# ==========================================================
# 8. TOP 10 PRODUCTS BY QUANTITY SOLD
# ==========================================================

top_quantity = (
    df.groupby("Description")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

print("\n========== TOP PRODUCTS BY QUANTITY ==========\n")

print(top_quantity)

plt.figure(figsize=(12, 7))

sns.barplot(
    data=top_quantity,
    x="Quantity",
    y="Description"
)

plt.title(
    "Top 10 Products by Quantity Sold",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Quantity Sold")

plt.ylabel("Product")

plt.tight_layout()

plt.savefig(
    CHART_PATH / "top_quantity_products.png",
    dpi=300
)

plt.show()

# ==========================================================
# 9. COUNTRY-WISE REVENUE ANALYSIS
# ==========================================================

country_sales = (
    df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

print("\n========== TOP 10 COUNTRIES ==========\n")

print(country_sales)

plt.figure(figsize=(12, 7))

sns.barplot(
    data=country_sales,
    x="Revenue",
    y="Country"
)

plt.title(
    "Top 10 Countries by Revenue",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Revenue (£)")

plt.ylabel("Country")

plt.tight_layout()

plt.savefig(
    CHART_PATH / "country_sales.png",
    dpi=300
)

plt.show()

# ==========================================================
# 10. CUSTOMER LIFETIME VALUE (CLV) PROXY
# ==========================================================

customer_sales = (
    df.groupby("CustomerID")
    .agg(
        Total_Revenue=("Revenue", "sum"),
        Total_Orders=("InvoiceNo", "nunique"),
        Total_Quantity=("Quantity", "sum")
    )
    .reset_index()
)

customer_sales["Average_Order_Value"] = (
    customer_sales["Total_Revenue"] /
    customer_sales["Total_Orders"]
)

customer_sales = customer_sales.sort_values(
    "Total_Revenue",
    ascending=False
)

print("\n========== TOP 10 CUSTOMERS ==========\n")

print(customer_sales.head(10))

plt.figure(figsize=(12, 6))

sns.barplot(
    data=customer_sales.head(10),
    x="Total_Revenue",
    y="CustomerID"
)

plt.title(
    "Top 10 Customers by Revenue",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Customer Revenue (£)")

plt.ylabel("Customer ID")

plt.tight_layout()

plt.savefig(
    CHART_PATH / "top_customers.png",
    dpi=300
)

plt.show()

# Note: This is historical customer revenue,
# not a predictive lifetime value model.

# ==========================================================
# 11. REPEAT CUSTOMER ANALYSIS
# ==========================================================

customer_orders = (
    df.groupby("CustomerID")["InvoiceNo"]
    .nunique()
)

repeat_customers = (
    customer_orders[customer_orders > 1]
)

one_time_customers = (
    customer_orders[customer_orders == 1]
)

print("\n========== CUSTOMER RETENTION ==========\n")

print(
    "Repeat Customers:",
    len(repeat_customers)
)

print(
    "One-Time Customers:",
    len(one_time_customers)
)

repeat_percentage = (
    len(repeat_customers) /
    len(customer_orders)
) * 100

print(
    f"Repeat Customer Percentage: "
    f"{repeat_percentage:.2f}%"
)

retention_data = pd.DataFrame({
    "Customer Type": [
        "Repeat Customers",
        "One-Time Customers"
    ],
    "Count": [
        len(repeat_customers),
        len(one_time_customers)
    ]
})

plt.figure(figsize=(8, 6))

plt.pie(
    retention_data["Count"],
    labels=retention_data["Customer Type"],
    autopct="%1.1f%%",
    startangle=90
)

plt.title(
    "Repeat vs One-Time Customers",
    fontsize=15,
    fontweight="bold"
)

plt.tight_layout()

plt.savefig(
    CHART_PATH / "customer_retention.png",
    dpi=300
)

plt.show()

# ==========================================================
# 12. WEEKDAY SALES ANALYSIS
# ==========================================================

weekday_sales = (
    df.groupby("Weekday")["Revenue"]
    .sum()
    .reindex([
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ])
    .reset_index()
)

plt.figure(figsize=(11, 6))

sns.barplot(
    data=weekday_sales,
    x="Weekday",
    y="Revenue"
)

plt.title(
    "Revenue by Weekday",
    fontsize=15,
    fontweight="bold"
)

plt.xlabel("Weekday")

plt.ylabel("Revenue (£)")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    CHART_PATH / "weekday_sales.png",
    dpi=300
)

plt.show()

# ==========================================================
# 13. CORRELATION ANALYSIS
# ==========================================================

numeric_data = df[
    [
        "Quantity",
        "UnitPrice",
        "Revenue"
    ]
]

correlation = numeric_data.corr()

plt.figure(figsize=(8, 6))

sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title(
    "Sales Data Correlation Heatmap",
    fontsize=15,
    fontweight="bold"
)

plt.tight_layout()

plt.savefig(
    CHART_PATH / "correlation_heatmap.png",
    dpi=300
)

plt.show()

# ==========================================================
# 14. EXPORT ANALYSIS RESULTS
# ==========================================================

monthly_sales.to_csv(
    OUTPUT_PATH / "monthly_sales.csv",
    index=False
)

top_products.to_csv(
    OUTPUT_PATH / "top_products.csv",
    index=False
)

country_sales.to_csv(
    OUTPUT_PATH / "country_sales.csv",
    index=False
)

customer_sales.to_csv(
    OUTPUT_PATH / "customer_analysis.csv",
    index=False
)

# ==========================================================
# 15. FINAL MESSAGE
# ==========================================================

print("\n==========================================")

print("SALES ANALYSIS COMPLETED SUCCESSFULLY!")

print("==========================================")

print("\nGenerated Charts:")

print("1. Monthly Revenue")

print("2. Monthly Sales Growth")

print("3. Top Products")

print("4. Top Products by Quantity")

print("5. Country Sales")

print("6. Top Customers")

print("7. Customer Retention")

print("8. Weekday Sales")

print("9. Correlation Heatmap")

print("\nOutput Location:")

print(CHART_PATH)

