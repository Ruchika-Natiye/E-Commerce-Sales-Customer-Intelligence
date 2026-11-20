
import os
import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(
    ROOT / "data/processed/cleaned_sales.csv",
    dtype={
        "InvoiceNo": str,
        "StockCode": str,
        "CustomerID": str
    },
    parse_dates=["InvoiceDate"]
)

password = quote_plus(os.getenv("MYSQL_PASSWORD", "ipcs@123"))

engine = create_engine(
    f"mysql+pymysql://{os.getenv('MYSQL_USER', 'IPCSNGPIT')}:"
    f"{password}@{os.getenv('MYSQL_HOST', 'localhost')}:"
    f"{os.getenv('MYSQL_PORT', '3306')}/"
    f"{os.getenv('MYSQL_DATABASE', 'ecommerce_intelligence')}"
)

# Remove duplicate invoice-product lines in the input
df = df.drop_duplicates(
    subset=["InvoiceNo", "StockCode"]
)

# Load staging data
with engine.begin() as conn:
    conn.execute(text("DELETE FROM staging_sales"))

df.to_sql(
    "staging_sales",
    engine,
    if_exists="append",
    index=False,
    chunksize=5000
)

with engine.begin() as conn:

    conn.execute(text("""
        INSERT INTO Customers
        SELECT CustomerID, MAX(Country)
        FROM staging_sales
        GROUP BY CustomerID
        ON DUPLICATE KEY UPDATE Country=VALUES(Country)
    """))

    conn.execute(text("""
        INSERT INTO Products
        SELECT StockCode, MAX(Description)
        FROM staging_sales
        GROUP BY StockCode
        ON DUPLICATE KEY UPDATE
        Description=VALUES(Description)
    """))

    conn.execute(text("""
        INSERT INTO Orders
        SELECT InvoiceNo, MAX(CustomerID), MIN(InvoiceDate)
        FROM staging_sales
        GROUP BY InvoiceNo
        ON DUPLICATE KEY UPDATE
        CustomerID=VALUES(CustomerID),
        InvoiceDate=VALUES(InvoiceDate)
    """))

    conn.execute(text("""
        INSERT INTO OrderDetails
        SELECT InvoiceNo, StockCode,
               SUM(Quantity), MAX(UnitPrice), SUM(Revenue)
        FROM staging_sales
        GROUP BY InvoiceNo, StockCode
        ON DUPLICATE KEY UPDATE
        Quantity=VALUES(Quantity),
        UnitPrice=VALUES(UnitPrice),
        Revenue=VALUES(Revenue)
    """))

print("Successfully loaded data into MySQL!")
