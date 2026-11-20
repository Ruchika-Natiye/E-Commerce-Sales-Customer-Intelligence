
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(
    ROOT / "data/processed/cleaned_sales.csv",
    dtype={"CustomerID": str})

# Customer-product matrix
matrix = df.pivot_table(
    index="CustomerID",
    columns="StockCode",
    values="Quantity",
    aggfunc="sum",
    fill_value=0
)

# Similarity
similarity = cosine_similarity(matrix)

similarity_df = pd.DataFrame(
    similarity,
    index=matrix.index,
    columns=matrix.index
)

def recommend_products(customer_id, top_n=5):

    customer_id = str(customer_id)

    if customer_id not in matrix.index:
        print("Customer not found!")
        return

    similar_customers = (
        similarity_df[customer_id]
        .drop(customer_id)
        .nlargest(10)
        .index
    )

    already_bought = set(
        matrix.loc[customer_id][
            matrix.loc[customer_id] > 0
        ].index
    )

    scores = matrix.loc[similar_customers].sum()

    scores = scores.drop(
        labels=list(already_bought),
        errors="ignore")

    recommended = scores.nlargest(top_n)

    names = (
        df.drop_duplicates("StockCode")
        .set_index("StockCode")["Description"])

    result = pd.DataFrame({
        "StockCode": recommended.index,
        "Product": recommended.index.map(names),
        "Score": recommended.values})
    return result

# Example
customer = matrix.index[0]
print(recommend_products(customer))
