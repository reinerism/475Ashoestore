import random

# Generate a list of states
states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
          'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
          'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
          'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
          'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

cities_by_state = {
    'AL': ['Birmingham', 'Montgomery', 'Mobile'],
    'AK': ['Anchorage', 'Fairbanks', 'Juneau'],
    'AZ': ['Phoenix', 'Tucson', 'Mesa'],
    'AR': ['Little Rock', 'Fort Smith', 'Fayetteville'],
    'CA': ['Los Angeles', 'San Francisco', 'San Diego'],
    'CO': ['Denver', 'Colorado Springs', 'Aurora'],
    'CT': ['Bridgeport', 'New Haven', 'Hartford'],
    'DE': ['Wilmington', 'Dover', 'Newark'],
    'FL': ['Miami', 'Orlando', 'Jacksonville'],
    'GA': ['Atlanta', 'Savannah', 'Athens'],
    'HI': ['Honolulu', 'Hilo', 'Kailua'],
    'ID': ['Boise', 'Idaho Falls', 'Nampa'],
    'IL': ['Chicago', 'Springfield', 'Aurora'],
    'IN': ['Indianapolis', 'Fort Wayne', 'Evansville'],
    'IA': ['Des Moines', 'Cedar Rapids', 'Davenport'],
    'KS': ['Wichita', 'Overland Park', 'Kansas City'],
    'KY': ['Louisville', 'Lexington', 'Bowling Green'],
    'LA': ['New Orleans', 'Baton Rouge', 'Shreveport'],
    'ME': ['Portland', 'Lewiston', 'Bangor'],
    'MD': ['Baltimore', 'Annapolis', 'Frederick'],
    'MA': ['Boston', 'Worcester', 'Springfield'],
    'MI': ['Detroit', 'Grand Rapids', 'Ann Arbor'],
    'MN': ['Minneapolis', 'Saint Paul', 'Duluth'],
    'MS': ['Jackson', 'Gulfport', 'Hattiesburg'],
    'MO': ['Kansas City', 'St. Louis', 'Springfield'],
    'MT': ['Billings', 'Missoula', 'Bozeman'],
    'NE': ['Omaha', 'Lincoln', 'Grand Island'],
    'NV': ['Las Vegas', 'Reno', 'Henderson'],
    'NH': ['Manchester', 'Nashua', 'Concord'],
    'NJ': ['Newark', 'Jersey City', 'Atlantic City'],
    'NM': ['Albuquerque', 'Santa Fe', 'Las Cruces'],
    'NY': ['New York City', 'Buffalo', 'Syracuse'],
    'NC': ['Charlotte', 'Raleigh', 'Asheville'],
    'ND': ['Fargo', 'Bismarck', 'Grand Forks'],
    'OH': ['Columbus', 'Cleveland', 'Cincinnati'],
    'OK': ['Oklahoma City', 'Tulsa', 'Norman'],
    'OR': ['Portland', 'Eugene', 'Salem'],
    'PA': ['Philadelphia', 'Pittsburgh', 'Harrisburg'],
    'RI': ['Providence', 'Warwick', 'Cranston'],
    'SC': ['Charleston', 'Columbia', 'Greenville'],
    'SD': ['Sioux Falls', 'Rapid City', 'Aberdeen'],
    'TN': ['Nashville', 'Memphis', 'Chattanooga'],
    'TX': ['Houston', 'Dallas', 'Austin'],
    'UT': ['Salt Lake City', 'Provo', 'St. George'],
    'VT': ['Burlington', 'Montpelier', 'Rutland'],
    'VA': ['Richmond', 'Norfolk', 'Virginia Beach'],
    'WA': ['Seattle', 'Tacoma', 'Spokane'],
    'WV': ['Charleston', 'Huntington', 'Morgantown'],
    'WI': ['Milwaukee', 'Madison', 'Green Bay'],
    'WY': ['Cheyenne', 'Casper', 'Laramie']
    }

# Generate a list of street names
streets = ['Main', 'Oak', 'Maple', 'Park', 'Washington',
            'High', 'First', 'Second', 'Third', 'Broadway',
            'Elm', 'Cherry', 'Cedar', 'Spruce', 'Pine',
            'Walnut', 'Market', 'Church', 'College', 'Center']

street_types = ['St', 'Ave', 'Pl', 'Dr', 'Cir','Ln', 'Ct', 'Blvd']

# Generate a list of apartment numbers
aptnums = ['Apt. 1', 'Apt. 2', 'Apt. 3', 'Suite 101', 'Suite 102',
           'Suite 201', 'Suite 202', 'Unit A', 'Unit B', 'Unit C']

# Generate a list of ZIP codes
zipcodes = [random.randint(10000, 99999) for _ in range(50)]

# Generate a list of customer IDs
customer_ids = list(range(1, 101))

# Generate random addresses for each customer
address_inserts = ["INSERT INTO CUSTOMER_ADDRESS (Cust_addr_id, Cust_addr_street, Cust_addr_aptnum, Cust_addr_city, Cust_addr_state, Cust_addr_zip, Customer_id) VALUES"]
for i in range(1, 101):
    addr_id = i
    street_num = str(random.randint(100, 999))
    street_name = random.choice(streets)
    street_type = random.choice(street_types)
    state = random.choice(states)
    city = random.choice(cities_by_state[state])
    apt_num = random.randint(1, 100) if random.random() < 0.5 else None
    street = f"{street_num} {street_name} {street_type}"
    if apt_num:
        apt_num = random.choice(aptnums)
    zip_code = str(random.randint(10000, 99999))
    customer_id = i
    address_inserts.append(f"({addr_id}, '{street}','{apt_num}','{city}', '{state}', {zip_code}, {customer_id}),")

address_inserts[-1] = address_inserts[-1][:-1] + ";"
# Print the inventory inserts
with open("cust_addr_inserts.sql", "w") as f:
    f.write("\n".join(address_inserts))