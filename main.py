from fastapi import FastAPI, HTTPException
import mariadb
from password import *
from typing import List


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

# Define FastAPI routes
app = FastAPI()

@app.get('/')
def index():
    return {'Home': 'Page'}

@app.get("/list_products")
async def list_products() -> List:
    sql = """SELECT * FROM products;"""
    cur.execute(sql)
    products = cur.fetchall()
    return products

@app.get("/list_categories")
async def list_categories() -> List:
    sql = """SELECT DISTINCT category FROM products;"""
    cur.execute(sql)
    categories = [category[0] for category in cur.fetchall()]
    return categories


@app.get("/get_product/{sku}")
async def get_product(sku: str):
    vals = (sku,)
    sql = """SELECT * FROM products WHERE sku = %s;"""
    cur.execute(sql, vals)
    product = cur.fetchone()
    if product:
        return product
    else:
        raise HTTPException(status_code=404, detail="Product not found")


@app.put("/update_product/{sku}/{product}", description="which sku's product you want to change?")
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

@app.post("/create_product/{name}/{category}/{sku}/{price}/{quantity}")
async def create_product(name: str, category: str, sku: str, price: float, quantity: int):
    sql = """
        INSERT INTO products (name, category, sku, price, quantity)
        VALUES (%s, %s, %s, %s, %s)
        """
    vals = (name, category, sku, price, quantity)
    cur.execute(sql, vals)
    conn.commit()
    val = (sku,)
    sql2 = """SELECT * FROM products WHERE sku = %s"""
    cur.execute(sql2, val)
    conn.commit()
    new_product = cur.fetchone()
    return new_product
#  Disadvantage: The above endpoint can add multiple products of same values

@app.delete("/delete_product/{sku}")
async def delete_product(sku: str):
    sql = """SELECT * FROM products WHERE sku = %s"""
    cur.execute(sql, (sku,))
    product = cur.fetchone()
    if product:
        sql = """DELETE FROM products WHERE sku = %s"""
        cur.execute(sql, (sku,))
        conn.commit()
        return {"message": f"Product with sku {sku} has been deleted successfully."}
    else:
        raise HTTPException(status_code=404, detail="Product not found.")