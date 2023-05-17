README.md
This is a simple FastAPI application for managing products in a database.

Requirements
Python 3.7 or higher
mariadb package
fastapi package
pydantic package
Installation


Configure the database connection:

Open the config dictionary in the code and update the following values:
host: Hostname of the database server (e.g., 'localhost')
port: Port number of the database server (e.g., 3306)
user: Username for the database connection
password: Password for the database connection
database: Name of the database
Run the application:


uvicorn main:app --reload
Usage
Access the home page: http://localhost:8000/
List all products: http://localhost:8000/list_products
List all categories: http://localhost:8000/list_categories
Get a product by SKU: http://localhost:8000/get_product/{sku}
Replace {sku} with the SKU of the product you want to retrieve
Update a product by SKU: http://localhost:8000/update_product/{sku}/{product}
Replace {sku} with the SKU of the product you want to update
Replace {product} with the new product name
Create a product: http://localhost:8000/create_product/{name}/{category}/{sku}/{price}/{quantity}
Replace {name} with the name of the product
Replace {category} with the category of the product
Replace {sku} with the SKU of the product
Replace {price} with the price of the product
Replace {quantity} with the quantity of the product
Delete a product by SKU: http://localhost:8000/delete_product/{sku}
Replace {sku} with the SKU of the product you want to delete
