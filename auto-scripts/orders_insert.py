#Author: Reiner Opitz
#03/13/2023
#this is an autoscripting code for the shoe store database 
import random
from datetime import datetime, timedelta

orders_inserts = ["INSERT INTO ORDERS (Order_date, Order_num, Order_status, Quantity, Total_cost, Customer_id, Store_id) VALUES"]

# Random list of order statuses
order_statuses = ['Still shopping', 'Checking out', 'Complete']
#list of the ids
customer_ids = list(range(1, 101))
#list generated from the data base using
"""
SELECT Price FROM SHOES ORDER BY Price DESC;
"""
shoe_prices = [300.00, 289.00, 289.00, 288.00, 286.00, 286.00, 284.00, 284.00, 283.00, 270.00, 265.00, 264.00, 263.00, 260.00, 254.00, 253.00, 251.00, 251.00, 248.00, 247.00, 242.00, 242.00, 240.00, 238.00, 235.00, 231.00, 226.00, 223.00, 219.00, 217.00, 215.00, 213.00, 213.00, 209.00, 207.00, 203.00, 195.00, 195.00, 195.00, 192.00, 190.00, 181.00, 181.00, 176.00, 171.00, 169.00, 169.00, 168.00, 160.00, 160.00, 159.00, 157.00, 156.00, 155.00, 149.00, 147.00, 146.00, 138.00, 137.00, 136.00, 135.00, 131.00, 130.00, 130.00, 129.00, 126.00, 124.00, 118.00, 118.00, 115.00, 108.00, 105.00, 102.00, 102.00, 101.00, 100.00, 98.00, 92.00, 89.00, 87.00, 87.00, 82.00, 81.00, 80.00, 78.00, 76.00, 76.00, 72.00, 72.00, 68.00, 66.00, 65.00, 60.00, 60.00, 54.00, 54.00, 52.00, 51.00, 51.00, 50.00]
# Loop through and generate 200 orders
for i in range(1, 201):
    # Generate a random date in the past 30 days
    order_date = datetime.now() - timedelta(days=random.randint(1, 30))
    order_num = i
    order_status = random.choice(order_statuses)
    quantity = random.randint(1, 5)
    total_cost = sum(random.sample(shoe_prices, quantity))
    customer_id = random.choice(customer_ids)
    store_id = random.randint(1, 4)
    order_date_str = order_date.strftime('%Y-%m-%d')
    orders_inserts.append(f"('{order_date_str}', {order_num}, '{order_status}', {quantity}, {total_cost}, {customer_id}, {store_id}),")

orders_inserts[-1] = orders_inserts[-1][:-1] + ";"
    # Print the inventory inserts
with open("order_inserts.sql", "w") as f:
    f.write("\n".join(orders_inserts))