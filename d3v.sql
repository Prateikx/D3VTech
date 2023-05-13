-- Create a database d3v
CREATE DATABASE d3v;

-- Select that database
USE d3v;

-- Create a table products
CREATE TABLE products (
  name VARCHAR(255),
  category VARCHAR(255),
  sku VARCHAR(10),  
  price DECIMAL(10,2),
  quantity INT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
-- Sku = Stock Keeping Unit

-- Create another table users
CREATE TABLE users (
  name VARCHAR(255),
  email VARCHAR(255)
);


