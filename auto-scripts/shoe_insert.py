from faker import Faker
import random
from faker.providers import BaseProvider

#faker does not offer a shoe generator so we have to customize it
class shoeProvider(BaseProvider):
    def shoe_name(self):
        shoe_names = ['Zoom Winflo 8', 'Boost 350 V2', 'Kyrie 7', 'Ultraboost 6.0 DNA', 'Adizero Ubersonic 4',     
                      'GT-2000 10', 'VaporMax Plus', 'Gel-Kayano 28', 'KD 14', 'Air Zoom Pegasus 38',     
                      'Reebok Nano X1', 'LeBron 18', 'FuelCell Rebel', 'Gel-Cumulus 23', 'Free RN 5.0',     
                      'Club C 85', 'Gel-Nimbus 23', 'Zoom Freak 3', 'Joyride Run Flyknit', 'Challenger 4',     
                      'GT-1000 10', 'Alphatorsion Boost', 'Adizero Boston 10', 'SuperRep Go', 'Runfalcon',     
                      'Blaze Foam', 'Machina', 'Hypervenom Phantom 3', 'Metcon 6', 'Senseboost GO',     
                      'ZoomX Invincible Run Flyknit', 'Air Max 97', 'Kaptiva', 'Gel-Quantum 360 6', 'Legend React',     
                      'Fresh Foam 1080v11', 'Galaxy 5', 'Ultraboost 21', 'GT-800 2E', 'Air Zoom Vomero 16']
        return self.random_element(shoe_names)

fake = Faker()
fake.add_provider(shoeProvider)

shoe_inserts = ["INSERT INTO SHOES (Shoe_id, Name, Size, Brand, Price, Style, Color, Gender) VALUES"]
#hard coded some generic colors but colors are not limited to these in the tables
colors = ['Red', 'Blue', 'Green', 'Black', 'White', 'Yellow', 'Orange', 'Purple', 'Gray']

for i in range(1, 101):
    shoe_id = i
    name = fake.shoe_name()
    size = random.choice([6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12])
    brand = random.choice(['Adidas','Puma','Nike','Reebok'])
    price = random.randint(50, 300)
    style = random.choice(['Sneakers', 'Running', 'Basketball', 'Athletic'])
    color = random.choice(colors)
    gender = random.choice(['Mens', 'Womens'])

    shoe_inserts.append(f"({shoe_id}, '{name}', {size}, '{brand}', {price}, '{style}', '{color}', '{gender}'),")

shoe_inserts[-1] = shoe_inserts[-1][:-1] + ";"

with open("shoe_inserts.sql", "w") as f:
    f.write("\n".join(shoe_inserts))