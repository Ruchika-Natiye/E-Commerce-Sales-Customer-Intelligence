
import pandas as pd
from mlxtend.frequent_patterns import fpgrowth, association_rules
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(ROOT / "data/processed/cleaned_sales.csv")

# Select top 100 products to limit memory usage
top_products = (
    df.groupby("StockCode")["Revenue"]
    .sum()
    .nlargest(100)
    .index)

df = df[df["StockCode"].isin(top_products)]

# Create invoice-product matrix
basket = (
    df.assign(Value=1)
    .pivot_table(
        index="InvoiceNo",
        columns="StockCode",
        values="Value",
        aggfunc="max",
        fill_value=0
    )
    .astype(bool)
)

# Frequent itemsets
frequent = fpgrowth(
    basket,
    min_support=0.01,
    use_colnames=True
)

print("Frequent Itemsets:")
print(frequent.head(10))

if not frequent.empty:

    rules = association_rules(
        frequent,
        metric="confidence",
        min_threshold=0.2
    )

    if not rules.empty:
        print("\nAssociation Rules:")
        print(
            rules.sort_values(
                "lift",
                ascending=False
            ).head(10)
        )

        rules.to_csv(
            ROOT / "outputs/market_basket_rules.csv",
            index=False
        )

    frequent.to_csv(
        ROOT / "outputs/frequent_itemsets.csv",
        index=False
    )

print("Market basket analysis completed!")
