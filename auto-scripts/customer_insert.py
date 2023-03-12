<<<<<<< HEAD
import random
from faker import Faker

customer_inserts = ["INSERT INTO CUSTOMER (Email, Phone_num, Customer_id, First_name, Last_name) VALUES"]

#create a faker instance to auto generate names
fake = Faker()
# create a set of fake domain names to randmoly assing
domain_names = ["live.com", "AOL.com","gmail.com","yahoo.com", "hotmail.com"]

# Generate random customer records for each customer ID
for customer_id in range(1, 101):
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = f"{first_name.lower()}.{last_name.lower()}@{random.choice(domain_names)}"
    area_code = str(random.randint(100, 999))
    phone_digits = "".join([str(random.randint(0, 9)) for _ in range(7)])
    # to put the number in ###-###-#### format
    phone_num = "{}-{}-{}".format(
    "".join([str(random.randint(1, 9)) for _ in range(3)]),
    "".join([str(random.randint(0, 9)) for _ in range(3)]),
    "".join([str(random.randint(0, 9)) for _ in range(4)])
    )
    customer_inserts.append(f"('{email}', '{phone_num}', {customer_id}, '{first_name}', '{last_name}'),")

customer_inserts[-1] = customer_inserts[-1][:-1] + ";"
# Print the customer inserts
with open("customer_inserts.sql", "w") as f:
=======
import random
from faker import Faker

customer_inserts = ["INSERT INTO INVENTORY (email, Phone_num, Customer_id, First_name, Last_name) VALUES"]

#create a faker instance to auto generate names
fake = Faker()
# create a set of fake domain names to randmoly assing
domain_names = ["live.com", "AOL.com","gmail.com","yahoo.com", "hotmail.com"]

# Generate random inventory records for each customer ID
for customer_id in range(1, 101):
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = f"{first_name.lower()}.{last_name.lower()}@{random.choice(domain_names)}"
    area_code = str(random.randint(100, 999))
    phone_digits = "".join([str(random.randint(0, 9)) for _ in range(7)])
    # to put the number in ###-###-#### format
    phone_num = "{}-{}-{}".format(
    "".join([str(random.randint(1, 9)) for _ in range(3)]),
    "".join([str(random.randint(0, 9)) for _ in range(3)]),
    "".join([str(random.randint(0, 9)) for _ in range(4)])
    )
    customer_inserts.append(f"('{email}', '{phone_num}', {customer_id}, '{first_name}', '{last_name}'),")

customer_inserts[-1] = customer_inserts[-1][:-1] + ";"
# Print the inventory inserts
with open("customer_inserts.sql", "w") as f:
>>>>>>> 0e6d1056d7a2ff834c89a7cc13336aacc6130539
    f.write("\n".join(customer_inserts))