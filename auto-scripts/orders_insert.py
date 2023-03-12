import random
from datetime import datetime, timedelta

orders_inserts = ["INSERT INTO ORDERS (Order_date, Order_num, Order_status, Quantity, Total_cost, Customer_id, Store_id) VALUES"]

# Random list of order statuses
order_statuses = ['Still shopping', 'Checking out', 'Complete']

# Loop through and generate 50 orders
for i in range(1, 51):
    # Generate a random date in the past 30 days
    order_date = datetime.now() - timedelta(days=random.randint(1, 30))
    order_num = i
    order_status = random.choice(order_statuses)
    quantity = random.randint(1, 20)
    total_cost = random.randint(10, 100)
    customer_id = random.randint(1, 100)
    store_id = random.randint(1, 4)
    order_date_str = order_date.strftime('%m/%d/%Y')
    orders_inserts.append(f"('{order_date_str}', {order_num}, '{order_status}', {quantity}, {total_cost}, {customer_id}, {store_id}),")

    orders_inserts[-1] = orders_inserts[-1][:-1] + ";"
    # Print the inventory inserts
with open("order_inserts.sql", "w") as f:
    f.write("\n".join(orders_inserts))