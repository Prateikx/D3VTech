from fastapi import FastAPI, HTTPException
from datetime import datetime
import mariadb
from password import *
from typing import List
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
with open('ELECTRONIC-CATALOG.json', 'r') as file:
    # Load the contents of the file into a Python object
    data = json.load(file)

# Access the contents of the JSON file
# print(data)

app = FastAPI()

@app.get('/')
def index():
    return {'Home': 'Page'}

@app.get("/products")
async def list_products() -> List:
    sql = """SELECT * FROM products;"""
    cur.execute(sql)
    products = cur.fetchall()
    return products

@app.get("/categories")
async def list_categories() -> List:
    sql = """SELECT DISTINCT category FROM products;"""
    cur.execute(sql)
    categories = [category[0] for category in cur.fetchall()]
    return categories


@app.get("/products/{sku}")
async def get_product(sku: str):
    vals = (sku,)
    sql = """SELECT * FROM products WHERE sku = %s;"""
    cur.execute(sql, vals)
    product = cur.fetchone()
    if product:
        return product
    else:
        raise HTTPException(status_code=404, detail="Product not found")


@app.put("/update/{sku}/{product}", description="which sku's product you want to change?")
async def update_product(sku: str, product: str):
    vals = (sku, product)
    sql = """SELECT * FROM products WHERE sku = %s"""
    cur.execute(sql, (vals[0],))
    sku = cur.fetchone()  
    if sku:          #Checking if product with sku exists or not
        sql = """UPDATE products
                    SET name = %s
                    WHERE sku = %s;"""  
        cur.execute(sql, (vals[1],vals[0]))
        conn.commit()
        sql2 = """SELECT * FROM products WHERE sku = %s"""
        cur.execute(sql2, (vals[0],))
        conn.commit()
        updated = cur.fetchone()
        return updated
    else:
        raise HTTPException(status_code=404, detail="Product not found")


    