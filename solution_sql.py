import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect("eastvantage.db")

# Load tables into DataFrames
customers = pd.read_sql("SELECT * FROM Customer", conn)
sales = pd.read_sql("SELECT * FROM Sales", conn)
orders = pd.read_sql("SELECT * FROM Orders", conn)
items = pd.read_sql("SELECT * FROM Items", conn)

# Merge data
df = customers.merge(sales, on="customer_id") \
              .merge(orders, on="sales_id") \
              .merge(items, on="item_id")

# Filter age 18-35
df = df[(df["age"] >= 18) & (df["age"] <= 35)]

# Group by and sum quantities
result = df.groupby(["customer_id", "age", "item_name"], as_index=False)["quantity"].sum()

# Remove zero quantities
result = result[result["quantity"] > 0]

# Save to CSV with ';' delimiter
result.to_csv("output_pandas.csv", sep=';', index=False, header=["Customer","Age","Item","Quantity"])

conn.close()
print("Pandas solution saved to output_pandas.csv")
