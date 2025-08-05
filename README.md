# Eastvantage-Assignment

Database

Customer Table
    customer_id (PK)
    age
    Sales Table
    sales_id (PK)
    customer_id (FK → Customer)

Orders Table
    order_id (PK)
    sales_id (FK → Sales)
    item_id (FK → Items)
    quantity

Items Table
    item_id (PK)
    item_name