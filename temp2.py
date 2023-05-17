# Step 1
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt, JWTError
from dotenv import load_dotenv
from pydantic import BaseModel
from passlib.context import CryptContext
import mariadb
from password import *
from typing import List
from Database_setup import *
from datetime import datetime, timedelta
import secrets

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

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

secret_key = secrets.token_hex(32)
print(secret_key)

# Step 2
load_dotenv()

# JWT Configuration
JWT_SECRET = secret_key
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION = timedelta(minutes=30)

# Configure FastAPI app
app = FastAPI()

# Configure password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configure OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Step 3
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

# The function verifies the signature of the token,
#  checks the expiration time, and returns the payload if the token is valid.
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return username

def create_user(user: UserCreate):
    # Hash the password
    hashed_password = pwd_context.hash(user.password)

    # Insert user into the database
    sql = "INSERT INTO users (name, email, password) VALUES (?, ?, ?)"
    values = (user.name, user.email, hashed_password)
    cur.execute(sql, values)
    conn.commit()

    # Return the created user
    return {
        "name": user.name,
        "email": user.email
    }

@app.get("/")
def Home():
    return {"Home": "Page"}

@app.post("/signup")
async def signup(user: UserCreate):
    created_user = create_user(user)
    return created_user

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

@app.get("/list_categories")
async def list_categories() -> List:
    sql = """SELECT DISTINCT category FROM products;"""
    cur.execute(sql)
    categories = [category[0] for category in cur.fetchall()]
    return categories

# Step 4
# Update the update_product endpoint
@app.put("/update_product/{sku}/{product}", description="which sku's product you want to change?")
async def update_product(sku: str, product: str, current_user: str = Depends(get_current_user)):
    # Check if the current user is authorized to perform the update
    if current_user != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized to perform this action")

    vals = (sku, product)
    sql = """SELECT * FROM products WHERE sku = %s"""
    cur.execute(sql, (vals[0],))
    sku = cur.fetchone()  
    if sku:          # Checking if product with sku exists or not
        sql = """UPDATE products
                    SET name = %s
                    WHERE sku = %s;"""  
        cur.execute(sql, (vals[1], vals[0]))
        conn.commit()
        sql2 = """SELECT * FROM products WHERE sku = %s"""
        cur.execute(sql2, (vals[0],))
        updated = cur.fetchone()
        return updated
    else:
        raise HTTPException(status_code=404, detail="Product not found")

# Update the delete_product endpoint
@app.delete("/delete_product/{sku}")
async def delete_product(sku: str, current_user: str = Depends(get_current_user)):
    # Check if the current user is authorized to perform the deletion
    if current_user != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized to perform this action")

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

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Authenticate the user (e.g., verify username and password against a user database)
    if form_data.username == "admin" and form_data.password == "admin":
        # Generate JWT token for authenticated user
        access_token = create_access_token(data={"sub": form_data.username}, expires_delta=JWT_EXPIRATION)
        return {"access_token": access_token, "token_type": "bearer"}

    # Return error if authentication fails
    raise HTTPException(status_code=401, detail="Invalid username or password")
