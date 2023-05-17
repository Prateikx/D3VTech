from datetime import datetime
import mariadb
import json
from password import *

# Load database configuration
config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': password,
    'database': database
}

# Define the SQL queries
PRODUCTS_QUERY = """
    CREATE TABLE IF NOT EXISTS products (
        name VARCHAR(255),
        category VARCHAR(255),
        sku VARCHAR(10) UNIQUE,  
        price DECIMAL(10,2),
        quantity INT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );
"""

USERS_QUERY = """
    CREATE TABLE IF NOT EXISTS users (
        name VARCHAR(255),
        email VARCHAR(255) UNIQUE,
        password VARCHAR(255) 
    );
"""

INSERT_PRODUCTS_QUERY = """
    INSERT INTO products (name, category, sku, price, quantity) 
    VALUES (%(name)s, %(category)s, %(sku)s, %(price)s, %(quantity)s)
"""

INSERT_USERS_QUERY = """
    INSERT INTO users (name, email) 
    VALUES (%(name)s, %(email)s)
"""

# Open the JSON file
with open('JSON.json', 'r') as file:
    # Load the contents of the file into a Python object
    data = json.load(file)

# print(data.get("products"))

# Connect to the database and create the tables if they don't exist
with mariadb.connect(**config) as conn:
    with conn.cursor() as cur:
        cur.execute(PRODUCTS_QUERY)
        cur.execute(USERS_QUERY)

        products = data.get('products')
        if products:
            try:
                cur.executemany(INSERT_PRODUCTS_QUERY, products)
                print(f'Successfully inserted {len(products)} products into the products table')
            except Exception as e:
                print(f'Error occurred while inserting products: {str(e)}')

        users = data.get('users')
        if users:
            try:
                cur.executemany(INSERT_USERS_QUERY, users)
                print(f'Successfully inserted {len(users)} users into the users table')
            except Exception as e:
                print(f'Error occurred while inserting users: {str(e)}')

        try:
            # Commit the changes
            conn.commit()
            print('Changes committed successfully')
        except Exception as e:
            conn.rollback()
            print(f'Error occurred while committing changes: {str(e)}')

