import sqlite3

# Connect to database (creates file if it doesn't exist)
conn = sqlite3.connect("eastvantage.db")
cursor = conn.cursor()

# Drop tables if they exist
cursor.executescript("""
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Sales;
DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS Items;
""")

# Create tables
cursor.execute("""
CREATE TABLE Customer (
    customer_id INTEGER PRIMARY KEY,
    age INTEGER NOT NULL
);
""")

cursor.execute("""
CREATE TABLE Sales (
    sales_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);
""")

cursor.execute("""
CREATE TABLE Items (
    item_id INTEGER PRIMARY KEY,
    item_name TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE Orders (
    order_id INTEGER PRIMARY KEY,
    sales_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    quantity INTEGER,
    FOREIGN KEY (sales_id) REFERENCES Sales(sales_id),
    FOREIGN KEY (item_id) REFERENCES Items(item_id)
);
""")

# Insert dummy customers
cursor.executemany("INSERT INTO Customer (customer_id, age) VALUES (?, ?)", [
    (1, 21), (2, 23), (3, 35)
])

# Insert items
cursor.executemany("INSERT INTO Items (item_id, item_name) VALUES (?, ?)", [
    (1, 'x'), (2, 'y'), (3, 'z')
])

# Insert sales
cursor.executemany("INSERT INTO Sales (sales_id, customer_id) VALUES (?, ?)", [
    (1, 1), (2, 2), (3, 3)
])

# Insert orders (quantities including NULL and 0 as per rules)
cursor.executemany("INSERT INTO Orders (order_id, sales_id, item_id, quantity) VALUES (?, ?, ?, ?)", [
    # Customer 1 - total x = 10
    (1, 1, 1, 5),
    (2, 1, 1, 5),
    (3, 1, 2, None),  # not purchased
    (4, 1, 3, None),  # not purchased

    # Customer 2 - total 1 for each item
    (5, 2, 1, 1),
    (6, 2, 2, 1),
    (7, 2, 3, 1),

    # Customer 3 - total 2 for z
    (8, 3, 3, 1),
    (9, 3, 3, 1),
    (10, 3, 1, None), # not purchased
    (11, 3, 2, None)  # not purchased
])

conn.commit()
conn.close()

print("eastvantage.db created with dummy data!")
