ship_addr_inserts = []
ship_addr_id = 1

for order in orders:
    customer_id = order[6]
    cust_addr_id = customer_address[customer_id-1][0]
    ship_addr_street = customer_address[customer_id-1][1]
    ship_addr_city = customer_address[customer_id-1][2]
    ship_addr_state = customer_address[customer_id-1][3]
    ship_addr_aptnum = customer_address[customer_id-1][4]
    ship_addr_zip = customer_address[customer_id-1][5]
    order_num = order[1]

    ship_addr_inserts.append(f"({ship_addr_id}, '{ship_addr_street}', '{ship_addr_city}', '{ship_addr_state}', '{ship_addr_aptnum}', {ship_addr_zip}, {order_num})")

    ship_addr_id += 1

ship_addr_query = "INSERT INTO SHIP_ADDR (Ship_addr_id, Ship_addr_street, Ship_addr_city, Ship_addr_state, Ship_addr_aptnum, Ship_addr_zip, Order_num) VALUES "
ship_addr_query += ",\n".join(ship_addr_inserts)