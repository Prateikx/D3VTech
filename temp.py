import json
import mariadb

config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'admin',
    'database': 'd3v'
}
conn = mariadb.connect(**config)
cur = conn.cursor()


# Open the JSON file
with open('ELECTRONIC-CATALOG.json', 'r') as file:
    # Load the contents of the file into a Python object
    data = json.load(file)


for p in data["products"]:
    if p["sku"]== "A0001":
        print(p['name'])


# @app.put("/update/{sku}/{product}", description="which sku's product you want to change?")
# async def update_product(sku: str, product: str):
#     now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     vals = (sku, product, now)
#     sql = """SELECT * FROM products WHERE sku = %s"""
#     cur.execute(sql, (vals[0],))
#     sku = cur.fetchone()
#     if sku:
#         sql = """UPDATE products
#                     SET name = %s,
#                     updated_at = %s
#                     WHERE sku = %s;"""
#         cur.execute(sql, (vals[1],vals[2], vals[0]))
#         conn.commit()
#         sql = """SELECT * FROM products Where sku= %s; """
#         cur.execute(sql, vals[0])
#         products = cur.fetchall()
#         return products
#     else:
#         raise HTTPException(status_code=404, detail="Product not found")

sql = """SELECT * FROM products WHERE sku = %s"""
cur.execute(sql, ("A0001",))
conn.commit()
updated = cur.fetchone()
print(updated)


# Working: using put method to get data from the database.
@app.put('/try1/{sku}')
def try1(sku):
    sql = """SELECT * FROM products WHERE sku = %s"""
    cur.execute(sql, (sku,))
    conn.commit()
    updated = cur.fetchone()
    return updated
