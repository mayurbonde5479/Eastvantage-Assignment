import sqlite3
import csv

# Connect to SQLite database
conn = sqlite3.connect("eastvantage.db")
cursor = conn.cursor()

# Query: sum quantities per customer 18-35 and omit zero purchases
query = """
SELECT c.customer_id AS Customer,
       c.age AS Age,
       i.item_name AS Item,
       SUM(o.quantity) AS Quantity
FROM Customer c
JOIN Sales s ON c.customer_id = s.customer_id
JOIN Orders o ON s.sales_id = o.sales_id
JOIN Items i ON o.item_id = i.item_id
WHERE c.age BETWEEN 18 AND 35
GROUP BY c.customer_id, i.item_name
HAVING SUM(o.quantity) > 0
ORDER BY c.customer_id;
"""

cursor.execute(query)
rows = cursor.fetchall()

# Write to CSV with ';' delimiter
with open("output_sql.csv", "w", newline="") as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(["Customer", "Age", "Item", "Quantity"])
    writer.writerows(rows)

conn.close()
print("SQL solution saved to output_sql.csv")
