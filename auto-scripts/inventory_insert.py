#Author: Reiner Opitz
#03/13/2023
#this is an autoscripting code for the shoe store database 
import random

max_quantity = 20
min_quantity = 1

# Generate random inventory records for each shoe ID and store combination
inventory_inserts = ["INSERT INTO INVENTORY (Shoe_id, Store_id, Quantity) VALUES"]
for shoe_id in range(1, 101):
    num_stores = random.randint(0, 4)
    for store_id in range(1, 5):
        if num_stores >= store_id - 1:
            quantity = random.randint(min_quantity, max_quantity)
            inventory_inserts.append(f"({shoe_id}, {store_id}, {quantity}),")
# End the last VALUES with a semicolon
inventory_inserts[-1] = inventory_inserts[-1][:-1] + ";"
# Write the SQL code to a file
with open("inventory_inserts.sql", "w") as f:
    f.write("\n".join(inventory_inserts))