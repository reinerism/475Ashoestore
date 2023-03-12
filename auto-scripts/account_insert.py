from faker import Faker
import random

fake = Faker()

account_inserts = ["INSERT INTO ACCOUNT (User_name, Password, Account_num, Customer_id) VALUES"]

for i in range(50):
    user_name = fake.user_name()
    password = str(random.randint(10000, 99999))
    account_num = random.randint(1, 1000)
    customer_id = random.randint(1, 100)
    account_inserts.append(f"('{user_name}', '{password}', {account_num}, {customer_id}),")

account_inserts[-1] = account_inserts[-1][:-1] + ";"

with open("account_inserts.sql", "w") as f:
    f.write("\n".join(account_inserts))