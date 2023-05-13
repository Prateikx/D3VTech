from datetime import datetime
import mariadb
from password import *
import json

# Load database configuration
config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': password,
    'database': database
}
conn = mariadb.connect(**config)
cur = conn.cursor()


# Open the JSON file
with open('JSON.json', 'r') as file:
    # Load the contents of the file into a Python object
    data = json.load(file)

# insert the products into the table
for product in data["products"]:
    name = product["name"]
    category = product["category"]
    sku = product["sku"]
    price = product["price"]
    quantity = product["quantity"]
    sql = "INSERT INTO products (name, category, sku, price, quantity) VALUES (%s, %s, %s, %s, %s)"
    val = (name, category, sku, price, quantity)
    cur.execute(sql, val)

print('successfully inserted the products into the products table')

# insert the users into the table
for user in data["users"]:
    name = user["name"]
    email = user["email"]
    sql = "INSERT INTO users (name, email) VALUES (%s, %s)"
    val = (name, email)
    cur.execute(sql, val)

print('successfully inserted the data into the user table')

# commit the changes
conn.commit()